# WebAssembly System Interface

## WASI 架構、能力模型、檔案系統、wasmtime（2019-2026）

### 前言

WASI（WebAssembly System Interface）是 WASM 從瀏覽器走向伺服器和邊緣的關鍵。它定義了一組標準化的系統 API——檔案系統、網路、時鐘、亂數——讓 WASM 模組可以在瀏覽器之外執行。

### WASI 架構與演進

| 版本 | 名稱 | 特點 |
|------|------|------|
| WASI 0 | wasi_unstable | 最初的實驗 API |
| Preview 1 | wasi_snapshot_preview1 | 第一個穩定快照 |
| Preview 2 | wasip2 | 基於元件模型 |
| Preview 3 | wasip3（草案） | 非同步 socket、完全元件化 |

### 能力模型

WASI 的核心設計是「最小權限原則」。模組必須明確宣告它需要哪些資源：

```
# 執行時授予精細權限
wasmtime --dir /data:ro          # 唯讀目錄
wasmtime --dir /tmp:rw           # 讀寫目錄
wasmtime --tcplisten 0.0.0.0:8080  # 網路監聽
wasmtime --env DATABASE_URL      # 環境變數
```

未宣告的資源無法存取，即使模組嘗試呼叫相關的 WASI API 也會失敗。

### wasmtime 執行期

wasmtime 是 Bytecode Alliance 開發的 WASM/WASI 執行期：

```bash
# 基本用法
wasmtime hello.wasm

# 指定檔案系統存取
wasmtime --dir /data app.wasm

# 多個模組連結
wasmtime --dir /data --tcplisten 0.0.0.0:8080 server.wasm
```

WASI 應用開發（Rust）：

```rust
fn main() {
    // 如果宿主授予了 --dir 權限，此程式碼可以執行
    let content = std::fs::read_to_string("/data/config.txt")
        .expect("讀取失敗（可能需要 --dir 權限）");
    println!("Config: {}", content);
}
```

編譯到 WASI 目標：

```bash
rustup target add wasm32-wasip1
cargo build --target wasm32-wasip1 --release
wasmtime --dir /data:. target/wasm32-wasip1/release/app.wasm
```

### WasmEdge

WasmEdge 是另一個重要的 WASM 執行期，特別在 AI 推論領域有優勢：

```bash
wasmedge --dir /data:. app.wasm
wasmedge --env OPENAI_KEY=xxx app.wasm
```

WasmEdge 支援 TensorFlow 和 ONNX 的 WASM 綁定，讓 AI 推論可以在邊緣設備上執行。

### 應用場景

1. **命令列工具**：跨平台的單一二進位工具
2. **伺服器端外掛**：安全的第三方程式碼執行環境
3. **邊緣運算**：在 CDN 節點上執行輕量級處理
4. **物聯網**：在資源受限的裝置上執行 WASM 模組

### 小結

WASI 讓 WASM 從瀏覽器走向了伺服器和邊緣。其能力模型提供了比容器更精細、比原生程序更安全的權限控制。隨著 WASI Preview 2/3 的成熟，WASM 在伺服器端的應用將持續擴大。

---

**下一步**：[邊緣運算與 Serverless](focus5.md)

## 延伸閱讀

- [WASI 規範](https://www.google.com/search?q=WASI+specification)
- [wasmtime 指南](https://www.google.com/search?q=wasmtime+guide)
- [WasmEdge 文件](https://www.google.com/search?q=WasmEdge+documentation)
- [WASI 能力模型](https://www.google.com/search?q=WASI+capability+model)
