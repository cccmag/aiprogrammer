# 邊緣運算實戰 — 用 Rust + WASM 打造邊緣應用

## 1. 引言

邊緣運算在 2026 年已經從實驗性技術發展為主流架構。WASM 憑藉其輕量沙箱、快速啟動和安全隔離的特性，成為邊緣運算的首選執行期。本文將透過完整案例，展示如何用 Rust + WASM 建構生產級的邊緣應用。

## 2. 邊緣應用架構設計

現代邊緣應用的典型架構包含三個層次：

```
邊緣應用三層架構：
─────────────────────────

用戶端（瀏覽器 / 行動裝置）
    │
    ├── CDN 邊緣節點
    │   ├── WASM 邊緣函數（請求處理、快取、認證）
    │   ├── WASM 內容轉換（圖片壓縮、格式轉換）
    │   └── WASM 邊緣推論（ML 模型推論）
    │
    ├── 區域邊緣節點
    │   ├── WASM 資料聚合
    │   ├── WASM 即時分析
    │   └── WASM 狀態同步
    │
    └── 中央資料中心
        ├── 持久化儲存
        ├── 模型訓練
        └── 全域協調
```

## 3. 實戰案例：智慧圖片處理邊緣服務

### 3.1 專案結構

```
edge-image-processor/
├── Cargo.toml
├── wit/
│   └── processor.wit        # WIT 介面定義
├── src/
│   ├── lib.rs               # WASM 元件
│   ├── resize.rs            # 圖片縮放
│   ├── optimize.rs          # 圖片最佳化
│   └── detect.rs            # 物體偵測
├── host/
│   ├── edge-deploy.rs       # 邊緣部署腳本
│   └── main.rs              # 主機端執行
└── test.sh                  # 測試腳本
```

### 3.2 WIT 介面定義

```wit
// processor.wit
package edge:image-processor@0.1.0;

interface image-types {
    record image {
        data: list<u8>,
        width: u32,
        height: u32,
        format: image-format,
    }

    enum image-format {
        jpeg,
        png,
        webp,
        avif,
    }

    record processed-image {
        data: list<u8>,
        format: image-format,
        original-size: u32,
        compressed-size: u32,
        compression-ratio: float64,
    }
}

interface resize {
    use image-types.{image};

    record resize-options {
        max-width: u32,
        max-height: u32,
        maintain-aspect-ratio: bool,
    }

    resize: func(img: image, opts: resize-options) -> image;
}

interface detect {
    use image-types.{image};

    record detection-result {
        label: string,
        confidence: float32,
        bounding-box: tuple<u32, u32, u32, u32>,
    }

    detect-objects: func(img: image) -> list<detection-result>;
}

world processor-world {
    import resize;
    import detect;

    export process-image: func(img: image) -> processed-image;
    export analyze-image: func(img: image) -> list<detection-result>;
}
```

### 3.3 Rust 實作

```rust
// src/lib.rs
cargo_component::component!("processor-world");

use crate::bindings::edge::image_processor::{
    image_types::{Image, ImageFormat, ProcessedImage},
    resize::{self, ResizeOptions},
    detect::{self, DetectionResult},
};

struct ImageProcessor;

impl ProcessorWorld for ImageProcessor {
    fn process_image(img: Image) -> ProcessedImage {
        let original_size = img.data.len() as u32;

        // 步驟 1：縮放到最大 1200px
        let resized = resize::resize(img, ResizeOptions {
            max_width: 1200,
            max_height: 1200,
            maintain_aspect_ratio: true,
        });

        // 步驟 2：轉換為 WebP 格式（較小的邊緣端最佳化）
        let compressed = optimize_webp(&resized);

        ProcessedImage {
            data: compressed,
            format: ImageFormat::Webp,
            original_size,
            compressed_size: compressed.len() as u32,
            compression_ratio: compressed.len() as f64 / original_size as f64,
        }
    }

    fn analyze_image(img: Image) -> Vec<DetectionResult> {
        detect::detect_objects(img)
    }
}

fn optimize_webp(img: &Image) -> Vec<u8> {
    // 使用 libwebp 的 WASM 版本進行圖片壓縮
    let mut encoder = webp::Encoder::new(&img.data, img.width, img.height);
    encoder.set_quality(80.0);
    encoder.encode_lossy()
}
```

### 3.4 邊緣部署設定

```rust
// host/edge-deploy.rs
use wasmtime::*;
use wasmtime_wasi::*;

fn deploy_to_edge(wasm_bytes: &[u8]) -> Result<(), Box<dyn std::error::Error>> {
    let mut config = Config::new();
    config.epoch_interruption(true);  // 啟用執行時間限制
    config.max_memory_size(128 * 1024 * 1024);  // 128 MB 上限

    let engine = Engine::new(&config)?;
    let mut linker = Linker::new(&engine);

    // 設定邊緣環境的 WASI 限制
    let wasi_ctx = WasiCtxBuilder::new()
        .set_stdout(StdoutFile::Null)   // 邊緣環境中無標準輸出
        .set_stderr(StderrFile::Null)
        .build();
    let mut store = Store::new(&engine, wasi_ctx);

    // 設定執行時間限制（最多 10 秒）
    store.set_epoch_deadline(10);

    let component = Component::from_file(&engine, wasm_bytes)?;
    let instance = linker.instantiate(&mut store, &component)?;

    // 設定邊緣快取
    let cache_config = EdgeCacheConfig {
        ttl_seconds: 300,        // 快取 5 分鐘
        vary_by: vec!["accept"],  // 根據 Accept header 區分
    };

    // 部署到邊緣節點
    let deployment = EdgeDeployment::new(instance, cache_config);
    deployment.activate()?;

    Ok(())
}
```

