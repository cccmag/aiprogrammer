# 行動裝置 AI 框架（2018-2028）

## 框架演進

行動裝置 AI 框架是邊緣 AI 的核心基礎設施。從 2018 年 Apple Core ML 與 TensorFlow Lite 正式發布開始，各家框架在模型格式、硬體加速與開發者體驗上展開激烈競爭。

## 主要框架比較

- **TensorFlow Lite（2019）** — 市佔率最高，支援 Android/iOS/Linux，靠 XNNPACK 委派加速 CPU 推論（[Google 搜尋](https://www.google.com/search?q=TensorFlow+Lite+XNNPACK+delegate)）。
- **Core ML（2018）** — Apple 生態專屬，深度整合 ANE（Apple Neural Engine），支援動態形狀與多輸出（[Google 搜尋](https://www.google.com/search?q=Core+ML+ANE+Apple+Neural+Engine)）。
- **ONNX Runtime Mobile（2020）** — 微軟主導，跨平台開放標準，支援 NNAPI 與 Core ML 委派。
- **MediaPipe（2021）** — Google 推出的跨平台多模態推論管線框架，擅長即時視訊處理。
- **PyTorch Mobile（2021）** — Meta 推出，支援即時追蹤（lazy tracing）與 Vulkan GPU 加速。
- **ExecuTorch（2024）** — Meta 新一代邊緣框架，針對手機與穿戴裝置設計。

## 關鍵技術

### 委派機制（Delegation）

框架透過委派將運算卸載至專用硬體。TFLite 的 GPU 委派使用 OpenCL/OpenGL ES，NNAPI 委派則連接 Android 的神經網路 HAL。

### 模型格式標準化

- 2023 年，MLIR 生態成熟，TensorFlow 與 PyTorch 都可透過 Torch-MLIR 統一編譯。
- 2025 年，GGUF 格式在手機 LLM 推論中崛起（[Google 搜尋](https://www.google.com/search?q=GGUF+mobile+LLM+inference)）。

## 效能數據

2026 年的旗艦手機（Snapdragon 8 Gen 5）在 MLPerf Mobile 上，ResNet-50 推論延遲已低於 2ms，較 2020 年改善超過 10 倍。

## 未來趨勢

- **多框架編譯層統合**：OpenXLA 將延伸至行動裝置。
- **大型語言模型在端**：Apple Intelligence 與 Google Gemini Nano 證明手機可執行 3B 參數模型。
- **異質計算排程**：動態分配 CPU/GPU/NPU 工作負載。

## 參考資源

- [Google 搜尋：Mobile AI framework comparison 2026](https://www.google.com/search?q=mobile+AI+framework+comparison+2026)
- [Google 搜尋：MLPerf Mobile benchmark results](https://www.google.com/search?q=MLPerf+Mobile+benchmark+2026)
