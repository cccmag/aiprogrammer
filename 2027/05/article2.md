# WASI 深入探討 — 系統介面實戰

## 1. 引言

WASI（WebAssembly System Interface）是 WASM 走出瀏覽器的關鍵。它定義了 WASM 模組與作業系統互動的標準介面——從檔案讀寫到網路通訊，從時鐘擷取到亂數產生。本文將從實戰角度，深入探討 WASI 的實作細節與開發模式。

## 2. WASI 的能力模型

WASI 最獨特的設計是其「能力為基礎的安全模型」（Capability-based Security）。每個 WASM 模組在預設情況下沒有任何系統存取權限，必須由主機明確授予：

```
WASI 能力授予示意圖：
─────────────────────────

主機授予的能力：
┌──────────────────────────────────┐
│ wasmtime run                      │
│   --dir ./data::/data             │  ← 檔案系統讀寫能力
│   --tcplisten 0.0.0.0:8080       │  ← 網路聆聽能力
│   --env DB_URL=postgres://...     │  ← 環境變數存取能力
│   --clock                         │  ← 時鐘存取能力
│   --random                        │  ← 亂數產生能力
│   module.wasm                     │
└──────────────────────────────────┘
```

### 2.1 在 Rust 中使用 WASI 檔案系統

```rust
use std::fs::{self, File};
use std::io::{Read, Write, BufReader};

/// 讀取配置檔案（需要主機授予目錄權限）
fn load_config(path: &str) -> Result<Config, Box<dyn std::error::Error>> {
    let file = File::open(path)?;
    let reader = BufReader::new(file);
    let config: Config = serde_json::from_reader(reader)?;
    Ok(config)
}

/// 寫入處理結果
fn save_result(path: &str, data: &[u8]) -> Result<(), Box<dyn std::error::Error>> {
    let mut file = File::create(path)?;
    file.write_all(data)?;
    Ok(())
}

/// 遞迴列出目錄內容
fn list_directory(path: &str, indent: usize) -> std::io::Result<()> {
    let entries = fs::read_dir(path)?;
    for entry in entries {
        let entry = entry?;
        let path = entry.path();
        let prefix = "  ".repeat(indent);
        if path.is_dir() {
            println!("{}[DIR] {}", prefix, path.display());
            list_directory(&path.display().to_string(), indent + 1)?;
        } else {
            println!("{}[FILE] {} ({} bytes)",
                prefix, path.display(), fs::metadata(&path)?.len());
        }
    }
    Ok(())
}
```

這些標準的 Rust `std::fs` 和 `std::io` API 在 `wasm32-wasip1` 目標下會自動對應到 WASI 系統呼叫。開發者無需使用任何特殊的 WASI API——標準程式庫已經做好抽象。

## 3. WASI 網路程式設計

WASI Preview 2 引入了完整的非同步網路支援：

```rust
use std::net::{TcpListener, TcpStream};
use std::io::{Read, Write};
use std::thread;

/// 簡易 HTTP 伺服器（WASI 相容）
fn start_http_server(addr: &str) -> Result<(), Box<dyn std::error::Error>> {
    let listener = TcpListener::bind(addr)?;
    println!("Server listening on {}", addr);

    for stream in listener.incoming() {
        match stream {
            Ok(mut stream) => {
                thread::spawn(move || {
                    handle_client(&mut stream).unwrap_or_else(|e| {
                        eprintln!("Client error: {}", e);
                    });
                });
            }
            Err(e) => eprintln!("Connection failed: {}", e),
        }
    }
    Ok(())
}

fn handle_client(stream: &mut TcpStream) -> Result<(), Box<dyn std::error::Error>> {
    let mut buffer = [0u8; 4096];
    let bytes_read = stream.read(&mut buffer)?;
    let request = String::from_utf8_lossy(&buffer[..bytes_read]);

    let response = format!(
        "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nHello from WASI! Your request was {} bytes",
        bytes_read
    );
    stream.write_all(response.as_bytes())?;
    stream.flush()?;
    Ok(())
}
```

在 `wasm32-wasip2` 目標下，非同步網路透過 WASI 的 `stream` 和 `poll` 介面實作。這意味著 WASM 模組可以處理大量並發連線，而無需為每個連線建立作業系統執行緒。

## 4. WASI 時鐘與時間操作

```rust
use std::time::{SystemTime, UNIX_EPOCH, Duration};

/// 高精度計時器
struct Stopwatch {
    start: SystemTime,
}

impl Stopwatch {
    fn new() -> Self {
        Stopwatch { start: SystemTime::now() }
    }

    fn elapsed_ms(&self) -> u128 {
        self.start.elapsed()
            .unwrap_or(Duration::ZERO)
            .as_millis()
    }

    fn elapsed_ns(&self) -> u128 {
        self.start.elapsed()
            .unwrap_or(Duration::ZERO)
            .as_nanos()
    }
}

/// 取得目前 UTC 時間的字串表示
fn current_timestamp() -> String {
    let now = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap_or(Duration::ZERO);
    let secs = now.as_secs();
    let nanos = now.subsec_nanos();

    // 格式化為 ISO 8601
    let days = secs / 86400;
    let time_secs = secs % 86400;
    let hours = time_secs / 3600;
    let minutes = (time_secs % 3600) / 60;
    let seconds = time_secs % 60;

    format!("2026-{:02}-{:02}T{:02}:{:02}:{:02}.{:09}Z",
        1, days as u32, hours, minutes, seconds, nanos)
}
```

