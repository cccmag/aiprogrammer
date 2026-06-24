# 焦點文章 6：VGG、GoogLeNet、ResNet

## 前言

AlexNet 之後，研究者相繼提出更深、更高效的 CNN 架構。本章節介紹三個影響深遠的架構：VGGNet、GoogLeNet 和 ResNet。

## VGGNet (2014)

牛津大學視覺幾何組提出，特点是「更深更統一」。

### 核心思想

全部使用 3×3 卷積核，逐步加深網路。

為什麼 3×3 卷積更好？

| 多個 3×3 vs 單個 5×5 | 說明 |
|----------------------|------|
| 參數更少 | 3×3×3 = 27 vs 5×5 = 25（感知野相同） |
| 更多非線性 | 每層 ReLU，增加區分能力 |
| 更深 | 可堆疊更多層 |

### VGG-16 結構

```
輸入(224x224x3)
↓ Conv(64)×2
↓ MaxPool
↓ Conv(128)×2
↓ MaxPool
↓ Conv(256)×3
↓ MaxPool
↓ Conv(512)×3
↓ MaxPool
↓ Conv(512)×3
↓ MaxPool
↓ GlobalAvgPool
↓ FC(4096)
↓ FC(4096)
↓ FC(1000)
↓ Softmax
```

### 貢獻

- 證明深度是視覺辨識的關鍵
- 結構統一，易於遷移學習
- 至今仍是遷移學習的熱門基礎網路

## GoogLeNet / Inception (2014)

Google 提出的高效架構，強調計算效率。

### Inception 模組

```python
def inception_module(x, filters_1x1, filters_3x3_reduce,
                     filters_3x3, filters_5x5_reduce, filters_5x5, pool_proj):
    # 1x1 卷積降維
    conv_1x1 = Conv2D(filters_1x1, 1, activation='relu')(x)

    # 1x1 降維後接 3x3
    conv_3x3 = Conv2D(filters_3x3_reduce, 1, activation='relu')(x)
    conv_3x3 = Conv2D(filters_3x3, 3, padding='same', activation='relu')(conv_3x3)

    # 1x1 降維後接 5x5
    conv_5x5 = Conv2D(filters_5x5_reduce, 1, activation='relu')(x)
    conv_5x5 = Conv2D(filters_5x5, 5, padding='same', activation='relu')(conv_5x5)

    # 池化後接 1x1
    pool = MaxPooling2D(pool_size=3, strides=1, padding='same')(x)
    pool_proj = Conv2D(pool_proj, 1, activation='relu')(pool)

    # 拼接所有分支
    return Concatenate()([conv_1x1, conv_3x3, conv_5x5, pool_proj])
```

### 創新點

- 多尺度特徵融合：同時使用 1×1、3×3、5×5 卷積
- 1×1 卷積降維：減少參數量
- 全域平均池化替代 FC：大幅减少參數

### 參數比較

| 架構 | 參數數量 |
|------|----------|
| AlexNet | 6000 萬 |
| VGG-16 | 1.38 億 |
| GoogLeNet | 500 萬 |

## ResNet (2015)

微軟研究院提出，解決深度網路訓練問題。

### 殘差連接

```python
def residual_block(x, filters):
    shortcut = x

    # 主路徑
    out = Conv2D(filters, 3, padding='same', activation='relu')(x)
    out = Conv2D(filters, 3, padding='same')(out)

    # 捷徑連接
    if x.shape[-1] != filters:
        shortcut = Conv2D(filters, 1)(x)

    # 殘差
    out = Add()([out, shortcut])
    out = Activation('relu')(out)

    return out
```

### 核心思想

輸出 = F(x) + x

其中 F(x) 是學習的殘差映射。

### 為什麼有效

1. **梯度直接流動**：短路連接使梯度直接傳到淺層
2. **易於學習**：網路只需學習殘差 F(x) = H(x) - x
3. **不增加額外參數**：捷徑連接幾乎不增加計算量

### 影響

- 首次訓練超過 100 層的 CNN
- 成為電腦視覺的標準骨幹網路
- 獲得 2016 年 CVPR 最佳論文獎

## 總結

VGG、GoogLeNet、ResNet 各自從不同角度推動 CNN 發展：VGG 證明深度重要性、GoogLeNet 展示高效架構、ResNet 解決訓練難題。

## 延伸閱讀

- https://www.google.com/search?q=VGGNet+GoogLeNet+ResNet+comparison
- https://www.google.com/search?q=residual+connection+ResNet+training+deep+networks