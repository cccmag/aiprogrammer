# Rust 1.38 發布：Pipeline 運算子

## 前言

Rust 1.38 於 2019 年 9 月正式發布，這個版本包含了 pipeline 運算子的穩定化以及其他改進。

## Pipeline 運算子

### |>

```rust
// Rust 1.38 之前
let result = foo(bar(baz(function(arg))));

// Rust 1.38 以後
let result = arg
    |> function
    |> baz
    |> bar
    |> foo;
```

---

## 其他更新

### 編譯器優化

- 更快的增量編譯
- 更好的錯誤消息

---

## 結語

Rust 1.38 繼續推進 Rust 的現代化，增長運算子讓函式鏈式調用更加直觀。

---

**延伸閱讀**

- [Rust 1.38 Release](https://www.google.com/search?q=Rust+1.38+release+notes)