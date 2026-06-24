# 人工神經網路復興

## 前言

2008 年是人工神經網路復甦的關鍵年份。雖然深度學習還未爆發，但研究社群已經開始積蓄力量。GPU 運算的興起即將徹底改變類神經網路的命運。

## 類神經網路的歷史

### 早期發展

```python
neural_network_history = {
    "1943": "McCulloch-Pitts 神經元模型",
    "1958": "Rosenblatt 感知器",
    "1969": "Minsky 批評感知器極限",
    "1986": "反向傳播演算法復甦"
}
```

### 第一次 AI 冬天

1969 年 Minsky 和 Papert 的書導致類神經網路研究停滯了近 20 年：

```
問題：感知器無法解決 XOR 問題

XOR 真值表：
A ⊕ B = 輸出
0 ⊕ 0 = 0
0 ⊕ 1 = 1
1 ⊕ 0 = 1
1 ⊕ 1 = 0
```

## 多層網路與反向傳播

### 突破：隱藏層

```python
# 多層網路可以解決 XOR 問題

xor_network = {
    "輸入層": "2 個神經元",
    "隱藏層": "2 個神經元（關鍵！）",
    "輸出層": "1 個神經元",
    "結果": "可以學習 XOR 函數"
}
```

### 反向傳播演算法

1986 年，Rumelhart、Hinton 和 Williams 重新發現了反向傳播：

```
┌──────────────────────────────────────┐
│         反向傳播原理                  │
├──────────────────────────────────────┤
│                                      │
│  前向傳播：                           │
│  輸入 → 隱藏層 → 輸出層              │
│                                      │
│  計算誤差：                           │
│  輸出誤差 = 期望輸出 - 實際輸出       │
│                                      │
│  反向傳播：                           │
│  誤差信號 → 隱藏層 → 輸入層           │
│                                      │
│  權重更新：                           │
│  新權重 = 舊權重 + 學習率 × 誤差梯度   │
│                                      │
└──────────────────────────────────────┘
```

## 2008 年的類神經網路

### 當時的應用

```python
nn_applications_2008 = {
    "手寫辨識": "銀行支票、郵件分類",
    "語音辨識": "早期語音輸入系統",
    "時間序列預測": "金融市場預測",
    "影像壓縮": "神經網路編碼"
}
```

### 效能限制

```python
# 2008 年的限制

nn_limitations = {
    "訓練時間": "大型網路需要數天",
    "區域最小值": "容易陷入局部最佳解",
    "過擬合": "泛化能力不足",
    "超參數": "難以調整"
}
```

## GPU 運算的影響

### 為何 GPU 適合類神經網路？

```python
# 類神經網路的矩陣運算

matrix_operations = {
    "輸入 × 權重": "矩陣乘法 (矩陣 × 矩陣)",
    "誤差反向": "轉置矩陣乘法",
    "特性": "高度平行，大量相同運算"
}

# GPU 的優勢
gpu_advantages = {
    "大量核心": "數百到數千個核心",
    "平行能力": "適合矩陣運算",
    "成本": "比超級電腦便宜"
}
```

### 效能提升

```
GPU 對類神經網路訓練的加速：

訓練時間縮減：
- 原本（CPU）：數天 → 數小時
- 加速比：10-100 倍（取決於網路規模）
```

## 深度學習的萌芽

### 淺層 vs 深層

```python
# 深度網路的優勢

deep_vs_shallow = {
    "淺層網路": "1-2 隱藏層，易訓練但表達力有限",
    "深層網路": "3+ 隱藏層，表達力強但訓練困難",
    "深度學習": "使用新技術訓練深層網路"
}
```

### 重要的前期工作

```python
# 深度學習之前的關鍵技術

pretraining_techniques = {
    "Hinton (2006)": "深度信念網路的貪心逐層預訓練",
    "Bengio (2007)": "自編碼器預訓練",
    "Ranzato (2007)": "Sparse Coding"
}
```

## 訓練技巧

### 漸進式訓練

```python
# 深度網路的訓練策略

training_strategy = {
    "1. 貪心預訓練": "逐層訓練自編碼器",
    "2. 微調": "使用反向傳播完整訓練",
    "3. 正則化": "Dropout（2014 年才發明）"
}
```

### 啟動函數的改進

```python
activation_functions = {
    "Sigmoid": "傳統，但容易梯度消失",
    "Tanh": "改善，但仍有問題",
    "ReLU (2010)": "Rectified Linear Unit，大幅改善"
}

# ReLU: f(x) = max(0, x)
# 解決梯度消失問題，訓練速度大幅提升
```

## 研究方向

### 2008 年的熱門研究

```python
research_topics_2008 = {
    "卷積神經網路 (CNN)": "影像辨識",
    "循環神經網路 (RNN)": "序列資料處理",
    "受限玻爾茲曼機 (RBM)": "生成模型",
    "自編碼器": "降維和特徵學習"
}
```

### 重要論文

```python
important_papers_before_2008 = {
    "1998": "LeCun - LeNet-5 (CNN for digits)",
    "2006": "Hinton - Deep Belief Networks",
    "2007": "Ng - Sparse Autoencoders"
}
```

## 即將到來的突破

### 為何 2009-2012 是關鍵期？

```python
reasons_for_breakthrough = {
    "GPU 普及": "ATI 和 NVIDIA 的顯示卡效能提升",
    "ImageNet": "大型標註資料集（2009）",
    "AlexNet": "2012 年的突破性結果",
    "軟體成熟": "Theano, Caffe, TensorFlow"
}
```

### 即將發生的里程碑

```python
upcoming_milestones = {
    "2009": "Ng 和 Stanford 的 GPU 深度學習論文",
    "2010": "Speech recognition with deep RNNs",
    "1": "2012AlexNet wins ImageNet with deep CNN"
}
```

## 程式範例

### 簡單的類神經網路（概念）

```python
# 概念化的類神經網路訓練

class SimpleNeuralNetwork:
    def __init__(self, layers):
        self.weights = []
        for i in range(len(layers) - 1):
            self.weights.append(
                [[0.0 for _ in range(layers[i])]
                 for _ in range(layers[i+1])]
            )

    def sigmoid(self, x):
        return 1.0 / (1.0 + math.exp(-x))

    def forward(self, inputs):
        activations = inputs
        for weight in self.weights:
            activations = [self.sigmoid(sum(a*w for a, w in zip(row, activations)))
                          for row in weight]
        return activations

    def train(self, inputs, targets, learning_rate=0.1):
        # Forward pass
        output = self.forward(inputs)

        # Backward pass (simplified)
        # ... 反向傳播實作

        return output
```

---

**延伸閱讀**

- [Neural network history](https://www.google.com/search?q=neural+network+history)
- [Deep+learning+origins](https://www.google.com/search?q=deep+learning+origins)
- [GPU+deep+learning](https://www.google.com/search?q=GPU+deep+learning)