# cmov

> 标签: Rust

## 简介

Conditional move CPU intrinsics which are guaranteed on major platforms (ARM32/ARM64, x86/x86_64,
RISC-V) to execute in constant-time and not be rewritten as branches by the compiler. Provides
wrappers for the CMOV family of instructions on x86/x86_64 and CSEL on AArch64, along with a
portable "best-effort" pure Rust fallback implementation.

## 官网

- crates.io 页面：https://crates.io/crates/cmov
- 文档：https://docs.rs/cmov
- 源码仓库：https://github.com/RustCrypto/utils

## 历史版本号

- 当前版本：0.5.4

- 0.4.4
- 0.4.5
- 0.4.6
- 0.5.0-pre.0
- 0.5.0-pre.1
- 0.5.0-pre.2
- 0.5.2
- 0.5.3
- 0.5.4

## 获取地址

- Cargo 安装：`cargo add cmov`
- 下载页面：https://crates.io/crates/cmov
- 文档：https://docs.rs/cmov
- 最低 Rust 版本：1.85
