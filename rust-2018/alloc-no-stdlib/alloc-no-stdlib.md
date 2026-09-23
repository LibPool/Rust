# alloc-no-stdlib

> 标签: Rust

## 简介

A dynamic allocator that may be used with or without the stdlib. This allows a package with nostd to allocate memory dynamically and be used either with a custom allocator, items on the stack, or by a package that wishes to simply use Box<>. It also provides options to use calloc or a mutable global variable for pre-zeroed memory

## 官网

- 官网：https://github.com/dropbox/rust-alloc-no-stdlib
- crates.io 页面：https://crates.io/crates/alloc-no-stdlib
- 文档：https://raw.githubusercontent.com/dropbox/rust-alloc-no-stdlib/master/tests/lib.rs
- 源码仓库：https://github.com/dropbox/rust-alloc-no-stdlib

## 历史版本号

- 当前版本：3.0.0

- 1.0.0
- 1.1.0
- 1.2.0
- 1.3.0
- 2.0.0
- 2.0.1
- 2.0.2
- 2.0.3
- 2.0.4
- 3.0.0

## 获取地址

- Cargo 安装：`cargo add alloc-no-stdlib`
- 下载页面：https://crates.io/crates/alloc-no-stdlib
- 文档：https://raw.githubusercontent.com/dropbox/rust-alloc-no-stdlib/master/tests/lib.rs
