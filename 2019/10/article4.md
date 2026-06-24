# Rust 2019 年度回顧：穩定性與生態系的成熟

## 前言

2019 年是 Rust 語言持續穩定發展的一年。本篇文章將回顧 Rust 在 2019 年的重要進展，包括語言特性、工具鏈更新和生態系發展。

## Rust 2019 版本回顧

### Rust 1.31：Rust 2018 Edition

Rust 1.31 發布了 Rust 2018 Edition，這是 Rust 的第二個 Edition：

```
Rust 2018 Edition 的重點：
- async/await 語法穩定
- 模組系統改進
- 更多的錯誤訊息改進
```

### Rust 1.38：Build Scripts 加速

Rust 1.38 帶來了 build script 加速：

```toml
# Cargo.toml 中使用 builtins 避免重複編譯
[build-dependencies]
built = "0.4"
```

### Rust 1.39：Async/Await 穩定

2019 年 11 月，Rust 1.39 發布，async/await 語法正式穩定：

```rust
async fn fetch_data() -> Result<String, Error> {
    let response = reqwest::get("https://api.example.com").await?;
    let text = response.text().await?;
    Ok(text)
}
```

## 工具鏈的進步

### Cargo 的改進

2019 年，Cargo 獲得了多項改進：

| 功能 | 說明 |
|------|------|
| Cargo.lock 自動更新 | 簡化依賴管理 |
| 增量編譯優化 | 加快編譯速度 |
| Workspace 支援 | 更好的多專案管理 |

### rustfmt 和 rustclippy

格式化工具 rustfmt 和 linter rustclippy 在 2019 年持續改進：

```bash
# 格式化程式碼
rustfmt src/main.rs

# 執行 linter
rustclippy
```

### rustup 的角色

rustup 仍然是 Rust 的首選版本管理工具：

```bash
# 管理多個 Rust 版本
rustup default stable
rustup toolchain list
rustup update
```

## 生態系的繁榮

### crates.io 統計

截至 2019 年底：

```
crates.io 統計：
- 總套件數：突破 30,000
- 總下載量：突破 10 億次
- 熱門類別：Web 開發、系統程式、網路
```

### 熱門 crate

2019 年最受歡迎的 crates：

```toml
# Web 框架
actix-web = "0.7"
rocket = "0.4"
warp = "0.2"

# 异步運行時
tokio = "0.2"
async-std = "0.99"

# 網路
reqwest = "0.10"
serde = "1.0"
```

### Web 框架之爭

2019 年，Rust 的 Web 框架競爭更加激烈：

```
Actix-web：
- 效能極高
- 類似 Actix 的Actor模型

Rocket：
- 安全性優先
- 宣告式路由

Warp：
- 組合式設計
- 過濾器模式
```

## async/await 的成熟

### 語法演進

async/await 從 2018 年的不穩定到 2019 年底完全穩定：

```rust
// 2018 年（需要 nightly）
#![feature(async_await)]
async fn foo() { }

#![feature(await)]
async fn bar() {
    something().await;
}

// 2019 年（穩定）
async fn foo() { }
async fn bar() {
    something().await;
}
```

### 生態支援

async/await 穩定後，相關生態迅速跟進：

```rust
// HTTP 客戶端
reqwest::get(url).await?;

// 資料庫
sqlx::query("SELECT * FROM users").fetch_all(&pool).await?;

// WebSocket
use tokio_tungstenite::connect_async;
let (ws_stream, _) = connect_async(url).await?;
```

## Rust 的應用場景

### 區塊鏈

Rust 在區塊鏈領域的應用持續擴大：

```
知名區塊鏈專案使用 Rust：
- Solana：高效能區塊鏈
- Parity Substrate：區塊鏈框架
- Polkadot：跨鏈協議
```

### 雲端服務

雲端服務廠商開始採用 Rust：

```
AWS：用於 Firecracker 微型 VM
Cloudflare：用於邊緣運算
Discord：用於效能關鍵服務
```

### 嵌入式開發

Rust 在嵌入式領域的應用也在成長：

```rust
#![no_std]
#![no_main]

use panic_halt as _;

#[arduino::main]
fn main() {
    let led = arduino::pins::d13::output::HIGH;
    loop {
        led.toggle();
        arduino::delay_ms(1000);
    }
}
```

## 社群發展

### Rust Foundation 成立

2019 年底，Rust Foundation 正式成立，成員包括：

```
Foundation 創始成員：
- Mozilla
- AWS
- Google
- Huawei
- Microsoft
- Mozilla（繼續支援）
```

### RustConf 2019

RustConf 2019 是這一年的重要活動：

- 超過 1000 人參加
- 主題演講涵蓋 async/await、生態系
- 工作坊涵蓋 Web、嵌入式、區塊鏈

## 結論

2019 年對 Rust 來說是穩定成熟的一年。async/await 的穩定、生態系的繁榮、社群的健康發展，都預示著 Rust 的光明未來。Rust 正在從一個新興語言成長為一個成熟的系統程式語言。

---

**延伸閱讀**

- [Rust 2019 年度回顧](https://www.google.com/search?q=Rust+2019+year+in+review)
- [Rust+async+await](https://www.google.com/search?q=Rust+async+await+stable+2019)
- [Rust+ecosystem+2019](https://www.google.com/search?q=Rust+ecosystem+crates+2019)