# AI + WASM：可攜式推論的未來（2024-2026）

## 邊緣 AI 的橫向擴展難題

在傳統的 AI 部署模式中，模型推論的執行期與硬體平台緊密綁定。NVIDIA GPU 需要 CUDA、Apple Silicon 需要 Core ML、瀏覽器需要 TensorFlow.js 或 ONNX Runtime Web——每種平台都需要不同的執行期和依賴庫。WASM 提供了一個突破性的替代方案：**一次編譯，隨處推論**。

### WASM 中的機器學習推論挑戰

在 WASM 中執行 ML 模型推論面臨幾個根本挑戰：

```
WASM 推論的技術挑戰：
─────────────────────────

挑戰 1：缺少硬體加速
├── WASM 指令集不包含 GPU 或 TPU 加速指令
├── 無法直接使用 CUDA / Metal / DirectML
├── SIMD 支援有限（WASM SIMD 128 位元，遠少於 x86 AVX-512）
└── 解決方案：WebNN（瀏覽器）或 WASI ML（伺服器）

挑戰 2：模型大小
├── 現代語言模型：數 GB 到數百 GB
├── WASM 線性記憶體限制：預設 4GB（可調整）
├── 邊緣裝置記憶體限制：1-8GB
└── 解決方案：量化模型 + 外部記憶體映射

挑戰 3：執行效能
├── WASM 約為原生效能的 70-95%（取決於計算類型）
├── 矩陣乘法（GEMM）對編譯器的依賴度高
├── 無法使用專用矩陣乘法指令（如 NVIDIA Tensor Core）
└── 解決方案：Cranelift 或 LLVM 後端 + 自適應演算法

挑戰 4：生態尚未成熟
├── 2024 年開始有 WASM ML 框架
├── 模型格式轉換工具不完整
└── 缺乏標準的 WASM ML 執行期 API
```

```
WASM 推論效能測試（ResNet-50，批次大小 1）：
─────────────────────────────────

平台：MacBook Pro M3 Max

原生 PyTorch (MPS):       約 5.2 ms
WASM (wasmtime + SIMD):   約 7.8 ms  (66% of native)
WASM (wasmer + LLVM):     約 6.9 ms  (75% of native)
WASM (browser + SIMD):    約 8.5 ms  (61% of native)

平台：Raspberry Pi 5

原生 TFLite:               約 45 ms
WASM (wasmtime + SIMD):   約 62 ms  (72% of native)

結論：CPU 密集推論在 WASM 上的效能約為原生 65-85%。
對於非即時應用或較小模型，這個差距是可接受的。
```

### WebNN 與 WASM 的協同運算

WebNN（Web Neural Network API）是 W3C 提出的瀏覽器硬體加速 API。它讓 WASM 推論可以將特定運算委託給 GPU 或 NPU：

```
WebNN + WASM 協同架構：
─────────────────────────

                  瀏覽器環境
    ┌──────────────────────────────────┐
    │          JavaScript 主機           │
    │                                   │
    │  ┌──────────────────────┐         │
    │  │     WASM 模組         │         │
    │  │                      │         │
    │  │  ┌────────────────┐  │         │
    │  │  │ 模型載入        │──│────► WASI 檔案系統
    │  │  ├────────────────┤  │         │
    │  │  │ 前處理          │  │         │
    │  │  │（影像/文字/音訊）│  │         │
    │  │  ├────────────────┤  │         │
    │  │  │ 推論排程器      │──│────► WebNN API
    │  │  ├────────────────┤  │         │
    │  │  │ 後處理          │  │         │
    │  │  └────────────────┘  │         │
    │  └──────────────────────┘         │
    │                                   │
    │  ┌──────────────────────┐         │
    │  │     WebNN API         │         │
    │  │  GPU / NPU 加速       │         │
    │  └──────────────────────┘         │
    └──────────────────────────────────┘
```

```rust
// WASM 模組中的推論排程 — 使用 WebNN 加速
use wasm_bindgen::prelude::*;

// 匯入 WebNN API
#[wasm_bindgen(module = "/webnn-shim.js")]
extern "C" {
    type MLContext;
    type MLGraph;

    fn create_context(device: &str) -> MLContext;
    fn build_graph(ctx: &MLContext, model: &[u8]) -> MLGraph;
    fn compute(graph: &MLGraph, input: &[f32]) -> Vec<f32>;
}

#[wasm_bindgen]
pub struct InferenceEngine {
    context: MLContext,
    graph: Option<MLGraph>,
}

#[wasm_bindgen]
impl InferenceEngine {
    #[wasm_bindgen(constructor)]
    pub fn new(device: &str) -> InferenceEngine {
        let context = create_context(device);
        InferenceEngine { context, graph: None }
    }

    pub fn load_model(&mut self, model_bytes: &[u8]) {
        let graph = build_graph(&self.context, model_bytes);
        self.graph = Some(graph);
    }

    pub fn run(&self, input: Vec<f32>) -> Vec<f32> {
        match &self.graph {
            Some(graph) => compute(graph, &input),
            None => panic!("模型尚未載入"),
        }
    }
}
```

### Rust WASM + Candle 的輕量推論

Candle 是 Hugging Face 開發的 Rust ML 框架，專為輕量推論設計。它沒有依賴 Python 執行期或 CUDA，可以輕鬆編譯為 WASM。

