# 焦點文章 5：AlexNet 突破性貢獻

## 前言

2012 年 AlexNet 在 ImageNet 比賽中以前所未有的優勢奪冠，標志著深度學習時代的來臨。本章節分析 AlexNet 的創新與影響。

## 比賽背景

ImageNet Large Scale Visual Recognition Challenge (ILSVRC)：
- 1000 個類別
- 120 萬訓練圖像
- 10 萬測試圖像
- Top-5 錯誤率評估

2010 年冠軍錯誤率：28%
2011 年冠軍錯誤率：26%

## AlexNet 架構

```python
# 簡化版 AlexNet
model = [
    # Conv1 + MaxPool + Norm
    Conv(11, 11, 96, stride=4, padding=0),
    MaxPool(3, 3, stride=2),
    LocalResponseNorm(size=5, alpha=0.0001, beta=0.75),

    # Conv2 + MaxPool + Norm
    Conv(5, 5, 256, padding=2),
    MaxPool(3, 3, stride=2),
    LocalResponseNorm(size=5, alpha=0.0001, beta=0.75),

    # Conv3-5
    Conv(3, 3, 384, padding=1),
    Conv(3, 3, 384, padding=1),
    Conv(3, 3, 256, padding=1),
    MaxPool(3, 3, stride=2),

    # FC layers
    Flatten(),
    FC(4096),
    Dropout(0.5),
    FC(4096),
    Dropout(0.5),
    FC(1000),
    Softmax()
]
```

## 五大創新

### 1. ReLU 激活函數

```python
# 首次在 CNN 中大規模使用 ReLU
def relu(x):
    return np.maximum(0, x)
```

好處：
- 計算效率高
- 收斂速度比 Sigmoid 快 6 倍
- 減輕梯度消失問題

### 2. GPU 並行訓練

- 使用 2 張 NVIDIA GTX 580 GPU
- 將網路分為兩部分，分別在兩張卡上運行
- 大幅縮短訓練時間

### 3. Dropout 正則化

```python
# 訓練時隨機丢弃神經元
h = fc(Wx + b)
h = Dropout(h, p=0.5)
```

防止過擬合，提高泛化能力。

### 4. 重疊池化

池化窗口大於步長：

```python
# 窗口 3x3，步長 2（重疊）
MaxPool(3, 3, stride=2)
```

### 5. 資料增強

訓練時隨機變換：
- 水平翻轉
- 隨機裁剪
- 色彩晃動

## 比賽結果

| 方法 | Top-5 錯誤率 |
|------|--------------|
| 傳統方法 (2011) | 26.2% |
| **AlexNet (2012)** | **15.3%** |
| 第二名 (2012) | 26.2% |

AlexNet 以巨大優勢奪冠，引發學術界對深度學習的熱潮。

## 歷史意義

1. **證明深度學習潛力**：深層網路可以從大量數據中學習有效特徵
2. **推動 GPU 運算**：深度學習需要強大算力
3. **開源精神**：AlexNet 團隊公開程式碼
4. **研究熱潮**：後續 CNN 架構如雨後春筍

## 總結

AlexNet 的成功是多重因素共同作用的結果：正確的網路架構、高效的激活函數、GPU 並行計算、有效的正則化與充足的訓練數據。

## 延伸閱讀

- https://www.google.com/search?q=AlexNet+2012+ImageNet+breakthrough
- https://www.google.com/search?q=AlexNet+architecture+ReLU+Dropout