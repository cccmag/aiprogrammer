# 文章集錦

## Rust 與機器學習推論專輯

### 程式相關（5 篇）

#### 1. [Rust ML 生態入門 — Candle/Burn/tract 框架定位與選擇](article1.md)

Rust ML 推論生態的三大框架：Candle（輕量無依賴）、Burn（可組合後端）、tract（ONNX 引擎）。各自的設計哲學、適用場景與選擇指南。包含 Hello World 等級的推論範例與效能比較。

#### 2. [Candle 框架實戰 — 輕量推論、Llama/Whisper 支援](article2.md)

深入 Candle 框架的實戰使用：模型載入、張量運算、Llama/Whisper 等主流模型的推論實作。從 safetensors 權重載入到前向傳播的完整流程。

#### 3. [Burn 深度學習框架 — 可組合後端設計、WGPU GPU 推論](article3.md)

Burn 的後端抽象設計（ndarray、WGPU、CUDA、Tokio 後端）、自訂模型的定義與訓練、WGPU 後端 GPU 推論的設定與效能調校。

#### 4. [tract ONNX 推論引擎 — ONNX 格式、載入執行、最佳化](article4.md)

ONNX 格式的技術規格、tract 的載入與執行流程、模型最佳化（節點融合、常數摺疊）、量化推論的實作方法與效能分析。

#### 5. [邊緣裝置 ML 部署 — 嵌入式推論、感測器資料處理](article5.md)

在 Raspberry Pi、Jetson Nano、ESP32 等邊緣裝置上部署 Rust ML 推論管線。感測器資料的即時處理、模型壓縮與部署策略。

### AI 相關（5 篇）

#### 6. [AI 輔助 Rust ML 開發 — LLM 生成模型綁定、自動優化](article6.md)

使用 LLM（Claude、GPT 等）自動生成 Rust ML 模型綁定程式碼、從 PyTorch 模型自動產生 Candle/Burn 部署程式碼、AI 輔助的推論效能最佳化。

#### 7. [ML 模型量化與最佳化 — FP32→FP16→INT8、剪枝、蒸餾](article7.md)

模型量化的理論與實務：FP32→FP16→INT8 的轉換流程、校準資料集的使用、模型剪枝與知識蒸餾在 Rust 部署中的應用。包含 Rust 程式碼範例。

#### 8. [Rust 與 Python ML 協作模式 — PyTorch 訓練→Rust 部署](article8.md)

完整的 ML 開發流程：Python/PyTorch 訓練模型 → ONNX 匯出 → Rust 推論引擎部署。包含權重轉換、精度驗證、CI/CD 整合的最佳實務。

#### 9. [即時 ML 推論系統設計 — 低延遲管線、非同步、併發](article9.md)

設計低延遲 ML 推論系統的架構模式：非同步推理管線（Tokio + Candle/Burn）、請求批次處理、併發控制、模型熱重載。包含生產級 Rust 系統設計。

#### 10. [Rust ML 的未來展望 — 2027 趨勢、生態發展、學習路徑](article10.md)

Rust ML 生態 2027 年的關鍵趨勢：邊緣 AI 爆發、WebGPU 推論、模型壓縮技術進步。從初學者到進階的 Rust ML 學習路徑建議。
