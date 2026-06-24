# 卷積神經網路原理

CNN 是電腦視覺的核心模型，本文介紹其原理。

## 1. 卷積層

```python
class ConvLayer(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size=3):
        super().__init__()
        self.conv = nn.Conv2d(in_channels, out_channels, kernel_size, padding=kernel_size//2)
        self.bn = nn.BatchNorm2d(out_channels)
        self.relu = nn.ReLU()

    def forward(self, x):
        return self.relu(self.bn(self.conv(x)))
```

## 2. 池化層

```python
max_pool = nn.MaxPool2d(2, 2)
avg_pool = nn.AvgPool2d(2, 2)
global_pool = nn.AdaptiveAvgPool2d((1, 1))
```

## 3. 經典架構

- LeNet：早期CNN
- AlexNet：深度學習突破
- VGG：簡單深層架構
- ResNet：殘差連接

---

## 延伸閱讀

- [CNN 基礎教程](https://www.google.com/search?q=convolutional+neural+network+tutorial+basics)
- [卷積層詳解](https://www.google.com/search?q=convolution+layer+explained+deep+learning)