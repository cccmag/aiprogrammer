# 文章 7：語音辨識技術

## 前言

語音辨識是將語音訊號轉換為文字的技術。本章節介紹語音辨識的基本原理與發展。

## 語音辨識流程

```
音頻 → 預處理 → 特徵提取 → 聲學模型 → 解碼 → 文字
```

## 音頻預處理

```python
import numpy as np

# 採樣
sample_rate = 16000  # 16kHz
duration = 1  # 1 秒
samples = np.random.randn(sample_rate * duration)

# 標準化
samples = samples / np.max(np.abs(samples))
```

## 特徵提取

### MFCC（梅爾頻率倒譜係數）

```python
import librosa

audio, sr = librosa.load('speech.wav', sr=16000)

# 提取 MFCC
mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)

print(f"MFCC shape: {mfccs.shape}")
```

## 聲學模型

### 早期方法

- GMM-HMM：高斯混合模型-隱馬爾可夫模型
- 需要手工設計特徵

### 深度學習方法

```python
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

model = Sequential([
    LSTM(128, input_shape=(None, 13)),
    Dense(64, activation='relu'),
    Dense(num_phonemes, activation='softmax')
])
```

## CTC（連接時序分類）

處理輸入輸出長度不對齊的問題：

```python
# CTC loss 用於訓練
from tensorflow.keras import backend as K

def ctc_loss(y_true, y_pred):
    # 計算 CTC loss
    batch_size = y_true.shape[0]
    input_length = y_pred.shape[1]
    label_length = y_true.shape[1]

    input_length_tensor = K.ones((batch_size, 1)) * input_length
    label_length_tensor = K.ones((batch_size, 1)) * label_length

    loss = K.ctc_batch_cost(y_true, y_pred, input_length_tensor, label_length_tensor)
    return loss
```

## 端到端語音辨識

```python
class EndToEndASR:
    def __init__(self, input_dim, hidden_dim, vocab_size):
        self.encoder = LSTM(hidden_dim, return_sequences=True)
        self.decoder = LSTM(hidden_dim, return_sequences=True)
        self.output = Dense(vocab_size, activation='softmax')

    def forward(self, audio_features):
        # audio_features: (time_steps, mfcc_dim)
        encoded = self.encoder(audio_features)
        decoded = self.decoder(encoded)
        output = self.output(decoded)
        return output
```

## 現有系統

| 系統 | 公司 | 特色 |
|------|------|------|
| Google Speech API | Google | 雲端服務 |
| Watson Speech to Text | IBM | 多語言支援 |
| Alexa Voice Service | Amazon | 嵌入式 |
| Siri | Apple | 設備端處理 |

## 挑戰

- 噪聲環境
- 多人說話
- 方言與口音
- 即時性要求

## 總結

語音辨識從 GMM-HMM 演進到深度學習，端到端模型大幅簡化了系統架構並提升了準確率。

## 延伸閱讀

- https://www.google.com/search?q=speech+recognition+deep+learning+MFCC
- https://www.google.com/search?q=CTC+connectionist+temporal+classification