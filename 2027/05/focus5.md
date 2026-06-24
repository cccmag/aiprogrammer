# WASM 在雲端：邊緣運算與 Serverless（2020-2026）

## 從瀏覽器沙箱到雲端原生執行期

WASM 在雲端的應用從 2020 年左右開始加速。其核心賣點很明確：一個輕量、安全、可移植的沙箱執行期，啟動時間比容器快 100-1000 倍，同時提供硬體級隔離。

### WASM 在 CDN 邊緣的應用

#### Fastly Compute@Edge

Fastly 在 2020 年推出了 Compute@Edge（原名 Terrarium），是第一家將 WASM 作為邊緣運算執行期的 CDN 平台：

```rust
// Fastly Compute@Edge — Rust 範例
use fastly::prelude::*;

#[fastly::main]
fn main(req: Request<Body>) -> Result<Request<Body>, Error> {
    // 解析請求路徑
    let path = req.get_path();

    // 從邊緣快取查詢
    let cache_key = format!("cache:{}", path);
    if let Some(cached) = fastly::cache::get(&cache_key) {
        return Ok(Response::from_body(cached));
    }

    // 向後端服務發送請求
    let backend_req = Request::get(format!("https://origin{}", path));
    let beresp = backend_req.send("origin-backend")?;

    // 將結果寫入邊緣快取
    fastly::cache::set(&cache_key, beresp.get_body_bytes(), 60);

    Ok(beresp)
}
```

Fastly 選擇 WASM 而非容器或 V8 isolate 的原因：

```
Fastly 的技術選擇分析：
─────────────────────────

容器（Docker）:
├── 啟動時間：100-500ms
├── 記憶體開銷：10-50 MB
├── 隔離層級：核心級（Namespaces + cgroups）
└── 密度：每臺機器 ~100 個容器

WASM（wasmtime）:
├── 啟動時間：< 1ms
├── 記憶體開銷：< 1 MB
├── 隔離層級：語言級（沙箱）
└── 密度：每臺機器 ~10,000+ 個 WASM 模組

V8 Isolate:
├── 啟動時間：~5ms
├── 記憶體開銷：~4 MB
├── 隔離層級：語言級（V8 isolate）
└── 密度：每臺機器 ~1,000 個 isolate
```

#### Cloudflare Workers

Cloudflare Workers 最初使用 V8 isolate，但在 2024 年開始支援 WASM 作為一等執行期。開發者可以用 Rust 撰寫 Workers，編譯為 WASM 後在 Cloudflare 的全球邊緣網路執行：

```rust
// Cloudflare Workers — Rust WASM 範例
use worker::*;

#[event(fetch)]
async fn main(req: Request, env: Env, _ctx: Context) -> Result<Response> {
    let router = Router::new();

    router
        .get_async("/api/data", |_req, ctx| async move {
            // 從 KV 儲存讀取資料
            let kv = ctx.kv("DATA_STORE")?;
            let value = kv.get("key").text().await?;

            // 使用 D1 資料庫查詢
            let d1 = ctx.d1("DB")?;
            let result = d1
                .prepare("SELECT * FROM items WHERE id = ?")
                .bind(&[1])?
                .all()
                .await?;

            Response::from_json(&result)?;
            Ok(response)
        })
        .run(req, env)
        .await
}
```

### Serverless WASM vs 容器化部署

```
部署模型比較：
─────────────────────────

傳統 Serverless（AWS Lambda - Firecracker）:
┌─────┐  ┌─────┐  ┌─────┐
│ Fn  │  │ Fn  │  │ Fn  │    每個函數在微虛擬機中執行
│ 1   │  │ 2   │  │ 3   │
└─────┘  └─────┘  └─────┘    啟動時間：~50ms（冷啟動）
                               記憶體開銷：~5MB / 執行個體

WASM Serverless（Fastly Compute@Edge）:
┌──────────────────────────┐
│ Fn 1 │ Fn 2 │ Fn 3 │ ... │    多個 WASM 模組在同一個
│       wasmtime 執行期      │    執行期中共存
└──────────────────────────┘
                              啟動時間：< 1ms（冷啟動）
                              記憶體開銷：~50KB / 執行個體
```

WASM 的優勢不僅是啟動時間。由於所有 WASM 模組共用同一個執行期，記憶體開銷被大幅降低：

```
粗估成本分析（100,000 函數 / 每小時）：
─────────────────────────────────

AWS Lambda（Firecracker）:
  100,000 × 5MB（每執行個體）= 500 GB 記憶體
  冷啟動約 50ms × 100,000 = 5,000 秒冷啟動延遲

Fastly Compute@Edge（WASM）:
  100,000 × 50KB（每模組）= 5 GB 記憶體
  冷啟動約 1ms × 100,000 = 100 秒冷啟動延遲

成本節省：約 90-95%（在同等計算量下）
```

### 沙箱安全與資源隔離

WASM 的安全模型在雲端環境中至關重要。不同於容器依賴核心級隔離（Namespaces、cgroups、seccomp），WASM 的安全來自語言級沙箱與 WASI 的能力模型：