## 4. 邊緣平台的比較

| 特性 | Fastly Compute@Edge | Cloudflare Workers | Fermyon Spin |
|------|-------------------|-------------------|-------------|
| **執行期** | wasmtime | V8 + wasmtime | wasmtime |
| **WASI 支援** | Preview 2 | Preview 1 | Preview 2 |
| **Component Model** | ✅ 完整 | ✅ 完整 | ✅ 完整 |
| **冷啟動** | < 1ms | < 5ms | < 1ms |
| **記憶體限制** | 128 MB | 128 MB | 256 MB |
| **CPU 時間限制** | 10 ms/req | 30 ms/req | 無硬限制 |
| **狀態儲存** | Fastly KV Store | Cloudflare KV / D1 | Spin KV / SQLite |
| **全球節點** | 150+ | 330+ | 自託管 |
| **Rust SDK** | fastly crate | worker crate | spin-sdk crate |

## 5. 邊緣應用的關鍵設計模式

### 5.1 無狀態設計

邊緣函數應該是無狀態的——所有狀態都透過外部儲存服務存取：

```rust
// 正確：使用外部 KV 儲存
fn handle_request(kv: &KVStore, key: &str) -> Result<String, Error> {
    match kv.get(key)? {
        Some(value) => Ok(value),
        None => {
            let computed = expensive_computation(key);
            kv.set(key, &computed, Some(300))?;  // 快取 5 分鐘
            Ok(computed)
        }
    }
}

// 錯誤：不應該依賴區域狀態
static COUNTER: std::sync::atomic::AtomicU64 = std::sync::atomic::AtomicU64::new(0);
fn bad_pattern() -> u64 {
    COUNTER.fetch_add(1, std::sync::atomic::Ordering::SeqCst)  // 不同邊緣節點不同值
}
```

### 5.2 請求管線模式

```rust
// 請求處理管線
struct RequestPipeline {
    steps: Vec<Box<dyn Fn(Request) -> Result<Request, Error>>>,
}

impl RequestPipeline {
    fn new() -> Self {
        RequestPipeline { steps: vec![
            Box::new(auth::validate_token),
            Box::new(rate_limiter::check),
            Box::new(cache::lookup),
            Box::new(router::dispatch),
        ]}
    }

    fn process(&self, req: Request) -> Result<Response, Error> {
        let mut current = req;
        for step in &self.steps {
            current = step(current)?;
        }
        Ok(Response::ok(current.body()))
    }
}
```

## 6. 邊緣快取策略

```rust
/// 智慧快取決策引擎
fn should_cache(req: &Request, resp: &Response) -> CacheDecision {
    // 只快取 GET 請求
    if req.method() != "GET" {
        return CacheDecision::Skip;
    }

    // 不快取需要認證的頁面
    if req.headers().has("Authorization") {
        return CacheDecision::Skip;
    }

    // 根據回應大小決定快取時間
    let size = resp.body().len();
    let ttl = if size < 1024 * 10 {        // < 10KB: 長期快取
        3600
    } else if size < 1024 * 100 {          // < 100KB: 中期快取
        600
    } else {                                // > 100KB: 短期快取
        60
    };

    CacheDecision::Cache { ttl, scope: CacheScope::Global }
}
```

## 7. 效能與成本分析

```
邊緣 WASM vs 容器部署的成本比較：
─────────────────────────

每月 1000 萬請求，平均回應時間 20ms：

容器部署（Kubernetes + Docker）：
├── 計算資源：3 個節點 × 4 vCPU × 8GB RAM = ~$600/月
├── 頻寬：100Mbps = ~$200/月
├── 營運成本：維護、監控、更新 = ~$500/月
└── 總計：~$1,300/月

邊緣 WASM（Fastly Compute@Edge）：
├── 請求費用：1000 萬 × $0.10/萬 = $1,000/月
├── 快取頻寬：包含在內
├── 營運成本：近乎零
└── 總計：~$1,000/月

此外，邊緣部署的使用者體驗更好：
- 全球平均延遲：容器 150ms vs 邊緣 25ms
- 可用性：容器 99.9% vs 邊緣 99.99%
```

## 8. 結語

Rust + WASM 在邊緣運算中的應用已臻成熟。無論是請求處理、內容轉換、還是即時分析，WASM 的輕量沙箱和快速啟動特性都使其成為邊緣環境的理想選擇。隨著 WASI Preview 2 和 Component Model 的普及，邊緣 WASM 的應用範疇將持續擴展——從簡單的請求過濾到複雜的 ML 推論，邊緣運算的未來將由 WASM 驅動。

---

## 延伸閱讀

- [Fastly Compute@Edge 開發指南](https://www.google.com/search?q=Fastly+Compute+at+Edge+Rust)
- [Cloudflare Workers WASM 整合](https://www.google.com/search?q=Cloudflare+Workers+WASM+integration)
- [Fermyon Spin 框架](https://www.google.com/search?q=Fermyon+Spin+WASM)
- [邊緣運算設計模式](https://www.google.com/search?q=edge+computing+design+patterns+WASM)
