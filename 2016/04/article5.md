# Rust 的函式式特性

## Rust：系統程式設計的現代選擇

Rust 結合了系統程式設計的性能和記憶體安全，並大量借鑒了函式式程式設計的概念。

## 閉包

Rust 的閉包極為高效，編譯器會根據使用場景自動最佳化：

```rust
// 基本閉包
let add = |x, y| x + y;
println!("{}", add(1, 2));  // 3

// 類型推斷
let square = |x| x * x;

// 捕獲環境
let multiplier = 10;
let scaled = |x| x * multiplier;
println!("{}", scaled(5));  // 50
```

## 迭代器與Iterator

Rust 的迭代器是函式式風格的典範：

```rust
let numbers = vec![1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

// map：轉換
let squares: Vec<i32> = numbers.iter().map(|x| x * x).collect();

// filter：篩選
let evens: Vec<&i32> = numbers.iter().filter(|x| *x % 2 == 0).collect();

// 鏈式操作
let result: i32 = numbers
    .iter()
    .filter(|x| *x % 2 == 0)
    .map(|x| x * x)
    .sum();

println!("Result: {}", result);  // 220
```

## Pattern Matching

Rust 的 match 是強大的模式匹配工具：

```rust
enum Message {
    Quit,
    Move { x: i32, y: i32 },
    Write(String),
    ChangeColor(u8, u8, u8),
}

fn process(msg: Message) {
    match msg {
        Message::Quit => println!("Quit"),
        Message::Move { x, y } => println!("Move to ({}, {})", x, y),
        Message::Write(text) => println!("Write: {}", text),
        Message::ChangeColor(r, g, b) => println!("Color: RGB({}, {}, {})", r, g, b),
    }
}
```

## Option 與 Result

Rust 的 Option 和 Result 類型體現了函式式錯誤處理：

```rust
// Option：處理可能不存在的值
fn find_user(id: u32) -> Option<String> {
    if id == 1 {
        Some("Alice".to_string())
    } else {
        None
    }
}

// 使用 map 轉換
let user = find_user(1).map(|name| format!("Hello, {}", name));

// 使用 unwrap_or 提供預設值
let greeting = find_user(99).unwrap_or("Guest".to_string());

// Result：處理可能失敗的操作
fn divide(a: f64, b: f64) -> Result<f64, String> {
    if b == 0.0 {
        Err("Division by zero".to_string())
    } else {
        Ok(a / b)
    }
}

// 使用 ? 運算子傳播錯誤
fn calculate() -> Result<f64, String> {
    let a = divide(10.0, 2.0)?;
    let b = divide(a, 0.0)?;  // 這裡會錯誤
    Ok(b)
}
```

## 所有權與函式式

Rust 的所有權系統實現了記憶體安全，無需 GC：

```rust
// 移動語義
let s1 = String::from("hello");
let s2 = s1;  // s1 無效，只有 s2 有效

// 複製（對於 Copy 類型）
let x = 5;
let y = x;  // x 和 y 都有效

// 借用
fn length(s: &String) -> usize {
    s.len()
}

let s = String::from("hello");
let len = length(&s);  //借用，不獲取所有權
```

## 高階函式

Rust 支援高階函式：

```rust
fn apply<F>(f: F, x: i32) -> i32
where
    F: Fn(i32) -> i32,
{
    f(x)
}

fn main() {
    let result = apply(|x| x * 2, 5);
    println!("{}", result);  // 10
}
```

## 持續演進

Rust 1.9 在 2016 年 2 月發布，持續加入新特性。2018 年將迎來第一個 Edition，帶來更多改進。

延伸閱讀：
- [Google 搜尋：Rust functional programming](https://www.google.com/search?q=Rust+functional+programming)
- [Google 搜尋：Rust iterators](https://www.google.com/search?q=Rust+iterators)