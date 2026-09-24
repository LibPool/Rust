# b64-ct

> 标签: Rust

## 简介

Fast and secure Base64 encoding/decoding.

This crate provides an implementation of Base64 encoding/decoding that is
designed to be resistant against software side-channel attacks (such as timing
& cache attacks), see the documentation for details. On certain platforms it
also uses SIMD making it very fast. This makes it suitable for e.g. decoding
cryptographic private keys in PEM format.

The API is very similar to the base64 implementation in the old rustc-serialize
crate, making it easy to use in existing projects.

## 官网

- crates.io 页面：https://crates.io/crates/b64-ct
- 源码仓库：https://github.com/fortanix/b64-ct/

## 历史版本号

- 当前版本：0.1.3

- 0.1.0
- 0.1.1
- 0.1.2
- 0.1.3

## 获取地址

- Cargo 安装：`cargo add b64-ct`
- 下载页面：https://crates.io/crates/b64-ct
