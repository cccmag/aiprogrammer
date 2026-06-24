# 混合量子-經典架構

## 分工協作的實用路徑（2021-2029）

### 為什麼需要混合？

2021 年，NISQ 硬體的限制越來越明確：錯誤率太高、量子位元太少、退相干時間太短。但研究者發現了一個務實的出路：**不讓量子計算機做所有事，而是讓它做它最擅長的事**。

混合架構的分工原則：

| 任務 | 適合的處理器 |
|------|-------------|
| 線性代數（大規模） | 經典 GPU/TPU |
| 取樣與糾纏生成 | 量子處理器 |
| 最佳化演算法 | 經典 CPU |
| 特徵映射 | 量子處理器 |
| 梯度計算 | 混合（參數偏移法則） |

### 經典架構

混合量子-經典的基本循環：

```python
class HybridModel:
    def __init__(self, n_qubits: int):
        self.quantum_circuit = VariationalQuantumCircuit(n_qubits)
        self.classical_head = None  # 經典層（如全連接層）
    
    def forward(self, x: list[float]) -> float:
        # 量子部分：特徵提取
        quantum_features = self.quantum_circuit.encode_and_sample(x)
        # 經典部分：後處理
        return self.classical_head(quantum_features) if self.classical_head else quantum_features
```

### 量子資料嵌入

混合模型的關鍵是**如何將經典資料嵌入到量子態**：

1. **角度編碼**：x ∈ [0, 1] → 旋轉角度 x·π。直接但表達能力有限。
2. **振幅編碼**：x → 歸一化向量 → 量子態振幅。指數級高效但難以實現。
3. **IQP 編碼**：基於隨機電路的特徵映射，對經典模擬有抵抗性。

```python
def iqp_encoding(x: list[float], n_qubits: int):
    """IQP-style 量子特徵編碼"""
    circuit = QuantumCircuit(n_qubits)
    for i in range(n_qubits):
        circuit.hadamard(i)
        circuit.rz(i, x[i % len(x)])
    for i in range(n_qubits - 1):
        circuit.cz(i, i + 1)  # 創造糾纏
    return circuit
```

### 端到端訓練

混合模型的訓練需要跨經典-量子邊界的反向傳播。關鍵技巧是**參數偏移法則**（parameter shift rule）：

```python
def parameter_shift(circuit, param_idx, x, shift=math.pi/2):
    """量子電路的解析梯度（無需反向傳播）"""
    cost_plus = circuit.run_with_params(x, param_idx, +shift)
    cost_minus = circuit.run_with_params(x, param_idx, -shift)
    return (cost_plus - cost_minus) / (2 * math.sin(shift))
```

這使量子電路可以被整合到 PyTorch/TensorFlow 的訓練循環中。

### 2029 年的混合典範

目前所有實際的量子 ML 應用都是混合的。IBM Qiskit、Google Cirq、Amazon Braket 都提供了混合編程框架。最重要的進展是**量子-經典計算圖的自動分化**（2024），讓開發者不需要手動處理參數偏移。

混合架構已被證明是近期量子 ML 的唯一可行路徑——它尊重當前硬體的約束，同時為未來全量子演算法預留了升級路徑。

---

**下一步**：[量子 ML 硬體](focus6.md)

## 延伸閱讀

- [Hybrid Quantum-Classical ML 指南](https://www.google.com/search?q=hybrid+quantum+classical+machine+learning)
- [Parameter Shift Rule](https://www.google.com/search?q=parameter+shift+rule+quantum+circuit)
- [Qiskit 混合訓練](https://www.google.com/search?q=Qiskit+hybrid+quantum+classical+training)
