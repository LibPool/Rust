# chess

> 标签: Rust

## 简介

This is a fast chess move generator.  It has a very good set of documentation, so you should take advantage of that.  It (now) generates all lookup tabels with a build.rs file, which means that very little pseudo-legal move generation requires branching.  There are some convenience functions that are exposed to, for example, find all the squares between two squares.  This uses a copy-on-make style structure, and the Board structure is as slimmed down as possible to reduce the cost of copying the board.  There are places to improve perft-test performance further, but I instead opt to be more feature-complete to make it useful in real applications.  For example, I generate both a hash of the board and a pawn-hash of the board for use in evaluation lookup tables (using Zobrist hashing).  There are two ways to generate moves, one is faster, the other has more features that will be useful if making a chess engine.  See the documentation for more details.

## 官网

- 官网：https://github.com/jordanbray/chess
- crates.io 页面：https://crates.io/crates/chess
- 文档：https://jordanbray.github.io/chess/chess/index.html
- 源码仓库：https://github.com/jordanbray/chess

## 历史版本号

- 当前版本：3.2.0

- 1.0.5
- 1.0.6
- 1.0.7
- 2.0.0
- 2.0.1
- 2.0.2
- 3.0.0
- 3.0.1
- 3.0.2
- 3.1.0
- 3.1.1
- 3.2.0
- 共 36 个版本，完整清单见 crates.io。

## 获取地址

- Cargo 安装：`cargo add chess`
- 下载页面：https://crates.io/crates/chess
- 文档：https://jordanbray.github.io/chess/chess/index.html
