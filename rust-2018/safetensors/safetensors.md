# safetensors

> 标签: Rust

## 简介

Provides functions to read and write safetensors which aim to be safer than
their PyTorch counterpart.
The format is 8 bytes which is an unsized int, being the size of a JSON header,
the JSON header refers the `dtype` the `shape` and `data_offsets` which are the offsets
for the values in the rest of the file.

## 官网

- 官网：https://github.com/huggingface/safetensors
- crates.io 页面：https://crates.io/crates/safetensors
- 文档：https://docs.rs/safetensors/
- 源码仓库：https://github.com/huggingface/safetensors

## 历史版本号

- 当前版本：0.8.0

- 0.4.3
- 0.4.4
- 0.4.5
- 0.5.0
- 0.5.1
- 0.5.2
- 0.5.3
- 0.6.0
- 0.6.1
- 0.6.2
- 0.7.0
- 0.8.0
- 共 22 个版本，完整清单见 crates.io。

## 获取地址

- Cargo 安装：`cargo add safetensors`
- 下载页面：https://crates.io/crates/safetensors
- 文档：https://docs.rs/safetensors/
- 最低 Rust 版本：1.80
