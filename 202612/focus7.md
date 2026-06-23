# AI + WebAssembly

## 瀏覽器 ML 推論、邊緣 AI、LLM 生成（2024-2026）

### 前言

AI 與 WebAssembly 的結合正在從兩個方向展開：一是用 WASM 在瀏覽器和邊緣裝置上執行 ML 推論，二是用 LLM 輔助 WASM 模組的生成和最佳化。兩者相互促進，正在創造全新的應用場景。

### 瀏覽器中的 ML 推論

**ONNX Runtime Web** 提供三種後端：

```
ONNX Runtime Web
├── WASM 後端 ── CPU 推論，通用相容
├── WebGL 後端 ── GPU 加速（2D 紋理）
└── WebGPU 後端 ── GPU 加速（Compute Shader）
```

```javascript
import * as ort from 'onnxruntime-web';

const session = await ort.InferenceSession.create('model.onnx');
const output = await session.run({ input: tensor });
```

**WasmEdge** 在邊緣 AI 場景的優勢：

- 支援 TensorFlow Lite 和 ONNX 模型
- 原生 WASM 執行，無需 JavaScript 膠水層
- 針對邊緣裝置的資源管理

### 邊緣 AI 應用場景

| 場景 | 模型 | 平台 | 延遲 |
|------|------|------|------|
| 人臉偵測 | MobileNet SSD | 瀏覽器 WASM | ~30ms |
| 離線翻譯 | Transformer（小型） | 邊緣 WasmEdge | ~50ms |
| 語音辨識 | Whisper（tiny） | 瀏覽器 WebGPU+WASM | ~100ms |
| 物件偵測 | YOLO（nano） | 邊緣 Cloudflare Workers | ~80ms |

### WASM 中的影像分類

```rust
use wasi_nn;

fn classify(img: &[u8]) -> Result<String, Error> {
    let graph = wasi_nn::GraphBuilder::new(
        wasi_nn::GraphEncoding::Onnx,
        wasi_nn::ExecutionTarget::CPU,
    ).build_from_bytes(&[model_bytes])?;

    let context = graph.init_context()?;
    context.set_input(0, wasi_nn::TensorType::F32, &[1, 3, 224, 224], img)?;
    context.compute()?;
    let output: Vec<f32> = context.get_output(0)?;
    Ok(format!("Confidence: {:.2}", output.iter().max_by(|a, b| a.partial_cmp(b).unwrap()).unwrap()))
}
```

### LLM 輔助 WASM 開發

LLM 可以在以下環節協助 WASM 開發：

1. **程式碼生成**：生成 WASM 友善的 Rust 程式碼（避免 std::io，使用 &[u8] 傳遞大量資料）
2. **編譯設定**：根據場景選擇最佳的最佳化參數（-Oz vs -O3）
3. **體積分析**：分析 twiggy 輸出，建議減少體積的方法
4. **安全審查**：檢測 unsafe 程式碼和潛在的邊界錯誤

### 效能數據

MobileNet V2 在瀏覽器中的推論效能（M3, Chrome）：

| 後端 | 推論時間 | FPS |
|------|---------|-----|
| WASM（單線程） | 85ms | 12 |
| WASM（SIMD） | 45ms | 22 |
| WebGL | 30ms | 33 |
| WebGPU | 12ms | 83 |

### 小結

AI + WASM 的整合正在快速成熟。ONNX Runtime Web 讓瀏覽器推論達到實用水準，WasmEdge 讓邊緣 AI 成為可能，LLM 輔助開發則讓 WASM 的開發效率大幅提升。這三者的結合將在 2027 年產生更多創新應用。

---

**下一步**：[回首頁](focus.md)

## 延伸閱讀

- [ONNX Runtime Web](https://www.google.com/search?q=ONNX+Runtime+Web)
- [WasmEdge AI](https://www.google.com/search?q=WasmEdge+AI+inference)
- [瀏覽器機器學習](https://www.google.com/search?q=browser+machine+learning+WebAssembly)
- [AI 輔助 WASM 開發](https://www.google.com/search?q=AI+assisted+WebAssembly+development)
