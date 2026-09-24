# brotli-decompressor

> 标签: Rust

## 简介

A brotli decompressor that with an interface avoiding the rust stdlib. This makes it suitable for embedded devices and kernels. It is designed with a pluggable allocator so that the standard lib's allocator may be employed. The default build also includes a stdlib allocator and stream interface. Disable this with --features=no-stdlib. Alternatively, --features=unsafe turns off array bounds checks and memory initialization but provides a safe interface for the caller.  Without adding the --features=unsafe argument, all included code is safe. For compression in addition to this library, download https://github.com/dropbox/rust-brotli

## 官网

- 官网：https://github.com/dropbox/rust-brotli-decompressor
- crates.io 页面：https://crates.io/crates/brotli-decompressor
- 文档：https://github.com/dropbox/rust-brotli-decompressor/blob/master/README.md
- 源码仓库：https://github.com/dropbox/rust-brotli-decompressor

## 历史版本号

- 当前版本：6.0.0

- 2.5.0
- 2.5.1
- 3.0.0
- 4.0.0
- 4.0.1
- 4.0.2
- 4.0.3
- 5.0.0
- 5.0.1
- 5.0.2
- 5.0.3
- 6.0.0
- 共 40 个版本，完整清单见 crates.io。

## 获取地址

- Cargo 安装：`cargo add brotli-decompressor`
- 下载页面：https://crates.io/crates/brotli-decompressor
- 文档：https://github.com/dropbox/rust-brotli-decompressor/blob/master/README.md
