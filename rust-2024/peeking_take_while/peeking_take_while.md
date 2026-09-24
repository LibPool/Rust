# peeking_take_while

> 标签: Rust

## 简介

Like `Iterator::take_while`, but calls the predicate on a peeked value. This allows you to use `Iterator::by_ref` and `Iterator::take_while` together, and still get the first value for which the `take_while` predicate returned false after dropping the `by_ref`.

## 官网

- crates.io 页面：https://crates.io/crates/peeking_take_while
- 源码仓库：https://github.com/fitzgen/peeking_take_while

## 历史版本号

- 当前版本：1.0.0

- 0.1.0
- 0.1.1
- 0.1.2
- 1.0.0

## 获取地址

- Cargo 安装：`cargo add peeking_take_while`
- 下载页面：https://crates.io/crates/peeking_take_while
