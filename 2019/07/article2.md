# Rust 1.37 發布：特性別名與 cargo vendor

## 前言

Rust 1.37 於 2019 年 8 月正式發布。這個版本包含多項實用功能，其中最重要的是特性別名（Feature Gatter）和 cargo vendor 命令的穩定化。本文將詳細解析這些新特性。

## 特性別名（Feature Gatter）

### 問題背景

在 Rust 中，當一個類別實現了多個 trait 時，方法調用會變得冗長：

```rust
// 沒有特性別名時
use std::fmt::Debug;

fn print_debug<T: Debug + Clone>(value: &T) {
    println!("{:?}", value.clone());
}

// 長期以來需要重複寫 trait bounds
```

### 特性別名的語法

Rust 1.37 允許為 trait 組合創建別名：

```rust
// 定義特性別名
trait CommonBounds = Debug + Clone + Send + Sync;

// 使用特性別名
fn print_debug<T: CommonBounds>(value: &T) {
    println!("{:?}", value.clone());
}
```

### 實際應用

```rust
use std::fmt::{Debug, Display};

trait Printable = Debug + Display;

struct Wrapper<T>(T);

impl<T: Printable> Wrapper<T> {
    fn print(&self) {
        println!("Debug: {:?}", self.0);
        println!("Display: {}", self.0);
    }
}
```

### 使用場景

1. **減少重複的 trait bounds**
2. **提高代碼可讀性**
3. **方便公共 API 的設計**

---

## cargo vendor 穩定化

### 什麼是 cargo vendor？

`cargo vendor` 命令用於將專案的所有依賴複製到本地目錄，這對於離線構建或確保可重現構建非常有用。

### 使用方式

```bash
# 將依賴 vendor 到 vendor 目錄
cargo vendor ./vendor

# 之後在 .cargo/config.toml 中配置
[cargo]
vendor_dir = "vendor"

# 使用 vendor 的依賴構建
cargo build --offline
```

### 實際範例

```bash
# 初始化新專案
cargo new my-project
cd my-project

# 添加依賴
echo 'serde = "1.0"' >> Cargo.toml
echo 'serde_json = "1.0"' >> Cargo.toml

# vendor 依賴
cargo vendor vendor

# 這會創建 vendor 目錄，包含所有依賴的源碼
```

### 配置文件

```toml
# .cargo/config.toml
[source.crates-io]
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "vendor"
```

---

## 其他重要更新

### 1. 匿名 trait 參數

```rust
fn foo(x: impl Clone + Default) {
    // x 同時是 Clone 和 Default
}

fn bar<T: Clone + Default>(x: T) {
    // 等價於上者
}
```

### 2. #[repr(align(N))] 改進

```rust
#[repr(C)]
struct Packet {
    #[repr(align(16))]
    header: [u8; 16],
    data: [u8; 64],
}
```

### 3. std::hint::black_box

```rust
use std::hint::black_box;

fn benchmark<F>(f: F)
where
    F: Fn(),
{
    let start = std::time::Instant::now();
    f();
    black_box(f);  // 防止編譯器優化掉 f
    println!("耗時: {:?}", start.elapsed());
}
```

---

## 社群回應

Rust 1.37 的特性別名功能得到了社群的積極響應。許多開發者認為這極大改善了大型專案的可維護性：

```rust
// 大型專案的典型使用場景
trait WebServiceBounds = Send + Sync + Clone + Default;

trait ApiClientBounds = Clone + Debug + Default + serde::Serialize + serde::de::DeserializeOwned;
```

---

## 結語

Rust 1.37 延續了 Rust 語言「務實創新」的理念。特性別名讓大型專案更容易維護，而 cargo vendor 的穩定化則滿足了企業級應用的需求。

---

**延伸閱讀**

- [Rust 1.37 Release Notes](https://www.google.com/search?q=Rust+1.37+release+notes)
- [RFC: Feature Gatter](https://www.google.com/search?q=Rust+feature+gatter+RFC)
- [Cargo vendor documentation](https://www.google.com/search?q=cargo+vendor+documentation)