```
WASM 沙箱的安全層次：
─────────────────────────

層次 1：指令級隔離
├── 無條件跳轉限制（br_if 的目標必須在當前函數內）
├── 線性記憶體邊界檢查（每次存取都檢查）
├── 無存取硬體暫存器或直接記憶體存取
└── 無內省（introspection）或自我修改程式碼

層次 2：WASI 能力隔離
├── 預設無任何系統存取權限
├── 每個檔案存取需要路徑級授權
├── 每個網路連線需要埠級授權
└── 資源使用量限制（記憶體、CPU、開啟檔案數）

層次 3：沙箱監控
├── CPU 時間配額（每個 WASM 模組的執行時間配額）
├── 記憶體配額（最大線性記憶體大小，預設 1GB）
├── 堆疊深度限制（防止棧溢出攻擊）
└── 資源洩漏偵測（未關閉的檔案描述子）
```

```rust
// wasmtime 中的資源限制設定
use wasmtime::*;

let mut config = Config::new();

// 記憶體限制
config.max_memory_size(64 * 1024 * 1024);      // 64 MB
config.max_memory_table_size(10_000);           // 最大表大小

// CPU 限制
config.max_wasm_stack(1024 * 1024);              // 1 MB 堆疊
config.epoch_interruption(true);                 // 允許時間中斷

// 編譯選項
config.cranelift_opt_level(OptLevel::SpeedAndSize);
config.wasm_component_model(true);               // 啟用元件模型

let engine = Engine::new(&config)?;
```

### Rust + WASM 的邊緣運算架構

```
現代邊緣運算架構：
─────────────────────────

                      ┌──────────────────┐
                      │  全域負載平衡器    │
                      └────────┬─────────┘
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                    │
    ┌─────▼─────┐      ┌─────▼─────┐      ┌─────▼─────┐
    │  邊緣節點 1  │      │  邊緣節點 2  │      │  邊緣節點 N  │
    │  (東京)     │      │  (法蘭克福)  │      │  (紐約)     │
    └─────┬─────┘      └─────┬─────┘      └─────┬─────┘
          │                    │                    │
    ┌─────▼─────┐      ┌─────▼─────┐      ┌─────▼─────┐
    │ WASM 執行期 │      │ WASM 執行期 │      │ WASM 執行期 │
    │ ┌────────┐ │      │ ┌────────┐ │      │ ┌────────┐ │
    │ │推理元件│ │      │ │推理元件│ │      │ │推理元件│ │
    │ ├────────┤ │      │ ├────────┤ │      │ ├────────┤ │
    │ │快取元件│ │      │ │快取元件│ │      │ │快取元件│ │
    │ ├────────┤ │      │ ├────────┤ │      │ ├────────┤ │
    │ │路由元件│ │      │ │路由元件│ │      │ │路由元件│ │
    │ └────────┘ │      │ └────────┘ │      │ └────────┘ │
    └─────┬─────┘      └─────┬─────┘      └─────┬─────┘
          │                    │                    │
    ┌─────▼────────────────────▼────────────────────▼─────┐
    │              中央資料中心（源伺服器）                  │
    │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐  │
    │  │ PostgreSQL│ │ Redis   │ │ ML 模型  │ │ WASM    │  │
    │  │           │ │         │ │ 訓練     │ │ 部署管道 │  │
    │  └─────────┘ └─────────┘ └─────────┘ └─────────┘  │
    └───────────────────────────────────────────────────┘
```

邊緣運算的 Rust + WASM 部署策略：

```bash
# 構建用於邊緣部署的 WASM 模組
cargo build --target wasm32-wasip2 --release \
  --features "edge-optimized"

# 使用 wasm-opt 進行邊緣最佳化
wasm-opt -Oz \
  --strip-debug \
  --enable-bulk-memory \
  --enable-reference-types \
  target/wasm32-wasip2/release/my-edge-module.wasm \
  -o dist/edge-module.wasm

# 部署到邊緣平台
fastly compute deploy
```

WASM 在雲端的應用已經從實驗走向主流。它的輕量沙箱模型、與容器互補的安全模型、以及 Rust 的工具鏈支援，使其成為邊緣運算和 Serverless 架構的理想執行期。可以預見，隨著 WASM Component Model 的普及，雲端應用將從容器微服務轉向 WASM 微元件。

---

## 延伸閱讀

- [Fastly Compute@Edge](https://www.google.com/search?q=Fastly+Compute+at+Edge+WASM)
- [Cloudflare Workers WASM](https://www.google.com/search?q=Cloudflare+Workers+WASM)
- [WASM Serverless 架構](https://www.google.com/search?q=WASM+serverless+architecture)
- [wasmtime 沙箱安全](https://www.google.com/search?q=wasmtime+sandbox+security)
- [AWS WASM 支援](https://www.google.com/search?q=AWS+Lambda+WASM+support)

---

*本篇文章為「AI 程式人雜誌 2026 年 7 月號」WASM 系列之五。*
