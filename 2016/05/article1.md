# Rust 1.9 的記憶體安全特性

## Rust 的安全承諾

Rust 1.9 在 2016 年 5 月發布，持續強化記憶體安全特性。Rust 的核心承諾是：**編譯時杜絕記憶體錯誤**。

## 所有權系統

Rust 的所有權系統是其記憶體安全的核心：

```rust
fn main() {
    // 移動語義
    let s1 = String::from("hello");
    let s2 = s1;  // s1 無效，所有權轉移到 s2
    // println!("{}", s1);  // 編譯錯誤！

    // Copy 類型
    let x = 5;
    let y = x;  // i32 實現 Copy，x 和 y 都有效
}
```

## 借用與引用

```rust
fn main() {
    let s = String::from("hello");

    // 不可變借用
    let r1 = &s;
    let r2 = &s;
    println!("{} and {}", r1, r2);

    // 可變借用（同時只有一個可變借用）
    let r3 = &mut s;
    r3.push_str(", world");
    println!("{}", r3);
}
```

## 生命週期

```rust
// 生命週期註解
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}
```

## Panic 處理

Rust 1.9 引入了更穩定的 panic 處理：

```rust
use std::panic;

fn main() {
    let result = panic::catch_unwind(|| {
        println!("About to panic!");
        panic!("This is a panic!");
    });

    match result {
        Ok(_) => println!("No panic"),
        Err(e) => println!("Caught panic: {:?}", e),
    }
}
```

## 小結

Rust 的記憶體安全通過編譯時檢查實現，無需 GC。這使得 Rust 成為系統程式設計的理想選擇。

延伸閱讀：
- [Google 搜尋：Rust ownership system](https://www.google.com/search?q=Rust+ownership+system)
- [Google 搜尋：Rust memory safety](https://www.google.com/search?q=Rust+memory+safety)