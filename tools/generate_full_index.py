#!/usr/bin/env python3
"""Build the full LibPool Rust library index from the official crates.io index.

Unlike the curated generator, this script consumes every crate that exists in
the official index repository so the result can be audited against the central
registry's own file count.  It is resumable and only writes missing markdown
files, so a partial or interrupted run can be continued safely.

Layout:
  rust-<edition>/<crate-name>/<crate-name>.md

Run from the repo root:
    python tools/generate_full_index.py --index D:/Temp/libpool-crates-index
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tarfile
import time
import urllib.parse
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CACHE_PATH = ROOT / "tools" / "cache" / "rust.json"
NAMES_PATH = ROOT / "tools" / "cache" / "rust_full_names.txt"
STATE_PATH = ROOT / "tools" / "cache" / "rust_full_state.json"
RUST_RELEASES = ["rust-2015", "rust-2018", "rust-2021", "rust-2024"]
EDITION_ORDER = ["2015", "2018", "2021", "2024"]


def load_cache() -> dict:
    if CACHE_PATH.exists():
        try:
            return json.loads(CACHE_PATH.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def save_cache(data: dict) -> None:
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CACHE_PATH.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")


def load_state() -> set[str]:
    if not STATE_PATH.exists():
        return set()
    try:
        data = json.loads(STATE_PATH.read_text(encoding="utf-8"))
        return set(data.get("generated", []))
    except Exception:
        return set()


def save_state(generated: set[str]) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "generated": sorted(generated),
        "updated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    STATE_PATH.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")


def index_names(index_dir: Path) -> list[str]:
    """Return every crate name in the official index, rooted by git HEAD."""
    if NAMES_PATH.exists():
        return [ln.strip() for ln in NAMES_PATH.read_text(encoding="utf-8").splitlines() if ln.strip()]
    proc = subprocess.run(
        ["git", "-C", str(index_dir), "ls-tree", "-r", "--name-only", "HEAD"],
        capture_output=True,
        text=True,
        check=True,
    )
    names: list[str] = []
    for line in proc.stdout.splitlines():
        path = line.strip()
        if not path or path == "config.json" or "/" not in path:
            continue
        if path.endswith("/") or path.startswith(".github"):
            continue
        name = path.rsplit("/", 1)[-1]
        if name:
            names.append(name)
    NAMES_PATH.write_text("\n".join(names) + "\n", encoding="utf-8")
    return names


def parse_crate_text(text: str) -> dict:
    """Parse an official index file body into compact library metadata."""
    versions: list[str] = []
    editions: set[str] = set()
    rust_versions: list[str] = []
    name = ""
    for line in text.splitlines():
        if not line.strip():
            continue
        try:
            item = json.loads(line)
        except Exception:
            continue
        if not isinstance(item, dict):
            continue
        if not name:
            name = item.get("name") or ""
        vers = item.get("vers") or ""
        if vers:
            versions.append(vers)
        edition = (item.get("edition") or "").strip()
        if edition in EDITION_ORDER:
            editions.add(edition)
        rv = (item.get("rust_version") or "").strip()
        if rv:
            rust_versions.append(rv)
    if not name or not versions:
        return {}
    # A crate with no declared edition defaults to 2015.
    min_edition = min(editions) if editions else "2015"
    return {
        "name": name,
        "versions": versions,
        "edition": min_edition,
        "rust_version": rust_versions[-1] if rust_versions else "",
    }


def parse_crate_file(path: Path) -> dict:
    """Parse a single official index file checked out from git."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return {}
    return parse_crate_text(text)


def crate_name_from_member(member: tarfile.TarInfo) -> str:
    """Return the crate name for an index file member, or an empty string."""
    if not member.isfile():
        return ""
    path = member.name.replace("\\", "/")
    parts = path.split("/")
    if len(parts) < 3:
        return ""
    name = parts[-1]
    if not name or name == "config.json" or name.startswith("."):
        return ""
    return name


def edition_dirs(edition: str) -> list[str]:
    if edition not in EDITION_ORDER:
        edition = "2015"
    idx = EDITION_ORDER.index(edition)
    return RUST_RELEASES[idx:]


