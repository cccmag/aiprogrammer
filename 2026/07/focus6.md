# Rust 2026 Edition

## Ownership 2.0、Async Iterator、Coroutines

### Edition 機制

Rust 的 Edition 機制是一項獨特的設計——它允許語言在不相當於舊程式碼的情況下引入破壞性變更：

```toml
[package]
edition = "2024"  # 每個 crate 選擇自己的 edition
```

不同 Edition 的 crate 可以在同一個專案中和平共處。這讓 Rust 能夠持續演進，同時維護向後相容的承諾。

**Edition 歷史**：
- **2015**：初始穩定版
- **2018**：NLL、模組系統重構、impl Trait
- **2021**：Cargo 功能解析器、IntoIterator for arrays、閉包捕獲改進
- **2024**：if let 鏈、型別推斷改進
- **2026**：Ownership 2.0、Async Iterator、Coroutines

### Ownership 2.0

Rust 2026 Edition 最重大的變化是所有權模型的升級。Ownership 2.0 解決了長期以來開發者與借用檢查器「戰鬥」的問題。

**精確借用（Precise Borrowing）**：

```rust
// Rust 2024：借用檢查器有時過於保守
fn process(items: &mut Vec<i32>) {
    let first = &items[0];  // 借用整個 Vec
    // items.push(1);        // 編譯錯誤！
    println!("{}", first);
    items.push(1);           // OK，first 已不再使用（NLL）
}

// Rust 2026：精確借用
fn process(items: &mut Vec<i32>) {
    let first = &items[0];  // 精確借用 Vec[0]，非整個 Vec
    items.push(1);           // OK，push 不影響 Vec[0]
    println!("{}", first);  // 仍然有效
}
```

**部分借用（Partial Borrowing）**：

```rust
struct Point { x: i32, y: i32 }

// Rust 2026：可以同時借用結構體的不同欄位
fn update_point(p: &mut Point) {
    let x = &p.x;           // 借用 x（唯讀）
    let y = &mut p.y;       // 借用 y（可變）
    // 編譯器知道 x 和 y 是不同的記憶體位置
    *y = *x + 1;
}
```

**借用地區（Borrow Regions）**：

```rust
// 2026：精確指定借用的範圍
fn example<'a, 'b>(data: &'a mut [i32]) -> &'b mut i32 
where 'b: 'a {
    &mut data[0]
}
```

### Async Iterator

Rust 2026 引入了原生的 Async Iterator：

```rust
// 非同步迭代器
trait AsyncIterator {
    type Item;
    
    async fn next(&mut self) -> Option<Self::Item>;
}

// 使用範例
async fn process_stream() {
    let mut stream = async_stream! {
        for i in 0..10 {
            tokio::time::sleep(Duration::from_secs(1)).await;
            yield i;
        }
    };
    
    while let Some(value) = stream.next().await {
        println!("Got: {}", value);
    }
}
```

這使得非同步資料流處理變得更加自然——不再需要手動實作 `Stream` trait。

### Coroutines

Coroutines 是 Rust 2026 引入的另一個重大功能：

```rust
// Generator coroutine
fn generate() -> impl Iterator<Item = i32> {
    coroutine {
        let mut i = 0;
        loop {
            yield i;
            i += 1;
        }
    }
}

// 有狀態的 coroutine
fn stateful_worker() -> impl Coroutine<Yield = String, Return = ()> {
    coroutine {
        let mut count = 0;
        loop {
            count += 1;
            yield format!("processed: {}", count);
        }
    }
}

// 用於非同步場景
fn async_coroutine() -> impl Coroutine<Yield = Task, Return = ()> {
    coroutine {
        // 分階段執行複雜任務
        let data = yield Task::Fetch("https://api.example.com/data".into());
        let processed = yield Task::Process(data);
        yield Task::Save(processed);
    }
}
```

Coroutines 與 async/await 的關係：
- **async/await**：用於 I/O 密集型非同步程式設計
- **coroutines**：用於需要暫停/恢復的通用控制流

### 其他新功能

**改進的型別推斷**：

```rust
// Rust 2026 的型別推斷更加智能
let result = [1, 2, 3]
    .iter()
    .filter_map(|x| if *x > 1 { Some(x * 2) } else { None })
    .collect();  // 自動推斷為 Vec<i32>
```

**模式匹配增強**：

```rust
// OR 模式 + 綁定
match value {
    (Ok(x) | Err(x)) if x > 0 => println!("Positive: {}", x),
    _ => println!("Non-positive or zero"),
}
```

**Traitlets**：

```rust
// 輕量級的 trait 定義，類似介面
trailet Drawable {
    fn draw(&self);
}

// 與傳統 trait 不同，trailet 支援動態分發
// 而不需要 Box<dyn Drawable> 的開銷
```

### 編譯時間的進一步縮短

Rust 2026 引入了「模組化程式碼生成」（Modular Codegen）：

```bash
# 2024：完整編譯（含 LTO）
cargo build --release  # 45 秒

# 2026：模組化程式碼生成
cargo build --release  # 12 秒（同一個專案）
```

這得益於：
1. ML 驅動的編譯最佳化——預測哪些函式需要內聯
2. 改進的增量編譯——更精確的依賴追蹤
3. 平行化 LTO——連結時最佳化也可以平行執行

### Edition 遷移工具

Rust 2026 Edition 包含了一個強大的遷移工具：

```bash
# 自動遷移到新版
cargo fix --edition
```

這個工具會：
1. 自動修正需要變更的語法
2. 標記需要手動審查的部分
3. 提供每個變更的詳細解釋

### 小結

Rust 2026 Edition 是 Rust 語言發展的又一個里程碑。Ownership 2.0 讓借用檢查器更加智能，Async Iterator 和 Coroutines 讓非同步程式設計更加靈活。這些改進的共同目標是：**讓 Rust 在保持記憶體安全的同時，開發效率也更高**。

Rust 2026 Edition 不是終點——Rust 團隊已經在規劃 Ownership 3.0、編譯器裡的多層次最佳化（ML compiler optimization）和更強大的類型系統。

---

**下一步**：[AI + Rust](focus7.md)

## 延伸閱讀

- [Rust 2026 Edition Guide](https://www.google.com/search?q=Rust+2026+Edition+guide)
- [Ownership 2.0 RFC](https://www.google.com/search?q=Rust+ownership+2.0+RFC)
- [Async Iterator RFC](https://www.google.com/search?q=Rust+async+iterator+RFC)
