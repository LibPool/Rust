# os-thread-local

> 标签: Rust

## 简介

OS-backed thread-local storage.

This crate provides a `ThreadLocal` type as an alternative to
`std::thread_local!` that allows per-object thread-local storage, while
providing a similar API. It always uses the thread-local storage primitives
provided by the OS.

## 官网

- crates.io 页面：https://crates.io/crates/os-thread-local
- 源码仓库：https://github.com/glandium/os-thread-local

## 历史版本号

- 当前版本：0.1.3

- 0.1.0
- 0.1.1
- 0.1.2
- 0.1.3

## 获取地址

- Cargo 安装：`cargo add os-thread-local`
- 下载页面：https://crates.io/crates/os-thread-local
