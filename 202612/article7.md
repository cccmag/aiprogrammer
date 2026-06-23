# 瀏覽器中的 ML 推論

## 1. 引言

機器學習推論傳統依賴於伺服器端的 GPU/TPU。但對於延遲敏感、隱私重要、或離線場景，在瀏覽器中直接執行 ML 推論具有獨特的價值。WASM 為此提供了高效能的計算基礎，而 ONNX Runtime Web 和 WasmEdge 等框架則提供了完整的推論解決方案。

## 2. ONNX Runtime Web 架構

### 2.1 整體設計

ONNX Runtime Web 將 ONNX 模型轉換為可在瀏覽器中執行的格式。其核心是 WASM 後端：

```
ONNX 模型 (.onnx)
    │
    ▼
ONNX Runtime Web
    ├── WebAssembly 後端 （通用，CPU 推論）
    ├── WebGL 後端 （GPU 加速，2D 紋理）
    └── WebGPU 後端 （GPU 加速，Compute Shader）
```

### 2.2 WASM 後端的角色

WASM 後端負責所有 CPU-bound 的運算——包括算子（operator）的實作、張量運算、和模型控制流：

```javascript
import * as ort from 'onnxruntime-web';

async function runInference() {
    // 初始化 WASM 後端
    await ort.init({
        backend: 'wasm',
        wasmPaths: {
            'ort-wasm.wasm': '/static/ort-wasm.wasm',
        }
    });

    // 載入模型
    const session = await ort.InferenceSession.create('/models/resnet50.onnx');

    // 準備輸入
    const input = new ort.Tensor('float32', imageData, [1, 3, 224, 224]);

    // 執行推論
    const outputs = await session.run({ input: input });
    console.log('預測結果:', outputs);
}
```

### 2.3 效能的權衡

| 後端 | 推論速度 | 初始化時間 | 相容性 |
|------|---------|-----------|--------|
| WASM | 中等 | 快 | 所有瀏覽器 |
| WebGL | 快 | 中等 | 大部分瀏覽器 |
| WebGPU | 極快 | 慢 | 最新瀏覽器 |

## 3. WasmEdge 的 AI 推論框架

WasmEdge 是 CNCF 的沙箱專案，提供了一個針對邊緣運算優化的 WASM 執行期，特別適合 AI 推論場景。

### 3.1 WasmEdge + TensorFlow

```rust
use wasmedge_tensorflow_interface;

#[wasm_bindgen]
pub fn classify_image(image_data: &[u8]) -> String {
    // 載入 TensorFlow Lite 模型
    let model = wasmedge_tensorflow_interface::load_model(
        "models/mobilenet_v2.tflite"
    );

    // 設定輸入
    let input = wasmedge_tensorflow_interface::Tensor::new(
        &[1, 224, 224, 3],
        image_data,
    );

    // 執行推論
    let outputs = model.run(&[input], &["output"]);

    // 解析結果
    let predictions = outputs[0].as_slice::<f32>();
    let max_idx = predictions.iter()
        .enumerate()
        .max_by(|a, b| a.1.partial_cmp(b.1).unwrap())
        .map(|(i, _)| i)
        .unwrap_or(0);

    format!("Class: {}, Confidence: {:.2}%", max_idx, predictions[max_idx] * 100.0)
}
```

### 3.2 WasmEdge 與 ONNX

WasmEdge 也支援 ONNX 模型，透過 wasi-nn 擴充：

```rust
use wasi_nn;

fn run_onnx_inference(input: &[f32]) -> Vec<f32> {
    // 初始化推論引擎
    let graph = wasi_nn::GraphBuilder::new(
        wasi_nn::GraphEncoding::Onnx,
        wasi_nn::ExecutionTarget::CPU,
    ).build_from_bytes(&[
        &model_bytes,
    ]).unwrap();

    // 建立推論上下文
    let context = graph.init_context().unwrap();

    // 設定輸入
    context.set_input(0, wasi_nn::TensorType::F32, &[1, 3, 224, 224], input).unwrap();

    // 執行推論
    context.compute().unwrap();

    // 獲取輸出
    context.get_output(0).unwrap()
}
```

## 4. 瀏覽器推論的應用場景

### 4.1 即時物件偵測

```javascript
// 在瀏覽器中即時執行人臉偵測
const video = document.getElementById('webcam');
const canvas = document.getElementById('overlay');

async function detectFaces() {
    const session = await ort.InferenceSession.create('face-detection.onnx');

    async function processFrame() {
        const input = preprocessFrame(video);
        const { boxes } = await session.run({ image: input });
        drawBoxes(canvas, boxes);
        requestAnimationFrame(processFrame);
    }

    processFrame();
}
```

### 4.2 離線翻譯

```javascript
// 完全離線的翻譯模型
const translator = await createTranslator('en', 'zh');
const result = await translator.translate('Hello, WebAssembly!');
console.log(result); // "你好，WebAssembly！"
```

### 4.3 文字轉語音

```javascript
// 瀏覽器中的 TTS 推論
const tts = await createTTS('zh-TW');
const audio = await tts.synthesize('歡迎來到 AI 程式人雜誌');
audio.play();
```

## 5. WebGPU 與 WASM 的協同

WebGPU 的 Compute Shader 和 WASM 的數值計算可以協同工作：

```
WASM 負責：
- 資料前處理（圖片解碼、正規化）
- 後處理（softmax、top-k 排序）
- 控制流（模型分支選擇）

WebGPU 負責：
- 矩陣乘法（卷積層）
- 大量平行計算（batch 推論）
- 張量操作（reshape、transpose）
```

## 6. 效能基準測試

以 MobileNet V2 在瀏覽器中推論為例（Chrome 120, M3）：

| 後端 | 推論時間 | FPS |
|------|---------|-----|
| WASM（單線程） | 85 ms | ~12 |
| WASM（SIMD） | 45 ms | ~22 |
| WebGL | 30 ms | ~33 |
| WebGPU | 12 ms | ~83 |

## 7. 結語

瀏覽器中的 ML 推論已經從實驗性質發展到生產就緒。ONNX Runtime Web 提供了完整的 WASM 推論框架，WasmEdge 則在邊緣場景有獨特優勢。隨著 WebGPU 的普及和 WASM 的持續最佳化，瀏覽器將成為輕量級 AI 推論的重要平台。

---

## 延伸閱讀

- [ONNX Runtime Web 文件](https://www.google.com/search?q=ONNX+Runtime+Web+documentation)
- [WasmEdge AI 推論](https://www.google.com/search?q=WasmEdge+AI+inference)
- [WebGPU 與 WASM 整合](https://www.google.com/search?q=WebGPU+WebAssembly+integration)
- [瀏覽器機器學習基準](https://www.google.com/search?q=browser+machine+learning+benchmark)
