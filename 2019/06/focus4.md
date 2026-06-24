# 神經網路建構

## nn.Module 與層

PyTorch 提供 `nn.Module` 作為神經網路模型的基類。

---

## nn.Module 基礎

### 基本結構

```python
import torch.nn as nn

class MyModel(nn.Module):
    def __init__(self):
        super(MyModel, self).__init__()
        # 定義層
        self.layer1 = nn.Linear(10, 5)
        self.layer2 = nn.Linear(5, 1)

    def forward(self, x):
        # 定義前饋邏輯
        x = torch.relu(self.layer1(x))
        x = self.layer2(x)
        return x
```

### 常用層

```python
# 線性層
linear = nn.Linear(in_features=10, out_features=5)

# 卷積層
conv1d = nn.Conv1d(in_channels=3, out_channels=64, kernel_size=3)
conv2d = nn.Conv2d(in_channels=3, out_channels=64, kernel_size=3)
conv3d = nn.Conv3d(in_channels=3, out_channels=64, kernel_size=3)

# 池化層
maxpool = nn.MaxPool2d(kernel_size=2, stride=2)
avgpool = nn.AvgPool2d(kernel_size=2, stride=2)
global_avgpool = nn.AdaptiveAvgPool2d((1, 1))

# Dropout
dropout = nn.Dropout(p=0.5)

# BatchNorm
bn = nn.BatchNorm2d(num_features=64)
```

---

## 激活函數

```python
# 不需要實例化參數的激活函數通常放在 forward 中
import torch.nn.functional as F

class MyNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = nn.Linear(10, 5)

    def forward(self, x):
        x = self.fc(x)
        x = F.relu(x)    # ReLU
        x = F.sigmoid(x) # Sigmoid
        x = F.softmax(x, dim=1)  # Softmax
        return x
```

---

## 預定義模型

### 常用架構

```python
import torchvision.models as models

# 載入預訓練模型
resnet18 = models.resnet18(pretrained=True)
alexnet = models.alexnet(pretrained=True)
vgg16 = models.vgg16(pretrained=True)

# 不預訓練
resnet18 = models.resnet18(pretrained=False)
```

### 修改預訓練模型

```python
# 修改最後一層
resnet18.fc = nn.Linear(resnet18.fc.in_features, 10)

# 凍結晶數
for param in resnet18.parameters():
    param.requires_grad = False
```

---

## 模型操作

```python
# 查看結構
model = nn.Sequential(
    nn.Linear(10, 5),
    nn.ReLU(),
    nn.Linear(5, 1)
)
print(model)

# 獲取特定層
layer = model[0]  # 第一層

# 枚舉所有參數
for name, param in model.named_parameters():
    print(name, param.shape)
```

---

## GPU 支援

```python
# 移動到 GPU
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)

# 移動張量
x = x.to(device)

# 多 GPU
model = nn.DataParallel(model)
```

---

## 延伸閱讀

- [PyTorch nn 文檔](https://www.google.com/search?q=pytorch+nn+module+tutorial)
- [神經網路建構指南](https://www.google.com/search?q=building+neural+networks+pytorch)

---

*本篇文章為「AI 程式人雜誌 2019 年 6 月號」系列文章之一。*