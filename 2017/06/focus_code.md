# 程式碼範例：RNN 與 LSTM 實作

## 程式碼說明

本目錄包含循環神經網路的基本實現，包括簡單 RNN、LSTM 和 GRU 單元。

## 檔案清單

- `rnn.py` - RNN/LSTM/GRU 實現
- `test.sh` - 測試腳本

## 簡單 RNN 實現

```python
class SimpleRNNCell:
    def __init__(self, input_size, hidden_size):
        self.Wx = np.random.randn(hidden_size, input_size) * 0.1
        self.Wh = np.random.randn(hidden_size, hidden_size) * 0.1
        self.b = np.zeros((hidden_size, 1))

    def forward(self, x, h_prev):
        self.x = x
        self.h_prev = h_prev
        self.h = np.tanh(np.dot(self.Wx, x) + np.dot(self.Wh, h_prev) + self.b)
        return self.h
```

## LSTM 實現

```python
class LSTMCell:
    def __init__(self, input_size, hidden_size):
        self.Wf = np.random.randn(hidden_size, input_size + hidden_size) * 0.1
        self.Wi = np.random.randn(hidden_size, input_size + hidden_size) * 0.1
        self.Wc = np.random.randn(hidden_size, input_size + hidden_size) * 0.1
        self.Wo = np.random.randn(hidden_size, input_size + hidden_size) * 0.1

    def forward(self, x, h_prev, C_prev):
        concat = np.vstack((h_prev, x))

        self.f = sigmoid(np.dot(self.Wf, concat))
        self.i = sigmoid(np.dot(self.Wi, concat))
        self.C_tilde = tanh(np.dot(self.Wc, concat))
        self.C = self.f * C_prev + self.i * self.C_tilde
        self.o = sigmoid(np.dot(self.Wo, concat))
        self.h = self.o * tanh(self.C)

        return self.h, self.C
```

## GRU 實現

```python
class GRUCell:
    def __init__(self, input_size, hidden_size):
        self.Wz = np.random.randn(hidden_size, input_size + hidden_size) * 0.1
        self.Wr = np.random.randn(hidden_size, input_size + hidden_size) * 0.1
        self.Wh = np.random.randn(hidden_size, input_size + hidden_size) * 0.1

    def forward(self, x, h_prev):
        concat = np.vstack((h_prev, x))

        self.z = sigmoid(np.dot(self.Wz, concat))
        self.r = sigmoid(np.dot(self.Wr, concat))

        concat_r = np.vstack((self.r * h_prev, x))
        self.h_tilde = tanh(np.dot(self.Wh, concat_r))

        self.h = (1 - self.z) * h_prev + self.z * self.h_tilde
        return self.h
```

## 使用方式

```bash
python3 rnn.py
```

## 測試內容

腳本會測試：
- RNN 前向傳播
- LSTM 前向傳播
- GRU 前向傳播
- 序列處理

## 延伸學習

- 實現反向傳播
- 添加偏置項
- 實現多層 RNN
- 實現雙向 RNN