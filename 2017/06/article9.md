# 文章 9：注意力機制

## 前言

注意力機制（Attention Mechanism）是近年來深度學習最重要的創新之一，解決了 Seq2Seq 模型中上下文向量成為瓶頸的問題。

## 為什麼需要注意力

Seq2Seq 模型的問題：
- 所有輸入資訊被壓縮到單一上下文向量
- 輸入越長，壓縮越多，丟失資訊越多

注意力機制的解決方案：
- 讓解碼器能夠直接「看到」輸入的每個部分
- 根據當前輸出動態調整關注的輸入區域

## 注意力機制原理

```python
class Attention:
    def __init__(self, hidden_size):
        self.hidden_size = hidden_size

    def score(self, decoder_state, encoder_states):
        # 計算每個 encoder 隱藏狀態的分數
        scores = []
        for enc_state in encoder_states:
            # 簡單的dot product attention
            score = np.dot(decoder_state.flatten(), enc_state.flatten())
            scores.append(score)
        return np.array(scores)

    def forward(self, decoder_state, encoder_states):
        # 計算注意力權重
        scores = self.score(decoder_state, encoder_states)
        weights = softmax(scores)

        # 計算加權上下文
        context = np.zeros_like(encoder_states[0])
        for weight, state in zip(weights, encoder_states):
            context += weight * state

        return context, weights
```

## 注意力類型

### 1. 加性注意力（Additive Attention）

```python
# 使用前饋網路計算分數
score = np.dot(V, np.tanh(np.dot(W1, decoder_state) + np.dot(W2, encoder_state)))
```

### 2. 乘法注意力（Multiplicative Attention）

```python
# 使用矩陣乘法計算分數
score = np.dot(decoder_state.T, np.dot(W, encoder_state))
```

### 3. 縮放乘法注意力（Scaled Dot-Product Attention）

Transformer 使用的注意力：

```python
import numpy as np

def scaled_dot_product_attention(Q, K, V, mask=None):
    d_k = Q.shape[-1]

    # 計算注意力分數
    scores = np.dot(Q, K.T) / np.sqrt(d_k)

    # Mask（可選）
    if mask is not None:
        scores = scores * mask

    # Softmax
    weights = softmax(scores, axis=-1)

    # 加權
    output = np.dot(weights, V)

    return output, weights
```

## Bahdanau 注意力

雙向 LSTM 編碼器的注意力：

```python
class BahdanauAttention:
    def __init__(self, hidden_size):
        self.W1 = np.random.randn(hidden_size, hidden_size) * 0.1
        self.W2 = np.random.randn(hidden_size, hidden_size) * 0.1
        self.V = np.random.randn(1, hidden_size) * 0.1

    def forward(self, decoder_state, encoder_outputs):
        # decoder_state: (hidden_size, 1)
        # encoder_outputs: (seq_len, hidden_size)

        scores = []
        for enc_output in encoder_outputs:
            # 計算分數
            score = self.V @ np.tanh(
                self.W1 @ decoder_state + self.W2 @ enc_output
            )
            scores.append(score[0, 0])

        weights = softmax(np.array(scores))
        context = sum(w * enc for w, enc in zip(weights, encoder_outputs))

        return context, weights
```

## 自注意力（Self-Attention）

讓序列內部不同位置相互注意：

```python
class SelfAttention:
    def forward(self, x):
        # x: (seq_len, d_model)
        Q = np.dot(x, self.W_q)
        K = np.dot(x, self.W_k)
        V = np.dot(x, self.W_v)

        # Scaled dot-product attention
        scores = np.dot(Q, K.T) / np.sqrt(self.d_k)
        weights = softmax(scores, axis=-1)

        return np.dot(weights, V)
```

## 總結

注意力機制讓模型能夠動態選擇輸入的不同部分進行處理，大幅提升了序列模型的性能。Transformer 完全基於注意力機制，摒棄了 RNN 的循環結構。

## 延伸閱讀

- https://www.google.com/search?q=attention+mechanism+deep+learning+explained
- https://www.google.com/search?q=self+attention+Transformer+explained