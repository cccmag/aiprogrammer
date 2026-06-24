# 3. 深度學習框架演進

## 框架生態概況

2018 年的深度學習框架生態：

### TensorFlow（Google）
- **2 月**：TensorFlow 1.7 發布，整合 Keras
- **11 月**：TensorFlow 2.0 開發者預覽版發布
- 簡化 API、預設 eager execution、統一的 tf.keras

### PyTorch（Facebook）
- **12 月**：PyTorch 1.0 正式版發布
- TorchScript、JIT 編譯器、量化工具
- 生態系統快速成長

### 其他框架
- **MXNet**：Amazon 支持，持續優化
- **PaddlePaddle**：百度開源，中文文件豐富
- **MindSpore**：華為發布

## TensorFlow 2.0 的變革

### 主要變化
1. **Eager execution 預設**：動態計算圖，減少除錯難度
2. **統一的 Keras API**：tf.keras 成為中央高級 API
3. **移除冗餘 API**：清理重複功能
4. **更好的相容性**：向後相容性改善

### 預訓練模型庫
TensorFlow Hub 與 TensorFlow Model Garden 提供預訓練模型。

## PyTorch 1.0 的穩定

### 生產級功能
1. **TorchScript**：將 PyTorch 模型轉為可部署格式
2. ** JIT 編譯**：加速執行
3. **分散式訓練**：更好的多 GPU 支援

### 生態成長
- Hugging Face Transformers
- fairseq、AllenNLP 等工具庫

## Keras 的崛起

Keras 成為事實上的標準高層 API：
- 簡潔的 API 設計
- 支援 TensorFlow、MXNet、Theano 後端
- 大量教學資源與社群支持

## 框架選擇建議

| 需求 | 推薦框架 |
|------|----------|
| 生產部署 | TensorFlow |
| 研究實驗 | PyTorch |
| 快速原型 | Keras |
| 移動端 | TensorFlow Lite |

## 參考資源

- https://www.google.com/search?q=2018+深度學習框架+年度回顧+TensorFlow+PyTorch+Keras
- https://www.google.com/search?q=TensorFlow+2.0+preview+改变+eager+execution+Keras+2018
- https://www.google.com/search?q=PyTorch+1.0+正式版+特性+torchscript+JIT+2018