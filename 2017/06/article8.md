# 文章 8：序列到序列模型

## 前言

序列到序列（Seq2Seq）模型是處理序列轉換任務的核心架構，廣泛應用於機器翻譯、對話系統等。

## 序列到序列架構

```
輸入序列 → [編碼器] → 上下文向量 → [解碼器] → 輸出序列
```

### 編碼器（Encoder）

處理輸入序列，產生上下文向量：

```python
class Encoder:
    def __init__(self, vocab_size, embed_size, hidden_size):
        self.embedding = Embedding(vocab_size, embed_size)
        self.lstm = LSTMCell(embed_size, hidden_size)

    def forward(self, source):
        # source: (seq_length,) word indices
        embeddings = self.embedding(source)
        h, C = np.zeros((hidden_size, 1)), np.zeros((hidden_size, 1))

        for t in range(len(source)):
            h, C = self.lstm.forward(embeddings[t], h, C)

        return h, C
```

### 解碼器（Decoder）

根據上下文向量生成輸出序列：

```python
class Decoder:
    def __init__(self, vocab_size, embed_size, hidden_size):
        self.embedding = Embedding(vocab_size, embed_size)
        self.lstm = LSTMCell(embed_size, hidden_size)
        self.output = Dense(hidden_size, vocab_size)

    def forward(self, target, context):
        # target: (seq_length,) word indices
        h, C = context[0], context[1]
        outputs = []

        for t in range(len(target)):
            h, C = self.lstm.forward(self.embedding(target[t]), h, C)
            logits = self.output(h)
            outputs.append(logits)

        return outputs
```

## 注意力機制

讓解碼器能夠「關注」輸入的不同部分：

```python
class Attention:
    def __init__(self, hidden_size):
        self.W = np.random.randn(hidden_size, hidden_size) * 0.1

    def forward(self, decoder_state, encoder_states):
        # encoder_states: list of hidden states
        scores = []
        for enc_state in encoder_states:
            score = np.dot(decoder_state.T, np.dot(self.W, enc_state))
            scores.append(score)

        # Softmax 歸一化
        scores = np.array(scores)
        weights = softmax(scores)

        # 加權上下文
        context = sum(w * enc for w, enc in zip(weights, encoder_states))
        return context, weights
```

## 訓練策略

### Teacher Forcing

在訓練時使用真實標籤而非上一個預測：

```python
def train_step(source, target, encoder, decoder, loss_fn):
    # 編碼
    context = encoder.forward(source)

    # 解碼（使用 teacher forcing）
    h, C = context[0], context[1]
    loss = 0

    for t in range(len(target)):
        # 使用真實目標而非預測
        h, C = decoder.lstm.forward(decoder.embedding(target[t]), h, C)
        logits = decoder.output(h)
        loss += loss_fn(logits, target[t])

    # 反向傳播
    loss.backward()
    optimizer.step()
    return loss
```

## 應用場景

| 應用 | 輸入 | 輸出 |
|------|------|------|
| 機器翻譯 | 中文句子 | 英文句子 |
| 文字摘要 | 長文章 | 短摘要 |
| 對話系統 | 用戶輸入 | 回覆 |
| 語音辨識 | 語音特徵 | 文字 |

## 挑戰與改進

- **上下文向量瓶頸**：使用注意力機制緩解
- **訓練不穩定**：使用梯度裁剪與正規化
- **推斷速度慢**：使用束搜索（Beam Search）

## 總結

Seq2Seq 是處理序列轉換的經典架構。編碼器-解碼器結構結合注意力機制，能處理各种序列轉換任務。

## 延伸閱讀

- https://www.google.com/search?q=seq2seq+encoder+decoder+attention
- https://www.google.com/search?q=sequence+to+sequence+model+machine+translation