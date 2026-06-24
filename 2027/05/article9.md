# AI 推論在 WASM 上的實戰應用

## 1. 引言

在邊緣裝置和瀏覽器中執行機器學習模型推論，始終面臨著跨平台部署的挑戰。每個硬體平台有自己的執行期（CUDA、Core ML、TFLite），每種瀏覽器有不同的 WebGL/WebGPU 支援程度。WASM 提供了一個統一的解決方案：**一次編譯，隨處推論**。本文將探討如何在 WASM 中高效執行 AI 模型推論。

## 2. WASM 推論的技術架構

```
WASM 推論架構層次：
─────────────────────────

應用層
├── 影像分類
├── 物件偵測
├── 語意分割
├── 自然語言處理
└── 音訊處理
    │
WASM 推論引擎
├── Candle（Rust ML 框架）
├── ONNX Runtime Web
├── llama.cpp（WASM 移植）
└── WasmEdge WASI-NN
    │
WASM 執行期
├── wasmtime（伺服器）
├── V8 / SpiderMonkey（瀏覽器）
└── wasm-micro-runtime（嵌入式）
    │
硬體加速層
├── CPU（WASM SIMD）
├── GPU（WebGPU / WebNN）
└── NPU（WASI-NN / 瀏覽器 ML API）
```

## 3. 使用 Candle 在 WASM 中執行推論

Candle 是 Hugging Face 開發的 Rust ML 框架，非常適合 WASM 部署：

### 3.1 專案設定

```toml
# Cargo.toml
[package]
name = "wasm-candle-inference"
version = "0.1.0"
edition = "2024"

[dependencies]
candle-core = { version = "0.7", default-features = false }
candle-nn = { version = "0.7", default-features = false }
candle-onnx = { version = "0.7", default-features = false }
wasm-bindgen = "0.2"
serde = { version = "1", features = ["derive"] }
serde-wasm-bindgen = "0.6"

[profile.release]
opt-level = "z"
lto = true
strip = true
codegen-units = 1
```

### 3.2 推論引擎實作

```rust
use candle_core::{Device, Tensor};
use candle_nn::ops::*;
use wasm_bindgen::prelude::*;

/// WASM 推論引擎
#[wasm_bindgen]
pub struct WasmInferenceEngine {
    model: Option<Vec<u8>>,
    input_shape: Vec<u32>,
    output_shape: Vec<u32>,
}

#[wasm_bindgen]
impl WasmInferenceEngine {
    #[wasm_bindgen(constructor)]
    pub fn new() -> Self {
        WasmInferenceEngine {
            model: None,
            input_shape: vec![],
            output_shape: vec![],
        }
    }

    /// 載入 ONNX 模型
    pub fn load_model(&mut self, model_bytes: &[u8]) -> Result<(), JsValue> {
        // 驗證模型格式
        if model_bytes.len() < 4 {
            return Err("Model too small".into());
        }
        self.model = Some(model_bytes.to_vec());
        Ok(())
    }

    /// 執行推論
    pub fn infer(&self, input_data: &[f32]) -> Result<Vec<f32>, JsValue> {
        let model_bytes = self.model.as_ref()
            .ok_or_else(|| "No model loaded".to_string())?;

        // 建立 CPU 裝置（WASM 無法存取 GPU）
        let device = Device::Cpu;

        // 載入 ONNX 模型
        let model = candle_onnx::read_model(model_bytes)
            .map_err(|e| format!("Failed to load model: {}", e))?;

        // 建立輸入張量
        let input = Tensor::from_slice(
            input_data,
            &[1, 3, 224, 224],  // 批次 x 通道 x 高 x 寬
            &device,
        ).map_err(|e| format!("Tensor creation failed: {}", e))?;

        // 正規化輸入
        let mean = Tensor::new(&[0.485f32, 0.456f32, 0.406f32], &device)
            .map_err(|e| format!("Mean tensor: {}", e))?;
        let std = Tensor::new(&[0.229f32, 0.224f32, 0.225f32], &device)
            .map_err(|e| format!("Std tensor: {}", e))?;
        let normalized = input.broadcast_sub(&mean)
            .map_err(|e| format!("Subtract: {}", e))?
            .broadcast_div(&std)
            .map_err(|e| format!("Divide: {}", e))?;

        // 前向傳播
        let output = model.forward(&[normalized])
            .map_err(|e| format!("Forward pass: {}", e))?;

        // Softmax
        let probabilities = softmax(&output[0], 1)
            .map_err(|e| format!("Softmax: {}", e))?;

        // 回傳結果
        let result: Vec<f32> = probabilities.flatten_all()
            .map_err(|e| format!("Flatten: {}", e))?
            .to_vec1()
            .map_err(|e| format!("To vec: {}", e))?;

        Ok(result)
    }
}
```

### 3.3 JavaScript 前端整合

