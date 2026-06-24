# 神經網路模組設計

## nn.Module 基礎

所有網路層和模型都應繼承 `nn.Module`：

```python
class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(784, 256)
        self.bn1 = nn.BatchNorm1d(256)
        self.fc2 = nn.Linear(256, 10)

    def forward(self, x):
        x = self.fc1(x)
        x = self.bn1(x)
        x = F.relu(x)
        x = self.fc2(x)
        return x
```

## 常用層

```python
nn.Linear(in_features, out_features)  # 全連接層
nn.Conv2d(in_ch, out_ch, kernel_size)   # 2D 卷積
nn.LSTM(input_size, hidden_size)        # LSTM 層
nn.Dropout(p)                            # Dropout
nn.BatchNorm1d(num_features)             # 批歸一化
```

## 自定義層

```python
class MyLayer(nn.Module):
    def __init__(self, in_features, out_features):
        super().__init__()
        self.weight = nn.Parameter(torch.randn(in_features, out_features))
        self.bias = nn.Parameter(torch.zeros(out_features))

    def forward(self, x):
        return torch.matmul(x, self.weight) + self.bias
```

## 參數管理

```python
# 列出所有參數
for name, param in model.named_parameters():
    print(f"{name}: {param.shape}")

# freeze 層
for param in model.fc1.parameters():
    param.requires_grad = False
```

---

## 延伸閱讀

- [nn.Module 官方文檔](https://www.google.com/search?q=PyTorch+nn.Module)
- [自定義神經網路層](https://www.google.com/search?q=custom+nn+module+PyTorch)
- [模型參數管理](https://www.google.com/search?q=PyTorch+parameter+management)

*本篇文章為「AI 程式人雜誌 2021 年 2 月號」精選文章。*