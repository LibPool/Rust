# mbedtls-platform-support

> 标签: Rust

## 简介

This Rust crate is a support library for the `mbedtls` crate, providing platform and target specific
implementations of all necessary functions. By separating this logic into a separate crate, multiple
versions of the mbedtls crate can coexist within a single crate.This helps to avoid link name conflict
errors. The crate exports Rust functions and defines C functions to support external overrides as
needed for custom implementation under various platforms or targets.

## 官网

- crates.io 页面：https://crates.io/crates/mbedtls-platform-support
- 文档：https://docs.rs/mbedtls-platform-support/
- 源码仓库：https://github.com/fortanix/rust-mbedtls

## 历史版本号

- 当前版本：0.1.3

- 0.1.0
- 0.1.1
- 0.1.3

## 获取地址

- Cargo 安装：`cargo add mbedtls-platform-support`
- 下载页面：https://crates.io/crates/mbedtls-platform-support
- 文档：https://docs.rs/mbedtls-platform-support/
