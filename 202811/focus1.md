# 邊緣 AI 導論（2017-2028）

## 什麼是邊緣 AI？

邊緣 AI（Edge AI）是指在終端裝置上直接執行人工智慧推論，而非依賴雲端伺服器。與傳統雲端 AI 相比，邊緣 AI 具備低延遲、離線運作、隱私保護與降低成本等優勢。2017 年 Google 發表 MobileNet 輕量化卷積神經網路，大幅降低模型參數量，揭開了邊緣 AI 時代的序幕。

## 發展歷程

- **2017** — Google 提出 MobileNet，使用深度可分離卷積（depthwise separable convolution）減少計算量（[Google 搜尋](https://www.google.com/search?q=MobileNet+2017+Google+depthwise+separable+convolution)）。
- **2018** — 樹莓派 3B+ 普及，開發者開始在單板電腦上執行輕量 AI 模型。
- **2019** — TensorFlow Lite 正式發布，支援 Android 與 iOS 裝置端推論（[Google 搜尋](https://www.google.com/search?q=TensorFlow+Lite+2019+launch)）。
- **2020** — 微軟推出 Embedded Learning Library（ELL），針對 ARM 架構最佳化。
- **2021** — NVIDIA Jetson Nano 帶起邊緣 GPU 推論風潮，邊緣 AI 進入商業應用階段。
- **2022** — Meta 發表 MobileViT，將 Vision Transformer 引入行動裝置。
- **2023** — 生成式 AI 浪潮下，邊緣裝置開始支援小型 LLM（如 Phi-2）。
- **2024** — Apple 發布 Core ML 6 與 ANE（Apple Neural Engine）深度整合。
- **2025** — Qualcomm Snapdragon X 系列 NPU 算力達 45 TOPs。
- **2026** — Arm Ethos-U85 NPU 量產，MCU 級別邊緣 AI 進入主流。
- **2027** — 邊緣 AI 框架一統化趨勢，OpenXLA 開始支援邊緣編譯。
- **2028** — 邊緣 AI 在工業 4.0 與智慧醫療中成為標準配置。

## 核心概念

邊緣 AI 的三個核心挑戰：**模型壓縮**（剪枝、量化、蒸餾）、**硬體加速**（NPU、GPU、DSP）與**框架支援**（TFLite、ONNX Runtime、Core ML）。本系列文章將逐一深入探討這些面向。

## 參考資源

- [Google 搜尋：Edge AI overview](https://www.google.com/search?q=Edge+AI+overview+2017+2028+history)
- [Google 搜尋：TinyML vs Edge AI](https://www.google.com/search?q=TinyML+vs+Edge+AI+difference)
