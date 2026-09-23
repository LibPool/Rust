# uint-zigzag

> 标签: Rust

## 简介

Uint is a convenience wrapper for zig-zag encoding integers to byte sequences.

This allows better compression since the majority of numbers are quite small resulting
in 1 or 2 bytes in the most common case vs 4 for 32-bit numbers or 8 for 64-bit numbers.

This also permits the user to not have to think about which integer type is the most efficient to compress.

## 官网

- 官网：https://github.com/mikelodder7/uint
- crates.io 页面：https://crates.io/crates/uint-zigzag
- 文档：https://docs.rs/uint-zigzag
- 源码仓库：https://github.com/mikelodder7/uint

## 历史版本号

- 当前版本：0.2.1

- 0.1.0
- 0.2.0
- 0.2.1

## 获取地址

- Cargo 安装：`cargo add uint-zigzag`
- 下载页面：https://crates.io/crates/uint-zigzag
- 文档：https://docs.rs/uint-zigzag