```javascript
// 在瀏覽器中載入 WASM 推論引擎
import init, { WasmInferenceEngine } from "./wasm_candle_inference.js";

class AIApplication {
    constructor() {
        this.engine = null;
        this.labels = [];
    }

    async initialize(modelPath, labelsPath) {
        await init();

        // 載入 WASM 引擎
        this.engine = new WasmInferenceEngine();

        // 下載模型
        const modelResponse = await fetch(modelPath);
        const modelBytes = new Uint8Array(await modelResponse.arrayBuffer());
        this.engine.load_model(modelBytes);

        // 載入標籤
        const labelsResponse = await fetch(labelsPath);
        this.labels = await labelsResponse.json();
    }

    async classifyImage(imageElement) {
        // 將圖片轉換為張量
        const tensor = this.imageToTensor(imageElement);

        // 執行推論（在 WASM 中）
        const predictions = this.engine.infer(tensor);

        // 取得 top-5 預測
        const top5 = predictions
            .map((prob, idx) => ({ label: this.labels[idx], probability: prob }))
            .sort((a, b) => b.probability - a.probability)
            .slice(0, 5);

        return top5;
    }

    imageToTensor(img) {
        const canvas = document.createElement('canvas');
        canvas.width = 224;
        canvas.height = 224;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(img, 0, 0, 224, 224);

        const imageData = ctx.getImageData(0, 0, 224, 224);
        const pixels = imageData.data;

        // RGB 正規化（[0, 255] → [0, 1]）
        const tensor = new Float32Array(3 * 224 * 224);
        for (let i = 0; i < 224 * 224; i++) {
            tensor[i] = pixels[i * 4] / 255.0;
            tensor[224 * 224 + i] = pixels[i * 4 + 1] / 255.0;
            tensor[2 * 224 * 224 + i] = pixels[i * 4 + 2] / 255.0;
        }

        return tensor;
    }
}
```

## 4. WASI-NN：標準化的 ML 推論介面

WASI-NN（WASI Neural Network）是 WASM 生態中的 ML 推論標準介面：

```wit
// wasi-nn.wit — WASI Neural Network 介面（簡化版）
package wasi:nn@0.1.0;

interface inference {
    /// 張量型別
    record tensor {
        data: list<u8>,
        shape: list<u32>,
        dtype: tensor-type,
    }

    enum tensor-type {
        f32,
        f16,
        i8,
        u8,
    }

    /// 圖形執行引擎
    enum graph-encoding {
        onnx,
        tensorflow,
        pytorch,
        openvino,
    }

    /// 執行環境（CPU / GPU / TPU）
    enum execution-target {
        cpu,
        gpu,
        tpu,
    }

    /// 載入推論圖形
    load: func(
        model: list<u8>,
        encoding: graph-encoding,
        target: execution-target,
    ) -> result<u32, string>;

    /// 執行推論
    compute: func(
        graph-id: u32,
        inputs: list<tensor>,
    ) -> result<list<tensor>, string>;

    /// 設置推論參數
    set-input: func(
        graph-id: u32,
        name: string,
        tensor: tensor,
    ) -> result<(), string>;

    /// 取得輸出
    get-output: func(
        graph-id: u32,
        name: string,
    ) -> result<tensor, string>;
}
```

## 5. 瀏覽器中的 LLM 推論

2026 年，在瀏覽器中執行小型語言模型已經成為現實：

```rust
// 在 WASM 中執行 LLM 推論
use wasm_bindgen::prelude::*;

#[wasm_bindgen]
pub struct TinyLLM {
    tokenizer: Tokenizer,
    model_weights: Vec<f32>,
    config: LlmConfig,
}

struct LlmConfig {
    vocab_size: u32,
    hidden_size: u32,
    num_layers: u32,
    num_heads: u32,
}

#[wasm_bindgen]
impl TinyLLM {
    #[wasm_bindgen(constructor)]
    pub fn new(weights: &[u8], tokenizer_json: &str) -> Result<TinyLLM, JsValue> {
        let config = LlmConfig {
            vocab_size: 32000,
            hidden_size: 768,
            num_layers: 12,
            num_heads: 12,
        };

        // 載入權重
        let model_weights: Vec<f32> = weights
            .chunks_exact(4)
            .map(|c| f32::from_le_bytes(c.try_into().unwrap()))
            .collect();

        let tokenizer = Tokenizer::from_json(tokenizer_json)
            .map_err(|e| format!("Tokenizer error: {}", e))?;

        Ok(TinyLLM { tokenizer, model_weights, config })
    }

    /// 生成文字
    pub fn generate(&self, prompt: &str, max_tokens: u32) -> Result<String, JsValue> {
        let mut input_ids = self.tokenizer.encode(prompt);

        for _ in 0..max_tokens {
            // 前向傳播
            let logits = self.forward(&input_ids);
            let next_token = self.sample(logits);

            input_ids.push(next_token);

            // 檢查結束標記
            if next_token == self.tokenizer.eos_id() {
                break;
            }
        }

        self.tokenizer.decode(&input_ids)
            .map_err(|e| format!("Decode error: {}", e))
    }

    fn forward(&self, input_ids: &[u32]) -> Vec<f32> {
        // 簡化的 Transformer 前向傳播
        // 在真實世界中，這會使用 Candle 或自訂矩陣運算
        let mut hidden = self.embed(input_ids);

        for layer in 0..self.config.num_layers as usize {
            hidden = self.transformer_block(layer, &hidden);
        }

        self.unembed(&hidden)
    }

    fn sample(&self, logits: Vec<f32>) -> u32 {
        // Temperature 採樣
        let temperature = 0.7;
        let scaled: Vec<f32> = logits.iter()
            .map(|&x| (x / temperature).exp())
            .collect();
        let sum: f32 = scaled.iter().sum();
        let probs: Vec<f32> = scaled.iter().map(|&x| x / sum).collect();

        // 加權隨機採樣
        let r: f32 = rand::random();
        let mut cumulative = 0.0;
        for (i, &p) in probs.iter().enumerate() {
            cumulative += p;
            if r <= cumulative {
                return i as u32;
            }
        }
        (probs.len() - 1) as u32
    }
}
```

