# 焦點文章 3：激活函數：神經網路的非線性変換

## 前言

激活函數（Activation Function）是神經網路中不可或缺的元件，它們為網路引入非線性，使網路能夠學習複雜模式。本章節介紹常見的激活函數及其特性。

## 為什麼需要激活函數

如果沒有激活函數，神經網路無論有多少層，都只是線性變換：

```
a⁽ˡ⁾ = W⁽ˡ⁾a⁽ˡ⁻¹⁾ + b⁽ˡ⁾
```

多層線性變換可以化簡為單層線性變換，無法處理非線性問題。

激活函數引入了非線性，使網路能夠：
- 學習複雜的輸入輸出關係
- 表達非線性決策邊界
- 實現函數逼近

## 常見激活函數

### Sigmoid 函數

```
σ(x) = 1 / (1 + e^(-x))
```

特性：
- 輸出範圍：(0, 1)
- 適用於二元分類輸出層
- 梯度在兩端趨近於 0（梯度消失問題）

### Tanh 函數

```
tanh(x) = (e^x - e^(-x)) / (e^x + e^(-x))
```

特性：
- 輸出範圍：(-1, 1)
- 零點對稱，收斂更快
- 同樣存在梯度消失問題

### ReLU（Rectified Linear Unit）

```
ReLU(x) = max(0, x)
```

特性：
- 輸出範圍：[0, +∞)
- 計算高效，收斂快速
- 可能導致「dying ReLU」問題（梯度為 0）

### Leaky ReLU

```
LeakyReLU(x) = max(αx, x)，其中 α 通常為 0.01
```

特性：
- 解決 ReLU 的 dying 問題
-允許負值有小幅梯度

### ELU（Exponential Linear Unit）

```
ELU(x) = x, if x > 0
ELU(x) = α(e^x - 1), if x ≤ 0
```

特性：
- 輸出接近零均值
- 收斂較快

## 激活函數比較

| 函數 | 輸出範圍 | 計算成本 | 梯度消失 |
|------|----------|----------|----------|
| Sigmoid | (0,1) | 中 | 嚴重 |
| Tanh | (-1,1) | 中 | 嚴重 |
| ReLU | [0,∞) | 低 | 輕微 |
| Leaky ReLU | (-∞,∞) | 低 | 無 |
| ELU | (-∞,∞) | 中 | 無 |

## 選擇指南

- **隱藏層**：優先使用 ReLU，嘗試 Leaky ReLU 或 ELU
- **輸出層**：
  - 二元分類：Sigmoid
  - 多類分類：Softmax
  - 回歸：Linear 或 ReLU（正值輸出時）

## 總結

激活函數是神經網路非線性的來源。現代深度學習主要使用 ReLU 及其變體，它們在計算效率和收斂速度上都有優勢。

## 延伸閱讀

- https://www.google.com/search?q=activation+functions+neural+network+ReLU+sigmoid
- https://www.google.com/search?q=dying+ReLU+problem+solution