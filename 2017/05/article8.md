# 文章 8：深度學習簡介

## 前言

深度學習是機器學習的一個分支，使用多層神經網路自動學習資料的層次化表徵。本章節介紹深度學習的核心概念與發展。

## 什麼是深度學習

深度學習的核心是「深度」神經網路——具有多個隱藏層的神經網路：

```
輸入 → 隱藏層1 → 隱藏層2 → ... → 隱藏層N → 輸出
```

每一層學習不同層次的特徵，從低層的簡單特徵到高層的複雜語義。

## 深度學習的歷史

| 年份 | 里程碑 |
|------|--------|
| 1943 | McCulloch-Pitts 神經元模型 |
| 1958 | 感知器 |
| 1986 | 反向傳播演算法 |
| 2006 | 深度信念網路，深度學習術語誕生 |
| 2012 | AlexNet 突破 ImageNet |
| 2015 | ResNet 解決深度訓練問題 |

## 為什麼現在才成功

深度學習的成功依賴三個條件：

1. **大量資料**：ImageNet 超過 1400 萬張標註圖像
2. **強大算力**：GPU 並行運算大幅加速訓練
3. **更好的演算法**：ReLU、殘差連接、BatchNorm 等

## 深度學習的關鍵技術

### 1. ReLU 激活函數

```python
def relu(x):
    return np.maximum(0, x)
```

解決梯度消失問題，加速收斂。

### 2. 反向傳播

利用鏈式法則計算梯度：

```python
# 誤差反向傳播
delta = output - target
for layer in reversed(network):
    delta = layer.backward(delta)
```

### 3. 批次正規化

```python
def batch_norm(x, gamma, beta, eps=1e-5):
    mu = np.mean(x, axis=0)
    var = np.var(x, axis=0)
    x_norm = (x - mu) / np.sqrt(var + eps)
    return gamma * x_norm + beta
```

### 4. Dropout

```python
def dropout(x, p=0.5):
    mask = (np.random.rand(*x.shape) > p) / (1 - p)
    return x * mask
```

防止過擬合。

## 主要應用領域

| 領域 | 應用 |
|------|------|
| 電腦視覺 | 影像分類、物體偵測、語義分割 |
| 自然語言處理 | 機器翻譯、情感分析、問答系統 |
| 語音辨識 | 語音轉文字、語音合成 |
| 推薦系統 | 個人化推薦 |
| 遊戲 | AlphaGo、Atari 遊戲 |

## 框架生態系

| 框架 | 開發者 |
|------|--------|
| TensorFlow | Google |
| PyTorch | Facebook |
| CNTK | Microsoft |
| MXNet | Amazon |

## 總結

深度學習透過多層非線性變換自動學習資料的層次化表示，在電腦視覺、自然語言處理等領域取得突破性進展。

## 延伸閱讀

- https://www.google.com/search?q=deep+learning+history+milestones
- https://www.google.com/search?q=deep+learning+why+now+big+data+gpu