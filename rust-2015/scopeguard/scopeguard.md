# scopeguard

> 标签: Rust

## 简介

A RAII scope guard that will run a given closure when it goes out of scope,
even if the code between panics (assuming unwinding panic).

Defines the macros `defer!`, `defer_on_unwind!`, `defer_on_success!` as
shorthands for guards with one of the implemented strategies.

## 官网

- crates.io 页面：https://crates.io/crates/scopeguard
- 文档：https://docs.rs/scopeguard/
- 源码仓库：https://github.com/bluss/scopeguard

## 历史版本号

- 当前版本：1.2.0

- 0.1.0
- 0.1.1
- 0.1.2
- 0.2.0
- 0.3.1
- 0.3.2
- 0.3.3
- 1.0.0
- 1.1.0
- 1.2.0

## 获取地址

- Cargo 安装：`cargo add scopeguard`
- 下载页面：https://crates.io/crates/scopeguard
- 文档：https://docs.rs/scopeguard/
