# str_stack

> 标签: Rust

## 简介

A string allocator for allocating many write-once strings.

This library is primarily useful for parsing where you need to repeatedly build
many strings, use them, and then throw them away. Instead of allocating many independent strings, this library will put them all in the same buffer.

## 官网

- crates.io 页面：https://crates.io/crates/str_stack
- 文档：https://docs.rs/str_stack/latest/str_stack/
- 源码仓库：https://github.com/Stebalien/str_stack

## 历史版本号

- 当前版本：0.1.1

- 0.1.0
- 0.1.1

## 获取地址

- Cargo 安装：`cargo add str_stack`
- 下载页面：https://crates.io/crates/str_stack
- 文档：https://docs.rs/str_stack/latest/str_stack/
