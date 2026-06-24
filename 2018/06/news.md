# 本月新知

## 2018 年 6 月程式與 AI 技術動態

### 程式語言與框架

**Apple WWDC 2018**

Apple 在 WWDC 2018 發布了多項重要更新：
- iOS 12、macOS Mojave、watchOS 5
- ARKit 2：增強實境開發工具
- Core ML 2：更快的機器學習推論
- Swift 4.2：語言改進

**Java 10 發布**

Java 10 在 2018 年 3 月發布，6 月已廣泛使用。新特性包括：
- 區域變量類型推斷（var）
- 不可變集合工廠方法
- G1 垃圾回收器改進

**Webpack 4 發布**

Webpack 4 是模組打包工具的重大更新：
- 零設定打包
- 支援 WebAssembly
- 效能大幅提升

### AI 與機器學習（CRITICAL: GPT 發布！）

**GPT 論文發布：生成式預訓練**

2018 年 6 月，OpenAI 發布了「Improving Language Understanding by Generative Pre-Training」論文，介紹了 GPT（Generative Pre-Training）模型。這是語言模型的重要突破！

GPT 的關鍵創新：
- 使用無監督預訓練 + 監督式微調
- 基於 Transformer 架構
- 117M 參數
- 在多個 NLP 任務上達到最先進結果

```
┌─────────────────────────────────────────────────────┐
│             GPT 的創新：預訓練 + 微調                │
├─────────────────────────────────────────────────────┤
│                                                     │
│  階段 1：無監督預訓練                                 │
│  ┌────────────────────────────────────┐           │
│  │ 大規模文字資料                       │           │
│  │           ▼                         │           │
│  │     Transformer 解碼器              │           │
│  │           ▼                         │           │
│  │    生成式語言模型                    │           │
│  └────────────────────────────────────┘           │
│               │                                    │
│               ▼                                    │
│  階段 2：監督式微調                                   │
│  ┌────────────────────────────────────┐           │
│  │  特定任務標註資料                    │           │
│  │           ▼                         │           │
│  │    添加輸出層                       │           │
│  │           ▼                         │           │
│  │    在任務上微調                     │           │
│  └────────────────────────────────────┘           │
│                                                     │
└─────────────────────────────────────────────────────┘
```

**Transformer 架構的影響**

2017 年的 Transformer 論文「Attention is All You Need」開創了新時代。2018 年 6 月，GPT 基於 Transformer 的解碼器部分，展示了預訓練語言模型的威力。

**文字生成模型的進展**

在 GPT 之前，文字生成主要基於：
- N-gram 語言模型
- RNN/LSTM 語言模型
- Encoder-decoder 模型

GPT 的預訓練方法為語言模型開闢了新道路。

**生成對抗網路（GAN）持續進展**

GAN 在 2018 年持續發展，各種變體被提出用於圖像生成、風格遷移等任務。

### 開發工具與雲端服務

**GitHub 被微軟收購**

2018 年 6 月 4 日，微軟正式宣佈收購 GitHub。這一事件對開源生態產生了深遠影響。

**TensorFlow 1.9 發布**

TensorFlow 1.9 帶來了更多 Keras 整合和效能改進。

**Kubeflow 1.0 開發中**

Kubernetes 上的 ML 工作流平臺 Kubeflow 正在快速發展。

### 業界動態

- **OpenAI 發布 GPT**：標誌著生成式 AI 的興起
- **DeepMind 發布 AlphaFold**：蛋白質折疊預測突破
- **Adobe Sensei 更新**：AI 驅動的創意工具
- **NVIDIA 發布 Jetson Xavier**：邊緣 AI 硬體

### 開源專案

- **ONNX 獲得更多支援**：Facebook、Microsoft 推動的模型交換格式
- **Hugging Face Transformers**：成立於 2016 年，2018 年開始流行
- **fast.ai v1.0 準備中**：高階深度學習庫

### 法規與倫理

- **GDPR 生效**：2018 年 5 月 25 日，歐盟 GDPR 正式生效
- **AI 倫理討論增加**：對 AI 偏見和透明性的關注提升

### 未來展望

GPT 的發布標誌著預訓練語言模型時代的開始。從 GPT 到 BERT（2018 年 10 月），再到更大的模型，生成式 AI 正在迅速發展。

---

## 延伸閱讀

- [GPT 原始論文](https://www.google.com/search?q=Improving+Language+Understanding+by+Generative+Pre-Training+2018)
- [Transformer 論文](https://www.google.com/search?q=Attention+is+All+You+Need+2017)
- [OpenAI 官方網站](https://www.google.com/search?q=OpenAI+official+site)
- [自然語言處理預訓練模型](https://www.google.com/search?q=pretrained+language+models+2018)