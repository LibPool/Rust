# hyperlane-log

> 标签: Rust

## 简介

A Rust logging library that supports both asynchronous and synchronous logging. It provides multiple log levels, such as error, info, and debug. Users can define custom log handling methods and configure log file paths. The library supports log rotation, automatically creating a new log file when the current file reaches the specified size limit. It allows flexible logging configurations, making it suitable for both high-performance asynchronous applications and traditional synchronous logging scenarios. The asynchronous mode utilizes Tokio's async channels for efficient log buffering, while the synchronous mode writes logs directly to the file system.

## 官网

- crates.io 页面：https://crates.io/crates/hyperlane-log
- 源码仓库：https://github.com/hyperlane-dev/hyperlane-log.git

## 历史版本号

- 当前版本：4.0.16

- 4.0.4
- 4.0.5
- 4.0.6
- 4.0.7
- 4.0.8
- 4.0.9
- 4.0.10
- 4.0.12
- 4.0.13
- 4.0.14
- 4.0.15
- 4.0.16
- 共 161 个版本，完整清单见 crates.io。

## 获取地址

- Cargo 安装：`cargo add hyperlane-log`
- 下载页面：https://crates.io/crates/hyperlane-log