```rust
// 使用 Candle 在 WASM 中執行推論
use candle_core::{Device, Tensor};
use candle_nn::ops::*;

pub fn run_inference(
    image_data: &[u8],
    model_weights: &[u8],
) -> Result<Vec<f32>, candle_core::Error> {
    // 在 CPU 裝置上執行（WASM 無法存取 GPU）
    let device = Device::Cpu;

    // 載入模型權重（從 WASM 線性記憶體中讀取）
    let weights: Vec<f32> = model_weights
        .chunks_exact(4)
        .map(|chunk| f32::from_le_bytes(chunk.try_into().unwrap()))
        .collect();

    // 建構計算圖
    let input = Tensor::from_slice(image_data, (1, 3, 224, 224), &device)?;
    let w = Tensor::from_slice(&weights, (1000, 512), &device)?;
    let b = Tensor::zeros((1000,), candle_core::DType::F32, &device)?;

    // 前向傳播
    let hidden = linear(&input, &w, Some(&b))?;
    let activated = relu(&hidden)?;
    let output = softmax(&activated, 1)?;

    // 回傳結果
    let result: Vec<f32> = output.flatten_all()?.to_vec1()?;
    Ok(result)
}
```

#### 模型量化策略

為了讓模型能在 WASM 的有限記憶體中執行，量化是必要的：

```rust
/// 將 f32 權重量化為 int8
pub fn quantize_to_i8(weights: &[f32]) -> (Vec<i8>, Vec<f32>) {
    let mut quantized = Vec::with_capacity(weights.len());
    let mut scales = Vec::new();

    // 分組量化（每 128 個權重一組）
    for chunk in weights.chunks(128) {
        let max_val = chunk
            .iter()
            .map(|v| v.abs())
            .fold(0.0_f32, f32::max);

        let scale = if max_val > 0.0 {
            127.0 / max_val
        } else {
            1.0
        };

        for v in chunk {
            quantized.push((v * scale).round() as i8);
        }
        scales.push(scale);
    }

    (quantized, scales)
}
```

```
量化對模型大小的影響：
─────────────────────────

模型：MobileNet v2（分類 1000 類）

f32 權重：               13.4 MB
int8 量化權重：           3.4 MB  (75% 減少)
int4 量化權重：           1.7 MB  (87% 減少)

Top-1 準確率：
f32 baseline:            71.8%
int8:                    71.2%  (-0.6%)
int4:                    69.5%  (-2.3%)

WASM + int8 模型：
WASM 二進制（不含權重）： 280 KB
量化權重：                 3.4 MB
總計：                     3.7 MB ← 可在瀏覽器中快速下載
```

### 邊緣 AI 模型的跨平台可攜性

WASM 作為推論執行期的最強優勢是可攜性：

```
單一 WASM 二進制 + 量化權重
          │
          ├── 瀏覽器（Chrome / Firefox / Safari / Edge）
          │    └── 無需安裝任何東西
          │
          ├── 伺服器端（wasmtime / wasmer）
          │    └── 輕量容器替代方案
          │
          ├── CDN 邊緣（Fastly / Cloudflare）
          │    └── 全球分佈的低延遲推論
          │
          ├── IoT 裝置（Linux ARM）
          │    └── 無需交叉編譯
          │
          └── 行動裝置（iOS / Android）
               └── 透過 WebView 或 wasmtime 嵌入
```

```bash
# 構建跨平台 WASM 推論模組
cargo build --target wasm32-wasip2 --release \
  --features "candle,quantized"

# 在瀏覽器中測試
wasm-pack build --target web
python3 -m http.server 8000 &
open http://localhost:8000

# 在伺服器中使用 wasmtime
wasmtime run --component \
  --dir models::/var/models \
  inference.wasm

# 在邊緣節點部署
fastly compute deploy
```

```
真實案例：智慧相機裁切服務
─────────────────────────

情境：使用者上傳照片 → 自動偵測人臉 → 智慧裁切

傳統部署：
├── 後端 Python Flask + PyTorch
├── Docker 容器：1.2 GB
├── GPU 依賴（每次請求 ~50ms）
├── 冷啟動：~2 秒
└── 每臺伺服器處理：~100 RPS

WASM 部署（邊緣）：
├── Rust WASM + Candle + 量化 MobileNet
├── WASM 模組：4.2 MB
├── CPU 推論（每次請求 ~80ms）
├── 冷啟動：< 1ms
└── 每臺邊緣節點處理：~500 RPS

邊緣部署減少延遲（從 200ms 降至 20ms）：
因資料不須往返中央資料中心
```

AI + WASM 的結合在 2026 年仍然是一個快速發展的領域。雖然 GPU 加速的支援仍然有限，但在邊緣裝置、瀏覽器、和輕量推論場景中，WASM 已經展現出作為通用 AI 推論層的巨大潛力。結合模型的持續量化（從 f32 到 int4，甚至二值化），即使是超過十億參數的模型也可能在 WASM 中執行。

---

## 延伸閱讀

- [Candle（Rust ML 框架）](https://www.google.com/search?q=Candle+Rust+ML+framework)
- [WebNN API](https://www.google.com/search?q=WebNN+API+W3C)
- [WASM ML 推論](https://www.google.com/search?q=WASM+machine+learning+inference)
- [模型量化技術](https://www.google.com/search?q=model+quantization+techniques)
- [邊緣 AI 部署](https://www.google.com/search?q=edge+AI+deployment+WASM)

---

*本篇文章為「AI 程式人雜誌 2026 年 7 月號」WASM 系列之七。*
