# 焦點文章 4：卷積網路架構演進

## 前言

從 1998 年的 LeNet 到現代的深度架構，CNN 經歷了漫長的演進歷程。本章節回顧經典架構的發展脈絡。

## LeNet (1998)

由 Yann LeCun 等人提出，是第一個成功的 CNN 架構：

```
輸入(32x32) → Conv(6) → AvgPool → Conv(16) → AvgPool
         → Flatten → FC(120) → FC(84) → 輸出(10)
```

用於手寫數字辨識（MNIST），達到 99% 以上的準確率。

## AlexNet (2012)

點燃深度學習革命的架構，ImageNet 比賽錯誤率從 26% 降至 15%：

```
輸入(227x227x3) → Conv(96) → MaxPool → Conv(256) → MaxPool
    → Conv(384) → Conv(384) → Conv(256) → MaxPool
    → Flatten → FC(4096) → FC(4096) → 輸出(1000)
```

創新點：
- ReLU 激活函數
- GPU 並行訓練
- Dropout 正則化
- 資料增強

## ZFNet (2013)

對 AlexNet 進行優化，錯誤率降至 11%：

- 調整卷積層通道數
- 優化卷積核大小

## VGGNet (2014)

牛津大學視覺幾何組提出，強調「更深更簡單」：

```
VGG-16:
輸入 → Conv(64)×2 → MaxPool
     → Conv(128)×2 → MaxPool
     → Conv(256)×3 → MaxPool
     → Conv(512)×3 → MaxPool
     → Conv(512)×3 → MaxPool
     → GlobalAvgPool → FC(4096) → FC(4096) → 輸出(1000)
```

特點：
- 全部使用 3×3 卷積核
- 網路深度達 16-19 層
- 結構統一，易於理解和改進

## GoogLeNet (2014)

引入 Inception 模組，減少參數量：

```
Inception 模組：
input → 1x1Conv → 3x3Conv
     → 1x1Conv → 5x5Conv
     → 3x3MaxPool → 1x1Conv
     → 拼接輸出
```

創新點：
- 多尺度特徵融合
- 1×1 卷積降維
- 只 500 萬參數（比 AlexNet 少 12 倍）

## ResNet (2015)

微軟研究院提出，引入殘差連接：

```
輸出 = F(x) + x
```

解決深度網路訓練困難的問題：
- 網路深度可達 152 層
- 殘差連接使梯度直接流向淺層
- ImageNet 錯誤率降至 3.6%

## 架構比較

| 架構 | 年份 | 層數 | Top-5 錯誤率 |
|------|------|------|--------------|
| AlexNet | 2012 | 8 | 15.3% |
| VGG-16 | 2014 | 16 | 7.3% |
| GoogLeNet | 2014 | 22 | 6.7% |
| ResNet-152 | 2015 | 152 | 3.6% |

## 總結

CNN 架構從 LeNet 的簡單設計，演進到更深、更高效的結構。殘差連接的提出解決了深度網路的訓練問題，開啟了更深網路的可能性。

## 延伸閱讀

- https://www.google.com/search?q=CNN+architecture+LeNet+AlexNet+VGG+ResNet
- https://www.google.com/search?q=ResNet+residual+connection+explained