# glium

> 标签: Rust

## 简介

Elegant and safe OpenGL wrapper.

Glium is an intermediate layer between OpenGL and your application. You still need to manually handle
the graphics pipeline, but without having to use OpenGL's old and error-prone API.

Its objectives:

 - Be safe to use. Many aspects of OpenGL that can trigger a crash if misused are automatically handled by glium.
 - Provide an API that enforces good pratices such as RAII or stateless function calls.
 - Be compatible with all OpenGL versions that support shaders, providing unified API when things diverge.
 - Avoid all OpenGL errors beforehand.
 - Produce optimized OpenGL function calls, and allow the user to easily use modern OpenGL techniques.

## 官网

- crates.io 页面：https://crates.io/crates/glium
- 文档：https://docs.rs/glium
- 源码仓库：https://github.com/glium/glium

## 历史版本号

- 当前版本：0.36.0

- 0.29.0
- 0.29.1
- 0.30.0
- 0.30.1
- 0.30.2
- 0.31.0
- 0.32.0
- 0.32.1
- 0.33.0
- 0.34.0
- 0.35.0
- 0.36.0
- 共 98 个版本，完整清单见 crates.io。

## 获取地址

- Cargo 安装：`cargo add glium`
- 下载页面：https://crates.io/crates/glium
- 文档：https://docs.rs/glium
