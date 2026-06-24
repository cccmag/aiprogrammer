# RNN 在 NLP 的應用

## 文字生成、機器翻譯、問答系統

循環神經網路在自然語言處理領域有著廣泛而深入的應用。從早期的語言模型到現代的序列到序列任務，RNN 及其變體（LSTM、GRU）一直是 NLP 領域的核心技術。

本章將探討 RNN 在三個主要 NLP 任務中的應用：**文字生成、機器翻譯、問答系統**。

---

## 文字生成

### 語言模型基礎

文字生成的核心是**語言模型**——預測下一個詞的條件機率：

```
P(w_t | w_1, w_2, ..., w_{t-1})
```

RNN 語言模型的基本結構：

```
┌─────────────────────────────────────────────────────┐
│              RNN 語言模型                            │
├─────────────────────────────────────────────────────┤
│                                                     │
│   w_1 ──► Embedding ──► RNN ──► Linear ──► w_2 的機率│
│                              │                      │
│                              │                      │
│                              └──── h_{t-1} ────► h_t │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 訓練過程

```python
# RNN 語言模型的訓練
def train_lm(model, corpus, optimizer, criterion):
    model.train()
    total_loss = 0

    for batch in corpus:
        # 輸入: 前 n-1 個詞
        # 目標: 後 n-1 個詞
        input_seq = batch[:-1]
        target_seq = batch[1:]

        # 前向傳播
        logits = model(input_seq)

        # 計算損失
        loss = criterion(logits.view(-1, vocab_size), target_seq.view(-1))

        # 反向傳播
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()
```

### 文字生成策略

**1. 貪心生成（Greedy）**
```python
# 每步選擇概率最高的詞
next_word = torch.argmax(probs)
```

**2. 溫度抽樣（Temperature Sampling）**
```python
# 降低溫度使分布更尖銳，提高溫度使分布更平滑
def temperature_sample(probs, temperature=0.8):
    probs = probs ** (1/temperature)
    probs = probs / probs.sum()
    return torch.multinomial(probs, 1)
```

**3. 頂 k 抽樣（Top-k Sampling）**
```python
# 只從概率最高的 k 個詞中抽樣
def top_k_sample(probs, k=10):
    top_k_probs, top_k_indices = torch.topk(probs, k)
    top_k_probs = top_k_probs / top_k_probs.sum()
    return top_k_indices[torch.multinomial(top_k_probs, 1)]
```

**4. 核抽樣（Nucleus Sampling）**
```python
# 從累積概率超過閾值的最小詞集合中抽樣
def nucleus_sample(probs, p=0.9):
    sorted_probs, sorted_indices = torch.sort(probs, descending=True)
    cumsum = torch.cumsum(sorted_probs, dim=-1)

    # 找到閾值位置
    nucleus = sorted_indices[cumsum <= p]
    if len(nucleus) < len(sorted_probs):
        nucleus = torch.cat([nucleus, sorted_indices[cumsum > p][:1]])

    nucleus_probs = sorted_probs[cumsum <= p]
    nucleus_probs = nucleus_probs / nucleus_probs.sum()
    return nucleus[torch.multinomial(nucleus_probs, 1)]
```

### 應用場景

| 應用 | 說明 | 範例 |
|------|------|------|
| 機器翻譯 | 生成目標語言文字 | 中譯英、譯英譯法 |
| 摘要生成 | 生成簡短摘要 | 新聞摘要 |
| 對話系統 | 生成回覆 | 聊天機器人 |
| 程式碼補全 | 生成程式碼 | GitHub Copilot |
| 詩歌創作 | 創意文字生成 | 古詩、現代詩 |

---

## 機器翻譯

### 神經機器翻譯（NMT）

神經機器翻譯是 RNN 最成功的應用之一。典型的 Seq2Seq + Attention 架構：

```
┌─────────────────────────────────────────────────────┐
│          神經機器翻譯架構                            │
├─────────────────────────────────────────────────────┤
│                                                     │
│   英文輸入:  "Hello world"                         │
│              │    │    │                           │
│              ▼    ▼    ▼                           │
│           ┌─────────────────────┐                   │
│           │  BiLSTM Encoder     │                   │
│           │                     │                   │
│           │  h1  h2  h3  h4     │                   │
│           └──────────┬──────────┘                   │
│                      │                             │
│                      ▼                             │
│           ┌─────────────────────┐                   │
│           │  Attention + LSTM   │                   │
│           │     Decoder         │                   │
│           └──────────┬──────────┘                   │
│                      │                             │
│              ┌───────┴───────┐                     │
│              ▼               ▼                     │
│           "你好"          "世界"                   │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 注意力視覺化

```
翻譯: "Hello world" → "你好世界"

注意力矩陣：
       你    好    世    界
      ┌────┬────┬────┬────┐
 Hello │ ██ │    │    │    │
      ├────┼────┼────┼────┤
 world │    │    │ ██ │ ██ │
      └────┴────┴────┴────┘

「你好」主要對應「Hello」
「世界」主要對應「world」
```

### 評估指標

**BLEU（Bilingual Evaluation Understudy）**

BLEU 測量候選翻譯與參考翻譯的 n-gram 重疊度：

