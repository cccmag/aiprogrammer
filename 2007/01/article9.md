# 開源 AI 框架：Torch 與 Theano

## 前言

2007 年，深度學習框架開始嶄露頭角。Torch 和 Theano 這兩個開源框架為日後深度學習的普及奠定了基礎。

## Torch 的歷史

### Lua 與 Torch

Torch 是一個基於 Lua 程式語言的科學計算框架：

```lua
-- Torch 基本語法
-- 張量操作
require 'torch'

-- 建立張量
a = torch.Tensor(3, 4)  -- 3x4 矩陣
b = torch.rand(3, 4)    -- 隨機初始化

-- 矩陣運算
c = torch.mm(a, b:t())  -- 矩陣乘法
d = torch.add(b, 2)      -- 加法

-- 類神經網路模組
require 'nn'

model = nn.Sequential()
model:add(nn.Linear(10, 5))
model:add(nn.ReLU())
model:add(nn.Linear(5, 1))
model:add(nn.Sigmoid())

-- 前向傳播
input = torch.rand(10)
output = model:forward(input)

-- 損失函數
criterion = nn.BCECriterion()
loss = criterion:forward(output, torch.Tensor({1}))
```

### 為何選擇 Lua

```
┌────────────────────────────────────────────────────────┐
│            選擇 Lua 的原因                              │
├────────────────────────────────────────────────────────┤
│                                                        │
│  Lua 的優勢：                                          │
│  - 輕量級直譯語言                                      │
│  - 快速啟動                                            │
│  - 簡單的 C 整合                                       │
│  - 良好的數值計算社群                                   │
│                                                        │
│  Lua 的劣勢：                                          │
│  - 程式設計師較少                                      │
│  - 生態系較小                                          │
│  - 對科學計算支援不如 Python                           │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## Theano 的歷史

### Python 與 Theano

Theano 是基於 Python 的符號式深度學習框架：

```python
# Theano 基本語法
import theano
from theano import tensor as T

# 定義變數
x = T.matrix('x')
y = T.matrix('y')

# 符號式操作
z = T.sum(T.dot(x, y))

# 編譯函式
f = theano.function([x, y], z)

# 使用
import numpy as np
x_val = np.random.rand(3, 4)
y_val = np.random.rand(4, 5)
result = f(x_val, y_val)
```

### 符號式計算

```python
# Theano 的符號式計算優點

# 1. 自動微分
x = T.dscalar('x')
f = x**2 + 2*x + 1
df = T.grad(f, x)  # 自動計算導數
df_fun = theano.function([x], df)

# 2. 最佳化
# Theano 會自動最佳化計算圖

# 3. GPU 支援
# theano.config.device = 'gpu'
# theano.config.floatX = 'float32'
```

## 深度學習的基本功能

### 兩者都支援的功能

```python
# 2007 年深度學習框架的核心功能
DEEP_LEARNING_FEATURES = {
    "線性層": "全連接層",
    "激勵函數": "Sigmoid, tanh, ReLU",
    "卷積層": "影像處理",
    "池化層": "降維",
    "循環層": "序列處理",
    "損失函數": "交叉熵、均方誤差",
    "優化器": "SGD, Adam",
    "GPU 加速": "CUDA 整合"
}
```

## 與現代框架的比較

### 2007 vs 2020

```
┌────────────────────────────────────────────────────────┐
│          深度學習框架演進                               │
├────────────────────────────────────────────────────────┤
│                                                        │
│  2007 (Torch/Theano)：                                │
│  - 需要手動實現大部分演算法                            │
│  - 有限的預訓練模型                                    │
│  - 只能小型資料集                                      │
│  - 學習曲線陡峭                                        │
│                                                        │
│  2020 (PyTorch/TensorFlow)：                          │
│  - 豐富的預訓練模型                                    │
│  - 自動微分                                            │
│  - 大規模分散式訓練                                    │
│  - 生態豐富                                            │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## 社群與生態

### 2007 年的社群

```python
# Torch 和 Theano 的社群
COMMUNITY_2007 = {
    "Torch": {
        "語言": "Lua",
        "主要使用者": "研究者",
        "優勢": "靈活性、速度",
        "劣勢": "生態小"
    },
    "Theano": {
        "語言": "Python",
        "主要使用者": "研究者",
        "優勢": "Python 整合、符號計算",
        "劣勢": "編譯時間長"
    },
    "其他框架": [
        "Caffe (UC Berkeley)",
        "TensorFlow (Google, 2015)",
        "CNTK (Microsoft, 2016)"
    ]
}
```

## 對深度學習普及的貢獻

### 降低研究門檻

```
┌────────────────────────────────────────────────────────┐
│          開源框架對深度學習的貢獻                       │
├────────────────────────────────────────────────────────┤
│                                                        │
│  1. 知識共享                                           │
│     └─ 研究者可以分享模型                              │
│                                                        │
│  2. 重現性                                             │
│     └─ 公開程式碼促進研究重現                          │
│                                                        │
│  3. 教育                                               │
│     └─ 學生可以學習最新技術                            │
│                                                        │
│  4. 協作                                               │
│     └─ 全球研究者共同改進框架                          │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## 後續影響

### Torch 到 PyTorch

Torch 的 Lua 版本後來發展成 PyTorch（Python 版本）：

```python
# PyTorch 範例（與 Torch 類似但 Python 語法）
import torch
import torch.nn as nn

# 模型定義
model = nn.Sequential(
    nn.Linear(10, 5),
    nn.ReLU(),
    nn.Linear(5, 1),
    nn.Sigmoid()
)

# 前向傳播
x = torch.rand(10)
output = model(x)

# 訓練
criterion = nn.BCELoss()
optimizer = torch.optim.Adam(model.parameters())

# 訓練迴圈
for epoch in range(100):
    optimizer.zero_grad()
    output = model(x)
    loss = criterion(output, y)
    loss.backward()
    optimizer.step()
```

## 結論

2007 年的 Torch 和 Theano 雖然還不是主流工具，但它們為日後深度學習框架的發展積累了重要經驗。

Torch 的動態計算圖和 Theano 的符號式計算，成為日後 PyTorch 和 TensorFlow 的設計基礎。

---

## 延伸閱讀

- [Torch 歷史](https://www.google.com/search?q=Torch+deep+learning+framework+history)
- [Theano 歷史](https://www.google.com/search?q=Theano+deep+learning+framework)
- [深度學習框架比較](https://www.google.com/search?q=deep+learning+framework+comparison)

---

*本篇文章為「AI 程式人雜誌 2007 年 1 月號」文章集錦系列。*