## 5. WASI 環境變數與命令列參數

```rust
use std::env;

fn main() {
    // 讀取環境變數（需要主機授予 --env 權限）
    let db_url = env::var("DATABASE_URL")
        .unwrap_or_else(|_| "http://localhost:5432".to_string());
    let log_level = env::var("LOG_LEVEL")
        .unwrap_or_else(|_| "info".to_string());

    // 讀取命令列參數
    let args: Vec<String> = env::args().collect();
    println!("Arguments: {:?}", args);
    println!("DATABASE_URL: {}", db_url);
    println!("LOG_LEVEL: {}", log_level);
}
```

## 6. 自訂 WASI 介面實作

在真實世界中，您可能需要自訂 WASI 介面。以下是使用 `wasmtime` 實作自訂 WASI 功能的範例：

```rust
use wasmtime::*;
use wasmtime_wasi::*;

struct CustomWasi {
    table: ResourceTable,
    ctx: WasiCtx,
}

impl CustomWasi {
    fn new(allow_net: bool, allowed_dirs: Vec<String>) -> Self {
        let mut ctx_builder = WasiCtxBuilder::new();

        if allow_net {
            ctx_builder = ctx_builder.inherit_network();
        }
        for dir in allowed_dirs {
            ctx_builder = ctx_builder.preopened_dir(
                dir.clone(), &dir, DirPerms::all(), FilePerms::all(),
            ).unwrap();
        }

        CustomWasi {
            table: ResourceTable::new(),
            ctx: ctx_builder.build(),
        }
    }
}
```

## 7. WASI 的實際應用場景

### 7.1 資料 ETL 管線

```
WASI ETL 管線：
─────────────────────────

來源資料（CSV / JSON / Parquet）
    │
    ▼
WASM ETL 元件（wasm32-wasip1）
    ├── 讀取來源檔案（WASI 檔案系統）
    ├── 解析與轉換資料
    ├── 套用過濾器與聚合
    └── 寫入目標檔案（WASI 檔案系統）
    │
    ▼
輸出資料（Parquet / Arrow）
```

### 7.2 外掛系統

WASI 的安全模型讓它成為外掛系統的理想執行期。以下是外掛載入流程：

```rust
// 主機端載入 WASI 外掛
fn load_plugin(wasm_bytes: &[u8], allowed_path: &str) -> Result<(), Box<dyn std::error::Error>> {
    let engine = Engine::new(&Config::new())?;
    let mut linker = Linker::new(&engine);

    // 設定 WASI 環境
    let wasi_ctx = WasiCtxBuilder::new()
        .preopened_dir(allowed_path, "/data", DirPerms::all(), FilePerms::all())?
        .build();
    let mut store = Store::new(&engine, wasi_ctx);

    // 載入 WASM 外掛
    let module = Module::new(&engine, wasm_bytes)?;
    linker.module(&mut store, "", &module)?;

    // 執行外掛
    let instance = linker.instantiate(&mut store, &module)?;
    let run = instance.get_typed_func::<(), ()>(&mut store, "_start")?;
    run.call(&mut store, ())?;

    Ok(())
}
```

## 8. WASI 的限制與未來

WASI 在 2026 年仍有以下限制：

1. **執行緒支援有限**：WASI 尚未標準化執行緒模型。雖然 `wasm32-wasip1` 支援基本執行緒，但 `wasm32-wasip2` 的執行緒 API 仍在制定中。
2. **GPU 存取**：WASI 目前不包含 GPU 存取介面。WASI-ML 提案正在解決這個問題。
3. **非同步 I/O**：WASI Preview 2 引入了非同步串流，但與 Linux io_uring 或 Windows IOCP 相比仍有差距。

## 9. 結語

WASI 將 WASM 從一個沙箱計算引擎轉變為功能完整的系統執行期。無論是檔案操作、網路通訊、還是時間度量，WASI 都提供了標準化的介面。結合 Rust 的標準程式庫抽象，開發者可以用最少的額外學習成本，將現有應用移植到 WASM 環境。

---

## 延伸閱讀

- [WASI Preview 2 規範](https://www.google.com/search?q=WASI+Preview+2+specification)
- [wasmtime WASI 整合指南](https://www.google.com/search?q=wasmtime+WASI+integration)
- [Rust WASI 應用開發](https://www.google.com/search?q=Rust+WASI+application+development)
- [WASI 網路 socket 範例](https://www.google.com/search?q=WASI+network+socket+example)
