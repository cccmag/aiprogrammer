# 邊緣 Serverless 框架比較

## 1. 引言

邊緣運算將計算從集中式雲端推向靠近使用者的邊緣節點。WebAssembly 憑藉極快的冷啟動速度、輕量級隔離、和多語言支援，成為邊緣 Serverless 平台的新一代執行期。本文比較三大主流邊緣 WASM 平台：Cloudflare Workers、Fastly Compute、和 Fermyon Spin。

## 2. Cloudflare Workers

### 2.1 平台概述

Cloudflare Workers 是最早支援 WASM 的邊緣 Serverless 平台之一。它在全球 330+ 城市部署邊緣節點，基於 Chrome V8 引擎執行。

### 2.2 WASM 支援

```rust
use worker::*;

#[event(fetch)]
pub async fn main(req: Request, env: Env) -> Result<Response> {
    // Workers 支援直接使用 WASM 模組
    let wasm_module = env.wasm("my-module")?;
    let result = wasm_module.call("compute", &[JsValue::from(42)])?;

    Response::ok(format!("Result: {:?}", result))
}
```

### 2.3 效能特性

| 指標 | 數據 |
|------|------|
| 冷啟動時間 | ~5ms（V8 isolate 復用） |
| 記憶體限制 | 128 MB |
| CPU 時間限制 | 30s（free）/ 60s（paid） |
| WASM 二進位大小限制 | 10 MB |
| 邊緣節點數 | 330+ |

### 2.4 KV 儲存整合

```rust
use worker::*;

#[event(fetch)]
pub async fn handler(req: Request, env: Env) -> Result<Response> {
    let kv = env.kv("my-namespace")?;
    let value = kv.get("counter").text().await?.unwrap_or("0".into());
    let count: i32 = value.parse().unwrap_or(0);
    kv.put("counter", &(count + 1).to_string())?.execute().await?;
    Response::ok(format!("Count: {}", count))
}
```

## 3. Fastly Compute

### 3.1 平台概述

Fastly Compute（前身為 Compute@Edge）基於 Lucet / wasmtime 執行期，原生支援 WASM 而非 JavaScript。

### 3.2 WASM 原生執行

Fastly Compute 的 WASM 模組直接運行在 wasmtime 上，無需 JavaScript 膠水層：

```rust
use fastly::*;

#[fastly::main]
fn main(req: Request) -> Result<Response, Error> {
    let url = req.get_url();
    let backend = "origin_0";

    // 直接回傳靜態內容
    if url.path() == "/hello" {
        return Ok(Response::from_body("Hello from Fastly WASM!")
            .with_content_type("text/plain"));
    }

    // 或代理到後端
    let bereq = Request::get(url.path());
    let beresp = bereq.send(backend)?;
    Ok(beresp)
}
```

### 3.3 效能特性

| 指標 | 數據 |
|------|------|
| 冷啟動時間 | ~200µs（wasmtime 實體化） |
| 記憶體限制 | 128 MB |
| 請求超時 | 30s |
| WASM 二進位大小限制 | 10 MB |
| 邊緣節點數 | 100+ |

### 3.4 字典與物件儲存

```rust
use fastly::*;

fn handle_config() -> Result<Response, Error> {
    // Fastly 的字典服務（鍵值儲存）
    let dict = Dictionary::open("app_config");
    let threshold: i32 = dict.get("threshold").unwrap_or("100").parse().unwrap();

    // 物件儲存（大型二進位資料）
    let store = ObjectStore::open("user_assets")?;
    let asset = store.lookup(format!("user_{}_avatar.png", user_id))?;

    Ok(Response::from_body(asset).with_content_type("image/png"))
}
```

## 4. Fermyon Spin

### 4.1 平台概述

Spin 是 Fermyon 開發的開源邊緣 WASM 框架。不同於 Workers 和 Fastly 的鎖定平台，Spin 可以部署在任何支援 WASI 的環境。

### 4.2 Spin 應用結構

一個 Spin 應用由多個 WASM 元件組成：

```rust
use spin_sdk::http::{IntoResponse, Request, Response};
use spin_sdk::http_component;

#[http_component]
fn handle_request(req: Request) -> anyhow::Result<impl IntoResponse> {
    let name = req
        .query_params()
        .get("name")
        .cloned()
        .unwrap_or("World".to_string());

    Ok(Response::builder()
        .status(200)
        .header("content-type", "text/plain")
        .body(format!("Hello, {}!\nProcessed by Spin WASM", name))
        .build())
}
```

### 4.3 效能特性

| 指標 | 數據 |
|------|------|
| 冷啟動時間 | ~100µs（WASM 實體化） |
| 記憶體限制 | 取決於部署環境 |
| WASM 二進位大小限制 | 無明確限制 |
| 部署方式 | Spin CLI / Kubernetes |
| 多語言支援 | Rust、Go、JS、Python |

### 4.4 Spin 的狀態管理

```rust
use spin_sdk::sqlite::{Connection, Value};

fn query_database(user_id: &str) -> Result<User, Error> {
    let conn = Connection::open_default()?;
    let row_set = conn.execute(
        "SELECT id, name, email FROM users WHERE id = ?",
        &[Value::String(user_id.to_string())],
    )?;

    for row in row_set.rows {
        let id = row.get::<String>("id")?;
        let name = row.get::<String>("name")?;
        let email = row.get::<String>("email")?;
        return Ok(User { id, name, email });
    }
    Err(Error::NotFound)
}
```

## 5. 對比總結

| 特性 | Cloudflare Workers | Fastly Compute | Fermyon Spin |
|------|-------------------|---------------|-------------|
| 執行期 | V8（JS + WASM） | wasmtime（純 WASM） | wasmtime（純 WASM） |
| 冷啟動 | ~5ms | ~200µs | ~100µs |
| 多語言 | JS/Rust/C++ | Rust/C/Go | Rust/Go/JS/Python |
| 鎖定程度 | 高（專有平台） | 高（專有平台） | 低（開源、可自託管） |
| 狀態管理 | KV、D1、R2 | Dict、Object Store | SQLite、Redis |
| WASM 版本 | MVP + GC | Preview 1 | Preview 2 + 元件模型 |
| 開源 | 否（運行時專有） | 否 | 是 |

## 6. 選擇建議

- **選擇 Cloudflare Workers 當你**：需要最廣泛的邊緣節點覆蓋、整合 Cloudflare 生態系（CDN、DDoS 防護）、需要 JavaScript 與 WASM 混合開發
- **選擇 Fastly Compute 當你**：需要極致的冷啟動效能、純 WASM 工作負載、強大的邊緣快取控制
- **選擇 Fermyon Spin 當你**：需要可移植性（避免平台鎖定）、需要元件模型支援、偏好開源解決方案、需要本地開發環境

## 7. 結語

三大邊緣 WASM 平台各有優勢。Cloudflare Workers 以規模和生態取勝，Fastly Compute 以純 WASM 效能見長，Fermyon Spin 則以開源和可移植性為核心。選擇哪個平台取決於你的具體需求——但無論選擇哪個，WASM 作為邊緣運算執行期的趨勢已經不可逆轉。

---

## 延伸閱讀

- [Cloudflare Workers WASM](https://www.google.com/search?q=Cloudflare+Workers+WebAssembly)
- [Fastly Compute 文件](https://www.google.com/search?q=Fastly+Compute+documentation)
- [Fermyon Spin 框架](https://www.google.com/search?q=Fermyon+Spin+framework)
- [邊緣運算平台比較 2026](https://www.google.com/search?q=edge+computing+platform+comparison+2026)
