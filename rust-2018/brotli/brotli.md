# brotli

> 标签: Rust

## 简介

A brotli compressor and decompressor that with an interface avoiding the rust stdlib. This makes it suitable for embedded devices and kernels. It is designed with a pluggable allocator so that the standard lib's allocator may be employed. The default build also includes a stdlib allocator and stream interface. Disable this with --features=no-stdlib. All included code is safe.

## 官网

- 官网：https://github.com/dropbox/rust-brotli
- crates.io 页面：https://crates.io/crates/brotli
- 文档：https://docs.rs/brotli/
- 源码仓库：https://github.com/dropbox/rust-brotli

## 历史版本号

- 当前版本：9.0.0

- 3.4.0
- 3.5.0
- 4.0.0
- 5.0.0
- 6.0.0
- 7.0.0
- 8.0.0
- 8.0.1
- 8.0.2
- 8.0.3
- 8.0.4
- 9.0.0
- 共 55 个版本，完整清单见 crates.io。

## 获取地址

- Cargo 安装：`cargo add brotli`
- 下载页面：https://crates.io/crates/brotli
- 文档：https://docs.rs/brotli/
- 最低 Rust 版本：1.59.0
