# 非同步與並行

## Async/await、Tokio、Rayon（2019-2023）

### 並行程式的挑戰

並行程式設計是系統程式設計中最困難的部分之一。常見的問題包括：

- **資料競爭**（Data Race）：多個執行緒同時讀寫相同記憶體
- **死鎖**（Deadlock）：多個執行緒互相等待資源
- **飢餓**（Starvation）：某些執行緒永遠無法取得資源
- **非同步回調地獄**：巢狀的回調導致程式碼難以理解

Rust 從設計之初就考慮了這些問題。它的型別系統和所有權模型為安全並行提供了基礎：

```rust
use std::thread;

fn main() {
    let data = vec![1, 2, 3];
    
    let handle = thread::spawn(move || {
        // move 關鍵字將 data 的所有權轉移到新執行緒
        println!("{:?}", data);
    });
    
    // println!("{:?}", data); // 編譯錯誤！data 的所有權已被轉移
    
    handle.join().unwrap();
}
```

### Send 與 Sync

Rust 中並行程式設計的兩個核心 trait：

- **`Send`**：型別可以安全地在執行緒間轉移所有權（如 `String`、`Vec<T>` 是 Send）
- **`Sync`**：型別可以安全地被多個執行緒共享引用（如 `i32`、`Mutex<T>` 是 Sync）

Rust 的編譯器會自動推導這兩個 trait，但也可以手動實作：

```rust
unsafe impl Send for MyType {}
unsafe impl Sync for MyType {}
```

這兩個 trait 的設計讓 Rust 能夠在**編譯期**防止資料競爭——如果一個型別不是 Send，就無法被傳遞到另一個執行緒；如果一個型別不是 Sync，就無法被多個執行緒共享。

### Async/await 的設計

2019 年 11 月，Rust 的 async/await 穩定。Rust 的非同步設計與其他語言有本質不同：

- **零成本抽象**：async 函式在編譯時被轉換為一個狀態機（state machine），不會分配堆記憶體
- **惰性執行**：Future 只有在被 poll 時才會執行，允許靈活的排程
- **無執行時期**：Rust 標準庫沒有內建的 async 執行時期（runtime），需要使用第三方庫（如 Tokio、async-std）

```rust
use tokio::time::{sleep, Duration};

async fn fetch_data(url: &str) -> Result<String, reqwest::Error> {
    let response = reqwest::get(url).await?;
    let body = response.text().await?;
    Ok(body)
}

#[tokio::main]
async fn main() {
    let result = fetch_data("https://api.example.com/data").await;
    match result {
        Ok(data) => println!("{}", data),
        Err(e) => eprintln!("Error: {}", e),
    }
}
```

Rust 的 async 函式編譯後實際上是一個狀態機：

```rust
// 這個 async 函式
async fn example() {
    let a = foo().await;
    let b = bar().await;
    baz(a, b).await;
}

// 被編譯成一個包含狀態的結構體
enum ExampleFuture {
    Start,
    WaitingOnFoo { /* intermediate state */ },
    WaitingOnBar { a: FooOutput },
    Done,
}
```

這意味著 Rust 的 async 函式**不需要分配額外的堆記憶體**——所有狀態都儲存在棧上。

### Tokio 執行時期

Tokio 是 Rust 中最流行的非同步執行時期，提供了：

- **多執行緒工作竊取（work-stealing）排程器**：類似 Go 的 M:N 排程
- **I/O 驅動器**：基於 epoll/kqueue/IOCP 的事件迴圈
- **定時器、訊號、程序管理等實用功能**

```rust
#[tokio::main]
async fn main() {
    // 建立多個並發任務
    let handles: Vec<_> = (0..10)
        .map(|i| {
            tokio::spawn(async move {
                println!("Task {} started", i);
                // 模擬非同步工作
                tokio::time::sleep(Duration::from_secs(1)).await;
                println!("Task {} finished", i);
            })
        })
        .collect();
    
    for handle in handles {
        handle.await.unwrap();
    }
}
```

Tokio 的關鍵設計決策：
- **多執行緒排程器**：充分利用多核心 CPU
- **工作竊取**：避免執行緒間的工作負載不平衡
- **非同步 I/O**：基於 OS 的事件驅動 I/O（epoll/kqueue）

### Rayon：資料並行

對於 CPU 密集的平行計算，Rust 提供了 Rayon 程式庫：

```rust
use rayon::prelude::*;

fn main() {
    let numbers: Vec<i64> = (0..1_000_000).collect();
    
    // 自動平行化
    let sum: i64 = numbers.par_iter().sum();
    
    // 平行 Map/Filter/Reduce
    let result: Vec<_> = numbers
        .par_iter()
        .filter(|&&n| n % 2 == 0)
        .map(|&n| n * n)
        .collect();
}
```

Rayon 的設計哲學是「**無痛平行化**」——只需將 `iter()` 改為 `par_iter()`，就能自動利用多核心。

### 並行與非同步的比較

| 特性 | 非同步 (Tokio) | 並行 (Rayon) |
|------|---------------|-------------|
| 適合場景 | I/O 密集型 | CPU 密集型 |
| 執行緒數量 | 少量（通常等於核心數） | 自動調度 |
| 任務切換 | 在 `.await` 點自動切換 | 隱含在工作竊取中 |
| 資源消耗 | 極低（狀態機） | 較高（OS 執行緒池） |
| 使用方式 | async/await | par_iter/par_for_each |

### 並行程式設計的未來：Rust 2026

Rust 2026 Edition 進一步強化了非同步和並行能力：

1. **Async Iterator**：非同步版本的迭代器，支援非同步的 `next()` 呼叫
2. **Async Drop**：非同步版本的 Drop——在 async 函式中安全地釋放資源
3. **Coroutines**：更靈活的中斷和恢復機制
4. **Structured Concurrency**：組織化、層級化的並發任務管理

### 小結

Rust 的非同步和並行設計體現了 Rust 的核心理念：在編譯期盡可能多地捕獲錯誤，同時提供零成本的抽象。Send/Sync trait 在編譯期防止了資料競爭，而 async/await 則提供了零成本的非同步抽象。

Rust 不會讓並行程式設計變得簡單——但它能讓並行程式變得安全。

---

**下一步**：[生態系統](focus5.md)

## 延伸閱讀

- [Asynchronous Programming in Rust](https://www.google.com/search?q=async+programming+in+Rust)
- [Tokio: The Async Runtime](https://www.google.com/search?q=Tokio+Rust+async+runtime)
- [Rayon: Data Parallelism in Rust](https://www.google.com/search?q=Rayon+Rust+data+parallelism)
