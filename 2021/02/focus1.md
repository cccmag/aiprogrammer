# PyTorch 生態系概覽

## 核心元件

### torch

PyTorch 的核心模組，提供：
- 張量運算（`torch.Tensor`）
- 線性代數（`torch.linalg`）
- 隨機數（`torch.random`）

```python
import torch

x = torch.randn(3, 4)
y = torch.matmul(x, x.T)
```

### autograd

自動微分引擎，追蹤所有運算並自動計算梯度：

```python
x = torch.tensor([1.0, 2.0], requires_grad=True)
y = x ** 2
y.sum().backward()  # 自動計算梯度
print(x.grad)  # [2, 4]
```

### nn.Module

神經網路的基類，所有網路層都繼承自此：

```python
class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = nn.Linear(10, 1)

    def forward(self, x):
        return self.fc(x)
```

## 發展歷程

| 版本 | 時間 | 主要功能 |
|------|------|----------|
| 0.1 | 2016/10 | 初始發布 |
| 1.0 | 2018/12 | 生產支援、 JIT |
| 1.4 | 2019/10 | Java 支援、分散式 |
| 1.8 | 2021/03 | linalg、行動優化 |

## 與 TensorFlow 的比較

| 特性 | PyTorch | TensorFlow |
|------|---------|------------|
| 計算圖 | 動態 | 靜態（+ eager） |
| 部署 | TorchScript | TF Serving |
| 生態 | 學術為主 | 產業為主 |

---

## 延伸閱讀

- [PyTorch+官方文檔](https://www.google.com/search?q=PyTorch+documentation)
- [PyTorch+vs+TensorFlow+2021](https://www.google.com/search?q=PyTorch+vs+TensorFlow+comparison+2021)
- [PyTorch+生態系介紹](https://www.google.com/search?q=PyTorch+ecosystem+overview)

*本篇文章為「AI 程式人雜誌 2021 年 2 月號」精選文章。*