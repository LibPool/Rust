#!/usr/bin/env python3
"""Generate the LibPool Rust library index from crates.io metadata.

Layout:
  rust-<edition>/<crate-name>/<crate-name>.md

Run from the repo root:
    python tools/generate_index.py
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
import threading
import time
import urllib.parse
import urllib.request
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path


CRATES_API = "https://crates.io/api/v1/crates"
SPARSE_INDEX = "https://index.crates.io"
USER_AGENT = "LibPool-Indexer/1.0 (+https://github.com/LibPool)"
CACHE_PATH = Path(__file__).resolve().parent / "cache" / "rust.json"
RUST_RELEASES = ["rust-2015", "rust-2018", "rust-2021", "rust-2024"]
API_LOCK = threading.Lock()


@dataclass
class RustLib:
    name: str
    tags: list[str] = field(default_factory=list)
    version: str = ""
    description: str = ""
    homepage: str = ""
    documentation: str = ""
    repository: str = ""
    license: str = ""
    rust_version: str = ""
    edition: str = ""
    versions: list[str] = field(default_factory=list)


def http_json(url: str) -> dict | None:
    last_exc: Exception | None = None
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.load(resp)
        except Exception as exc:  # retry transient failures
            last_exc = exc
            if getattr(exc, "code", None) in (429, 500, 502, 503, 504):
                time.sleep(1 + attempt * 2)
                continue
            if attempt < 2:
                time.sleep(0.4 * (attempt + 1))
                continue
            break
    print(f"  fetch failed: {url} -> {last_exc}", flush=True)
    return None


def http_lines(url: str) -> list[str]:
    last_exc: Exception | None = None
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=30) as resp:
                return [ln for ln in resp.read().decode("utf-8", errors="replace").splitlines() if ln.strip()]
        except Exception as exc:
            last_exc = exc
            if getattr(exc, "code", None) in (429, 500, 502, 503, 504):
                time.sleep(1 + attempt * 2)
                continue
            if attempt < 2:
                time.sleep(0.3 * (attempt + 1))
                continue
            break
    print(f"  fetch failed: {url} -> {last_exc}", flush=True)
    return []


def sparse_index_url(name: str) -> str:
    n = name.lower()
    if len(n) == 1:
        return f"{SPARSE_INDEX}/1/{n}"
    if len(n) == 2:
        return f"{SPARSE_INDEX}/2/{n}"
    if len(n) == 3:
        return f"{SPARSE_INDEX}/3/{n[0]}/{n}"
    return f"{SPARSE_INDEX}/{n[:2]}/{n[2:4]}/{n}"


def sparse_versions(name: str) -> list[dict]:
    lines = http_lines(sparse_index_url(name))
    out = []
    for line in lines:
        try:
            item = json.loads(line)
        except Exception:
            continue
        if isinstance(item, dict) and item.get("name") == name:
            out.append(item)
    return out


def load_seeds(path: Path) -> list[RustLib]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return [RustLib(name=item["name"], tags=item.get("tags", [])) for item in data]


def load_cache() -> dict:
    if CACHE_PATH.exists():
        try:
            return json.loads(CACHE_PATH.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def save_cache(data: dict) -> None:
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CACHE_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def crawl_popular(limit: int) -> list[RustLib]:
    libs: list[RustLib] = []
    page = 1
    per_page = 100
    pages = math.ceil(limit / per_page)
    print(f"Crawling crates.io top downloads, up to {limit} crates...", flush=True)
    while len(libs) < limit and page <= pages:
        url = f"{CRATES_API}?page={page}&per_page={per_page}&sort=downloads"
        data = http_json(url)
        rows = ((data or {}).get("crates")) or []
        if not rows:
            break
        for row in rows:
            if len(libs) >= limit:
                break
            name = row.get("name") or ""
            if not name:
                continue
            libs.append(
                RustLib(
                    name=name,
                    version=row.get("max_version") or row.get("newest_version") or "",
                    description=(row.get("description") or "").strip(),
                    homepage=(row.get("homepage") or "").strip(),
                    documentation=(row.get("documentation") or "").strip(),
                    repository=(row.get("repository") or "").strip(),
                )
            )
        print(f"  page {page}: collected {len(libs)}", flush=True)
        page += 1
        time.sleep(0.1)
    return libs


def edition_dirs(edition: str) -> list[str]:
    editions = ["2015", "2018", "2021", "2024"]
    if edition in editions:
        idx = editions.index(edition)
        return RUST_RELEASES[idx:]
    # Edition is per-crate; an undeclared crate defaults to 2015 and still
    # compiles as a dependency in every later edition.
    return RUST_RELEASES


def enrich_one(lib: RustLib, cache: dict, use_cache: bool) -> tuple[RustLib, dict | None]:
    key = lib.name
    if use_cache and key in cache:
        entry = cache[key]
        lib.version = entry.get("version", "")
        lib.description = entry.get("description", "")
        lib.homepage = entry.get("homepage", "")
        lib.documentation = entry.get("documentation", "")
        lib.repository = entry.get("repository", "")
        lib.license = entry.get("license", "")
        lib.rust_version = entry.get("rust_version", "")
        lib.edition = entry.get("edition", "")
        lib.versions = entry.get("versions", [])
        lib.tags = list(dict.fromkeys(lib.tags + entry.get("tags", [])))
        return lib, None

    if lib.description or lib.version:
        items = sparse_versions(lib.name)
        if items:
            lib.versions = [it.get("vers") for it in items if it.get("vers") and not it.get("yanked")]
            if not lib.versions:
                lib.versions = [it.get("vers") for it in items if it.get("vers")]
            current = next((it for it in items if it.get("vers") == lib.version), None)
            if not current:
                current = items[-1]
            if current:
                lib.rust_version = (current.get("rust_version") or "").strip()
                lib.edition = (current.get("edition") or "").strip()
                lib.license = (current.get("license") or "").strip()
            if not lib.edition:
                for it in items:
                    if it.get("edition"):
                        lib.edition = it["edition"]
                        break
            if not lib.rust_version:
                for it in items:
                    if it.get("rust_version"):
                        lib.rust_version = it["rust_version"]
                        break
            if not lib.homepage:
                lib.homepage = f"https://crates.io/crates/{urllib.parse.quote(lib.name)}"
            entry = {
                "version": lib.version,
                "description": lib.description,
                "homepage": lib.homepage,
                "documentation": lib.documentation,
                "repository": lib.repository,
                "license": lib.license,
                "rust_version": lib.rust_version,
                "edition": lib.edition,
                "versions": lib.versions,
                "tags": lib.tags,
            }
            return lib, entry

    with API_LOCK:
        data = http_json(f"{CRATES_API}/{urllib.parse.quote(lib.name)}")
    if not data:
        return lib, None
    meta = data.get("crate") or {}
    lib.name = meta.get("name") or lib.name
    lib.version = meta.get("max_version") or meta.get("newest_version") or ""
    lib.description = (meta.get("description") or "").strip()
    lib.homepage = (meta.get("homepage") or "").strip()
    lib.documentation = (meta.get("documentation") or "").strip()
    lib.repository = (meta.get("repository") or "").strip()
    lib.license = (meta.get("license") or "").strip()
    versions = data.get("versions") or []
    lib.versions = [v.get("num") for v in versions if v.get("num") and not v.get("yanked")]
    if not lib.versions:
        lib.versions = [v.get("num") for v in versions if v.get("num")]
    current = next((v for v in versions if v.get("num") == lib.version), None)
    if current:
        lib.rust_version = (current.get("rust_version") or "").strip()
        lib.edition = (current.get("edition") or "").strip()
    if not lib.edition:
        for v in versions:
            if v.get("edition"):
                lib.edition = v["edition"]
                break
    if not lib.rust_version:
        for v in versions:
            if v.get("rust_version"):
                lib.rust_version = v["rust_version"]
                break
    keywords = list(meta.get("keywords") or [])
    lib.tags = list(dict.fromkeys(lib.tags + keywords))
    if not lib.homepage:
        lib.homepage = f"https://crates.io/crates/{urllib.parse.quote(lib.name)}"
    entry = {
        "version": lib.version,
        "description": lib.description,
        "homepage": lib.homepage,
        "documentation": lib.documentation,
        "repository": lib.repository,
        "license": lib.license,
        "rust_version": lib.rust_version,
        "edition": lib.edition,
        "versions": lib.versions,
        "tags": lib.tags,
    }
    return lib, entry


def readme_md(lib: RustLib) -> str:
    version_lines = "\n".join(f"- {v}" for v in lib.versions[-12:] or ["-"])
    if len(lib.versions) > 12:
        version_lines += f"\n- 共 {len(lib.versions)} 个版本，完整清单见 crates.io。"
    websites = [f"- crates.io 页面：https://crates.io/crates/{urllib.parse.quote(lib.name)}"]
    if lib.homepage and lib.homepage != f"https://crates.io/crates/{urllib.parse.quote(lib.name)}":
        websites.insert(0, f"- 官网：{lib.homepage}")
    if lib.documentation:
        websites.append(f"- 文档：{lib.documentation}")
    if lib.repository:
        websites.append(f"- 源码仓库：{lib.repository}")

    downloads = [
        f"- Cargo 安装：`cargo add {lib.name}`",
        f"- 下载页面：https://crates.io/crates/{urllib.parse.quote(lib.name)}",
    ]
    if lib.documentation:
        downloads.append(f"- 文档：{lib.documentation}")
    if lib.rust_version:
        downloads.append(f"- 最低 Rust 版本：{lib.rust_version}")
    if lib.license:
        downloads.append(f"- 许可证：{lib.license}")

    tags = ", ".join(sorted(set(lib.tags))) if lib.tags else "Rust"
    desc = lib.description or f"{lib.name} - Rust crate from crates.io"
    return f"""# {lib.name}

