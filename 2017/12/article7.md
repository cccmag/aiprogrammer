# 電腦視覺：CNN 架構演進

## 前言

從 2012 年 AlexNet 到 2017 年的 SENet，CNN 架構經歷了巨大演進。讓我們回顧這個歷程。

## CNN 架構時間線

```
┌─────────────────────────────────────────────────────────┐
│              CNN 架構演進                               │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  2012: AlexNet - 8層, 60M 參數, 錯誤率 15.3%           │
│                                                         │
│  2013: ZFNet - 8層, 改進卷積架構, 錯誤率 14.8%         │
│                                                         │
│  2014: VGGNet - 16/19層, 簡單架構, 錯誤率 7.3%        │
│                                                         │
│  2014: GoogLeNet - 22層, Inception, 錯誤率 6.7%       │
│                                                         │
│  2015: ResNet - 152層, 殘差連接, 錯誤率 3.6%           │
│                                                         │
│  2016: DenseNet - 269層, 密集連接, 錯誤率 3.0%         │
│                                                         │
│  2017: SENet - 154層, Squeeze-and-Excitation, 2.3%    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## AlexNet (2012)

```python
class AlexNet(nn.Module):
    def __init__(self, num_classes=1000):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 96, kernel_size=11, stride=4),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2),
            nn.Conv2d(96, 256, kernel_size=5, padding=2),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2),
            nn.Conv2d(256, 384, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(384, 384, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(384, 256, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2),
        )
        self.classifier = nn.Sequential(
            nn.Dropout(p=0.5),
            nn.Linear(256 * 5 * 5, 4096),
            nn.ReLU(inplace=True),
            nn.Dropout(p=0.5),
            nn.Linear(4096, 4096),
            nn.ReLU(inplace=True),
            nn.Linear(4096, num_classes),
        )
```

## ResNet (2015)

```python
class ResidualBlock(nn.Module):
    expansion = 1

    def __init__(self, in_channels, out_channels, stride=1):
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels, out_channels,
                              kernel_size=3, stride=stride, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.conv2 = nn.Conv2d(out_channels, out_channels,
                              kernel_size=3, stride=1, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(out_channels)

        if stride != 1 or in_channels != out_channels:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_channels, out_channels,
                         kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(out_channels)
            )
        else:
            self.shortcut = nn.Identity()

    def forward(self, x):
        out = torch.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        out += self.shortcut(x)
        out = torch.relu(out)
        return out
```

## DenseNet (2017)

```python
class DenseBlock(nn.ModuleList):
    def __init__(self, num_layers, in_channels, growth_rate):
        super().__init__()
        for i in range(num_layers):
            self.append(self._make_layer(in_channels + i * growth_rate, growth_rate))

    def forward(self, x):
        features = [x]
        for layer in self:
            new_feature = layer(torch.cat(features, dim=1))
            features.append(new_feature)
        return torch.cat(features, dim=1)
```

## SENet (2017)

```python
class SEBlock(nn.Module):
    """Squeeze-and-Excitation Block"""
    def __init__(self, channels, reduction=16):
        super().__init__()
        self.squeeze = nn.AdaptiveAvgPool2d(1)
        self.excitation = nn.Sequential(
            nn.Linear(channels, channels // reduction),
            nn.ReLU(inplace=True),
            nn.Linear(channels // reduction, channels),
            nn.Sigmoid()
        )

    def forward(self, x):
        b, c, _, _ = x.size()
        y = self.squeeze(x).view(b, c)
        y = self.excitation(y).view(b, c, 1, 1)
        return x * y.expand_as(x)
```

## 預訓練模型使用

```python
import torchvision.models as models

# 直接載入使用
resnet18 = models.resnet18(pretrained=True)
alexnet = models.alexnet(pretrained=True)
vgg16 = models.vgg16(pretrained=True)
densenet121 = models.densenet121(pretrained=True)
```

---

**延伸閱讀**

- [AlexNet Paper](https://www.google.com/search?q=AlexNet+Krizhevsky+2012)
- [ResNet Paper](https://www.google.com/search?q=ResNet+He+2016)
- [SENet Paper](https://www.google.com/search?q=SENet+Hu+2018)

---

*本篇文章為「AI 程式人雜誌 2017 年 12 月號」年終回顧系列之一。*