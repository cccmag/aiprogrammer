# 回顧與結語

## 2020 年 8 月號結語

### 本月主題回顧

本期雜誌深入探討了 Transformer 架構，這個自 2017 年由 Google 提出的創新模型，已成為深度學習領域最重要的架構之一。

#### Transformer 的核心組件

我們回顧了 Transformer 的關鍵創新：

1. **注意力機制**：透過 QKV 計算，直接建模序列內任意位置的依賴關係
2. **多頭注意力**：從多個子空間學習不同的相關性模式
3. **位置編碼**：為序列注入順序資訊
4. **殘差連接**： enable 訓練深層網路

#### 主要模型演化

| 模型 | 特點 | 發布時間 |
|------|------|---------|
| 原始 Transformer | Encoder-Decoder | 2017 |
| BERT | 雙向 Encoder | 2018 |
| GPT | 自回歸 Decoder | 2018 |
| GPT-2 | 大型化 | 2019 |
| T5 | Text-to-Text | 2020 |
| GPT-3 | Few-shot Learning | 2020 |

### Encoder vs Decoder

本期深入比較了兩種主要範式：

- **Encoder-only (BERT)**：適合理解任務，雙向上下文
- **Decoder-only (GPT)**：適合生成任務，自回歸方式

### 開源生態

Hugging Face Transformers 庫的蓬勃發展，使得最強大的 NLP 模型變得人人可用。

### 未來展望

Transformer 的應用已超越 NLP：
- **電腦視覺**：ViT、DETR
- **音訊處理**：語音辨識、音樂生成
- **多模態**：CLIP、DALL-E
- **強化學習**：Decision Transformer

### 讀者互動

親愛的讀者，感謝您閱讀本期 AI 程式人雜誌。

如果您對本期內容有任何疑問、建議或想法，歡迎透過以下方式與我們交流：

- GitHub Issues
- 電子郵件

下期我們將探討電腦視覺的進展，敬請期待。

### 訂閱資訊

AI 程式人雜誌每月出刊，您可以在以下平台訂閱：

- GitHub Releases
- 電子報

---

*本期雜誌由 OpenCode + Big Pickle 撰寫*

*陳鍾誠 (ccckmit) 編輯*

*2020 年 8 月*