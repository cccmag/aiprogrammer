# Rust 生態：系統程式新選擇

## 前言

Rust 語言在 2017 年持續獲得關注，其記憶體安全特性使其成為系統程式和 AI 基礎設施的有力選擇。

## Rust 1.20

```rust
// Rust 1.20 新特性

// Associated Constants
struct Color {
    r: u8,
    g: u8,
    b: u8,
}

impl Color {
    const WHITE: Color = Color { r: 255, g: 255, b: 255 };
    const BLACK: Color = Color { r: 0, g: 0, b: 0 };

    const fn new(r: u8, g: u8, b: u8) -> Self {
        Color { r, g, b }
    }
}

// 使用
let white = Color::WHITE;
```

## Rust 的優點

```rust
// Rust 核心優勢

// 1. 記憶體安全
// 編譯器強制執行所有權和借用規則

let s1 = String::from("hello");
let s2 = s1;  // s1 被移動，不再有效
// println!("{}", s1);  // 編譯錯誤！

// 2. 無垃圾回收
// 編譯時確定生命週期，無運行時開銷

// 3. 零成本抽象
// 高級特性無性能損失

// 4. 併發安全
// 防止資料競爭

use std::sync::Arc;
use std::thread;

let data = Arc::new(vec![1, 2, 3]);
let data_clone = Arc::clone(&data);

thread::spawn(move || {
    println!("{:?}", data_clone);
});
```

## Rust 在 AI 領域的應用

```rust
// 簡單的神經網路層
#[derive(Debug)]
struct Linear {
    weights: Vec<Vec<f32>>,
    biases: Vec<f32>,
}

impl Linear {
    fn new(input_size: usize, output_size: usize) -> Self {
        Linear {
            weights: vec![vec![0.0; input_size]; output_size],
            biases: vec![0.0; output_size],
        }
    }

    fn forward(&self, input: &[f32]) -> Vec<f32> {
        self.weights.iter()
            .zip(self.biases.iter())
            .map(|(w, &b)| {
                w.iter().zip(input.iter()).map(|(wi, &xi)| wi * xi).sum::<f32>() + b
            })
            .collect()
    }
}
```

## Rust 工具鏈

```bash
# 套件管理
cargo new my_project
cargo build
cargo run
cargo test

# 相關套件
# - ndarray: 多維陣列
# - candle: 深度學習 (類似 PyTorch)
# - tract: 邊緣 AI 推論
```

## 2018 年展望

Rust 2018 Edition 預計帶來：
- 更簡潔的語法
- 更好的 IDE 支援
- 更多標準庫改進

---

**延伸閱讀**

- [Rust Official](https://www.google.com/search?q=Rust+official)
- [The Rust Programming Language Book](https://www.google.com/search?q=Rust+programming+language+book)

---

*本篇文章為「AI 程式人雜誌 2017 年 12 月號」年終回顧系列之一。*