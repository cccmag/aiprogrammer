# 本月新聞

## Rust AI 生態重大事件

### Candle 0.9 發布：LLM 訓練支援與動態圖

HuggingFace 於本月發布 Candle 0.9 版本，新增了 LLM 訓練的基礎支援，包括 FSDP（Fully Sharded Data Parallelism）的實驗性實作、動態計算圖（eager mode），以及對 LLaMA-4 QLoRA fine-tuning 的原生支援。這標誌著 Candle 從純推論框架向訓練框架的重要轉折。

### Burn 0.15 引入編譯期形狀檢查

Burn 社群發布 0.15 版本，核心亮點是 `burn-tensor-checked` crate——利用 Rust 的 const generics 在編譯期驗證張量形狀的正確性。形狀不匹配的運算現在會在編譯時被捕獲，而非在執行期 panic。

### WebGPU ML Extension 提案進入第二階段

W3C 的「WebGPU Neural Network Extension」提案本月進入 Candidate Recommendation 階段。該標準定義了 GPU 上的矩陣乘法、卷積、歸一化等運算的標準化介面。wgpu 團隊已實作了草案的大部分內容。

### tract 0.22 支援 200+ ONNX 算子

tract 本月發布 0.22 版本，ONNX 算子支援數量突破 200 個，覆蓋了 CV（YOLOv8、ResNet）、NLP（BERT、T5）、語音（Whisper）等主流模型。`no_std` 路徑的最佳化使其二進位體積縮小至 180KB。

### ESP32-S3 Rust AI SDK 正式發布

樂鑫（Espressif）正式發布基於 Rust 的 ESP AI SDK，支援在 ESP32-S3 上執行 MobileNet、TinyML 等模型。SDK 整合了 `tract` 推論引擎並提供了感測器驅動和 I2S 音訊輸入的 Rust 介面。

---

## 產業動態

- **HuggingFace** 宣布其推論基礎設施的 30% 已遷移至 Rust（Candle + axum）
- **Google** 開源了 Rust 編寫的 ML 資料管線工具 `datapipe-rs`
- **Mozilla** 的 WebGPU ML 研究小組發布了 Rust + WGSL 的訓練範例庫
- **AWS** 在 Nitro 晶片中整合了 Rust ML 推論引擎，用於機密運算場景

---

**參考資料**

- https://www.google.com/search?q=Candle+0.9+LLM+training+release
- https://www.google.com/search?q=Burn+compile+time+shape+checking
- https://www.google.com/search?q=WebGPU+Neural+Network+Extension+W3C
- https://www.google.com/search?q=tract+ONNX+0.22+release
- https://www.google.com/search?q=ESP32+S3+Rust+AI+SDK+Espressif
