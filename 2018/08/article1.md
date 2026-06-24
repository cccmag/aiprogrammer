# PyTorch vs TensorFlow 比較

## 1. 設計理念

### PyTorch：研究優先

PyTorch 的設計目標是讓研究人員能快速實驗想法：

- 動態計算圖，即時執行
- 直覺的 Python API
- 類似 NumPy 的張量操作
- 簡易的 Debug 體驗

### TensorFlow：生產優先

TensorFlow 的設計目標是支援大規模部署：

- 靜態計算圖（1.x），最佳化後執行速度快
- 豐富的部署工具（TensorFlow Serving、Lite）
- 完整的生態系（TensorBoard、TF Hub）
- 支援 TPU 和邊緣裝置

## 2. API 比較

```python
# PyTorch
import torch
import torch.nn as nn

class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = nn.Linear(10, 2)

    def forward(self, x):
        return self.fc(x)

model = Net()
optimizer = torch.optim.Adam(model.parameters())
```

```python
# TensorFlow 1.x
import tensorflow as tf

x = tf.placeholder(tf.float32, shape=[None, 10])
y = tf.placeholder(tf.float32, shape=[None, 2])

W = tf.Variable(tf.random_normal([10, 2]))
b = tf.Variable(tf.zeros([2]))
pred = tf.matmul(x, W) + b

optimizer = tf.train.AdamOptimizer(0.001).minimize(loss)
```

## 3. 動態 vs 靜態

```python
# PyTorch：動態圖，輕鬆處理可變長度輸入
def dynamic_rnn(input_seq):
    hidden = torch.zeros(1, 128)
    for step in input_seq:
        # 每次迴圈都可以有不同的計算
        hidden = rnn_cell(step, hidden)
    return hidden

# TensorFlow 1.x：需要靜態展開或 dynamic_rnn
outputs, state = tf.nn.dynamic_rnn(
    cell, input_seq, dtype=tf.float32
)
```

## 4. 張量操作

```python
# PyTorch（類似 NumPy）
x = torch.randn(3, 4)
print(x.shape)           # torch.Size([3, 4])
print(x.sum(dim=1))      # 按行求和
print(x.t())             # 轉置
print(x.view(2, 6))      # reshape

# NumPy
import numpy as np
x = np.random.randn(3, 4)
print(x.shape)
print(np.sum(x, axis=1))
```

## 5. 部署支援

| 面向 | PyTorch | TensorFlow |
|------|---------|------------|
| Server 部署 | TorchServe (2019) | TensorFlow Serving |
| 行動裝置 | PyTorch Mobile (2020) | TensorFlow Lite |
| 網頁 | ONNX.js | TensorFlow.js |
| 嵌入式 | 受限 | TensorFlow Lite |

## 6. 生態系

| 工具 | PyTorch | TensorFlow |
|------|---------|------------|
| 視覺化 | TensorBoard (支援) | 原生 TensorBoard |
| 模型庫 | TorchVision, TorchText | TF-Hub, TF-Models |
| 分散式訓練 | 原生支援 | Parameter Server |
| 模型量化 | 支援 | 完整支援 |

## 7. 2018 年的選擇建議

- **研究/論文** → PyTorch
- **產品部署** → TensorFlow
- **個人學習** → 兩者皆可
- **企業應用** → TensorFlow
- **快速原型** → PyTorch

## 8. 融合趨勢

TensorFlow 2.0（2019）將 Eager Execution 預設開啟，許多設計向 PyTorch 靠攏。兩個框架的差異正在縮小。

---

**參考資料**
- [PyTorch vs TensorFlow 2018](https://www.google.com/search?q=PyTorch+TensorFlow+comparison+2018)
- [Deep Learning Framework Comparison](https://www.google.com/search?q=deep+learning+framework+comparison+2018)