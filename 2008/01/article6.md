# 類神經網路的早期發展

## 前言

類神經網路（Neural Network）是人工智慧領域中最重要的技術之一。雖然深度學習在 2010 年代才爆發，但類神經網路的概念和早期研究可以追溯到 1950 年代。本文回顧類神經網路的早期發展歷程。

## 類神經網路的起源

### 1943年：McCulloch-Pitts 神經元

類神經網路的歷史始於 1943 年：

```python
# McCulloch-Pitts 神經元模型概念
class MCPNeuron:
    def __init__(self, weights, threshold):
        self.weights = weights
        self.threshold = threshold

    def activate(self, inputs):
        # 加權總和
        total = sum(w * x for w, x in zip(self.weights, inputs))
        # 階梯函數輸出
        return 1 if total >= self.threshold else 0
```

這是第一個神經網路的數學模型，雖然簡單，但奠定了日後發展的基礎。

## 感知器（Perceptron）

### 1958年：Frank Rosenblatt

Frank Rosenblatt 發明了感知器，這是第一個具有學習能力的演算法：

```
┌────────────────────────────────────┐
│         感知器模型                  │
│                                    │
│    輸入 ──→ [Σ] ──→ 輸出           │
│            ↑                       │
│            │ w                     │
│         權重                       │
│                                    │
└────────────────────────────────────┘
```

### 感知器學習演算法

```python
class Perceptron:
    def __init__(self, num_inputs, learning_rate=0.1):
        self.weights = [0.0] * num_inputs
        self.bias = 0.0
        self.lr = learning_rate

    def predict(self, inputs):
        weighted_sum = sum(w * x for w, x in zip(self.weights, inputs))
        return 1 if weighted_sum + self.bias > 0 else 0

    def train(self, training_data, epochs):
        for _ in range(epochs):
            for inputs, label in training_data:
                prediction = self.predict(inputs)
                error = label - prediction
                # 更新權重
                for i in range(len(inputs)):
                    self.weights[i] += self.lr * error * inputs[i]
```

## 第一次 AI 冬天

### 1969年：Minsky 的批評

1969 年，Marvin Minsky 和 Seymour Papert 發表了《感知器》一書，嚴厲批評了感知器的限制：

| 限制 | 說明 |
|------|------|
| 線性不可分 | 無法解決 XOR 問題 |
| 單層網路限制 | 只有一個神經元層 |
| 計算複雜度 | 硬體無法支援 |

```
XOR 問題：
輸入 A  XOR  B = 輸出
  0    ⊕    0  =   0
  0    ⊕    1  =   1
  1    ⊕    0  =   1
  1    ⊕    1  =   0

感知器無法學習這個模式！
```

這導致了類神經網路研究的停滯，被稱為「第一次 AI 冬天」。

## 多層感知器與反向傳播

### 突破：多層網路

1986 年，Rumelhart、Hinton 和 Williams 發表了反向傳播（Backpropagation）演算法：

```python
class MultiLayerPerceptron:
    def __init__(self, layer_sizes):
        # 初始化網路結構
        self.weights = []
        for i in range(len(layer_sizes) - 1):
            self.weights.append(
                [[0.0 for _ in range(layer_sizes[i])]
                 for _ in range(layer_sizes[i+1])]
            )

    def forward(self, inputs):
        activations = inputs
        for weight in self.weights:
            activations = self._sigmoid(
                [[sum(a*w for a, w in zip(act, col))]
                 for col in zip(*weight)]
            )
        return activations

    def backprop(self, inputs, target, learning_rate):
        # 計算輸出層誤差
        output = self.forward(inputs)
        error = target - output

        # 反向傳播誤差
        for layer in reversed(range(len(self.weights))):
            # 更新權重
            pass  # 簡化
```

### 反向傳播的核心概念

```
┌──────────────────────────────────────┐
│         反向傳播演算法               │
├──────────────────────────────────────┤
│                                      │
│  前向傳播：輸入 → 隱藏層 → 輸出      │
│                                      │
│  計算誤差：輸出與目標的差異          │
│                                      │
│  反向傳播：誤差 → 隱藏層 → 輸入      │
│                                      │
│  更新權重：根據誤差調整              │
│                                      │
└──────────────────────────────────────┘
```

## 支援向量機的競爭

### 1990年代的對手

在類神經網路復甦的同時，支援向量機（SVM）也興起了：

| 特性 | 類神經網路 | 支援向量機 |
|------|-----------|-----------|
| 學習方式 | 梯度下降 | 最大化邊界 |
| 理論基礎 | 启发式 | 統計學習理論 |
| 效能 | 好 | 非常好 |
| 調參難度 | 高 | 中等 |
| 大規模資料 | 慢 | 可扩展 |

### 主流地位的交替

```
1990s-2000s：
類神經網路 ──→ 研究社群邊緣化
支援向量機 ──→ 主流方法
```

## 淺層網路的極限

### 2000 年代初期的困境

類神經網路面臨的問題：

```python
challenges = {
    "梯度消失": "深層網路訓練困難",
    "區域最小值": "容易陷入局部最佳解",
    "過擬合": "泛化能力不足",
    "計算成本": "訓練時間過長",
    "特徵工程": "需要手動特徵提取"
}
```

### 淺層 vs 深層

| 架構 | 隱藏層數 | 能力 |
|------|----------|------|
| 淺層網路 | 1-2 層 | 有限 |
| 深層網路 | 3+ 層 | 強大但難訓練 |

## 離散學習的进展

### Hopfield 網路（1982）

John Hopfield 提出了離散類神經網路：

```python
class HopfieldNetwork:
    def __init__(self, size):
        self.weights = [[0.0] * size for _ in range(size)]

    def store(self, patterns):
        for pattern in patterns:
            for i in range(len(pattern)):
                for j in range(len(pattern)):
                    if i != j:
                        self.weights[i][j] += pattern[i] * pattern[j]

    def recall(self, pattern, iterations=10):
        for _ in range(iterations):
            for i in range(len(pattern)):
                activation = sum(
                    self.weights[i][j] * pattern[j]
                    for j in range(len(pattern))
                )
                pattern[i] = 1 if activation > 0 else -1
        return pattern
```

### Boltzmann 機

受限玻爾茲曼機（RBM）成為日後深度學習的基石。

## 2008 年的類神經網路

### 當時的狀況

2008 年時，類神經網路的情況：

- **研究社群**：小規模但穩定
- **主流應用**：語音辨識、金融預測
- **深度學習**：即將興起
- **硬體支援**：GPU 運算開始普及

### 即將到來的突破

```
即將到來的發展（2008-2012）：

2008：Netflix Prize 展現神經網路潛力
2009：深度學習在語音辨識突破
2010：ImageNet 競賽開始
2011：深度學習在電腦視覺進展
2012：AlexNet 突破，CIFAR-10 影像分類
```

## 早期研究的啟示

### 成功的關鍵因素

類神經網路最終成功的因素：

```python
success_factors = {
    "資料": "大規模標註資料庫（如 ImageNet）",
    "算力": "GPU 通用運算",
    "演算法": "預訓練、ReLU、Dropout",
    "軟體": "Theano、Torch、TensorFlow",
    "商業驅動": "語音辨識、翻譯需求"
}
```

---

**延伸閱讀**

- [Neural network history](https://www.google.com/search?q=neural+network+history)
- [Perceptron+history](https://www.google.com/search?q=Perceptron+history)
- [Deep+learning+origins](https://www.google.com/search?q=deep+learning+origins)