def readme_md(meta: dict, cache_entry: dict | None) -> str:
    name = meta["name"]
    versions = meta.get("versions") or []
    version_lines = "\n".join(f"- {v}" for v in versions[-12:] or ["-"])
    if len(versions) > 12:
        version_lines += f"\n- 共 {len(versions)} 个版本，完整清单见 crates.io。"
    url = f"https://crates.io/crates/{urllib.parse.quote(name)}"

    description = (cache_entry or {}).get("description") or f"{name} - Rust crate from crates.io"
    homepage = (cache_entry or {}).get("homepage") or ""
    documentation = (cache_entry or {}).get("documentation") or ""
    repository = (cache_entry or {}).get("repository") or ""
    license = (cache_entry or {}).get("license") or ""
    rust_version = (cache_entry or {}).get("rust_version") or meta.get("rust_version") or ""
    tags = (cache_entry or {}).get("tags") or ["Rust"]

    websites = [f"- crates.io 页面：{url}"]
    if homepage and homepage != url:
        websites.insert(0, f"- 官网：{homepage}")
    if documentation:
        websites.append(f"- 文档：{documentation}")
    if repository:
        websites.append(f"- 源码仓库：{repository}")

    downloads = [
        f"- Cargo 安装：`cargo add {name}`",
        f"- 下载页面：{url}",
    ]
    if documentation:
        downloads.append(f"- 文档：{documentation}")
    if rust_version:
        downloads.append(f"- 最低 Rust 版本：{rust_version}")
    if license:
        downloads.append(f"- 许可证：{license}")

    tag_line = ", ".join(sorted(set(tags))) if tags else "Rust"
    return f"""# {name}

> 标签: {tag_line}

## 简介

{description}

## 官网

{chr(10).join(websites)}

## 历史版本号

- 当前版本：{versions[-1] if versions else "未知"}

{version_lines}

## 获取地址

{chr(10).join(downloads)}
"""


