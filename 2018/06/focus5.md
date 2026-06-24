# GPT 模型的誕生：生成式預訓練的突破

## 前言

2018 年 6 月，OpenAI 發布了「Improving Language Understanding by Generative Pre-Training」論文，介紹了 GPT（Generative Pre-Training）模型。這是預訓練語言模型時代的重要里程碑！

## GPT 論文核心資訊

- **標題**：Improving Language Understanding by Generative Pre-Training
- **作者**：Alec Radford, Karthik Narasimhan, Tim Salimans, Ilya Sutskever
- **發布時間**：2018 年 6 月
- **機構**：OpenAI
- **模型規模**：117M 參數

## GPT 的核心創新

### 1. 無監督預訓練

在大規模文字資料上預訓練一個語言模型，無需人工標注。

### 2. Transformer 解碼器架構

GPT 使用 Transformer 的解碼器部分（只使用 mask self-attention）。

### 3. 監督式微調

在特定任務上微調預訓練模型。

```
┌─────────────────────────────────────────────────────┐
│              GPT 的預訓練 + 微調流程                 │
├─────────────────────────────────────────────────────┤
│                                                     │
│  階段 1：無監督預訓練                                 │
│  ┌────────────────────────────────────┐           │
│  │ BooksCorpus (8B 詞)                 │           │
│  │           ▼                         │           │
│  │     12 層 Transformer 解碼器        │           │
│  │           ▼                         │           │
│  │   生成式語言模型目標                │           │
│  │   (預測下一個詞)                    │           │
│  └────────────────────────────────────┘           │
│               │                                    │
│               ▼                                    │
│  階段 2：監督式微調                                   │
│  ┌────────────────────────────────────┐           │
│  │   特定任務標註資料                  │           │
│  │   (分類、蘊涵、問答等)              │           │
│  │           ▼                         │           │
│  │   添加線性輸出層                   │           │
│  │           ▼                         │           │
│  │   聯合訓練語言模型目標              │           │
│  │   + 任務目標                       │           │
│  └────────────────────────────────────┘           │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## GPT 的架構

### Transformer 解碼器

GPT 使用了 12 層 Transformer 解碼器：
- 隱藏層維度：768
- 注意力頭數：12
- 總參數：117M

### 關鍵技術

1. **Masked Self-Attention**：每個位置只能看到之前的詞
2. **Position-wise FFN**：前饋網路
3. **Layer Norm**：層標準化

## GPT 的應用

### 為多種任務微調

GPT 在多個 NLP 任務上取得領先：
- 文字分類
- 蘊涵判断
- 問答系統
- 語意相似度

### 零樣本學習

預訓練語言模型已經學習到了語言的一般知識，無需微調即可執行某些任務。

## GPT 與之前工作的區別

| 特性 | 之前方法 | GPT |
|------|----------|-----|
| 預訓練 | 無或有限 | 大規模無監督預訓練 |
| 微調 | 需要大量標注 | 只需少量微調 |
| 架構 | CNN/RNN | Transformer |
| 遷移學習 | 較弱 | 強 |

## 為什麼 GPT 重要？

1. **開創預訓練範式**：預訓練 + 微調成為 NLP 的標準流程
2. **驗證Transformer能力**：證明 Transformer 可以學習通用語言表示
3. **推動後續研究**：啟發了 BERT (2018年10月) 等後續工作

## GPT 的局限性

1. **單向性**：只能看到之前的上下文（masked）
2. **規模限制**：117M 參數，相對較小
3. **計算成本**：預訓練需要大量計算資源

## 結語

GPT 的發布標誌著預訓練語言模型時代的開始。雖然此時的規模不大，但這條路線在之後的幾年裡發展迅速，催生了 GPT-2、BERT 等重要模型。

---

**延伸閱讀**

- [GPT 原始論文](https://www.google.com/search?q=Improving+Language+Understanding+by+Generative+Pre-Training+2018)
- [OpenAI 官方網站](https://www.google.com/search?q=OpenAI+official+site)
- [Transformer 架構](https://www.google.com/search?q=Transformer+Attention+is+All+You+Need+2017)

---

*本篇文章為「AI 程式人雜誌 2018 年 6 月號」GPT 與生成式 AI 系列之一。*