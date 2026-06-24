# 焦點文章 7：RNN 應用與實作

## 前言

RNN 廣泛應用於自然語言處理與語音辨識。本章節展示如何使用 Python 實作簡單的 RNN 應用。

## 文字分類

使用 LSTM 進行情感分類：

```python
import numpy as np

class TextClassifier:
    def __init__(self, vocab_size, embed_size, hidden_size, num_classes):
        self.embedding = Embedding(vocab_size, embed_size)
        self.lstm = LSTMCell(embed_size, hidden_size)
        self.output = Dense(hidden_size, num_classes)

    def forward(self, x):
        # x: (seq_length,)  word indices
        embedded = self.embedding(x)
        h, C = np.zeros((hidden_size, 1)), np.zeros((hidden_size, 1))

        for t in range(len(x)):
            h, C = self.lstm.forward(embedded[t], h, C)

        logits = self.output(h)
        return softmax(logits)
```

## 語言模型

預測下一個詞：

```python
class LanguageModel:
    def __init__(self, vocab_size, embed_size, hidden_size):
        self.embedding = Embedding(vocab_size, embed_size)
        self.lstm = LSTMCell(embed_size, hidden_size)
        self.output = Dense(hidden_size, vocab_size)

    def forward(self, x):
        # x: (seq_length,) word indices
        embedded = self.embedding(x)
        h, C = np.zeros((hidden_size, 1)), np.zeros((hidden_size, 1))

        for t in range(len(x)):
            h, C = self.lstm.forward(embedded[t], h, C)

        logits = self.output(h)
        return logits

    def sample(self, seed, length):
        # 從語言模型取樣
        h, C = np.zeros((hidden_size, 1)), np.zeros((hidden_size, 1))
        result = [seed]

        for _ in range(length):
            embedded = self.embedding(np.array([result[-1]]))
            h, C = self.lstm.forward(embedded[0], h, C)
            logits = self.output(h).flatten()
            probs = softmax(logits)
            next_word = np.random.choice(len(probs), p=probs)
            result.append(next_word)

        return result
```

## 使用 Keras 實作

```python
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense

model = Sequential([
    Embedding(vocab_size, embed_size, input_length=max_length),
    LSTM(hidden_size, return_sequences=False),
    Dense(num_classes, activation='softmax')
])

model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])
```

## 序列到序列模型

機器翻譯：

```python
class Seq2Seq:
    def __init__(self, src_vocab, tgt_vocab, embed_size, hidden_size):
        self.encoder = Encoder(src_vocab, embed_size, hidden_size)
        self.decoder = Decoder(tgt_vocab, embed_size, hidden_size)

    def forward(self, src, tgt):
        # 編碼
        context = self.encoder.forward(src)

        # 解碼
        outputs = []
        h, C = context[-1], np.zeros_like(context[-1])

        for t in range(len(tgt)):
            h, C, prob = self.decoder.forward(tgt[t], h, C, context)
            outputs.append(prob)

        return outputs
```

## 文字生成範例

```python
# 訓練資料
text = "The quick brown fox jumps over the lazy dog"
chars = list(set(text))
char_to_idx = {c: i for i, c in enumerate(chars)}
idx_to_char = {i: c for c, i in char_to_idx.items()}

# 訓練模型
model = LanguageModel(vocab_size=len(chars), embed_size=16, hidden_size=64)
train(model, text, epochs=100)

# 生成文字
seed_idx = char_to_idx['T']
generated = model.sample(seed_idx, length=50)
generated_text = ''.join([idx_to_char[i] for i in generated])
print(generated_text)
```

## Attention 機制

增强序列到序列模型的性能：

```python
class Attention:
    def __init__(self, hidden_size):
        self.W = np.random.randn(hidden_size, hidden_size) * 0.1

    def forward(self, decoder_h, encoder_outputs):
        # 計算注意力權重
        scores = [np.dot(decoder_h.T, np.dot(self.W, enc_h))
                  for enc_h in encoder_outputs]
        attn_weights = softmax(np.array(scores))

        # 加權總和
        context = sum(w * enc for w, enc in zip(attn_weights, encoder_outputs))
        return context, attn_weights
```

## 總結

RNN 的應用涵蓋文字分類、語言模型、機器翻譯等多個領域。Keras 等高階API大幅簡化了 RNN 的實作。

## 延伸閱讀

- https://www.google.com/search?q=RNN+text+classification+implementation
- https://www.google.com/search?q=LSTM+language+model+Python