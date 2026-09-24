# trust-dns-server

> 标签: Rust

## 简介

Trust-DNS is a safe and secure DNS server with DNSSEC support.
 Eventually this could be a replacement for BIND9. The DNSSEC support allows
 for live signing of all records, in it does not currently support
 records signed offline. The server supports dynamic DNS with SIG0 authenticated
 requests. Trust-DNS is based on the Tokio and Futures libraries, which means
 it should be easily integrated into other software that also use those
 libraries.

## 官网

- 官网：https://trust-dns.org/
- crates.io 页面：https://crates.io/crates/trust-dns-server
- 文档：https://docs.rs/trust-dns-server
- 源码仓库：https://github.com/bluejekyll/trust-dns

## 历史版本号

- 当前版本：0.23.2

- 0.21.0
- 0.21.1
- 0.21.2
- 0.22.0
- 0.23.0-alpha.2
- 0.22.1
- 0.23.0-alpha.3
- 0.23.0-alpha.4
- 0.23.0-alpha.5
- 0.23.0
- 0.23.1
- 0.23.2
- 共 60 个版本，完整清单见 crates.io。

## 获取地址

- Cargo 安装：`cargo add trust-dns-server`
- 下载页面：https://crates.io/crates/trust-dns-server
- 文档：https://docs.rs/trust-dns-server
- 最低 Rust 版本：1.64.0