> 标签: {tags}

## 简介

{desc}

## 官网

{chr(10).join(websites)}

## 历史版本号

- 当前版本：{lib.version or "未知"}

{version_lines}

## 获取地址

{chr(10).join(downloads)}
"""


def generate(root: Path, libs: list[RustLib], out_dir: Path) -> dict[str, int]:
    counts = defaultdict(int)
    for lib in libs:
        if not lib.version:
            continue
        text = readme_md(lib)
        for release in edition_dirs(lib.edition):
            target = out_dir / release / lib.name
            target.mkdir(parents=True, exist_ok=True)
            (target / f"{lib.name}.md").write_text(text, encoding="utf-8")
            counts[release] += 1
    return dict(counts)


def write_rust_readme(root: Path, libs: list[RustLib], counts: dict[str, int]) -> None:
    lines = [
        "# Rust 库索引",
        "",
        "本目录收录来自 crates.io 的 Rust 库索引，按 Rust Edition 与 crate 名路径组织：",
        "",
        "- Edition 目录：`rust-2015`、`rust-2018`、`rust-2021`、`rust-2024`",
        "- crate 路径：`<crate>/<crate>.md`",
        "- 库若兼容后续 Edition，会同时出现在所有后续 Edition 目录中",
        f"- 当前共收录 {len(libs)} 个 crate（含按下载量爬取的头部 crate 与人工种子）。",
        "",
        "## 数据源",
        "",
        "- crates.io API：https://crates.io/api/v1/crates/<crate>",
        "- crates.io 官网：https://crates.io/",
        "- 文档站：https://docs.rs/",
        "",
        "## 生成方式",
        "",
        "```bash",
        "python tools/build_seed_list.py",
        "python tools/generate_index.py --crawl --crawl-limit 3000",
        "```",
        "",
        "按 Edition 统计：",
        "",
    ]
    lines += [f"- {k}：{v} 个库" for k, v in counts.items()]
    (root / "README.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", default="tools/seeds/rust.json")
    ap.add_argument("--out", default=".")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--crawl", action="store_true")
    ap.add_argument("--crawl-limit", type=int, default=3000)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--refresh-cache", action="store_true")
    args = ap.parse_args()

    root = Path(args.out).resolve()
    libs = []
    if args.crawl:
        libs = crawl_popular(args.crawl_limit)
        seed_path = Path(args.seeds)
        if seed_path.exists():
            existing = {lib.name for lib in libs}
            for seed in load_seeds(seed_path):
                if seed.name not in existing:
                    libs.append(seed)
    else:
        libs = load_seeds(Path(args.seeds))
    if args.limit:
        libs = libs[: args.limit]

    cache = load_cache()
    print(f"Processing {len(libs)} crates...", flush=True)
    results: list[tuple[RustLib, dict | None]] = []
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futures = [ex.submit(enrich_one, lib, cache, not args.refresh_cache) for lib in libs]
        for i, fut in enumerate(as_completed(futures), 1):
            lib, entry = fut.result()
            results.append((lib, entry))
            if entry:
                cache[lib.name] = entry
            if i % 500 == 0 or i == len(futures):
                save_cache(cache)
                print(f"  enriched {i}/{len(futures)}", flush=True)
    save_cache(cache)
    counts = generate(root, [lib for lib, _ in results], root)
    print("Generated per edition:", json.dumps(counts, sort_keys=True), flush=True)
    write_rust_readme(root, [lib for lib, _ in results], counts)
    return 0


if __name__ == "__main__":
    sys.exit(main())
