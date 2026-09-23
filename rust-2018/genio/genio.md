# genio

> 标签: Rust

## 简介

A type safe, low level replacement for `std::io`.

Supports `no_std` for embedded development, just disable cargo feature
`std`.

Because of limitations of `std::io::Error` type, `genio` provides `Read` and
`Write` traits that allow implementors to choose their own type. This type can
be better at expressing what kinds of error can happen.

## 官网

- 官网：https://github.com/Kixunil/genio
- crates.io 页面：https://crates.io/crates/genio
- 文档：https://docs.rs/genio
- 源码仓库：https://github.com/Kixunil/genio

## 历史版本号

- 当前版本：0.2.1

- 0.1.0
- 0.2.0
- 0.2.1

## 获取地址

- Cargo 安装：`cargo add genio`
- 下载页面：https://crates.io/crates/genio
- 文档：https://docs.rs/genio
