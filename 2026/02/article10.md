# 用 PyTorch 寫第一個神經網路

## 為什麼選擇 PyTorch？

PyTorch 是目前最流行的深度學習框架之一。它的設計哲學是「命令式」——你可以像寫一般的 Python 程式一樣寫神經網路，這讓除錯和理解都更直觀。

## 安裝

```bash
pip install torch torchvision
```

## 建立第一個神經網路

我們用 PyTorch 建立一個簡單的多層感知器（MLP）來解決鳶尾花分類問題：

```python
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# 載入資料
iris = load_iris()
X, y = iris.data, iris.target

# 分割資料
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 標準化
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# 轉換為 PyTorch 張量
X_train = torch.FloatTensor(X_train)
y_train = torch.LongTensor(y_train)
X_test = torch.FloatTensor(X_test)
y_test = torch.LongTensor(y_test)
```

## 定義網路結構

```python
class IrisNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(4, 10)   # 輸入 4 特徵 → 隱藏層 10
        self.fc2 = nn.Linear(10, 10)  # 隱藏層 10 → 隱藏層 10
        self.fc3 = nn.Linear(10, 3)   # 隱藏層 10 → 輸出 3 類別
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.fc3(x)
        return x

model = IrisNet()
print(model)
```

## 訓練迴圈

```python
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)

epochs = 200
for epoch in range(epochs):
    # 前向傳播
    outputs = model(X_train)
    loss = criterion(outputs, y_train)

    # 反向傳播
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if (epoch + 1) % 50 == 0:
        _, predicted = torch.max(outputs.data, 1)
        accuracy = (predicted == y_train).sum().item() / len(y_train)
        print(f"Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}, Acc: {accuracy:.3f}")
```

## 評估模型

```python
model.eval()
with torch.no_grad():
    outputs = model(X_test)
    _, predicted = torch.max(outputs.data, 1)
    accuracy = (predicted == y_test).sum().item() / len(y_test)
    print(f"測試集準確率: {accuracy:.3f}")
```

## 用模型做預測

```python
def predict(features):
    model.eval()
    with torch.no_grad():
        tensor = torch.FloatTensor(features).unsqueeze(0)
        tensor = torch.FloatTensor(scaler.transform(tensor))
        outputs = model(tensor)
        _, predicted = torch.max(outputs.data, 1)
        return iris.target_names[predicted.item()]

# 預測新樣本
new_sample = [[5.1, 3.5, 1.4, 0.2]]  # 類似 Setosa 的特徵
print(f"預測結果: {predict(new_sample)}")
```

## 深入理解程式碼

### 模型定義

`nn.Module` 是所有神經網路的基礎類別。`__init__` 中定義層，`forward` 中定義前向傳播邏輯。`nn.Linear(in, out)` 是全連接層，參數數量為 `in × out + out`。

### 損失函式與最佳化器

- `CrossEntropyLoss`：分類任務的標準損失函式（包含 Softmax）
- `Adam`：最受歡迎的最佳化器之一，自適應學習率

### 訓練流程

```
1. forward() → 計算預測
2. criterion() → 計算損失
3. zero_grad() → 清除舊梯度
4. backward() → 計算新梯度
5. optimizer.step() → 更新權重
```

### 評估模式

`model.eval()` 關閉 Dropout 和 BatchNorm 的訓練行為。`torch.no_grad()` 停用梯度計算，減少記憶體使用並加速運算。

## 下一步

這個簡單的三層神經網路只是開始。接下來你可以：

- 增加更多層和神經元
- 使用 CNN 處理影像
- 使用 RNN/LSTM 處理序列資料
- 嘗試更複雜的資料集（如 CIFAR-10、MNIST）

PyTorch 的學習曲線比你想像的平緩——從今天的範例開始，你已經踏出了深度學習的第一步。

---

## 延伸閱讀

- [PyTorch 官方教學](https://www.google.com/search?q=pytorch+tutorial)
- [PyTorch 神經網路入門](https://www.google.com/search?q=pytorch+neural+network+basics)
- [PyTorch vs TensorFlow](https://www.google.com/search?q=pytorch+vs+tensorflow)
