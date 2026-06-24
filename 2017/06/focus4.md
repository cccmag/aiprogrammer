# 焦點文章 4：LSTM：長短期記憶網路

## 前言

LSTM（Long Short-Term Memory）是為了解決標準 RNN 的長期依賴問題而設計的。本章節詳細介紹 LSTM 的結構與原理。

## 長期依賴問題

標準 RNN 難以學習長期依賴：

```
短期依賴：the cat sat on the mat → 容易學習
長期依賴：I grew up in France... I speak fluent French → 難以學習
```

原因：梯度在反向傳播時指数衰減。

## LSTM 的核心思想

LSTM 引入「記憶細胞」（Memory Cell）與「門控」（Gate）機制：

- **記憶細胞**：長時間儲存資訊
- **門控**：控制資訊的流動

## LSTM 結構

### 三個門

1. **遺忘門（Forget Gate）**：決定丟棄哪些資訊
2. **輸入門（Input Gate）**：決定保存哪些新資訊
3. **輸出門（Output Gate）**：決定輸出什麼

### 記憶細胞更新

```
f_t = σ(W_f · [h_{t-1}, x_t] + b_f)       # 遺忘門
i_t = σ(W_i · [h_{t-1}, x_t] + b_i)       # 輸入門
C̃_t = tanh(W_C · [h_{t-1}, x_t] + b_C)   # 候選值
C_t = f_t × C_{t-1} + i_t × C̃_t           # 新記憶細胞
o_t = σ(W_o · [h_{t-1}, x_t] + b_o)       # 輸出門
h_t = o_t × tanh(C_t)                       # 隱藏狀態
```

## Python 實現

```python
class LSTMCell:
    def __init__(self, input_size, hidden_size):
        self.hidden_size = hidden_size

        # 權重矩陣
        self.Wf = np.random.randn(hidden_size, input_size + hidden_size) * 0.1
        self.Wi = np.random.randn(hidden_size, input_size + hidden_size) * 0.1
        self.Wc = np.random.randn(hidden_size, input_size + hidden_size) * 0.1
        self.Wo = np.random.randn(hidden_size, input_size + hidden_size) * 0.1

        # 偏置
        self.bf = np.zeros((hidden_size, 1))
        self.bi = np.zeros((hidden_size, 1))
        self.bc = np.zeros((hidden_size, 1))
        self.bo = np.zeros((hidden_size, 1))

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def forward(self, x_t, h_prev, C_prev):
        self.x_t = x_t
        self.h_prev = h_prev
        self.C_prev = C_prev

        concat = np.vstack((h_prev, x_t))

        # 遺忘門
        self.f_t = self.sigmoid(np.dot(self.Wf, concat) + self.bf)

        # 輸入門
        self.i_t = self.sigmoid(np.dot(self.Wi, concat) + self.bi)

        # 候選值
        self.C̃_t = np.tanh(np.dot(self.Wc, concat) + self.bc)

        # 更新記憶細胞
        self.C_t = self.f_t * C_prev + self.i_t * self.C̃_t

        # 輸出門
        self.o_t = self.sigmoid(np.dot(self.Wo, concat) + self.bo)

        # 隱藏狀態
        self.h_t = self.o_t * np.tanh(self.C_t)

        return self.h_t, self.C_t
```

## 為什麼 LSTM 有效

### 梯度傳播路徑

LSTM 的記憶通道允許梯度直接流動：

```
∂C_t / ∂C_{t-1} = f_t
```

遺忘門 f_t 接近 1 時，梯度可以無衰減地傳播。

### 門控機制

網路可以學習何時遺忘、何時記憶：

- f_t → 0：完全遺忘過去
- f_t → 1：完全保留過去
- i_t → 0：不記憶新輸入
- i_t → 1：完全記憶新輸入

## LSTM 變體

### 窺視孔連接（Peephole Connections）

允許門查看記憶細胞：

```python
self.f_t = σ(W_f · [C_{t-1}, h_{t-1}, x_t] + b_f)
```

## 總結

LSTM 是目前最成功的序列模型之一。其記憶細胞與門控機制使網路能夠學習長期依賴，解決了標準 RNN 的核心問題。

## 延伸閱讀

- https://www.google.com/search?q=LSTM+long+short+term+memory+explained
- https://www.google.com/search?q=LSTM+forget+input+output+gate