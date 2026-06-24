# 深度學習框架：TensorFlow、Keras、PyTorch

## 前言

2018 年是深度學習框架百花齊放的一年。TensorFlow、Keras、PyTorch 是三個最流行的框架。

## TensorFlow

### 特點

- Google 開發和維護
- 生態系統完善
- 生產環境部署能力強

### Keras

Keras 是一個高層 API，可以運行在 TensorFlow、Theano 或 CNTK 之上。

```python
from keras.models import Sequential
from keras.layers import Dense, Dropout

model = Sequential([
    Dense(64, activation='relu', input_shape=(784,)),
    Dropout(0.5),
    Dense(10, activation='softmax')
])

model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])
```

### TensorFlow 1.7 整合 Keras

TF 1.7 開始，`tf.keras` 成為官方支援的模組。

## PyTorch

### 特點

- Facebook 開發
- 動態計算圖
- 調試方便

### 基本使用

```python
import torch
import torch.nn as nn

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(784, 64)
        self.fc2 = nn.Linear(64, 10)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.softmax(self.fc2(x), dim=1)
        return x

model = Net()
optimizer = torch.optim.Adam(model.parameters())
```

## 框架比較

| 特性 | TensorFlow | Keras | PyTorch |
|------|------------|-------|---------|
| 學習曲線 | 較陡 | 平緩 | 中等 |
| 靈活性 | 高 | 低 | 高 |
| 調試 | 較難 | 容易 | 容易 |
| 部署 | 優秀 | 一般 | 一般 |
| 生態系統 | 完善 | 一般 | 成長中 |

## 選擇建議

- **初學者**：Keras
- **研究人員**：PyTorch
- **生產環境**：TensorFlow

## 結語

選擇框架時，考慮你的需求、經驗和團隊背景。重要的是理解底層原理，而非過度依賴特定框架。

---

**延伸閱讀**

- [TensorFlow 官方網站](https://www.google.com/search?q=TensorFlow+official+site)
- [PyTorch 官方網站](https://www.google.com/search?q=PyTorch+official+site)
- [Keras 官方網站](https://www.google.com/search?q=Keras+official+site)

---

*本篇文章為「AI 程式人雜誌 2018 年 5 月號」類神經網路導論系列之一。*