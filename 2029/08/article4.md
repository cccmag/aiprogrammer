# 量子卷積神經網路

## 前言

量子卷積神經網路（QCNN）由 Cong 等人於 2019 年提出，是量子 ML 中結構最完整的深度學習架構之一。

## QCNN 結構

QCNN 包含三個核心元件：量子卷積層（捲積 + 糾纏）、池化層（部分測量 + 棄置）、全連接層（測量分類）。

```python
import numpy as np

def quantum_conv_layer(state, n_qubits):
    """簡單量子卷積：交替單 qubit 旋轉與 CNOT 糾纏"""
    for i in range(n_qubits - 1):
        # 單 qubit 旋轉 (卷積)
        theta = np.pi / 4
        Ry = np.array([[np.cos(theta/2), -np.sin(theta/2)],
                        [np.sin(theta/2),  np.cos(theta/2)]])
        
        # 應用 Ry 閘 (簡化模擬)
        idx = [2*i, 2*i+1]
        
        # CNOT 糾纏 (池化準備)
        pass
    return state
```

## 分層架構

```python
class QCNN:
    def __init__(self, n_qubits, n_classes=2):
        self.n_qubits = n_qubits
        self.n_classes = n_classes
        self.params = np.random.randn(n_qubits * 3)
    
    def conv_layer(self, state, params, idx):
        """卷積層：參數化旋轉 + 最近鄰糾纏"""
        theta = params[idx]
        Ry = np.array([[np.cos(theta/2), -np.sin(theta/2)],
                        [np.sin(theta/2),  np.cos(theta/2)]])
        return Ry @ state
    
    def pool_layer(self, state, keep_qubits):
        """池化層：棄置部分 qubit"""
        # 取前 keep_qubits 個 qubit 的機率
        probs = np.abs(state.reshape(-1, 2**(self.n_qubits - keep_qubits)))**2
        reduced = np.sum(probs, axis=1)
        return reduced / np.sum(reduced)
    
    def forward(self, x):
        state = np.zeros(2**self.n_qubits)
        state[0] = 1.0  # |0...0>
        
        # 編碼
        for i in range(self.n_qubits):
            angle = np.arctan(x[i % len(x)])
            self.conv_layer(state, self.params, i)
        
        # 測量分類
        probs = np.abs(state)**2
        return probs[:self.n_classes] / np.sum(probs[:self.n_classes])

# 測試
model = QCNN(n_qubits=4)
x_test = np.array([0.5, -0.3, 0.8, 0.1])
pred = model.forward(x_test)
print(f"預測機率: {pred}")
```

## QCNN 的優勢

QCNN 具有避免「貧瘠高原」（barren plateau）問題的理論保證，因為其分層結構限制了糾纏程度，使梯度在深層網路中仍然穩定。此外，QCNN 的參數量遠小於古典 CNN。

## 結語

QCNN 是量子深度學習中最有前景的架構之一，在量子化學、量子多體物理和高能物理等領域已有應用案例。

---

**延伸閱讀**

- [QCNN 原始論文](https://www.google.com/search?q=Quantum+Convolutional+Neural+Networks+C+Cong+2019)
- [QCNN 綜述](https://www.google.com/search?q=quantum+convolutional+neural+network+tutorial)
- [Barren Plateau 問題](https://www.google.com/search?q=barren+plateau+quantum+neural+networks)
