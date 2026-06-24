# 文章索引

## 框架基礎與實作 (article1–5)

這五篇文章專注於三大框架的核心功能與實作。

| # | 主題 | 說明 |
|---|------|------|
| 1 | [TensorFlow 2.0 自動微分](article1.md) | GradientTape 與 tf.function |
| 2 | [PyTorch 動態計算圖](article2.md) | Define-by-Run 與 autograd |
| 3 | [JAX 純函式式設計](article3.md) | jit、grad、vmap、pmap |
| 4 | [tf.keras 高階 API](article4.md) | Sequential、Functional API |
| 5 | [TorchScript 與部署](article5.md) | 模型轉換與 JIT 編譯 |

## 部署與進階 (article6–10)

這五篇文章涵蓋模型部署與效能優化。

| # | 主題 | 說明 |
|---|------|------|
| 6 | [TensorFlow Lite](article6.md) | 邊緣裝置部署 |
| 7 | [PyTorch Mobile](article7.md) | 行動裝置推論 |
| 8 | [框架效能比較](article8.md) | 訓練速度與記憶體 |
| 9 | [遷移與共存](article9.md) | 跨框架模型轉換 |
| 10 | [未來展望](article10.md) | 框架發展趨勢 |

## 閱讀建議

初學者建議從 article1 開始，選擇一個框架深入學習。建議選擇 PyTorch 作為入門框架，因為其語法直觀且除錯方便。

本期提供的 `_code/ml_demo.py` 展示了在沒有 GPU 的純 CPU 環境中實現機器學習的基礎概念，幫助讀者理解底層原理。

所有框架的完整教學，建議參考各框架官方文件（2020 年初版本）。