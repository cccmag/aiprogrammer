# 網頁 AI 技術（2021-2028）

## 瀏覽器中的 AI

網頁 AI（Web AI）讓機器學習推論直接在瀏覽器中執行，無需安裝任何套件。2021 年 TensorFlow.js 3.0 與 WebAssembly SIMD 的成熟，使得瀏覽器 AI 從概念驗證進入實際應用。相比原生應用，網頁 AI 具有跨平台、零部署與隱私保護的優勢。

## 技術基礎

### WebGL 與 WebGPU

TensorFlow.js 早期透過 WebGL 進行 GPU 加速。2023 年 WebGPU 正式標準化後，AI 推論速度提升 3-5 倍，因為 WebGPU 支援計算著色器（compute shader）與更高效的顯存管理（[Google 搜尋](https://www.google.com/search?q=WebGPU+machine+learning+inference)）。

### WebAssembly（WASM）

使用 WASM 執行模型推論，可達原生速度的 60-80%。XNNPACK 的 WASM 後端讓 TFLite 在瀏覽器中高效運行。

### ONNX Runtime Web

微軟推出 ONNX Runtime Web，支援 WebGPU 與 WASM 後端，可載入標準 ONNX 模型直接在瀏覽器中推論。

## 主要框架與工具

- **TensorFlow.js** — 最成熟的 Web AI 框架，支援 CPU（WASM）、WebGL、WebGPU 後端。
- **MediaPipe Solutions** — Google 提供的人物分割、手部追蹤等預訓練模型，封裝為 Web API。
- **Transformers.js** — 在瀏覽器中執行 Hugging Face Transformer 模型（[Google 搜尋](https://www.google.com/search?q=Transformers.js+Hugging+Face+browser)）。
- **WebLLM** — 透過 WASM + WebGL 在瀏覽器運行 LLM，2025 年已可執行 7B 模型。
- **MLC Web** — 統一編譯框架，將 PyTorch 模型編譯為 WASM 在瀏覽器中運行。

## 程式碼範例

以下使用 Transformers.js 在瀏覽器中執行情感分析：

```javascript
import { pipeline } from '@xenova/transformers';

async function analyzeSentiment(text) {
    const classifier = await pipeline(
        'sentiment-analysis',
        'Xenova/distilbert-base-uncased-finetuned-sst-2-english'
    );
    const result = await classifier(text);
    console.log(result);
}

analyzeSentiment('Edge AI is transforming the embedded world!');
```

## 效能限制與突破

瀏覽器 AI 的主要瓶頸在於 GPU 資源有限（與其他瀏覽器分頁共享）以及 WASM 的記憶體限制。2026 年 WebGPU 的進一步標準化與 SharedArrayBuffer 的廣泛支援，讓多執行緒推論成為可能。

## 參考資源

- [Google 搜尋：Web AI inference benchmark 2026](https://www.google.com/search?q=Web+AI+inference+benchmark+TensorFlow.js+WebGPU)
- [Google 搜尋：Transformers.js tutorial](https://www.google.com/search?q=Transformers.js+tutorial+web+browser)
