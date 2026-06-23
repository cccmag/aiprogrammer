# 即時 ML 推論系統設計 — 低延遲管線、非同步、併發

## 1. 引言

生產環境的 ML 推論系統需要同時滿足低延遲、高吞吐和可靠性要求。Rust 的所有權模型和無 GC 架構使其成為設計此類系統的理想語言。本文探討如何使用 Tokio + Candle/Burn/tract 構建高效的即時推論服務。

## 2. 系統架構

```
用戶端請求
    ↓
負載均衡器
    ↓
推論服務器 (Rust + Tokio)
    ├── 請求排隊 (Channel)
    ├── 批次處理器 (Batch Aggregator)
    ├── 模型推論 (Candle/Burn/tract)
    └── 回應處理 (Post-processing)
    ↓
用戶端回應
```

## 3. 非同步推論管線

### 單一請求推論

最基本的非同步推論服務：

```rust
use axum::{
    extract::State,
    routing::post,
    Json, Router,
};
use std::sync::Arc;
use tokio::sync::Mutex;

struct AppState {
    model: Arc<Mutex<TractModel>>,
}

async fn infer_handler(
    State(state): State<Arc<AppState>>,
    Json(input): Json<Vec<f32>>,
) -> Json<Vec<f32>> {
    let model = state.model.lock().await;
    let output = model.predict(&input).unwrap();
    Json(output)
}
```

### 批次處理

批次處理可以顯著提升 GPU 利用率：

```rust
use tokio::sync::mpsc;
use tokio::time::{interval, Duration};

struct BatchCollector {
    buffer: Vec<(u64, Vec<f32>)>,  // (request_id, input)
    max_batch_size: usize,
    max_wait_ms: u64,
}

impl BatchCollector {
    async fn run(
        mut rx: mpsc::Receiver<(u64, Vec<f32>)>,
        model: Arc<dyn Model>,
        results: Arc<dashmap::DashMap<u64, Vec<f32>>>,
    ) {
        let mut tick = interval(Duration::from_millis(self.max_wait_ms));

        loop {
            tokio::select! {
                Some((id, input)) = rx.recv() => {
                    self.buffer.push((id, input));
                    if self.buffer.len() >= self.max_batch_size {
                        self.flush(&model, &results).await;
                    }
                }
                _ = tick.tick() => {
                    if !self.buffer.is_empty() {
                        self.flush(&model, &results).await;
                    }
                }
            }
        }
    }

    async fn flush(
        &mut self,
        model: &Arc<dyn Model>,
        results: &Arc<dashmap::DashMap<u64, Vec<f32>>>,
    ) {
        // 1. 合併批次
        let batch_inputs: Vec<Vec<f32>> = self.buffer
            .iter().map(|(_, input)| input.clone()).collect();

        // 2. 批次推論
        let batch_outputs = model.predict_batch(&batch_inputs).await;

        // 3. 分發結果
        for ((id, _), output) in self.buffer.drain(..).zip(batch_outputs) {
            results.insert(id, output);
        }
    }
}
```

## 4. 模型熱重載

在不中斷服務的情況下更新模型：

```rust
use std::sync::Arc;
use tokio::sync::RwLock;

pub struct HotReloadModel {
    current: Arc<RwLock<Box<dyn Model>>>,
    model_path: String,
}

impl HotReloadModel {
    pub fn new(path: &str) -> Self {
        let model = Self::load_model(path);
        Self {
            current: Arc::new(RwLock::new(model)),
            model_path: path.to_string(),
        }
    }

    pub async fn predict(&self, input: &[f32]) -> Vec<f32> {
        let model = self.current.read().await;
        model.predict(input)
    }

    pub async fn reload(&self) {
        let new_model = Self::load_model(&self.model_path);
        let mut current = self.current.write().await;
        *current = new_model;
    }
}

// 定期檢查檔案變更
async fn watch_model_reload(reloader: Arc<HotReloadModel>) {
    let mut last_modified = std::time::SystemTime::now();

    loop {
        tokio::time::sleep(Duration::from_secs(30)).await;

        if let Ok(metadata) = std::fs::metadata(&reloader.model_path) {
            if let Ok(modified) = metadata.modified() {
                if modified > last_modified {
                    reloader.reload().await;
                    last_modified = modified;
                    tracing::info!("模型已重新載入");
                }
            }
        }
    }
}
```

## 5. 低延遲最佳化

| 技術 | 延遲改善 | 實作 |
|------|---------|------|
| 預先分配緩衝區 | 30-50% | `Vec::with_capacity()` |
| 記憶體池 | 20-30% | `lol_alloc` / 自訂配置器 |
| Pin CPU 核心 | 10-20% | `core_affinity` |
| 預熱（Warm-up） | 首次延遲消除 | 啟動時執行假推論 |
| 模型量化 | 2-3x | INT8 推論 |
| 批次處理 | 2-4x | 動態批次聚合 |

## 6. 監控與指標

使用 Prometheus 監控推論服務：

```rust
use metrics::{
    counter, histogram,
    describe_counter, describe_histogram,
};

pub fn track_inference() {
    describe_histogram!(
        "inference_latency_ms",
        "推論延遲（毫秒）"
    );
    describe_counter!(
        "inference_requests_total",
        "推論請求總數"
    );
}

pub async fn tracked_infer(
    model: &dyn Model,
    input: &[f32],
) -> Vec<f32> {
    counter!("inference_requests_total").increment(1);

    let start = std::time::Instant::now();
    let result = model.predict(input);
    let elapsed = start.elapsed().as_millis() as f64;

    histogram!("inference_latency_ms", elapsed);

    // 記錄模型版本
    tracing::info!(
        latency_ms = elapsed,
        model_version = model.version(),
        "推論完成"
    );

    result
}
```

## 7. 完整伺服器範例

```rust
#[tokio::main]
async fn main() {
    // 初始化模型
    let model = HotReloadModel::new("model.quant.onnx");
    let model = Arc::new(model);

    // 啟動模型熱重載 watch
    tokio::spawn(watch_model_reload(model.clone()));

    // 設定路由
    let app = Router::new()
        .route("/predict", post(infer_handler))
        .route("/metrics", get(metrics_handler))
        .with_state(model);

    // 啟動伺服器
    let listener = tokio::net::TcpListener::bind("0.0.0.0:8080").await.unwrap();
    axum::serve(listener, app).await.unwrap();
}
```

## 8. 結語

即時 ML 推論系統的設計需要在延遲、吞吐和資源使用間取得平衡。Rust 的非同步生態（Tokio/Axum）與 ML 框架（Candle/Burn/tract）的整合提供了完整的生產級解決方案。批次處理、模型熱重載和 Prometheus 監控是生產部署的必備元件。

## 延伸閱讀

- [Tokio async inference](https://www.google.com/search?q=Tokio+async+ML+inference+Rust)
- [Axum ML serving](https://www.google.com/search?q=Axum+ML+model+serving+Rust)
- [Low latency ML systems](https://www.google.com/search?q=low+latency+machine+learning+inference+system+design)
