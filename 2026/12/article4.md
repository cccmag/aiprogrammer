# WASI 與邊緣運算

## 1. 引言

WebAssembly 的原始設計目標是瀏覽器。但很快地，人們發現 WASM 的輕量、安全、高效特性在伺服器端同樣有巨大價值。WASI（WebAssembly System Interface）的誕生讓 WASM 走出了瀏覽器，可以在命令列、伺服器、邊緣節點上執行。

## 2. WASI 架構設計

### 2.1 能力模型（Capability Model）

WASI 最核心的設計理念是「最小權限原則」。不同於傳統程序擁有完整的系統權限，WASI 模組必須明確宣告它需要存取哪些資源：

```
WASI 模組
├── filesystem: /data (read-only)
│              /tmp (read-write)
├── networking: example.com:443 (outbound)
├── random: yes
└── clock: monotonic
```

這種能力模型比 Linux 的 user/group 權限模型更精細，也比容器的 namespace 隔離更輕量。

### 2.2 WASI 層級

| 層級 | 名稱 | 功能 |
|------|------|------|
| WASI 0 | wasi_unstable | 最初的實驗 API |
| WASI Preview 1 | wasi_snapshot_preview1 | 第一個穩定快照（2020） |
| WASI Preview 2 | wasip2 | 基於元件模型（2024） |
| WASI Preview 3 | wasip3（草案） | 非同步 socket、完全元件化（2026） |

## 3. wasmtime 執行期

wasmtime 是 Bytecode Alliance 開發的 WASM/WASI 執行期，也是目前最成熟的 WASM 執行期之一。

### 3.1 基本使用

```bash
# 安裝 wasmtime
curl https://wasmtime.dev/install.sh -sSf | bash

# 執行 WASM 模組
wasmtime hello.wasm

# 賦予檔案系統權限
wasmtime --dir /data hello.wasm

# 賦予網路權限
wasmtime --tcplisten 0.0.0.0:8080 server.wasm
```

### 3.2 使用 Rust 開發 WASI 應用

```rust
use std::fs;
use std::io::Read;

fn main() {
    // WASI 環境下，std::fs 可以工作（如果被允許）
    let mut file = fs::File::open("/data/config.txt").unwrap();
    let mut contents = String::new();
    file.read_to_string(&mut contents).unwrap();
    println!("Config: {}", contents);
}
```

編譯到 WASI 目標：

```bash
rustup target add wasm32-wasip1
cargo build --target wasm32-wasip1 --release
wasmtime --dir /data target/wasm32-wasip1/release/myapp.wasm
```

## 4. WasmEdge 執行期

WasmEdge 是另一個重要的 WASM 執行期，特別在 AI 推論領域有獨特優勢：

```bash
# 使用 WasmEdge 執行 WASM 模組
wasmedge app.wasm
wasmedge --dir /data:. app.wasm
```

WasmEdge 支援 TensorFlow 和 ONNX 的 WASM 綁定，讓 WASM 模組可以直接執行機器學習推論。

## 5. 檔案系統與網路存取

### 5.1 檔案系統

WASI Preview 1 的檔案系統 API 是本機（同步）的，Preview 2/3 則提供了非同步版本：

```rust
use wasi::fs::*;

fn read_file_example() -> Result<(), Box<dyn std::error::Error>> {
    let fd = open("/data/log.txt")?;
    let metadata = stat(fd)?;
    let mut buf = vec![0u8; metadata.size as usize];
    read(fd, &mut buf)?;
    println!("{}", String::from_utf8_lossy(&buf));
    close(fd)?;
    Ok(())
}
```

### 5.2 網路存取

WASI Preview 2 新增了 network socket API：

```rust
use wasi::network::*;

async fn fetch_url(url: &str) -> Result<String, Error> {
    let sock = open_tcp_socket()?;
    sock.connect("example.com:80").await?;
    sock.send(format!("GET / HTTP/1.1\r\nHost: example.com\r\n\r\n")).await?;
    let response = sock.receive().await?;
    Ok(String::from_utf8_lossy(&response).to_string())
}
```

## 6. WASM 作為邊緣運算執行期

### 6.1 為什麼 WASM 適合邊緣運算？

1. **冷啟動極快**：WASM 模組的實體化時間通常在 50-500 µs，遠快於容器的 100-500ms
2. **輕量級隔離**：每個 WASM 模組的記憶體開銷約 1-10 MB（Container 需要 50-200 MB）
3. **多語言支援**：同一個邊緣平台可以執行 Rust、C、Go、AssemblyScript 寫的模組
4. **安全**：WASI 的能力模型比容器安全策略更精細、更可控

### 6.2 邊緣計算模型

```
客戶端請求
    │
    ▼
邊緣節點（CDN 邊緣）
    ├── WASM 沙箱 1 (Rust 認證模組)
    ├── WASM 沙箱 2 (Go 資料處理)
    └── WASM 沙箱 3 (AssemblyScript 路由)
    │
    ▼
後端服務 （必要時）
```

## 7. 結語

WASI 是 WebAssembly 從瀏覽器走向伺服器和邊緣的關鍵。它的能力模型提供了一種比容器更安全、比原生程序更輕量的執行環境。隨著 WASI Preview 2/3 的成熟和各大雲端平台的支援，WASM 正在成為邊緣運算的新標準執行期。

---

## 延伸閱讀

- [WASI 官方規範](https://www.google.com/search?q=WASI+specification)
- [wasmtime 指南](https://www.google.com/search?q=wasmtime+guide)
- [WasmEdge 文件](https://www.google.com/search?q=WasmEdge+documentation)
- [Bytecode Alliance](https://www.google.com/search?q=Bytecode+Alliance)
