# async-tar

> 标签: Rust

## 简介

A Rust implementation of an async TAR file reader and writer. This library does not
currently handle compression, but it is abstract over all I/O readers and
writers. Additionally, great lengths are taken to ensure that the entire
contents are never required to be entirely resident in memory all at once.

## 官网

- 官网：https://github.com/dignifiedquire/async-tar
- crates.io 页面：https://crates.io/crates/async-tar
- 文档：https://docs.rs/async-tar
- 源码仓库：https://github.com/dignifiedquire/async-tar

## 历史版本号

- 当前版本：0.6.1

- 0.1.0
- 0.1.1
- 0.1.2
- 0.2.0
- 0.3.0
- 0.4.0
- 0.4.1
- 0.4.2
- 0.5.0
- 0.5.1
- 0.6.0
- 0.6.1

## 获取地址

- Cargo 安装：`cargo add async-tar`
- 下载页面：https://crates.io/crates/async-tar
- 文档：https://docs.rs/async-tar
- 最低 Rust 版本：1.85
