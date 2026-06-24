# 深度學習框架比較（2018）

## 主流框架的優劣勢分析

### 2018 年框架生態

2018 年的深度學習框架市場呈現「一超多強」格局：TensorFlow 領跑，PyTorch、Caffe、MXNet 等多元競爭。

### TensorFlow

**優點**：
- 生態系最完整（TensorBoard、Serving、Lite、TPU）
- 企業採用率最高
- 支援跨平台部署

**缺點**：
- API 變動頻繁（1.x 期間）
- 學習曲線較陡
- 靜態圖除錯困難（直到 Eager Execution 改善）

```python
# TensorFlow 1.10 標準寫法
import tensorflow as tf

x = tf.placeholder(tf.float32, shape=[None, 784])
y = tf.placeholder(tf.float32, shape=[None, 10])

weights = tf.Variable(tf.random_normal([784, 10]))
biases = tf.Variable(tf.zeros([10]))

pred = tf.matmul(x, weights) + biases
loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(y, pred))
train_op = tf.train.AdamOptimizer(0.001).minimize(loss)
```

### PyTorch

**優點**：
- 動態圖，直覺除錯
- 學術界採用率最高
- Python 原生設計

**缺點**：
- 生態系較小
- 部署工具不如 TensorFlow
- 行動裝置支援有限

```python
# PyTorch 動態圖範例
import torch
import torch.nn as nn

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(784, 128)
        self.fc2 = nn.Linear(128, 10)
    
    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

model = Net()
loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
```

### Keras（TensorFlow 整合版）

**優點**：
- API 最簡潔
- 快速原型開發
- 文件完善

**缺點**：
- 彈性受限
- 自訂複雜網路困難

### Caffe

**優點**：
- 影像處理效能佳
- Model Zoo 豐富

**缺點**：
- 缺乏靈活性
- Python 整合不佳

### MXNet

**優點**：
- 效能優異
- 支援多語言（Python、R、Scala、Julia）

**缺點**：
- 社群規模小

### 比較表

| 面向 | TensorFlow | PyTorch | Keras | Caffe |
|------|-------------|---------|-------|-------|
| 學習曲線 | 中 | 低 | 最低 | 中 |
| 彈性 | 高 | 高 | 低 | 中 |
| 除錯體驗 | 中（EG） | 高 | 高 | 低 |
| 部署 | 最佳 | 中 | 中 | 中 |
| 學術界 | 中 | 最高 | 高 | 中 |
| 企業界 | 最高 | 中 | 高 | 中 |
| 生態系 | 完整 | 成長中 | 完整 | 中 |

### 選擇建議

- **快速原型、研究** → Keras 或 PyTorch
- **生產部署、企業** → TensorFlow
- **影像處理、Caffe 模型** → Caffe 或 PyTorch
- **多語言支援** → MXNet

### 小結

2018 年的框架之爭沒有贏家，各有適用場景。選擇時應考慮團隊技能、部署需求和研究/產品階段。

---

**下一步**：[TFHub 遷移學習模組庫](focus7.md)