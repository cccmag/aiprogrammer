# RNN 與 LSTM 序列處理

## 1. 序列資料處理的挑戰

不同於影像和表格資料，序列資料的輸入長度會變化，且每個位置的輸入與前後位置有關聯。

```python
# 序列資料範例
text = ["我", "愛", "深度", "學", "習"]  # 文字
audio = [0.1, 0.3, -0.2, 0.5, ...]  # 語音信號
prices = [100, 102, 101, 105, ...]  # 股價
```

## 2. 循環神經網路（RNN）

### 基本結構

```python
class SimpleRNN:
    def __init__(self, input_size, hidden_size):
        self.hidden_size = hidden_size
        # 輸入到隱藏層
        self.W_xh = np.random.randn(input_size, hidden_size)
        # 隱藏層到隱藏層（遞迴）
        self.W_hh = np.random.randn(hidden_size, hidden_size)
        self.b_h = np.zeros(hidden_size)

    def step(self, x, h_prev):
        h_curr = np.tanh(
            np.dot(x, self.W_xh) +
            np.dot(h_prev, self.W_hh) +
            self.b_h
        )
        return h_curr
```

### Keras RNN 層

```python
from keras.layers import SimpleRNN, Embedding

model = Sequential([
    Embedding(vocab_size, 64, input_length=max_length),
    SimpleRNN(64, return_sequences=True),
    SimpleRNN(64),
    Dense(num_classes, activation='softmax')
])
```

## 3. LSTM：長短期記憶網路

### 解決梯度消失問題

```python
class LSTMCell:
    def __init__(self, input_size, hidden_size):
        self.hidden_size = hidden_size
        # 遺忘閘輸入權重
        self.W_f = np.random.randn(input_size + hidden_size, hidden_size)
        # 輸入閘輸入權重
        self.W_i = np.random.randn(input_size + hidden_size, hidden_size)
        # 輸出閘輸入權重
        self.W_o = np.random.randn(input_size + hidden_size, hidden_size)
        # 候選值輸入權重
        self.W_c = np.random.randn(input_size + hidden_size, hidden_size)

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def step(self, x, h_prev, c_prev):
        combined = np.concatenate([x, h_prev])
        
        # 遺忘閘：決定丟棄哪些資訊
        f = self.sigmoid(np.dot(combined, self.W_f))
        
        # 輸入閘：決定新增哪些資訊
        i = self.sigmoid(np.dot(combined, self.W_i))
        
        # 輸出閘：決定輸出什麼
        o = self.sigmoid(np.dot(combined, self.W_o))
        
        # 候選值
        c_tilde = np.tanh(np.dot(combined, self.W_c))
        
        # 更新細胞狀態
        c_curr = f * c_prev + i * c_tilde
        
        # 輸出隱藏狀態
        h_curr = o * np.tanh(c_curr)
        
        return h_curr, c_curr
```

### Keras LSTM 層

```python
from keras.layers import LSTM, Dense, Embedding

model = Sequential([
    Embedding(vocab_size, 128, input_length=max_length),
    LSTM(128, return_sequences=True),
    LSTM(64),
    Dense(num_classes, activation='softmax')
])
```

## 4. 雙向 LSTM

```python
from keras.layers import Bidirectional

model = Sequential([
    Embedding(vocab_size, 128),
    Bidirectional(LSTM(64)),
    Dense(num_classes, activation='softmax')
])
```

## 5. 序列到序列模型

```python
# Encoder-Decoder 結構
encoder_inputs = Input(shape=(max_length,))
x = Embedding(vocab_size, 128)(encoder_inputs)
encoder_outputs, state_h, state_c = LSTM(128, return_state=True)(x)

decoder_inputs = Input(shape=(max_length,))
x = Embedding(vocab_size, 128)(decoder_inputs)
decoder_outputs = LSTM(128, return_sequences=True)(
    x, initial_state=[state_h, state_c]
)
decoder_outputs = TimeDistributed(Dense(vocab_size, activation='softmax'))(decoder_outputs)

model = Model([encoder_inputs, decoder_inputs], decoder_outputs)
```

## 6. 小結

RNN 通過遞迴連接處理序列資料，但原始 RNN 有梯度消失問題。LSTM/GRU 通过門控機制解決了這個問題，成為序列建模的主流選擇。

---

**參考資料**
- [LSTM Paper](https://www.google.com/search?q=LSTM+long+short+term+memory+paper)
- [Sequence Models in Keras](https://www.google.com/search?q=Keras+LSTM+sequence+model+tutorial)