```python
from sacrebleu import corpus_bleu

bleu = corpus_bleu(candidate, references)
print(f"BLEU: {bleu.score}")
```

### 知名系統

| 系統 | 機構 | 特點 |
|------|------|------|
| Google Translate | Google | 2016 年從 SMT 轉向 NMT |
| DeepL | DeepL | 高品質翻譯 |
| MarianNMT | 開源 | 高效、C++ 實現 |
| Transformer NMT | 主流 | 基於注意力機制 |

---

## 問答系統

### 任務類型

問答系統有多種不同類型：

| 類型 | 輸入 | 輸出 | 示例 |
|------|------|------|------|
| 完形填空 | 段落+問題 | 答案詞 | 「拿破崙生於[?]，卒於...」|
| 抽取式 QA | 段落+問題 | 答案span | 「誰發明了 LSTM?」|
| 生成式 QA | 問題 | 自然語言回答 | 「為什麼天空是藍的?」|
| 多選題 | 問題+選項 | 正確選項 | 選擇題 |

### 抽取式問答

抽取式 QA 是 RNN 的經典應用：

```
輸入：
「LSTM 由 Sepp Hochreiter 和 Jürgen Schmidhuber 於 1997 年提出。」
問題：「LSTM 是誰提出的？」

輸出：
Answer: Sepp Hochreiter, Jürgen Schmidhuber
Start: 0, End: 24
```

### BiLSTM + Attention 模型

```python
class QAModel(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim):
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.context_lstm = nn.LSTM(embed_dim, hidden_dim, bidirectional=True)
        self.question_lstm = nn.LSTM(embed_dim, hidden_dim, bidirectional=True)
        self.attention = BiAttention(hidden_dim * 2)
        self.start_lstm = nn.LSTM(hidden_dim * 4, hidden_dim)
        self.end_lstm = nn.LSTM(hidden_dim * 4, hidden_dim)
        self.start_fc = nn.Linear(hidden_dim, 1)
        self.end_fc = nn.Linear(hidden_dim, 1)

    def forward(self, context, question):
        # 編碼問題
        q_embed = self.embedding(question)
        q_enc, _ = self.question_lstm(q_embed)

        # 編碼上下文
        c_embed = self.embedding(context)
        c_enc, _ = self.context_lstm(c_embed)

        # 注意力
        c_with_attn = self.attention(c_enc, q_enc)

        # 預測答案邊界
        start_scores = self.start_fc(start_lstm_out)
        end_scores = self.end_fc(end_lstm_out)

        return start_scores, end_scores
```

### SQuAD 數據集

SQuAD（Stanford Question Answering Dataset）是最流行的 QA 數據集之一：

```
Context: 在阿聯酋發現了一具保存完好的鯊魚化石...
Question: 鯊魚化石在哪裡被發現？
Answer: 阿聯酋

Context: 蘋果公司的 CEO 是...
Question: 蘋果公司的 CEO 是誰？
Answer: Tim Cook
```

### RoBERTa 在 QA 上的表現

2019 年，使用預訓練語言模型（如 BERT、RoBERTa）在 QA 任務上取得了突破性進展，大幅超越了之前的 RNN 模型。

---

## 實作：情感分析

情感分析是 RNN 的另一個經典應用：

```python
import torch
import torch.nn as nn

class SentimentLSTM(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim, num_layers=2):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.lstm = nn.LSTM(
            embed_dim, hidden_dim,
            num_layers=num_layers,
            bidirectional=True,
            batch_first=True,
            dropout=0.2
        )
        self.fc = nn.Linear(hidden_dim * 2, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        # x: [batch, seq_len]
        embedded = self.embedding(x)  # [batch, seq_len, embed_dim]
        lstm_out, (hidden, cell) = self.lstm(embedded)

        # 取最後一個時間步的隱藏狀態
        hidden_concat = torch.cat([hidden[-2], hidden[-1]], dim=1)

        # 分類
        out = self.fc(hidden_concat)
        return self.sigmoid(out).squeeze()
```

### 訓練結果

```
Epoch 1: Loss=0.452, Acc=78.2%
Epoch 2: Loss=0.312, Acc=85.1%
Epoch 3: Loss=0.245, Acc=88.4%
Epoch 4: Loss=0.198, Acc=90.2%
Epoch 5: Loss=0.167, Acc=91.5%

測試集準確率: 89.8%
```

---

## 總結

RNN 在 NLP 領域有著豐富的應用：

1. **文字生成**：從語言模型到創意寫作
2. **機器翻譯**：Seq2Seq + Attention 架構
3. **問答系統**：從完形填空到生成式回答

這些應用展示了 RNN 處理序列資料的強大能力。然而，隨著 Transformer 和預訓練語言模型的興起，RNN 在很多任務上已被超越。但在某些場景（如需要順序處理的即時系統），RNN 仍然是重要的選擇。

---

## 延伸閱讀

- [RNN NLP applications](https://www.google.com/search?q=RNN+NLP+applications+text+generation)
- [LSTM sentiment analysis](https://www.google.com/search?q=LSTM+sentiment+analysis+tutorial)
- [Machine translation RNN](https://www.google.com/search?q=neural+machine+translation+RNN+attention)

---

*本篇文章為「AI 程式人雜誌 2019 年 7 月號」循環神經網路系列之七。*