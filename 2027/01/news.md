# 本月新知

## 2027 年 1 月程式與 AI 技術動態

### Rust ML 生態

**Candle 1.5 發布：新增多模態模型支援**

Hugging Face 發布的 Candle 1.5 版本加入了對多模態模型（如 LLaVA、CLIP）的原生支援。Candle 1.5 也導入了自訂運算核心（Custom Kernel）API，允許開發者用純 Rust 實作高效的自定義算子，而不需要撰寫 CUDA C++。

**Burn WGPU 後端達到生產級效能**

Burn 框架的 WGPU 後端在 2027 年初的基準測試中，GPU 推論效能已達到 CUDA 後端的 92%。這意味著開發者可以在不需要 CUDA 的環境中（macOS、行動裝置）獲得接近 NVIDIA GPU 的推論速度。

**tract 6.0 支援 ONNX Runtime 相容格式**

tract 6.0 發布，新增對 ONNX Runtime 擴展格式的直接載入支援，以及更完善的 INT8 量化流程。tract 6.0 也加入了動態形狀（Dynamic Shapes）的處理能力，使輸入大小不固定的模型推論成為可能。

### 程式語言與框架

**Rust 2027 Edition 草案發布**

Rust 團隊發布 2027 Edition 的 RFC 草案，重點包括：泛型關聯型別（Generic Associated Types）的穩定化、asynchronous drop 的初步支援、以及模式匹配的進一步增強。Rust 2027 Edition 預計年中正式發布。

**PyTorch 3.0 強化 Rust 綁定**

PyTorch 3.0 發布，內建了透過 PyO3 實現的官方 Rust 綁定。開發者現在可以直接從 Rust 呼叫 PyTorch 的訓練 API，而不再需要透過 Python 子程序或 C FFI。這大幅簡化了 Rust-Python ML 的協作流程。

**WebGPU 標準 1.0 正式發布**

W3C 發布 WebGPU 1.0 標準，所有主流瀏覽器均已完成實作。這對 Rust ML 生態意義重大——Burn 等框架可以直接在瀏覽器中進行 GPU 加速的 ML 推論，不需要任何插件或後端切換。

### AI 與機器學習

**Claude 7 的 Rust ML 程式碼生成能力**

Anthropic 發布 Claude 7，在 Rust ML 程式碼生成上達到全新水準。Claude 7 可以從 PyTorch 模型定義自動產生對應的 Candle/Burn/tract 部署程式碼，包括量化、批次處理等最佳化步驟。

**邊緣 AI 晶片市場爆發**

2027 年 CES 展會上，多家廠商發布了專為邊緣 ML 推論設計的 RISC-V AI 晶片。這些晶片支援 INT8/INT4 矩陣運算加速，並有 Rust 的交叉編譯工具鏈支援。Rust 的 no_std 特性使其成為此類晶片上的理想 ML 推論語言。

**量化工具鏈成熟**

多個 Rust ML 專案發布了整合的量化工具鏈，支援從 ONNX 模型自動進行 FP32→FP16→INT8 的量化校準（Calibration），並產生可部署的量化模型檔案。這讓開發者不需要手動處理量化參數。

### 開發工具

**cargo-ml 工具發布**

社群發布了 cargo-ml——一個專門管理 Rust ML 專案的 Cargo 子命令。它整合了模型下載、格式轉換、量化、推論測試等功能，讓 Rust ML 開發流程類似於 Python 的 transformers/huggingface_hub 體驗。

**VS Code Rust ML 擴充套件**

微軟發布了 VS Code 的 Rust ML 專用擴充套件，提供張量形狀可視化、模型結構圖、推論效能分析等功能，並整合了 Candle/Burn/tract 的除錯支援。

### 業界動態

- **Tesla 將車載視覺推論管線遷移至 Rust**：從 Python+CUDA 遷移至 Candle+WGPU，降低了車載系統的耗電與記憶體使用
- **Google 在 Android 中整合 Rust ML 推論框架**：tract 成為 Android 新版本的預設 ONNX 推論引擎之一
- **NASA 採用 Rust ML 進行衛星影像分析**：邊緣推論直接在衛星上處理影像，節省回傳頻寬
- **Hugging Face 新增 Rust 模型部署管道**：支援從 Model Hub 一鍵匯出 Candle/tract 格式的部署套件
- **Rust 基金會成立 ML 工作小組**：專注於標準化 Rust ML 生態的 API 設計與互通性

---

*參考搜尋：* [Rust ML 2027 新聞](https://www.google.com/search?q=Rust+machine+learning+2027+news) | [Candle framework 1.5](https://www.google.com/search?q=Candle+1.5+Rust+ML+2027) | [Burn WGPU 效能](https://www.google.com/search?q=Burn+WGPU+GPU+inference+performance+2027) | [tract ONNX 6.0](https://www.google.com/search?q=tract+ONNX+Rust+6.0+2027) | [WebGPU 1.0](https://www.google.com/search?q=WebGPU+1.0+standard+2027)
