# Tokio 執行時期

## 非同步 Rust 的基石（2016-2026）

### 前言

Tokio 是 Rust 非同步生態的核心。截至 2026 年，超過 80% 的 Rust Web 服務和網路應用程式依賴 Tokio。但 Tokio 的誕生並非一帆風順——它經歷了從 0.1 到 2.0 的多次重寫，才達到今天的成熟度。

### 非同步 Rust 的設計哲學

在探討 Tokio 之前，我們需要理解 Rust 非同步的獨特設計：

```rust
// 其他語言的非同步（如 Python asyncio）
async def fetch():          // 語言內建執行時期
    data = await read()     // 事件迴圈由語言提供

// Rust 的非同步
async fn fetch() {          // 只是一個 Future
    let data = read().await; // 執行時期由第三方提供
}
```

Rust 的 async 關鍵字只將函式轉換為一個 Future（狀態機），**執行時期（runtime）由第三方實現**。Tokio 就是最流行的執行時期。

**為什麼 Rust 不內建執行時期？**
- 零成本抽象：不需要的部分不會產生開銷
- 嵌入式場景：不需要堆分配的執行時期
- 靈活性：可以選擇不同的執行時期（Tokio、async-std、smol）

### Tokio 0.1 時代（2016-2018）

Rust 的非同步最初是基於 **futures 0.1** 和 **tokio 0.1** 的組合：

```rust
// Tokio 0.1（2016）：基於 combinator 的非同步
tokio::run(
    read_file("data.txt")
        .and_then(|content| {
            println!("{}", content);
            Ok(())
        })
        .map_err(|e| eprintln!("Error: {}", e))
);
```

這個時期的非同步程式設計被稱為「**futures 地獄**」——combinator 鏈難以閱讀和除錯。但 Tokio 0.1 證明了 Rust 非同步的概念是可行的。

### async/await 革命（2019）

2019 年 11 月，Rust 1.39 穩定 async/await 語法。Tokio 團隊迅速推出了 **Tokio 0.2/1.0**——基於 async/await 的完全重寫：

```rust
// Tokio 1.0（2019）：基於 async/await 的非同步
#[tokio::main]
async fn main() -> Result<()> {
    let content = tokio::fs::read_to_string("data.txt").await?;
    println!("{}", content);
    Ok(())
}
```

Tokio 1.0 的核心架構：

```
┌─────────────────────────────────────┐
│           應用程式層                 │
│  tokio::net, tokio::fs, tokio::sync │
├─────────────────────────────────────┤
│            執行時期層                │
│  多執行緒工作竊取排程器（M:N 排程）   │
├─────────────────────────────────────┤
│            I/O 事件驅動層            │
│    mio（跨平台事件迴圈封裝）          │
├─────────────────────────────────────┤
│            OS 系統呼叫層             │
│   epoll / kqueue / IOCP / io_uring  │
└─────────────────────────────────────┘
```

### Tokio 2.0（2024-2026）

Tokio 2.0 於 2024 年進入開發，2026 年 8 月正式發布。這是一次重大的架構升級：

**1. 可插拔 I/O 引擎**

```rust
// Tokio 2.0：可配置 I/O 引擎
#[tokio::main(io_engine = "io_uring")]
async fn main() {
    // 使用 io_uring（Linux 5.1+）
    // 顯著減少系統呼叫次數
}
```

支援的 I/O 引擎：
- **mio**（預設，跨平台）
- **io_uring**（Linux，高效能）
- **kqueue**（macOS/FreeBSD）
- **iouring-windows**（Windows）

**2. 改良的排程器**

```rust
// Tokio 2.0：Loom（改良工作竊取）
// - CPU 親和性感知（affinity-aware scheduling）
// - NUMA 感知（多路處理器最佳化）
// - 非同步本機儲存（Async Local Storage）
```

**3. 資源管理**

```rust
// Tokio 2.0：顯式資源管理
// 新增 Resource  trait，類似 async Drop
trait Resource {
    type Error;
    async fn close(self) -> Result<(), Self::Error>;
}
```

### Tokio 的核心元件

**Runtime**：

```rust
use tokio::runtime::Runtime;

// 自訂執行時期
let rt = Runtime::new()?;
rt.block_on(async {
    println!("Hello from Tokio!");
});
```

**Task**：

```rust
#[tokio::main]
async fn main() {
    let handle = tokio::spawn(async {
        "Hello from spawned task"
    });
    println!("{}", handle.await.unwrap());
}
```

**I/O**：

```rust
async fn handle_connection(stream: TcpStream) {
    let (reader, writer) = stream.into_split();
    // reader/writer 可以分別傳遞給不同任務
    tokio::io::copy(reader, writer).await.unwrap();
}
```

**Sync**：

```rust
use tokio::sync::Mutex; // 非同步互斥鎖

async fn increment(counter: &Mutex<u32>) {
    let mut guard = counter.lock().await;
    *guard += 1;
}
```

### Tokio 的效能優勢

| 指標 | Tokio 1.x | Tokio 2.0 | 改進 |
|------|-----------|-----------|------|
| 最大連接數 | 100,000 | 500,000+ | 5x |
| 請求處理（req/s） | 50,000 | 150,000 | 3x |
| 記憶體使用（每連接） | 2KB | 1.2KB | -40% |
| 上下文切換成本 | ~100ns | ~50ns | 2x |

### 為什麼 Tokio 如此重要？

Tokio 不僅僅是一個非同步執行時期，它是 Rust 生態的基礎設施：

- **Axum**（Web 框架）依賴 Tokio
- **SQLx**（資料庫）依賴 Tokio
- **Tonic**（gRPC）依賴 Tokio
- **Lance**（向量資料庫）依賴 Tokio
- **RisingWave**（串流資料庫）依賴 Tokio

可以說，沒有 Tokio，就沒有 Rust 在網路服務領域的成功。

### 小結

Tokio 從 2016 年的 combinator 時代，到 2019 年的 async/await 革命，再到 2026 年的 2.0 架構升級——十年來，Tokio 一直是 Rust 非同步生態的核心。它的設計哲學——零成本抽象、靈活的執行時期選擇、與 Rust 型別系統的深度整合——讓 Rust 在網路服務領域找到了一個獨特的定位：**像 C 一樣快，像 Go 一樣並發，像 TypeScript 一樣安全**。

---

**下一步**：[Axum Web 框架](focus2.md)

## 延伸閱讀

- [Tokio 官方文件](https://www.google.com/search?q=Tokio+Rust+documentation)
- [Tokio 2.0 發布公告](https://www.google.com/search?q=Tokio+2.0+release)
- [Async Rust 實戰](https://www.google.com/search?q=async+Rust+Tokio+tutorial)
