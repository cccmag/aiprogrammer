# Rust 1.26 穩定版發布

## 前言

2018 年 5 月，Rust 1.26 穩定版發布，帶來了多項重要改進。

## 主要新特性

### impl Trait

```rust
fn create_counter() -> impl Iterator<Item = i32> {
    (0..10).map(|x| x * 2)
}
```

這讓函數可以返回一個「實現了特定特徵的類型」，而無需明確指定具體類型。

### 問候語法

現在可以使用 `?` 運算子來處理 Result 類型：

```rust
fn read_file() -> Result<String> {
    let mut file = File::open("test.txt")?;
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;
    Ok(contents)
}
```

### 128 位元整數

```rust
let large: i128 = 1 << 100;
```

### 區間匹配

```rust
match score {
    90..=100 => println!("A"),
    80..=89 => println!("B"),
    _ => println!("C"),
}
```

## Rust 的優勢

- 記憶體安全（無 GC、無空指針）
- 零成本抽象
- 優秀的並發支援
- 活躍的社群

## 應用場景

- Web 開發（Rust + Rocket/Actix）
- 系統程式設計
- 區塊鏈開發
- 嵌入式開發

## 結語

Rust 持續演進，正在成為系統程式設計的首選語言之一。

---

**延伸閱讀**

- [Rust 官方網站](https://www.google.com/search?q=Rust+official+site)
- [Rust 1.26 發布說明](https://www.google.com/search?q=Rust+1.26+release+notes)