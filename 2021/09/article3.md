# 類神經網路基礎

類神經網路是深度強化學習的基礎。

## 1. 基本結構

```python
import torch
import torch.nn as nn

class SimpleNN(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super().__init__()
        self.layer1 = nn.Linear(input_dim, hidden_dim)
        self.layer2 = nn.Linear(hidden_dim, hidden_dim)
        self.output = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        x = torch.relu(self.layer1(x))
        x = torch.relu(self.layer2(x))
        return self.output(x)
```

## 2. 激活函數

- ReLU：max(0, x)
- Sigmoid：1 / (1 + exp(-x))
- Tanh：(exp(x) - exp(-x)) / (exp(x) + exp(-x))
- Softmax：exp(x) / sum(exp(x))

## 3. 損失函數

- MSE：均方誤差
- CrossEntropy：交叉熵
- BCE：二元交叉熵

---

## 延伸閱讀

- [PyTorch 官方教程](https://www.google.com/search?q=PyTorch+tutorial+neural+networks)
- [深度學習基礎](https://www.google.com/search?q=deep+learning+fundamentals+neural+networks)