# Rust 1.20：Associated Constants 與其他改進

## 前言

Rust 1.20 於 2017 年 8 月發布，引入了 Associated Constants 這個社群期待已久的功能。

## Associated Constants

```rust
// Rust 1.20 之前
struct Color {
    r: u8,
    g: u8,
    b: u8,
}

impl Color {
    const WHITE: Color = Color { r: 255, g: 255, b: 255 };
    const BLACK: Color = Color { r: 0, g: 0, b: 0 };
}

// Rust 1.20+ 可以直接在 impl 區塊中定義常數
impl Color {
    const WHITE: Color = Color { r: 255, g: 255, b: 255 };
    const BLACK: Color = Color { r: 0, g: 0, b: 0 };
}

// 介面也可以有預設實作
trait Animal {
    const NUM_LEGS: u32;
    fn name(&self) -> &str;
}

struct Dog;
impl Animal for Dog {
    const NUM_LEGS: u32 = 4;
    fn name(&self) -> &str { "Dog" }
}
```

## 其他改進

```rust
// ::<>:: 語法增強
Vec::<i32>::with_capacity(100);

// 更好的迭回器 combinator 鏈
let result: Vec<i32> = (0..10)
    .filter(|x| x % 2 == 0)
    .map(|x| x * x)
    .collect();
```

## Rust 在系統程式設計的優勢

Rust 的記憶體安全特性使其成為 AI 系統程式設計的選擇：

```rust
// 高效能 AI 推論引擎
pub struct Model {
    weights: Vec<f32>,
}

impl Model {
    pub fn infer(&self, input: &[f32]) -> Vec<f32> {
        // 類神經網路推論
        input.iter()
            .zip(self.weights.iter())
            .map(|(i, w)| i * w)
            .collect()
    }
}
```

---

**延伸閱讀**

- [Rust 1.20 Release Notes](https://www.google.com/search?q=Rust+1.20+release)
- [Associated Constants RFC](https://www.google.com/search?q=associated+constants+rust)