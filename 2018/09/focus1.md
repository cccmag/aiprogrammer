# CNN 發展史：從 LeNet 到 ResNet

## 1. 早期神經網路（1998）

### LeNet-5

Yann LeCun 在 1998 年提出 LeNet-5，是 CNN 的開山之作：

```python
# LeNet-5 架構
# Input: 32x32 灰階影像
# C1: 6 個 5x5 卷積核 -> 28x28
# S2: 2x2 池化 -> 14x14
# C3: 16 個 5x5 卷積 -> 10x10
# S4: 2x2 池化 -> 5x5
# C5: 120 個 5x5 卷積 -> 1x1
# F6: 84 全連接
# Output: 10 分類
```

LeNet-5 主要用於手寫數字辨識（MNIST），開創了CNN 的先河。

## 2. AlexNet（2012）

### ImageNet 競賽突破

```python
# AlexNet 架構（簡化）
# 8 層網路
Conv(11, 11, 96) -> MaxPool(3, 3)  # 224x224 -> 55x55 -> 27x27
Conv(5, 5, 256) -> MaxPool(3, 3)    # 27x27 -> 13x13
Conv(3, 3, 384)                     # 13x13
Conv(3, 3, 384)
Conv(3, 3, 256) -> MaxPool(3, 3)   # 13x13 -> 6x6
FC(4096) -> FC(4096) -> FC(1000)
```

**關鍵創新**：
- ReLU 激活函數
- Dropout 正則化
- GPU 並行訓練
- 資料增強

## 3. VGGNet（2014）

### 簡單而深的架構

```python
# VGG-16 架構
# 全部使用 3x3 卷積核
# 堆疊多層取代大卷積核

Conv(3, 3, 64) x 2 -> MaxPool(2, 2)  # 224 -> 112
Conv(3, 3, 128) x 2 -> MaxPool(2, 2) # 112 -> 56
Conv(3, 3, 256) x 3 -> MaxPool(2, 2) # 56 -> 28
Conv(3, 3, 512) x 3 -> MaxPool(2, 2) # 28 -> 14
Conv(3, 3, 512) x 3 -> MaxPool(2, 2) # 14 -> 7
FC(4096) -> FC(4096) -> FC(1000)
```

**優點**：小卷積核減少參數，層數更深表示能力更強

## 4. GoogLeNet / Inception（2014）

### Inception 模組

```python
# Inception 模組
# 多尺度並行卷積
branch1 = Conv(1, 1, 64) -> Conv(3, 3, 128)   # 1x1 -> 3x3
branch2 = Conv(1, 1, 64) -> Conv(5, 5, 32)    # 1x1 -> 5x5
branch3 = MaxPool(3, 3) -> Conv(1, 1, 64)    # pool -> 1x1
branch4 = Conv(1, 1, 64)                      # 1x1

output = concat([branch1, branch2, branch3, branch4])
```

## 5. ResNet（2015）

### 殘差連接

```python
class ResidualBlock(nn.Module):
    def __init__(self, in_channels, out_channels, stride=1):
        super().__init__()
        self.conv1 = Conv3x3(in_channels, out_channels, stride)
        self.conv2 = Conv3x3(out_channels, out_channels)
        self.shortcut = (stride != 1 or in_channels != out_channels) ? \
            Conv1x1(in_channels, out_channels, stride) : Identity()

    def forward(self, x):
        out = relu(self.conv1(x))
        out = self.conv2(out)
        out += self.shortcut(x)  # 殘差連接
        return relu(out)
```

ResNet 解决了深層網路的梯度消失問題，可以訓練超過 1000 層的網路。

## 6. 發展時間軸

| 年份 | 模型 | 貢獻 |
|------|------|------|
| 1998 | LeNet-5 | CNN 開山之作 |
| 2012 | AlexNet | 深度學習突破，ReLU、Dropout |
| 2014 | VGGNet | 小卷積核、深度網路 |
| 2014 | GoogLeNet | Inception、并行多尺度 |
| 2015 | ResNet | 殘差連接 |

## 7. 小結

從 LeNet 到 ResNet，CNN 經歷了近 20 年的發展。每代架構都在深度、寬度和效率之間取得新的平衡。

---

**下一步**：[卷積層、池化層原理詳解](focus2.md)

## 延伸閱讀

- [CNN History Survey](https://www.google.com/search?q=CNN+history+LeNet+AlexNet+VGG+ResNet)
- [Deep Learning Image Classification](https://www.google.com/search?q=deep+learning+image+classification+history)