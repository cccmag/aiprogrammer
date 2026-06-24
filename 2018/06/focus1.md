# 語言模型概述：什麼是語言模型？

## 前言

語言模型（Language Model, LM）是 NLP 領域的基礎任務之一。它預測一個句子出現的機率，或者給定前文預測下一個詞。

## 語言模型的定義

### 機率語言模型

給定一個詞序列，語言模型計算這個序列出現的機率：

```
P(w_1, w_2, ..., w_n) = P(w_1) × P(w_2|w_1) × ... × P(w_n|w_1, ..., w_{n-1})
```

### 條件機率預測

給定前文，預測下一個詞：

```
P(next_word | context)
```

## 評估指標

### 困惑度（Perplexity）

最常用的語言模型評估指標：

```
PP(W) = P(w_1, ..., w_N)^(-1/N)
```

較低的困惑度表示更好的語言模型。

### 交叉熵

```
H = -(1/N) × Σ log_2 P(w_i | w_1, ..., w_{i-1})
```

困惑度 = 2^H

## 應用場景

1. **機器翻譯**：評估譯文的流暢度
2. **語音辨識**：選擇最可能的文字序列
3. **文字生成**：給定開頭生成續寫
4. **拼寫糾錯**：識別不符合語言習慣的用詞

## 語言模型的歷史

```
1950s ── N-gram 模型
    │
    │  基於計數的統計方法
    │  马可夫假設
    │
2000s ── 類神經網路語言模型
    │
    │  NNLM (Bengio, 2003)
    │  RNN 語言模型
    │
2013 ── 詞嵌入時代
    │
    │  word2vec, GloVe
    │
2015 ── 注意力機制
    │
    │  seq2seq + attention
    │
2017 ── Transformer
    │
    │  Attention is All You Need
    │
2018 ── GPT ★ (本期主題)
    │
      生成式預訓練時代開始
```

## 結語

語言模型是 NLP 的核心問題。從統計方法到深度學習，語言模型的能力持續提升。GPT 的發布開創了預訓練語言模型的新時代。

---

**延伸閱讀**

- [語言模型基礎](https://www.google.com/search?q=language+model+tutorial)
- [GPT 論文：Improving Language Understanding by Generative Pre-Training](https://www.google.com/search?q=Improving+Language+Understanding+by+Generative+Pre-Training+2018)

---

*本篇文章為「AI 程式人雜誌 2018 年 6 月號」GPT 與生成式 AI 系列之一。*