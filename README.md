# Rust 库索引

本目录收录来自 crates.io 的 Rust 库索引，按 Rust Edition 与 crate 名路径组织：

- Edition 目录：`rust-2015`、`rust-2018`、`rust-2021`、`rust-2024`
- crate 路径：`<crate>/<crate>.md`
- 库若兼容后续 Edition，会同时出现在所有后续 Edition 目录中
- 当前共收录 338681 个 crate（来源为 crates.io 官方索引全量文件清单）。

## 数据源

- crates.io 官方索引：https://github.com/rust-lang/crates.io-index
- crates.io 稀疏索引：https://index.crates.io/
- crates.io 官网：https://crates.io/
- 文档站：https://docs.rs/

## 生成方式

```bash
python tools/generate_full_index.py --index D:/Temp/crates-index-master.tar.gz
```

按 Edition 统计：

- rust-2015：338681 个库
- rust-2018：338681 个库
- rust-2021：338681 个库
- rust-2024：338681 个库
