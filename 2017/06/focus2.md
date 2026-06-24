# 焦點文章 2：RNN 的結構與前向傳播

## 前言

理解 RNN 的前向傳播是掌握其運作原理的基礎。本章節詳細解說 RNN 的網路結構與前向傳播計算。

## RNN 單元結構

RNN 的基本單元包含：
- **輸入門**：接收當前輸入 x_t
- **隱藏狀態**：儲存「記憶」h_t
- **輸出門**：產生輸出 o_t

```python
class SimpleRNNCell:
    def __init__(self, input_size, hidden_size):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.W = np.random.randn(hidden_size, input_size) * 0.1
        self.U = np.random.randn(hidden_size, hidden_size) * 0.1
        self.b = np.zeros((hidden_size, 1))

    def forward(self, x_t, h_prev):
        self.h_prev = h_prev
        self.x_t = x_t

        # 計算新的隱藏狀態
        self.h_t = np.tanh(np.dot(self.W, x_t) + np.dot(self.U, h_prev) + self.b)

        return self.h_t
```

## 前向傳播公式

對於每個時間步 t：

```
a_t = W_xh × x_t + W_hh × h_{t-1} + b_h
h_t = tanh(a_t)
o_t = W_hy × h_t + b_y
```

其中：
- x_t: 時刻 t 的輸入
- h_{t-1}: 上一時刻的隱藏狀態
- h_t: 當前隱藏狀態
- o_t: 當前輸出

## 完整前向傳播

```python
def forward(self, X):
    """
    X: (seq_length, input_size, batch_size)
    """
    seq_length = X.shape[0]
    batch_size = X.shape[2]

    self.hidden_states = []
    h_t = np.zeros((self.hidden_size, batch_size))

    for t in range(seq_length):
        h_t = self.rnn_cell.forward(X[t], h_t)
        self.hidden_states.append(h_t)

    return h_t  # 返回最後一個隱藏狀態
```

## 損失函數

根據任務選擇損失函數：

### 序列分類
```python
loss = cross_entropy(output, target)
```

### 序列生成
```python
loss = cross_entropy(output, target)  # 每個時間步預測下一個詞
```

### 序列到序列
```python
loss = sum(cross_entropy(output_t, target_t) for t in range(seq_length))
```

## 輸出層設計

### 多類分類（Softmax）

```python
def softmax(x):
    exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return exp_x / np.sum(exp_x, axis=-1, keepdims=True)

y_t = softmax(V @ h_t + c)
```

### 時間序列迴歸

```python
o_t = V @ h_t + c  # 線性輸出
```

## 實際範例：語言模型

```python
class LanguageModel:
    def __init__(self, vocab_size, embed_size, hidden_size):
        self.embedding = Embedding(vocab_size, embed_size)
        self.rnn = SimpleRNN(embed_size, hidden_size)
        self.output = Dense(hidden_size, vocab_size)

    def forward(self, x):
        # x: (seq_length, batch_size)
        embedded = self.embedding(x)  # (seq_length, embed_size, batch_size)
        hidden = self.rnn.forward(embedded)
        output = self.output(hidden)
        return output
```

## 總結

RNN 的前向傳播在每個時間步結合當前輸入與前一隱藏狀態，計算新的隱藏狀態。這種遞迴結構使 RNN 能夠處理任意長度的序列。

## 延伸閱讀

- https://www.google.com/search?q=RNN+forward+propagation+explained
- https://www.google.com/search?q=hidden+state+recurrent+neural+network