# compio-send-wrapper

> 标签: Rust

## 简介

This Rust library implements a wrapper type called SendWrapper which allows you to move around non-Send types
between threads, as long as you access the contained value only from within the original thread. You also have to
make sure that the wrapper is dropped from within the original thread. If any of these constraints is violated,
a panic occurs.

## 官网

- crates.io 页面：https://crates.io/crates/compio-send-wrapper
- 文档：https://docs.rs/compio-send-wrapper
- 源码仓库：https://github.com/compio-rs/send_wrapper

## 历史版本号

- 当前版本：0.7.2

- 0.7.0
- 0.7.1
- 0.7.2

## 获取地址

- Cargo 安装：`cargo add compio-send-wrapper`
- 下载页面：https://crates.io/crates/compio-send-wrapper
- 文档：https://docs.rs/compio-send-wrapper