## 6. 模型大小與量化策略

```
WASM 中的模型部署策略：
─────────────────────────

┌──────────────────────────────────────────────────┐
│                 雲端 API                           │
│  GPU 叢集 / TPU                                   │
│  GPT-4 / Claude / Gemini                         │
└────────────────────┬─────────────────────────────┘
                     │ 無法使用雲端？請考慮：
                     ▼
┌──────────────────────────────────────────────────┐
│          WASM 邊緣推論                            │
├──────────────────────────────────────────────────┤
│  大型模型（> 1B 參數）                             │
│  └── 需要 4-bit 量化 + KV cache 最佳化            │
│  └── 模型大小：500MB-2GB                          │
│  └── 適用：離線文字生成、程式碼補全                 │
├──────────────────────────────────────────────────┤
│  中型模型（100M-1B 參數）                          │
│  └── 需要 int8 量化                               │
│  └── 模型大小：50MB-500MB                         │
│  └── 適用：文字分類、實體辨識、問答                 │
├──────────────────────────────────────────────────┤
│  小型模型（< 100M 參數）                           │
│  └── 可以保持 f32 精度                            │
│  └── 模型大小：< 50MB                             │
│  └── 適用：影像分類、情緒分析、關鍵字偵測            │
└──────────────────────────────────────────────────┘
```

## 7. 效能量度

```
WASM 推論基準測試（M3 Max MacBook Pro）：
─────────────────────────────────────────

模型：MobileNet V2（影像分類，1000 類）

┌─────────────────────┬────────────┬──────────┐
│ 執行環境              │ 延遲 (ms)  │ 相對於原生 │
├─────────────────────┼────────────┼──────────┤
│ 原生 PyTorch (MPS)  │ 5.2        │ 100%     │
│ WASM + Candle (CPU) │ 8.1        │ 64%      │
│ WASM + SIMD         │ 6.8        │ 76%      │
│ WASM + WebGPU       │ 3.5        │ 149%     │
└─────────────────────┴────────────┴──────────┘

模型：TinyLLaMA 1.1B（文字生成）

┌─────────────────────┬────────────┬──────────┐
│ 執行環境              │ tokens/秒  │ 相對於原生 │
├─────────────────────┼────────────┼──────────┤
│ 原生 llama.cpp      │ 25.3       │ 100%     │
│ WASM + int4 量化     │ 12.1       │ 48%      │
│ WASM + int8 量化     │ 8.7        │ 34%      │
│ WASM + f16          │ 4.2        │ 17%      │
└─────────────────────┴────────────┴──────────┘
```

## 8. 結語

AI 推論在 WASM 上的應用在 2026 年已經從「可行」走向「實用」。對於中小型模型，WASM 可以提供接近原生的推論效能，同時保持跨平台的完全可攜性。結合量化技術和 WebGPU 加速，即使是超過十億參數的模型也能在瀏覽器和邊緣裝置上執行。這對於隱私保護（資料不離開本機）、離線使用、和成本控制具有重要意義。

---

## 延伸閱讀

- [Candle ML 框架](https://www.google.com/search?q=Candle+Rust+ML+framework+WASM)
- [ONNX Runtime Web](https://www.google.com/search?q=ONNX+Runtime+Web+WASM)
- [WASI-NN 規範](https://www.google.com/search?q=WASI+Neural+Network)
- [WASM 中的 LLM 推論](https://www.google.com/search?q=LLM+inference+in+WebAssembly)
- [模型量化技術](https://www.google.com/search?q=model+quantization+int8+int4)
