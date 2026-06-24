# 深度學習框架格局：TensorFlow, PyTorch, Caffe2

## 前言

2017 年是深度學習框架的關鍵一年。TensorFlow 持續主導，PyTorch 强势崛起，Caffe2 強調跨平台部署。本篇文章回顧這一年框架生態的發展。

## TensorFlow：持續主導

### TensorFlow 1.0 里程碑

2017 年 2 月發布的 TensorFlow 1.0 帶來了多項重要改進：

```python
# TensorFlow 1.0 核心概念

# 1. 計算圖
import tensorflow as tf

# 定義計算圖
x = tf.placeholder(tf.float32, name="x")
y = tf.placeholder(tf.float32, name="y")
z = x + y

# 執行
with tf.Session() as sess:
    result = sess.run(z, feed_dict={x: 1.0, y: 2.0})

# 2. Keras 整合 (後來加入)
from tensorflow import keras

model = keras.Sequential([
    keras.layers.Dense(64, activation='relu'),
    keras.layers.Dense(10, activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy')
```

### TensorFlow 生態

```
┌─────────────────────────────────────────────────────────┐
│              TensorFlow 生態                            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  TensorFlow Core                                       │
│       │                                                 │
│       ├── tf.keras (高級 API)                          │
│       ├── tf.data (資料處理)                           │
│       ├── tf.estimator (估計器)                         │
│       ├── TensorFlow Lite (行動/邊緣)                   │
│       ├── TensorFlow.js (瀏覽器)                        │
│       └── TensorFlow Serving (部署)                     │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## PyTorch：快速崛起

### PyTorch 的設計

PyTorch 於 2017 年 1 月發布，迅速獲得研究人員青睐：

```python
import torch
import torch.nn as nn

# 動態計算圖
class DynamicNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 64, 3)
        self.conv2 = nn.Conv2d(64, 128, 3)

    def forward(self, x):
        # 每個樣本可以有不同計算路徑
        x = self.conv1(x)
        if x.size(2) > 32:
            x = self.conv2(x)
        return x

# 易於除錯
model = DynamicNet()
output = model(input_tensor)  # 就像普通 Python 程式碼
```

### PyTorch 優勢

```python
# 1. Python 優先，與 Python 生態無縫整合
# 2. 動態計算圖，易於除錯
# 3. 命令式編程，所見即所得
# 4. 豐富的預訓練模型庫
```

## Caffe2：跨平台部署

### Caffe2 的特點

Caffe2 由 Facebook 開發，強調便攜性和效能：

```python
# Caffe2 的特點

# 1. 輕量級核心
# 2. 跨平台支援
#    - 雲端 (CPU/GPU)
#    - 行動端 (iOS/Android)
#    - 邊緣設備
# 3. 與 PyTorch 整合 (最終形成 PyTorch 1.0)

# 部署示例
from caffe2.python import workspace, model_helper

# 建立模型
train_model = model_helper.ModelHelper(name="my_model")

# 添加 ops
train_model.FC(["input", "w", "b"], ["output"])
```

## 框架比較

| 特性 | TensorFlow | PyTorch | Caffe2 |
|------|------------|---------|--------|
| 發布年份 | 2015 | 2017 | 2017 |
| 開發者 | Google | Facebook | Facebook |
| 計算圖 | 靜態 | 動態 | 靜態/動態 |
| 除錯 | 困難 | 容易 | 一般 |
| 生態 | 龐大 | 快速成長 | 中等 |
| 部署 | 優秀 | 改善中 | 優秀 |
| 使用場景 | 生產/研究 | 研究優先 | 邊緣部署 |

## 2017 年框架發展

```
時間線：
2017/01 - PyTorch 發布
2017/02 - TensorFlow 1.0 發布
2017/04 - Caffe2 開源
2017/07 - Caffe2 與 PyTorch 宣佈整合
2017/09 - PyTorch 0.3 發布
2017/10 - TensorFlow 1.4 發布
```

## 框架選擇指南

```python
# 根據場景選擇框架

# 1. 生產部署：TensorFlow
# TF Serving 成熟，生態完整

# 2. 研究原型：PyTorch
# 快速迭代，易於除錯

# 3. 邊緣部署：Caffe2/TensorFlow Lite
# 輕量級，跨平台支援

# 4. 企業應用：多框架組合
# 研發用 PyTorch，生產用 TensorFlow
```

## ONNX：模型交換格式

2017 年 12 月，Microsoft 和 Facebook 發布了 ONNX (Open Neural Network Exchange)：

```python
# ONNX 允許模型在不同框架間轉換

# PyTorch → ONNX
import torch.onnx
model = torchvision.models.resnet18(pretrained=True)
torch.onnx.export(model, dummy_input, "model.onnx")

# 然後可以在其他框架中使用
# Caffe2, TensorFlow, MXNet 都支援 ONNX
```

## 總結

2017 年框架生態的三個趨勢：

1. **研究框架的崛起**：PyTorch 挑戰 TensorFlow 地位
2. **部署框架的成熟**：TensorFlow Lite, Core ML
3. **互操作性**：ONNX 促進框架協作

---

**延伸閱讀**

- [TensorFlow](https://www.google.com/search?q=TensorFlow+official)
- [PyTorch](https://www.google.com/search?q=PyTorch+official)
- [Caffe2](https://www.google.com/search?q=Caffe2+GitHub)
- [ONNX](https://www.google.com/search?q=ONNX+Microsoft+Facebook)

---

*本篇文章為「AI 程式人雜誌 2017 年 12 月號」年終回顧系列之一。*