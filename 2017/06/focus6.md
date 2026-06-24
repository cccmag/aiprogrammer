# 焦點文章 6：雙向 RNN 與深度 RNN

## 前言

標準 RNN 只有單向資訊流，但很多任務需要同時考慮過去與未來的上下文。本章節介紹雙向 RNN 與深度 RNN 的設計。

## 雙向 RNN（Bidirectional RNN）

### 思想

雙向 RNN 同時訓練兩個方向的 RNN：
- **正向 RNN**：從左到右處理序列
- **反向 RNN**：從右到左處理序列

最終輸出結合兩個方向的隱藏狀態：

```python
class BidirectionalRNN:
    def __init__(self, cell_class, input_size, hidden_size):
        self.forward_rnn = RNNCell(cell_class, input_size, hidden_size)
        self.backward_rnn = RNNCell(cell_class, input_size, hidden_size)

    def forward(self, x):
        # 正向
        h_forward = []
        h_f = np.zeros((self.hidden_size, 1))
        for t in range(len(x)):
            h_f = self.forward_rnn.forward(x[t], h_f)
            h_forward.append(h_f)

        # 反向
        h_backward = []
        h_b = np.zeros((self.hidden_size, 1))
        for t in reversed(range(len(x))):
            h_b = self.backward_rnn.forward(x[t], h_b)
            h_backward.append(h_b)

        # 拼接
        outputs = [np.concatenate([h_forward[t], h_backward[t]], axis=0)
                   for t in range(len(x))]

        return outputs
```

### 應用場景

雙向 RNN 適用於需要完整上下文的任務：

| 任務 | 說明 |
|------|------|
| 命名實體識別 | 需要知道上下文才能確定類別 |
| 語音辨識 | 需要知道前後音頻幀 |
| 機器翻譯 | 需要完整的源語言語句 |

### 限制

- 需要完整序列才能預測（不能用於即時語音辨識）
- 不適用於語言模型（只能看到過去）

## 深度 RNN（Deep RNN）

### 思想

堆疊多層 RNN，增加網路的表達能力：

```python
class DeepRNN:
    def __init__(self, num_layers, cell_class, input_size, hidden_size):
        self.num_layers = num_layers
        self.layers = [
            RNNCell(cell_class, input_size if i == 0 else hidden_size, hidden_size)
            for i in range(num_layers)
        ]

    def forward(self, x):
        h = [np.zeros((layer.hidden_size, 1)) for layer in self.layers]

        for t in range(len(x)):
            h[0] = self.layers[0].forward(x[t], h[0])
            for i in range(1, self.num_layers):
                h[i] = self.layers[i].forward(h[i-1], h[i])

        return h[-1]
```

### 為什麼需要多層

| 層數 | 功能 |
|------|------|
| 第一層 | 學習低層特徵（音素、字母） |
| 第二層 | 學習更高層特徵（詞素、詞） |
| 第三層 | 學習語義表示 |

通常 2-4 層就能獲得良好的性能。

## 訓練技巧

### 1. 梯度裁剪

```python
def clip_gradients(gradients, max_norm=5.0):
    total_norm = np.sqrt(sum(np.sum(g**2) for g in gradients))
    clip_coef = max_norm / (total_norm + 1e-6)
    return [g * clip_coef if clip_coef < 1 else g for g in gradients]
```

### 2. 批次正規化

```python
# Layer Normalization
def layer_norm(x, gain, bias):
    mean = np.mean(x, axis=-1, keepdims=True)
    std = np.std(x, axis=-1, keepdims=True)
    return gain * (x - mean) / (std + 1e-6) + bias
```

### 3. Dropout

```python
def dropout(x, p=0.5, training=True):
    if training:
        mask = (np.random.rand(*x.shape) > p) / (1 - p)
        return x * mask
    return x
```

## 總結

雙向 RNN 透過結合前後上下文提升性能，深度 RNN 透過層級結構增加表達能力。這些技術大幅增強了 RNN 的能力。

## 延伸閱讀

- https://www.google.com/search?q=bidirectional+RNN+deep+RNN+explained
- https://www.google.com/search?q=stacked+recurrent+neural+networks