# noto-sans-mono-bitmap

> 标签: Rust

## 简介

Provides pre-rasterized characters from the "Noto Sans Mono" font in different sizes and font
weights for multiple unicode ranges. This crate is `no_std` and needs no allocations or floating
point operations. Useful in kernels and bootloaders when only "soft-float" is available. Strictly
speaking, this crate is more than a basic bitmap font, because it encodes each pixel as a byte
and not as a bit, which results in a much nicer result on the screen.

## 官网

- 官网：https://github.com/phip1611/noto-sans-mono-bitmap-rs
- crates.io 页面：https://crates.io/crates/noto-sans-mono-bitmap
- 文档：https://docs.rs/noto-sans-mono-bitmap
- 源码仓库：https://github.com/phip1611/noto-sans-mono-bitmap-rs

## 历史版本号

- 当前版本：0.3.2

- 0.1.0
- 0.1.1
- 0.1.2
- 0.1.3
- 0.1.4
- 0.1.5
- 0.1.6
- 0.2.0
- 0.3.0
- 0.3.1
- 0.3.2

## 获取地址

- Cargo 安装：`cargo add noto-sans-mono-bitmap`
- 下载页面：https://crates.io/crates/noto-sans-mono-bitmap
- 文档：https://docs.rs/noto-sans-mono-bitmap
- 最低 Rust 版本：1.56.1