def write_rust_readme(counts: dict[str, int], total: int) -> None:
    lines = [
        "# Rust 库索引",
        "",
        "本目录收录来自 crates.io 的 Rust 库索引，按 Rust Edition 与 crate 名路径组织：",
        "",
        "- Edition 目录：`rust-2015`、`rust-2018`、`rust-2021`、`rust-2024`",
        "- crate 路径：`<crate>/<crate>.md`",
        "- 库若兼容后续 Edition，会同时出现在所有后续 Edition 目录中",
        f"- 当前共收录 {total} 个 crate（来源为 crates.io 官方索引全量文件清单）。",
        "",
        "## 数据源",
        "",
        "- crates.io 官方索引：https://github.com/rust-lang/crates.io-index",
        "- crates.io 稀疏索引：https://index.crates.io/",
        "- crates.io 官网：https://crates.io/",
        "- 文档站：https://docs.rs/",
        "",
        "## 生成方式",
        "",
        "```bash",
        "python tools/generate_full_index.py --index D:/Temp/crates-index-master.tar.gz",
        "```",
        "",
        "按 Edition 统计：",
        "",
    ]
    lines += [f"- {k}：{v} 个库" for k, v in counts.items()]
    (ROOT / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def count_editions() -> dict[str, int]:
    counts = {release: 0 for release in RUST_RELEASES}
    for release in RUST_RELEASES:
        release_dir = ROOT / release
        if not release_dir.exists():
            continue
        for entry in release_dir.iterdir():
            if entry.is_dir() and not entry.name.startswith("."):
                counts[release] += 1
    return counts


def generate_from_tarball(args: argparse.Namespace, cache: dict) -> int:
    generated = load_state()
    counts = {release: 0 for release in RUST_RELEASES}
    started = len(generated)
    print(f"Resuming with {started:,} already-generated crates", flush=True)

    names: list[str] = []
    done = 0
    skipped = 0
    if not args.max_crates and (args.rebuild_names or not NAMES_PATH.exists()):
        with tarfile.open(args.index, "r:gz") as tar:
            for member in tar:
                name = crate_name_from_member(member)
                if name:
                    names.append(name)
        NAMES_PATH.parent.mkdir(parents=True, exist_ok=True)
        NAMES_PATH.write_text("\n".join(names) + "\n", encoding="utf-8")
        print(f"Official index has {len(names):,} crate files", flush=True)

    with tarfile.open(args.index, "r:gz") as tar:
        for member in tar:
            if done % args.checkpoint_every == 0 and done:
                save_state(generated)
                print(f"  generated {done:,}; {len(generated):,} total", flush=True)
            name = crate_name_from_member(member)
            if not name:
                continue
            if name in generated:
                continue
            if args.max_crates and done >= args.max_crates:
                break
            done += 1
            raw = tar.extractfile(member)
            if raw is None:
                skipped += 1
                generated.add(name)
                continue
            text = raw.read().decode("utf-8", errors="replace")
            meta = parse_crate_text(text)
            if not meta:
                skipped += 1
                generated.add(name)
                continue
            entry = cache.get(name)
            text_md = readme_md(meta, entry)
            for release in edition_dirs(meta["edition"]):
                target = args.out / release / name
                try:
                    target.mkdir(parents=True, exist_ok=True)
                    md = target / f"{name}.md"
                    if not md.exists():
                        md.write_text(text_md, encoding="utf-8")
                    counts[release] += 1
                except Exception as exc:
                    print(f"  write error {target}: {exc}", flush=True)
            generated.add(name)
            if args.max_crates and done >= args.max_crates * 20:
                # Keep smoke tests from streaming the entire 338k-file archive.
                break

    save_state(generated)
    counts = count_editions()
    write_rust_readme(counts, len(generated))
    print("Edition counts:", json.dumps(counts, sort_keys=True), flush=True)
    print(f"Done: {len(generated):,} crates (skipped {skipped:,})", flush=True)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--index", type=Path, default=Path("D:/Temp/libpool-crates-index"))
    parser.add_argument("--out", type=Path, default=ROOT)
    parser.add_argument("--max-crates", type=int, default=0, help="smoke-test limit")
    parser.add_argument("--checkpoint-every", type=int, default=2000)
    parser.add_argument("--rebuild-names", action="store_true")
    args = parser.parse_args()

    if args.rebuild_names and NAMES_PATH.exists():
        NAMES_PATH.unlink()
    cache = load_cache()
    if args.index.is_file() and args.index.suffix.lower() == ".gz":
        return generate_from_tarball(args, cache)
    names = index_names(args.index)
    print(f"Official index has {len(names):,} crate files", flush=True)
    if args.max_crates:
        names = names[: args.max_crates]
        print(f"Smoke-test mode: processing {len(names):,} crates", flush=True)

    generated = load_state()
    counts = {release: 0 for release in RUST_RELEASES}
    started = len(generated)
    print(f"Resuming with {started:,} already-generated crates", flush=True)

    done = 0
    pending = [name for name in names if name not in generated]
    for name in pending:
        if len(name) == 1:
            rel = Path("1") / name
        elif len(name) == 2:
            rel = Path("2") / name
        elif len(name) == 3:
            rel = Path("3") / name[0] / name
        else:
            rel = Path(name[:2]) / name[2:4] / name
        meta = parse_crate_file(args.index / rel)
        if not meta:
            generated.add(name)
            done += 1
            if done % 1000 == 0:
                print(f"  skipped/invalid {done} so far", flush=True)
            continue
        entry = cache.get(name)
        text = readme_md(meta, entry)
        for release in edition_dirs(meta["edition"]):
            target = args.out / release / name
            try:
                target.mkdir(parents=True, exist_ok=True)
                md = target / f"{name}.md"
                if not md.exists():
                    md.write_text(text, encoding="utf-8")
                counts[release] += 1
            except Exception as exc:
                print(f"  write error {target}: {exc}", flush=True)
        generated.add(name)
        done += 1
        if done % args.checkpoint_every == 0:
            save_state(generated)
            print(f"  generated {done}/{len(pending)}; {len(generated):,} total", flush=True)

    save_state(generated)
    counts = count_editions()
    write_rust_readme(counts, len(generated))
    print("Edition counts:", json.dumps(counts, sort_keys=True), flush=True)
    print(f"Done: {len(generated):,} crates", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
