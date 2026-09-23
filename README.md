# Rust 库索引

本目录收录来自 crates.io 的 Rust 库索引，按 Rust Edition 与 crate 名路径组织：

- Edition 目录：`rust-2015`、`rust-2018`、`rust-2021`、`rust-2024`
- crate 路径：`<crate>/<crate>.md`
- 库若兼容后续 Edition，会同时出现在所有后续 Edition 目录中
- 当前共收录 3106 个 crate（含按下载量爬取的头部 crate 与人工种子）。

## 数据源

- crates.io API：https://crates.io/api/v1/crates/<crate>
- crates.io 官网：https://crates.io/
- 文档站：https://docs.rs/

## 生成方式

```bash
python tools/build_seed_list.py
python tools/generate_index.py --crawl --crawl-limit 3000
```

按 Edition 统计：

- rust-2015：3006 个库
- rust-2018：3029 个库
- rust-2021：3070 个库
- rust-2024：3101 个库