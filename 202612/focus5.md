# 邊緣運算與 Serverless WASM

## Workers、Fastly、Spin、狀態管理（2021-2026）

### 前言

WASM 在邊緣運算中的核心優勢非常明確：微秒級的冷啟動、MB 級的記憶體開銷、精細的安全隔離、以及多語言支援。這些特性讓 WASM 成為邊緣 Serverless 平台的新一代執行期。

### 為什麼 WASM 適合邊緣運算？

| 特性 | 容器（Docker） | WASM（wasmtime） |
|------|--------------|-----------------|
| 冷啟動時間 | 100-500ms | 50-500µs |
| 記憶體開銷 | 50-200 MB | 1-10 MB |
| 二進位大小 | 100 MB+ | 10 KB - 1 MB |
| 安全隔離 | Namespace + cgroup | 能力模型 + 沙箱 |
| 多語言 | 需自備執行環境 | 編譯到 WASM 即可 |

### Cloudflare Workers

全球 330+ 節點，基於 V8 引擎：

```rust
use worker::*;

#[event(fetch)]
pub async fn handler(req: Request, env: Env) -> Result<Response> {
    let wasm = env.wasm("processor")?;
    let result = wasm.call("compute", &[JsValue::from(42)])?;
    Response::ok(format!("Result: {:?}", result))
}
```

**特點**：生態最大、JavaScript + WASM 混合、KV/D1/R2 整合。

### Fastly Compute

純 WASM 執行期（wasmtime），無 JS 膠水層：

```rust
use fastly::*;

#[fastly::main]
fn main(req: Request) -> Result<Response, Error> {
    Ok(Response::from_body("Hello from Fastly!")
        .with_content_type("text/plain"))
}
```

**特點**：純 WASM 原生執行、極致冷啟動、強大的邊緣快取。

### Fermyon Spin

開源 WASM 框架，基於元件模型：

```rust
use spin_sdk::http::{IntoResponse, Request, Response};
use spin_sdk::http_component;

#[http_component]
fn handle(req: Request) -> anyhow::Result<impl IntoResponse> {
    Ok(Response::builder()
        .status(200)
        .body("Hello from Spin!")
        .build())
}
```

**特點**：開源可自託管、支援元件模型、SQLite/Redis 整合、本地開發友善。

### 狀態管理

邊緣應用需要處理狀態：

| 方案 | 平台 | 適合場景 |
|------|------|---------|
| KV Store | Workers / Fastly | 設定、計數器、快取 |
| D1 (SQLite) | Workers | 關聯式查詢 |
| Object Store | Fastly | 大型二進位檔案 |
| Redis / SQLite | Spin | 通用 |


### 小結

三大邊緣 WASM 平台各有優勢：Workers 以規模和生態取勝，Fastly 以純 WASM 效能見長，Spin 以開源和可移植性為核心。無論選擇哪個平台，WASM 正在成為邊緣運算的事實標準執行期。

---

**下一步**：[元件模型](focus6.md)

## 延伸閱讀

- [Cloudflare Workers WASM](https://www.google.com/search?q=Cloudflare+Workers+WASM)
- [Fastly Compute 文件](https://www.google.com/search?q=Fastly+Compute+documentation)
- [Fermyon Spin](https://www.google.com/search?q=Fermyon+Spin)
- [邊緣 WASM 平台比較](https://www.google.com/search?q=edge+WASM+platform+comparison)
