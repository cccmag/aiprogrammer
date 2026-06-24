# 預訓練革命

## 前言

從 Word2Vec 到 BERT，語言表示學習經歷了漫長的演化過程。本篇文章將回顧預訓練技術的發展歷程，探討它如何改變了 NLP 的研究和應用方式。

## 早期的詞嵌入

### Word2Vec

2013 年，Tomas Mikolov 和 Google 團隊發表了 Word2Vec，這是第一個廣泛使用的詞嵌入方法。Word2Vec 包括兩種架構：

- **CBOW**：根據上下文預測中心詞
- **Skip-gram**：根據中心詞預測上下文

Word2Vec 的核心假設是「分佈假說」：具有相似上下文的詞具有相似的含義。

```python
# Word2Vec 示意
word_embedding["king"] - word_embedding["man"] + word_embedding["woman"] ≈ word_embedding["queen"]
```

### GloVe

2014 年，Stanford 團隊提出了 GloVe（Global Vectors），結合了全局語料庫統計和局部上下文資訊。

## 從靜態到動態

### 靜態詞嵌入的局限

Word2Vec 和 GloVe 產生的詞嵌入是靜態的——每個詞只有一個固定的表示。這無法處理一詞多義的問題。

```
bank 可以是「銀行」或「河岸」

靜態嵌入：只有一個 bank 表示
動態嵌入：根據上下文動態調整
```

### ELMo 的突破

2018 年，Allen Institute 發布了 ELMo（Embeddings from Language Models）。ELMo 使用雙向 LSTM 來學習上下文相關的詞表示：

```
The cat sat on the [bank]
           ↓
ELMo：根據上下文確定 bank 的意義（河岸）

The man sat on the [bank]
           ↓
ELMo：根據上下文確定 bank 的意義（銀行）
```

ELMo 的創新在於其「深層」雙向語言模型，能夠捕捉語義的細微差別。

## GPT：生成式預訓練

### OpenAI 的突破

2018 年 6 月，OpenAI 發布了 GPT（Generative Pre-training），這是第一個大規模生成式預訓練模型。

GPT 的核心思想：
1. **無監督預訓練**：使用語言建模目標在大規模語料上預訓練
2. **監督微調**：在特定任務上進行有監督的微調

### GPT 的架構

GPT 使用了 Transformer 的解碼器部分，這使其適合生成任務：

```
輸入：The weather is
輸出：<|endoftext|> sunny today <|endoftext|>
```

GPT 的單向性使其更適合生成式任務，但在需要雙向理解的任務上有所限制。

## 預訓練範式的確立

### 預訓練+微調模式

從 GPT 和 BERT 開始，預訓練+微調成為 NLP 的標準範式：

```
                    預訓練階段
    ┌─────────────────────────────────────┐
    │                                     │
    │  大量無標注文本  →  語言模型/掩碼語言模型  │
    │                                     │
    └─────────────────────────────────────┘
                      ↓
                    微調階段
    ┌─────────────────────────────────────┐
    │                                     │
    │  預訓練模型  →  + 任務特定標註資料  →  任務模型  │
    │                                     │
    └─────────────────────────────────────┘
```

### 這種模式的優勢

1. **遷移學習**：預訓練學到的語言知識可以遷移到下游任務
2. **資料效率**：大幅減少任務特定資料的需求
3. **通用性**：同一個預訓練模型可用於多種不同任務

## 預訓練技術的影響

### 研究影響

預訓練技術徹底改變了 NLP 研究的方式：
- 研究者可以基於預訓練模型快速實驗新想法
- 基準測試的門檻大幅提升
- 新的研究方向不斷涌現

### 應用影響

預訓練模型也深刻影響了 NLP 應用：
- 文字分類、情感分析、問答系統的效能大幅提升
- 小樣本學習和零樣本學習成為可能
- 聊天機器人、智慧助理等產品更加智慧

## 總結

預訓練革命的關鍵里程碑：

| 時間 | 模型 | 創新 |
|------|------|------|
| 2013 | Word2Vec | 詞嵌入 |
| 2018 | ELMo | 深層雙向 LSTM |
| 2018 | GPT | 生成式預訓練 |
| 2018 | BERT | 雙向 Transformer + MLM |
| 2019 | GPT-2 | 大規模生成 |

這場革命仍在持續，更強大的模型和方法正在不斷涌現。

---

**延伸閱讀**

- [Word2Vec 原始論文](https://www.google.com/search?q=Word2Vec+Mikolov+2013)
- [ELMo 論文](https://www.google.com/search?q=ELMo+Bidirectional+language+models)
- [GPT OpenAI](https://www.google.com/search?q=OpenAI+GPT+pre+training)