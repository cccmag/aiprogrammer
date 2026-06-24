# PyTorch 介紹

## 動態計算圖與設計哲學

PyTorch 是 Facebook AI Research 開發的開源深度學習框架，於 2016 年首次發布。

---

## PyTorch 的核心理念

### 1. 動態計算圖

PyTorch 採用動態計算圖（Define-by-Run）：

```python
# 每次執行都重新構建計算圖
import torch

x = torch.tensor([1.0], requires_grad=True)
y = x ** 2
z = y.sum()
z.backward()

# 計算圖根據程式碼執行流程即時構建
```

vs TensorFlow 1.x 的靜態圖：

```python
# 先定義計算圖
import tensorflow as tf

x = tf.placeholder(tf.float32)
y = x ** 2
z = tf.reduce_sum(y)

# 再執行
with tf.Session() as sess:
    result = sess.run(z, feed_dict={x: [1.0, 2.0, 3.0]})
```

### 2. Python 優先

PyTorch 設計貼近 Python 慣例，無需學習新的 DSL。

---

## 為什麼選擇 PyTorch？

### 優勢

```python
# 直覺的 debugging
x = torch.tensor([1.0], requires_grad=True)
y = x * 2

# 可以在任何 Python debugger 中設置斷點
# 直接檢查張量值
print(x, y)  # 即時輸出
```

### 生態系統

```
PyTorch
  ├── torchvision  - 電腦視覺
  ├── torchtext    - 自然語言處理
  ├── torchaudio   - 音訊處理
  ├── ignite       - 訓練輔助
  └── captum       - 模型解釋
```

### 應用場景

1. **研究**：實驗新穎架構
2. **教育**：易於教學和學習
3. **生產**：TorchScript 部署
4. **行動**：PyTorch Mobile

---

## PyTorch 版本時間線

| 版本 | 時間 | 主要功能 |
|-----|------|---------|
| 0.1 | 2016 | 初始版本 |
| 0.3 | 2018 | ONNX 支援 |
| 0.4 | 2018 | 張量設備、NamedTensor |
| 1.0 | 2018 | TorchScript、Mobile、量化 |
| 1.1 | 2019 | JIT 改進、TensorBoard |
| 1.2 | 2019 | 改進的 Mobile、ONNX 出口 |

---

## PyTorch 與 TensorFlow 比較

| 方面 | PyTorch | TensorFlow |
|-----|---------|-----------|
| 計算圖 | 動態 | 靜態（1.x）/ 動態（2.x） |
| API 風格 | Python 優先 | 有點像 MATLAB |
| 除錯 | 直接 | 需要特別工具 |
| 部署 | TorchScript | SavedModel |
| 社群 | 學術界大 | 產業界大 |
| 行動支援 | PyTorch Mobile | TensorFlow Lite |

---

## 基本使用流程

```python
import torch
import torch.nn as nn
import torch.optim as optim

# 1. 準備資料
x = torch.randn(100, 10)
y = torch.randn(100, 1)

# 2. 定義模型
model = nn.Linear(10, 1)

# 3. 定義損失和優化器
criterion = nn.MSELoss()
optimizer = optim.SGD(model.parameters(), lr=0.01)

# 4. 訓練迴圈
for epoch in range(100):
    optimizer.zero_grad()
    outputs = model(x)
    loss = criterion(outputs, y)
    loss.backward()
    optimizer.step()
```

---

## 延伸閱讀

- [PyTorch 官方網站](https://www.google.com/search?q=PyTorch+official+website)
- [PyTorch 官方教程](https://www.google.com/search?q=Pytorch+tutorials)
- [PyTorch vs TensorFlow](https://www.google.com/search?q=Pytorch+vs+Tensorflow+comparison+2019)

---

*本篇文章為「AI 程式人雜誌 2019 年 6 月號」系列文章之一。*