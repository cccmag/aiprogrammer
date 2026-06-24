# Transformer 的演化樹

## 前言

從 2017 年的原始 Transformer 論文，到 2020 年的各種變體，讓我們回顧這個架構的演化歷程。

---

## 一、2017：原點

### Attention is All You Need

Google 發表了原始 Transformer 論文。

核心元件：
- Position-wise Feed-Forward Networks
- Multi-Head Attention
- Positional Encoding
- Encoder-Decoder Architecture

---

## 二、2018：預訓練時代

### GPT (Generative Pre-trained Transformer)

OpenAI 的貢獻：
- 使用 Left-to-Right Transformer Decoder
- 預訓練 + 微調範式
- 1.17 億參數

### BERT (Bidirectional Encoder Representations)

Google 的創新：
- 雙向 Transformer Encoder
- Masked Language Model
- Next Sentence Prediction
- 3.4 億參數（large）

---

## 三、2019：最佳化與探索

### GPT-2

- 15 億參數
- 質疑開源策略
- 展示強大的零樣本能力

### Transformer-XL

創新：
- 片段循環機制
- 相對位置編碼
- 解決固定長度上下文限制

### XLNet

結合：
- Permutation Language Modeling
- 雙向注意力
- 自回歸模型

### RoBERTa

Facebook 的優化：
- 去除 NSP
- 動態遮罩
- 更多訓練資料

### DistilBERT

 Hugging Face 的蒸餾：
- 參數減少 40%
- 速度提升 60%
- 保留 97% 效能

---

## 四、2020：規模與多樣性

### GPT-3

- 1750 億參數
- Few-shot Learning
- 幾乎不需要任務特定的微調

### T5

Google 的統一框架：
- Text-to-Text 範式
- 所有任務統一為翻譯問題
- 11B 參數

### ELECTRA

Google 的新預訓練目標：
- Replaced Token Detection
- 更高效地利用計算
- 小模型也能有好效果

### BART

Facebook 的 Encoder-Decoder：
- 降噪自編碼器
- 適合生成任務
- 靈活的預訓練目標

---

## 五、演化樹結構

```
                    Transformer (2017)
                          |
          +---------------+---------------+
          |                               |
      Encoder                           Decoder
          |                               |
    +-----+-----+                    +----+-----+
    |           |                    |         |
   BERT       T5                  GPT       CTRL
    |           |                    |
  RoBERTa    Bart                  GPT-2
    |           |                    |
 ALBERT     Marian                  GPT-3
    |
 ELECTRA
```

---

## 六、關鍵創新時間線

| 年份 | 創新 | 影響 |
|------|------|------|
| 2017 | Transformer 架構 | 開創新時代 |
| 2018 | GPT, BERT | 預訓練+微調 |
| 2019 | XLNet, Transformer-XL, RoBERTa | 最佳化 |
| 2020 | GPT-3, T5, BART, ELECTRA | 大型化、多樣化 |

---

## 七、2020 年後的趨勢

### 多語言模型

- mBERT
- XLM-R
- M2M-100

### 多模態模型

- CLIP (2021)
- DALL-E (2021)
- GPT-4V (2023)

### 程式碼模型

- Codex (2021)
- CodeT5
- PaLM-Coder

---

## 結語

Transformer 從一個機器翻譯模型，發展成為深度學習的核心架構。其演化涵蓋了：
- 更高效的預訓練目標
- 更大的模型規模
- 更廣泛的應用領域

這個演化仍在繼續。

---

*延伸閱讀：[transformer+evolution+timeline+2017-2020](https://www.google.com/search?q=transformer+evolution+timeline+2017+2018+2019+2020)