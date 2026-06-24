# 文章 10：RNN 應用案例

## 前言

RNN 及其變體（LSTM、GRU）在各個領域都有廣泛應用。本章節列舉幾個典型的應用案例。

## 1. 機器翻譯

Seq2Seq + Attention 架構：

```python
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, LSTM, Dense, Attention

# 編碼器
encoder_inputs = Input(shape=(max_encoder_len, embedding_dim))
encoder_lstm = LSTM(hidden_dim, return_sequences=True, return_state=True)
encoder_outputs, state_h, state_c = encoder_lstm(encoder_inputs)

# 解碼器
decoder_inputs = Input(shape=(max_decoder_len, embedding_dim))
decoder_lstm = LSTM(hidden_dim, return_sequences=True, return_sequences=True)
decoder_outputs = decoder_lstm(decoder_inputs, initial_state=[state_h, state_c])

# 輸出
dense = Dense(vocab_size, activation='softmax')
outputs = dense(decoder_outputs)
```

## 2. 文字生成

```python
# 使用 LSTM 生成文字
model = Sequential([
    Embedding(vocab_size, embed_size, input_length=seq_length),
    LSTM(128, return_sequences=True),
    Dropout(0.3),
    LSTM(128),
    Dense(vocab_size, activation='softmax')
])

model.compile(loss='categorical_crossentropy', optimizer='adam')
```

## 3. 情感分析

```python
# 使用雙向 LSTM
model = Sequential([
    Embedding(vocab_size, embed_size, input_length=max_length),
    Bidirectional(LSTM(64)),
    Dense(64, activation='relu'),
    Dropout(0.5),
    Dense(1, activation='sigmoid')
])

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
```

## 4. 語音辨識

```python
# 音頻 → 文字
model = Sequential([
    LSTM(128, input_shape=(time_steps, mfcc_features)),
    LSTM(128),
    Dense(vocab_size, activation='softmax')
])
```

## 5. 影片分類

```python
# 對每幀使用 CNN + RNN
from tensorflow.keras.layers import TimeDistributed

model = Sequential([
    TimeDistributed(CNN_base(), input_shape=(frames, height, width, channels)),
    TimeDistributed(Flatten()),
    LSTM(256, return_sequences=False),
    Dense(num_classes, activation='softmax')
])
```

## 6. 音樂生成

```python
# 使用 LSTM 生成音樂
def generate_music(seed, length=500):
    result = seed
    h, C = np.zeros((hidden_size, 1)), np.zeros((hidden_size, 1))

    for _ in range(length):
        embedded = embedding[np.newaxis, result[-1]]
        h, C = lstm(embedded, h, C)
        output = dense(h)
        next_note = np.random.choice(len(output), p=output.flatten())
        result.append(next_note)

    return result
```

## 7. 股票預測

```python
# 使用 LSTM 預測股價
model = Sequential([
    LSTM(50, return_sequences=True, input_shape=(look_back, features)),
    LSTM(50),
    Dense(1)
])

model.compile(loss='mse', optimizer='adam')
```

## 8. 手寫識別

```python
# 使用 CNN + LSTM
model = Sequential([
    TimeDistributed(Conv2D(32, (3, 3))),
    TimeDistributed(MaxPooling2D((2, 2))),
    TimeDistributed(Flatten()),
    LSTM(128),
    Dense(num_classes, activation='softmax')
])
```

## 總結

RNN 的應用非常廣泛，從自然語言處理到語音辨識、影片分析都有其身影。LSTM 和 GRU 解決了長期依賴問題，使 RNN 能夠處理更複雜的任務。

## 延伸閱讀

- https://www.google.com/search?q=RNN+applications+deep+learning
- https://www.google.com/search?q=LSTM+GRU+use+cases+examples