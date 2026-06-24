# 多層感知器 MLP

## 從理論到架構

多層感知器（Multilayer Perceptron, MLP）是最基本的神經網路架構，由輸入層、一個或多個隱藏層以及輸出層組成。每一層由多個神經元組成，層與層之間全連接。

```
輸入層        隱藏層          輸出層
  x1 ────┐
          ├─── h1 ────┐
  x2 ────┤            │
          ├─── h2 ────┼─── y1
  x3 ────┤            │
          ├─── h3 ────┘
  x4 ────┘
```

## MLP 的數學定義

一個 L 層 MLP 的計算過程可以描述為：

```
z^(1) = W^(1)·x + b^(1)
a^(1) = σ^(1)(z^(1))

z^(2) = W^(2)·a^(1) + b^(2)
a^(2) = σ^(2)(z^(2))

...

y = a^(L) = σ^(L)(z^(L))
```

其中 W^(l) 是權重矩陣，b^(l) 是偏置向量，σ^(l) 是啟用函數。

## 通用近似定理

MLP 最重要的一個理論結果是通用近似定理（Universal Approximation Theorem）：

> 一個具有至少一個隱藏層的前饋神經網路，只要隱藏層有足夠多的神經元，就可以以任意精度逼近任何連續函數。

### 直觀理解

這意味著：
- MLP 可以學習任何從輸入到輸出的連續映射
- 隱藏層的寬度（神經元數量）決定了表示能力
- 深度（層數）可以指數級地減少所需的神經元數量

### 限制

通用近似定理只告訴我們存在性，沒有告訴我們如何找到合適的權重。實際訓練中，我們需要：
- 足夠的資料
- 合適的網路架構
- 有效的訓練演算法
- 恰當的超參數

## 隱藏層的意義

### 特徵轉換

隱藏層的作用是將輸入資料轉換到新的表示空間。每一層都在學習更高層次的特徵：

```
原始輸入 → 低階特徵 → 中階特徵 → 高階特徵 → 決策
像素    → 邊緣    → 形狀    → 物體部件 → 分類
```

### 非線性

如果沒有非線性啟用函數，多層網路將等價於單層網路：

```
W2·(W1·x + b1) + b2 = (W2·W1)·x + (W2·b1 + b2) = W'·x + b'
```

這就是為什麼每個隱藏層之後都需要非線性啟用函數。

## 實戰考量

### 架構設計

```python
model = MLP(
    sizes=[784, 256, 128, 10],
    activations=['relu', 'relu', 'softmax']
)
```

設計原則：
- 神經元數量逐層遞減
- 隱藏層數量和大小取決於問題複雜度
- 輸出層大小由任務決定（分類=類別數，回歸=1）

### 初始化

權重初始化對訓練非常重要：

```python
# Xavier 初始化（適用於 Sigmoid/Tanh）
std = math.sqrt(2.0 / (n_in + n_out))
W = np.random.randn(n_out, n_in) * std

# He 初始化（適用於 ReLU）
std = math.sqrt(2.0 / n_in)
W = np.random.randn(n_out, n_in) * std
```

### 訓練流程

```python
for epoch in range(num_epochs):
    for batch in batches:
        # 前向傳播
        predictions = model.forward(batch.x)
        # 計算損失
        loss = cross_entropy(predictions, batch.y)
        # 反向傳播
        model.backward(batch.y)
        # 更新權重
        model.update(learning_rate)
```

## MLP 的局限性

1. **參數效率低**：全連接層隨著神經元數量增加，參數量呈平方級增長
2. **無法處理結構化資料**：對圖像、序列等結構化資料沒有先驗知識
3. **容易過擬合**：參數量大，需要大量資料和正則化

這些局限推動了 CNN、RNN 等更專業架構的發展。

---

## 延伸閱讀

- [Universal Approximation Theorem](https://www.google.com/search?q=universal+approximation+theorem+neural+network)
- [MLP 實戰指南](https://www.google.com/search?q=multilayer+perceptron+tutorial+python)
- [Weight Initialization](https://www.google.com/search?q=neural+network+weight+initialization+xavier+he)

*本篇文章為「AI 程式人雜誌 2022 年 1 月號」歷史回顧系列之一。*
