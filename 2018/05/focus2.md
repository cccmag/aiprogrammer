# 多層感知器（MLP）：隱藏層與非線性活化

## 前言

多層感知器（Multi-Layer Perceptron, MLP）由輸入層、一或多個隱藏層和輸出層組成。加入隱藏層後，MLP 可以學習任何非線性函數。

## MLP 結構

```
┌─────────────────────────────────────────────────────┐
│                   多層感知器結構                      │
├─────────────────────────────────────────────────────┤
│                                                     │
│   輸入層     隱藏層 1    隱藏層 2    輸出層           │
│                                                     │
│   x1 ────► h1_1 ────► h2_1 ────► y1                │
│   x2 ────► h1_2 ────► h2_2 ────► y2                │
│   x3 ────► h1_3 ────►        ────► ...             │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## 前向傳播

### 單層計算

```
z = W * x + b
a = σ(z)
```

### 多層計算

```python
class MLP:
    def __init__(self, layer_sizes):
        self.weights = []
        self.biases = []

        for i in range(len(layer_sizes) - 1):
            w = np.random.randn(layer_sizes[i], layer_sizes[i+1]) * 0.01
            b = np.zeros((1, layer_sizes[i+1]))
            self.weights.append(w)
            self.biases.append(b)

    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))

    def forward(self, X):
        self.activations = [X]
        self.z_values = []

        for i in range(len(self.weights)):
            z = np.dot(self.activations[-1], self.weights[i]) + self.biases[i]
            self.z_values.append(z)
            a = self.sigmoid(z)
            self.activations.append(a)

        return self.activations[-1]
```

## 万用逼近定理

1989 年，George Cybenko 證明了万用逼近定理：

> 一個具有單個隱藏層的前饋神經網路，只要隱藏層有足夠多的神經元，就可以以任意精度逼近任何連續函數。

這意味著，從理論上來說，一個兩層網路可以解決任何問題。

## 網路設計原則

### 輸入/輸出層

- 輸入層大小取決於特征維度
- 輸出層大小取決於任務（分類=類別數，迴歸=1）

### 隱藏層

1. **寬度**：每層神經元數量
2. **深度**：隱藏層數量
3. **經驗法則**：
   - 單隱藏層通常足夠
   - 隱藏層神經元數量通常在輸入和輸出之間

```
┌─────────────────────────────────────────────────────┐
│              網路架構設計指南                        │
├─────────────────────────────────────────────────────┤
│                                                     │
│   小資料集：                                        │
│   - 較少的隱藏層                                     │
│   - 避免過擬合                                      │
│                                                     │
│   大資料集：                                        │
│   - 可以使用更多隱藏層                               │
│   - 更寬的網路                                       │
│                                                     │
│   複雜任務：                                        │
│   - 需要更深的網路                                   │
│   - 考慮 CNN、RNN 等特殊架構                        │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## 結語

多層感知器是深度學習的基礎。雖然 MLP 在處理圖像和序列資料時不如 CNN 和 RNN 高效，但它是理解深度學習原理的最好起點。

下一篇文章將介紹活化函數，這是類神經網路非線性能力的來源。

---

## 延伸閱讀

- [MLP 詳細教程](https://www.google.com/search?q=multilayer+perceptron+tutorial)
- [萬用逼近定理證明](https://www.google.com/search?q=universal+approximation+theorem+neural+network)
- [深度網路設計原則](https://www.google.com/search?q=neural+network+architecture+design)

---

*本篇文章為「AI 程式人雜誌 2018 年 5 月號」類神經網路導論系列之一。*