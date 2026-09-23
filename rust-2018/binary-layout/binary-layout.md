# binary-layout

> 标签: Rust

## 简介

The binary-layout library allows type-safe, inplace, zero-copy access to structured binary data. You define a custom data layout and give it a slice of binary data, and it will allow you to read and write the fields defined in the layout from the binary data without having to copy any of the data. It's similar to transmuting to/from a `#[repr(packed)]` struct, but much safer.

## 官网

- 官网：https://github.com/smessmer/binary-layout
- crates.io 页面：https://crates.io/crates/binary-layout
- 文档：https://docs.rs/binary-layout
- 源码仓库：https://github.com/smessmer/binary-layout

## 历史版本号

- 当前版本：4.0.2

- 2.1.0
- 3.0.0
- 3.1.0
- 3.1.1
- 3.1.2
- 3.1.3
- 3.1.4
- 3.2.0
- 3.3.0
- 4.0.0
- 4.0.1
- 4.0.2
- 共 20 个版本，完整清单见 crates.io。

## 获取地址

- Cargo 安装：`cargo add binary-layout`
- 下载页面：https://crates.io/crates/binary-layout
- 文档：https://docs.rs/binary-layout
- 最低 Rust 版本：1.59
