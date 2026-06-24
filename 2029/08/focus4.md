# 量子神經網路

## 量子版的感知機與多層架構（2020-2029）

### 量子神經元

2020 年，多個研究團隊獨立提出了**量子神經網路**（Quantum Neural Network, QNN）的架構。量子神經元是經典感知機的量子類比：

```python
class QuantumNeuron:
    def __init__(self, n_inputs: int):
        self.weights = [random.uniform(0, 2*math.pi)
                        for _ in range(n_inputs)]
        self.bias = random.uniform(0, 2*math.pi)
    
    def forward(self, x: list[float]) -> float:
        phase = sum(w * xi for w, xi in zip(self.weights, x))
        return math.cos(phase + self.bias)**2
```

### 從量子神經元到多層量子網路

量子神經網路的核心組成：

1. **編碼層**：將經典資料 x 映射到量子態 |φ(x)⟩。常見編碼有**角度編碼**（每個特徵對應一個旋轉角度）和**振幅編碼**（將特徵存儲到振幅中）。

2. **可變層**：參數量子電路，包含旋轉閘（RX, RY, RZ）和糾纏閘（CNOT, CZ）。

3. **測量層**：計算期望值作為輸出。

```python
class QuantumNeuralNetwork:
    def __init__(self, n_qubits: int, n_layers: int):
        self.n_qubits = n_qubits
        self.params = [[random.uniform(0, 2*math.pi) for _ in range(4)]
                       for _ in range(n_qubits * n_layers)]
    
    def predict(self, x: list[float]) -> float:
        # 簡化的 QNN 前向傳播
        encoded = [math.cos(xi) for xi in x]
        for layer in self.params:
            # 旋轉 + 糾纏
            pass
        return sum(encoded) / len(x)
```

### 表達能力理論

2021-2022 年，量子神經網路的表達能力被嚴格分析。關鍵發現：

- **量子 ReLU 不存在**：量子運算是么正的（unitray），而 ReLU 非線性不是么正——這導致量子 NN 的啟發函數必須用心巧妙設計。
- **糾纏作為非線性**：量子糾纏本質上提供了一種非經典的非線性，這是量子 NN 可能超越經典 NN 的根源。
- **參數數量**：一個 n 量子位元的量子 NN 對應的參數空間是 O(poly(n))，但其表達的函數可能對應到 O(2ⁿ) 維度的希爾伯特空間。

### 訓練挑戰

QNN 的訓練比經典 NN 困難得多：

1. **荒原高原**再次出現：隨機初始化的 QNN 在深度增加時，梯度呈指數級衰減。
2. **取樣雜訊**：每個梯度估計需要大量量子測量（量子測量的機率性）。
3. **參數對抗**：參數擾動可能導致量子態的急劇變化。

### 2029 年趨勢

量子卷積神經網路（QuCNN）在量子化學和材料科學中顯示了實際優勢。同時，**生成式量子模型**（如量子 GAN、量子擴散模型）開始湧現。但至今，QNN 仍未被證實在實際規模的問題上超越經典深度學習。

---

**下一步**：[混合量子-經典架構](focus5.md)

## 延伸閱讀

- [Quantum Neural Networks 綜述](https://www.google.com/search?q=quantum+neural+networks+survey+2025)
- [QuCNN 架構](https://www.google.com/search?q=quantum+convolutional+neural+network)
- [Quantum GAN](https://www.google.com/search?q=quantum+generative+adversarial+network)
