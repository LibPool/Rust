# matrixmultiply

> 标签: Rust

## 简介

General matrix multiplication for f32 and f64 matrices. Operates on matrices with general layout (they can use arbitrary row and column stride). Detects and uses SIMD features on x86/x86-64 and AArch64 transparently for higher performance. Uses a microkernel strategy, so that the implementation is easy to parallelize and optimize.

Supports multithreading.

## 官网

- crates.io 页面：https://crates.io/crates/matrixmultiply
- 文档：https://docs.rs/matrixmultiply/
- 源码仓库：https://github.com/bluss/matrixmultiply/

## 历史版本号

- 当前版本：0.3.11

- 0.3.0
- 0.3.1
- 0.3.2
- 0.3.3
- 0.3.4
- 0.3.5
- 0.3.6
- 0.3.7
- 0.3.8
- 0.3.9
- 0.3.10
- 0.3.11
- 共 33 个版本，完整清单见 crates.io。

## 获取地址

- Cargo 安装：`cargo add matrixmultiply`
- 下载页面：https://crates.io/crates/matrixmultiply
- 文档：https://docs.rs/matrixmultiply/
- 最低 Rust 版本：1.75.0
