# PyTorch 0.2：動態計算圖再進化

## 前言

PyTorch 0.2 在 2017 年 1 月發布，帶來了多項改進，包括 nn.DataParallel 的改進、更豐富的優化功能和更好的 CUDA 記憶體管理。

## PyTorch 的核心優勢

### 動態計算圖

PyTorch 的最大特點是動態計算圖：

```python
import torch

# 每次執行都可以是不同的圖
def forward(x):
    if x.sum() > 0:
        return x * 2
    else:
        return x * 3
```

### Python 原生

```python
# 直接使用 Python 控制流
for i in range(10):
    x = x * W[i] + b[i]
```

## PyTorch 0.2 的新功能

### DataParallel 改進

```python
import torch.nn as nn

# 多 GPU 訓練更加穩定
model = nn.DataParallel(model, device_ids=[0, 1, 2])
```

### torch.optim 增強

```python
import torch.optim as optim

# 更多優化器選項
optimizer = optim.Adam(model.parameters(), lr=0.001, amsgrad=True)
```

### CUDA 記憶體優化

```python
# 更好的記憶體管理
torch.cuda.empty_cache()
```

## autograd 系統

### 自動微分

```python
import torch

x = torch.tensor([2.0], requires_grad=True)
y = x ** 2 + 3 * x + 1
y.backward()
print(x.grad)  # 梯度：2x + 3 = 7
```

## 結語

PyTorch 0.2 展示了這個框架的持續進步。其動態計算圖設計和 Python 原生風格深受研究者喜愛，在學術界的影響力持續擴大。

---

## 延伸閱讀

- [PyTorch 0.2 發布說明](https://www.google.com/search?q=PyTorch+0.2+release+notes)
- [PyTorch+動態計算圖](https://www.google.com/search?q=PyTorch+dynamic+computation+graph)
- [PyTorch+tutorial](https://www.google.com/search?q=PyTorch+tutorial+deep+learning)

---

*本篇文章為「AI 程式人雜誌 2017 年 2 月號」文章系列之一。*