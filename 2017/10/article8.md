# Facebook 發布 PyTorch：動態計算圖的深度學習框架

## 前言

PyTorch 於 2017 年 1 月由 Facebook AI Research (FAIR) 發布，迅速成為深度學習研究的首選框架。它的動態計算圖設計讓除錯和實驗變得前所未有的簡單。

## PyTorch 的設計理念

### 動態計算圖

```
┌─────────────────────────────────────────────────────────┐
│         動態計算圖 vs 靜態計算圖                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  PyTorch (動態)          TensorFlow (靜態)              │
│                                                         │
│  ┌─────────┐               定義 → 編譯 → 執行           │
│  │ 程式碼  │                                              │
│  └────┬────┘                                              │
│       │                                                   │
│       ▼                                                   │
│  定義即執行                                              │
│                                                         │
│  優勢：                                                   │
│  - 隨時檢查中間變數                                        │
│  - 條件分支自然                                          │
│  - 迴圈結構簡單                                          │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Python 優先

PyTorch 與 Python 深度整合，研究者可以直接使用熟悉的 Python 程式碼：

```python
import torch
import torch.nn as nn

class SimpleNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 16, 3)
        self.conv2 = nn.Conv2d(16, 32, 3)
        self.fc = nn.Linear(32 * 6 * 6, 10)

    def forward(self, x):
        x = torch.relu(self.conv1(x))
        x = torch.max_pool2d(x, 2)
        x = torch.relu(self.conv2(x))
        x = torch.max_pool2d(x, 2)
        x = x.view(x.size(0), -1)
        x = self.fc(x)
        return x

model = SimpleNet()
print(model)
```

## 核心特性

### 張量運算

```python
# 建立張量
x = torch.randn(3, 4)
y = torch.randn(3, 4)

# 基本運算
z = x + y
z = torch.matmul(x, y.t())
z = torch.sum(x, dim=1)

# GPU 加速
x = x.cuda()
y = y.cuda()
z = x + y
```

### 自動微分

```python
# 自動計算梯度
x = torch.tensor([1.0, 2.0, 3.0], requires_grad=True)
y = x ** 2
z = y.sum()

z.backward()
print(x.grad)  # dz/dx = 2x = [2, 4, 6]
```

### 神經網路模組

```python
# 使用預設義的層
model = nn.Sequential(
    nn.Linear(784, 256),
    nn.ReLU(),
    nn.Dropout(0.2),
    nn.Linear(256, 10)
)

optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
criterion = nn.CrossEntropyLoss()

# 訓練循環
for images, labels in dataloader:
    optimizer.zero_grad()
    outputs = model(images)
    loss = criterion(outputs, labels)
    loss.backward()
    optimizer.step()
```

## 與其他框架的比較

| 特性 | PyTorch | TensorFlow | MXNet |
|------|---------|------------|-------|
| 計算圖 | 動態 | 靜態（2.0 後也支援動態） | 混合 |
| 除錯 | 容易 | 困難 | 一般 |
| 生態 | 快速成長 | 龐大 | 一般 |
| 部署 | TorchScript | TF Serving | ONNX |

## PyTorch 生態

```
┌─────────────────────────────────────────────────────────┐
│              PyTorch 生態系統                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ├── torchvision    電腦視覺                            │
│  ├── torchtext      自然語言處理                        │
│  ├── torchaudio     音訊處理                           │
│  ├── ignite        訓練輔助工具                         │
│  ├── skorch        scikit-learn 介面                    │
│  └── ONNX          模型交換格式                         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 應用範例

### 影像分類

```python
import torchvision.models as models

model = models.resnet18(pretrained=True)
model.fc = nn.Linear(512, 10)

# 遷移學習
for param in model.parameters():
    param.requires_grad = False

model.fc.requires_grad = True
```

###  RNN 生成

```python
class RNNGenerator(nn.Module):
    def __init__(self, vocab_size, embed_size, hidden_size):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_size)
        self.lstm = nn.LSTM(embed_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, vocab_size)

    def forward(self, x, hidden=None):
        embedded = self.embedding(x)
        output, hidden = self.lstm(embedded, hidden)
        return self.fc(output), hidden
```

## 研究優勢

PyTorch 的動態特性使其成為研究的首選：

1. **快速原型**：可以直接修改網路結構
2. **易於除錯**：Python 除錯工具都能使用
3. **符合直覺**：像寫一般 Python 程式碼一样

## 結論

PyTorch 的發布標誌著深度學習框架進入了一個更加靈活和易用的時代。它的動態計算圖設計深刻影響了後續的框架開發，如 Chainer、JAX 等。

---

**延伸閱讀**

- [PyTorch Official Site](https://www.google.com/search?q=PyTorch+official+website)
- [PyTorch Tutorials](https://www.google.com/search?q=PyTorch+tutorials+2017)
- [Facebook AI Research](https://www.google.com/search?q=Facebook+AI+Research+PyTorch)

---

*本篇文章為「AI 程式人雜誌 2017 年 10 月號」AI 相關文章之一。*