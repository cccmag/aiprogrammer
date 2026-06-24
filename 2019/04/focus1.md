# 自然語言處理概述

## NLP 的發展歷程

自然語言處理（Natural Language Processing，NLP）是電腦科學與人工智慧的交叉領域，致力於讓電腦夠理解、解釋和生成人類語言。

---

##  NLP 的發展歷程

### 早期階段（1950s-1980s）

NLP 的歷史可以追溯到 1950 年代，當時的研究者嘗試使用規則系統來處理語言：

- **1950s**：圖靈測試提出，探討機器是否能「思考」
- **1960s**：ELIZA 等早期對話系統誕生
- **1970s-1980s**：專家系統和句法分析為主流

### 統計學習時代（1990s-2012）

1990 年代，隨著電腦效能提升和大量文字資料可用，統計方法開始主導 NLP：

```
規則系統 → 統計學習
手動特徵 → 自動學習特徵
```

關鍵技術：
- 隱馬爾可夫模型（HMM）
- 條件隨機場（CRF）
- N-gram 語言模型
- SVM 文字分類

### 深度學習時代（2013-現在）

2013 年 Word2Vec 的發表開啟了 NLP 的深度學習時代：

| 年份 | 里程碑 |
|-----|--------|
| 2013 | Word2Vec 詞嵌入技術實用化 |
| 2014 | Sequence-to-Sequence 模型 |
| 2015 | Attention 機制提出 |
| 2017 | Transformer 架構 |
| 2018 | BERT 預訓練模型 |

---

## 基本任務與挑戰

### NLP 主要任務

```
┌─────────────────────────────────────────┐
│              NLP 任務分類               │
├─────────────────────────────────────────┤
│                                         │
│  文字分類  ──────► 情感分析、垃圾郵件偵測 │
│                                         │
│  序列標註  ──────► 命名實體識別、詞性標註 │
│                                         │
│  序列到序列  ────► 機器翻譯、摘要生成    │
│                                         │
│  問答系統  ──────► 閱讀理解對話系統     │
│                                         │
└─────────────────────────────────────────┘
```

### 核心挑戰

**歧義性（Ambiguity）**

自然語言充滿歧義：

```
「他的蘋果」可能是：
- 水果蘋果
- Apple 公司的產品
- 別人的蘋果（一種攻擊）

「打」可以搭配：
- 打電話、打球、打橋牌
- 打毛衣、打工、打仗
```

**上下文依賴**

詞的意義往往依賴上下文：

```
「銀行」在以下句子中有不同含義：
- 我去銀行存款（金融機構）
- 河岸的銀行（河岸）
```

**組合語意學**

句子整體意義不等於單詞意義的簡單組合，需要理解語法結構和語用原則。

---

## 傳統方法與深度學習

### 傳統方法

**Bag of Words（詞袋模型）**

```python
from collections import Counter

def bow(sentence, vocab):
    vector = [0] * len(vocab)
    for word in sentence:
        if word in vocab:
            vector[vocab[word]] += 1
    return vector
```

優點：簡單、解釋性強
缺點：忽略詞序、語意稀疏

**TF-IDF**

```python
import math

def tf_idf(word, document, corpus):
    tf = document.count(word) / len(document)
    idf = math.log(len(corpus) / sum(1 for doc in corpus if word in doc))
    return tf * idf
```

### 深度學習方法

**詞嵌入**

```python
# 詞嵌入將詞映射到稠密向量
word -> embedding -> dense vector
```

優點：捕捉語意關係、維度低、可學習

**卷積神經網路（CNN）**

```python
# 文字分類 CNN
embedding -> Conv1D -> MaxPool -> Dense -> output
```

**循環神經網路（RNN）**

```python
# 序列處理 RNN
x1 -> [RNN] -> h1
x2 -> [RNN] -> h2
x3 -> [RNN] -> h3
```

**Transformer**

```python
# 自注意力機制
self_attention = softmax(QK^T / sqrt(d_k)) V
```

---

## 為什麼 NLP 困難？

### 語言的複雜性

1. **符號系統**：人類語言是離散的符號系統
2. **結構依賴**：句子結構決定語意
3. **世界知識**：理解語言需要背景知識
4. **推理能力**：有時需要邏輯推理

### 資料的挑戰

- **多語言**：超過 7000 種語言
- **領域差異**：新聞、醫學、法律用語各異
- **噪聲**：拼寫錯誤、網路用語

### 評估的困難

語言生成難以自動評估，往往需要人為主觀判斷。

---

## 現代 NLP 的發展方向

### 預訓練語言模型

從 Word2Vec 到 BERT，預訓練+微調已成為標準流程：

```
預訓練（大規模無標籤資料）
    ↓
微調（特定任務少量標籤資料）
    ↓
應用
```

### 多任務學習

單一模型學習多種 NLP 任務，如 T5、GPT 系列。

### 低資源學習

面對缺乏標註資料的語言和領域，遷移學習和少樣本學習變得重要。

---

## 延伸閱讀

- [NLP 發展歷史](https://www.google.com/search?q=history+of+natural+language+processing)
- [Word2Vec 原始論文](https://www.google.com/search?q=Mikolov+Word2Vec+2013)
- [BERT 論文解讀](https://www.google.com/search?q=BERT+language+model+paper)

---

*本篇文章為「AI 程式人雜誌 2019 年 4 月號」系列文章之一。*