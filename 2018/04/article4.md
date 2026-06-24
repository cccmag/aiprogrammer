# WebAssembly 支援更多語言

## 前言

2018 年，WebAssembly（Wasm）在主流瀏覽器獲得全面支援，並且越來越多的語言可以編譯到 Wasm。

## 主要進展

### Rust 到 WebAssembly

```bash
cargo install wasm-pack
wasm-pack build --target web
```

現在可以用 Rust 開發高性能的 Web 應用。

### C/C++ 到 WebAssembly

Emscripten 工具鏈持續改進，使得 C/C++ 程式可以輕鬆編譯到 Wasm。

### 其他語言

- Go (TinyGo)
- Kotlin
- Python (Pyodide)
- Ruby

## 應用場景

1. **影像/影片處理**：高性能的瀏覽器端處理
2. **遊戲**：Unity WebGL 導出
3. **AI 推論**：在瀏覽器中運行機器學習模型
4. **加密運算**：安全的用戶端加密

## 未來展望

WebAssembly 有潛力成為 Web 開發的第三種語言（HTML、CSS、JS、Wasm）。

---

**延伸閱讀**

- [WebAssembly 官方網站](https://www.google.com/search?q=WebAssembly+official+site)
- [Rust + WebAssembly 教程](https://www.google.com/search?q=rust+wasm+tutorial)