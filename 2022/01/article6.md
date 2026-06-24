# 卷積神經網路 CNN

## 為什麼需要卷積？

MLP 處理圖像的基本問題是：
1. **參數爆炸**：224×224 的彩色圖像，輸入就有 150528 個像素。第一層 1024 個神經元 → 1.5 億個參數
2. **缺乏平移不變性**：貓在圖像的左側還是右側，應該被視為同一個特徵
3. **忽略空間結構**：全連接層打亂了像素之間的空間關係

卷積神經網路（Convolutional Neural Network, CNN）通過**局部連接**、**權重共享**和**池化**來解決這些問題。

## 卷積運算

卷積操作使用一個小型的「濾波器（kernel）」在輸入圖像上滑動：

```
輸入圖像 (5×5)         濾波器 (3×3)          輸出特徵圖 (3×3)
┌───┬───┬───┬───┬───┐  ┌───┬───┬───┐  ┌───┬───┬───┐
│ 1 │ 0 │ 2 │ 1 │ 0 │  │ 1 │ 0 │ 1 │  │ 7 │ 6 │ 4 │
├───┼───┼───┼───┼───┤  ├───┼───┼───┤  ├───┼───┼───┤
│ 0 │ 1 │ 1 │ 2 │ 1 │  │ 0 │ 1 │ 0 │  │ 8 │ 7 │ 5 │
├───┼───┼───┼───┼───┤  ├───┼───┼───┤  ├───┼───┼───┤
│ 2 │ 0 │ 1 │ 0 │ 2 │  │ 1 │ 0 │ 1 │  │ 6 │ 8 │ 6 │
├───┼───┼───┼───┼───┤  └───┴───┴───┘  └───┴───┴───┘
│ 1 │ 2 │ 0 │ 1 │ 1 │
├───┼───┼───┼───┼───┤
│ 0 │ 1 │ 1 │ 0 │ 1 │
└───┴───┴───┴───┴───┘
```

### 特徵視覺化

不同濾波器檢測不同的特徵：

```
濾波器 1（邊緣檢測）：
-1  0  1
-1  0  1    →  檢測垂直邊緣
-1  0  1

濾波器 2（水平邊緣）：
-1  -1  -1
 0   0   0   →  檢測水平邊緣
 1   1   1
```

## CNN 的核心組件

### 卷積層

```python
conv = nn.Conv2d(
    in_channels=3,    # 輸入通道數（RGB=3）
    out_channels=64,  # 輸出通道數（濾波器數量）
    kernel_size=3,    # 濾波器大小（3×3）
    stride=1,         # 步長
    padding=1         # 填充
)
```

### 池化層

池化降低特徵圖的空間尺寸，減少參數並提供平移不變性：

```python
# 最大池化：取 2×2 區域中的最大值
pool = nn.MaxPool2d(kernel_size=2, stride=2)
```

```
池化前 (4×4)         MaxPool 2×2        池化後 (2×2)
 2  5  1  3                          5  6
 7  3  8  2          ────────→       8  9
 4  1  9  6
 0  3  2  5
```

## LeNet-5 架構

LeNet-5 是第一個成功的 CNN 架構，由 Yann LeCun 在 1998 年提出，用於手寫數字識別：

```
輸入 (32×32)
    ↓
Conv1 (6@28×28) — 5×5 卷積
    ↓
Pool1 (6@14×14) — 2×2 平均池化
    ↓
Conv2 (16@10×10) — 5×5 卷積
    ↓
Pool2 (16@5×5) — 2×2 平均池化
    ↓
FC3 (120) — 全連接
    ↓
FC4 (84) — 全連接
    ↓
輸出 (10) — Softmax
```

## 現代 CNN 架構

### AlexNet（2012）

- 5 卷積層 + 3 全連接層
- 首次使用 ReLU 和 Dropout
- ImageNet 競賽的轉折點

### VGG（2014）

- 全使用 3×3 卷積
- 16-19 層
- 簡單而有效的設計原則

### ResNet（2015）

- 引入殘差連接
- 可訓練 152+ 層
- ImageNet 錯誤率首次低於人類

### EfficientNet（2019）

- 使用神經架構搜索優化深度、寬度和解析度
- 在計算量約束下達到最佳效能

## CNN 的 PyTorch 實作

```python
class SimpleCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 32, 3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, 3, padding=1)
        self.conv3 = nn.Conv2d(64, 128, 3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc = nn.Linear(128 * 4 * 4, 10)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.pool(self.relu(self.conv1(x)))  # 32×16×16
        x = self.pool(self.relu(self.conv2(x)))  # 64×8×8
        x = self.pool(self.relu(self.conv3(x)))  # 128×4×4
        x = x.view(-1, 128 * 4 * 4)
        x = self.fc(x)
        return x
```

## 結論

CNN 通過三種關鍵技術——局部連接、權重共享和池化——為圖像處理提供了高效的特徵提取方式。從 LeNet 到 EfficientNet，CNN 的演進推動了電腦視覺領域的革命。

---

## 延伸閱讀

- [LeNet-5 1998](https://www.google.com/search?q=LeNet+5+Yann+LeCun+1998)
- [CS231n CNN 課程](https://www.google.com/search?q=CS231n+convolutional+neural+networks)
- [CNN 視覺化解釋](https://www.google.com/search?q=CNN+visualization+feature+maps)

*本篇文章為「AI 程式人雜誌 2022 年 1 月號」精選文章。*
