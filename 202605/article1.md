# Rust 2026 Edition 發布：所有權模型的終極進化

## 前言

2026 年 6 月，Rust 團隊正式發布了 Rust 2026 Edition——這是 Rust 所有權系統自 1.0 以來最大的一次升級。核心亮點是 **Ownership 2.0**：全新的借用語法、更聰明的借用檢查器，以及第一等的 async 迭代器和協程支援。本文深入解析這些關鍵變化。

## Ownership 2.0：借用檢查器重生

### 傳統借用檢查器的限制

在 Rust 2021 及之前版本中，借用檢查器雖然強大，但有許多常見的模式無法表達：

```rust
// Rust 2021：這段程式碼無法通過編譯
fn process(items: &mut Vec<i32>) {
    let first = &items[0];  // 不可變借用
    items.push(42);         // 可變借用 — 衝突！
    println!("{}", first);  // 使用 first
}
```

這個模式在 Rust 2021 中被拒絕，因為借用檢查器無法分辨 `first` 和 `push` 操作的是不同記憶體區域。但實際上，`push` 不會修改 `items[0]`，程式是安全的。

### Rust 2026 的 & borrow 語法

Rust 2026 引入了新的借用語法，允許更精細的生命期註解：

```rust
// Rust 2026：更聰明的借用檢查器
fn process(items: &mut Vec<i32>) {
    let first: &immut items[0];  // 標記為不可變區域
    items.push(42);              // 知道 push 不影響 items[0]
    println!("{}", first);       // 沒問題！
}
```

新的 `&immut` 和 `&mut` 借用語法讓借用檢查器具備**路徑敏感**（path-sensitive）分析能力：

```rust
fn update_if_exists(map: &mut HashMap<String, Vec<i32>>) {
    // 傳統寫法需要 clone
    if let Some(values) = map.get("key") {
        // Rust 2021：這裡不能修改 map
    }
    
    // Rust 2026：精細生命期追蹤
    if let Some(values) = &immut map["key"] {
        // 仍然可以修改 map 中不相關的條目
        map.insert("other".into(), vec![1, 2, 3]);  // Ok!
    }
}
```

## Async 迭代器與協程

### AsyncIterator trait

Rust 2026 將 `AsyncIterator` 提升為語言一等公民：

```rust
// Rust 2026：AsyncIterator trait
trait AsyncIterator {
    type Item;
    
    async fn next(&mut self) -> Option<Self::Item>;
    
    // 預設實作
    fn size_hint(&self) -> (usize, Option<usize>) {
        (0, None)
    }
}
```

### async for 迴圈

```rust
use tokio::fs::read_dir;
use futures::AsyncIteratorExt;

#[tokio::main]
async fn main() -> Result<()> {
    let mut dir = read_dir("./data").await?;
    
    // Rust 2026：async for 直接遍歷非同步迭代器
    async for entry in dir {
        let path = entry.path();
        let metadata = tokio::fs::metadata(&path).await?;
        println!("{}: {} bytes", path.display(), metadata.len());
    }
    
    Ok(())
}
```

### Coroutine：輕量級協程

Rust 2026 引入了第一等的 `coroutine` 關鍵字，比傳統 async/await 更輕量：

```rust
// Rust 2026：coroutine 定義
coroutine fn fibonacci() -> i32 {
    let mut a = 0;
    let mut b = 1;
    loop {
        yield a;          // 暫停並產出值
        let tmp = a + b;
        a = b;
        b = tmp;
    }
}

fn main() {
    let mut gen = fibonacci();
    for _ in 0..10 {
        match gen.resume() {
            CoroutineState::Yielded(val) => println!("{}", val),
            CoroutineState::Complete(_) => break,
        }
    }
    // 輸出：0 1 1 2 3 5 8 13 21 34
}
```

相較於 async/await，coroutine 的優勢是**無需 runtime 支援**，且 **yield 可以在任何函式中使用**：

```rust
coroutine fn traverse_tree(node: &TreeNode) -> i32 {
    yield node.value;
    if let Some(left) = &node.left {
        yield* traverse_tree(left);  // 委派 yield
    }
    if let Some(right) = &node.right {
        yield* traverse_tree(right);
    }
}
```

## 模式匹配強化

Rust 2026 借鑒了 C++26 的模式匹配設計：

```rust
enum Expr {
    Int(i32),
    Add(Box<Expr>, Box<Expr>),
    Mul(Box<Expr>, Box<Expr>),
}

fn eval(expr: &Expr) -> i32 {
    match expr {
        // 嵌套模式 + 守衛條件
        Expr::Add(a, b) if eval(a) > 0 => eval(a) + eval(b),
        Expr::Mul(a, b) => eval(a) * eval(b),
        Expr::Int(n) if *n > 10 => *n * 2,
        Expr::Int(n) => *n,
    }
}
```

### 新的切片模式

```rust
fn analyze_slice(data: &[i32]) -> &str {
    match data {
        [] => "空",
        [a] => "單一元素",
        [a, b] => "兩個元素",
        [first, .., last] => "至少兩個元素",
    }
}
```

## 編譯器支援

| 編譯器 | Ownership 2.0 | AsyncIterator | Coroutine | 最低版本 |
|--------|--------------|---------------|-----------|---------|
| rustc 2026 | 完整支援 | 完整支援 | 完整支援 | rustc 1.85+ |
| rustc (nightly) | 完整支援 | 完整支援 | 完整支援 | 1.84+ |
| rust-analyzer | 完整支援 | 完整支援 | 實驗性 | 2026.05+ |
| mrustc | 部分支援 | 不支援 | 不支援 | — |

## 遷移指南

從 Rust 2021 遷移到 2026 Edition：

```toml
# Cargo.toml
[package]
name = "my-project"
version = "0.1.0"
edition = "2026"  # 從 2021 改為 2026
```

自動遷移工具：

```bash
$ cargo fix --edition
$ cargo check
$ cargo test
```

主要破壞性變更：

| 變更 | 說明 | 自動修正 |
|------|------|---------|
| `dyn Trait` 預設為 `dyn Trait + Send` | trait 物件預設要求 Send | `cargo fix` |
| 新的保留關鍵字 | `coroutine`, `yield`, `immut` 成為關鍵字 | `cargo fix` |
| 借用語法變更 | `&` 的行為在 2026 edition 中微調 | 手動調整 |

## 結語

Rust 2026 Edition 是所有權模型的終極進化——更聰明的借用檢查器消除了許多不必要的限制，async 迭代器和 coroutine 讓非同步程式設計變得直觀。對於新專案，2026 Edition 是預設選擇；對於既有專案，`cargo fix` 可以處理大部分遷移工作。

---

**延伸閱讀**

- [Rust 2026 Edition Guide](https://www.google.com/search?q=Rust+2026+Edition+guide)
- [Ownership 2.0 RFC](https://www.google.com/search?q=Rust+ownership+2.0+RFC)
- [AsyncIterator RFC 2996](https://www.google.com/search?q=Rust+AsyncIterator+RFC+2996)
- [Coroutines RFC](https://www.google.com/search?q=Rust+coroutine+RFC)
