# Qiskit/Pennylane 實戰

## 前言

Qiskit（IBM）和 PennyLane（Xanadu）是目前最主流的量子 ML 框架。本文透過實例展示兩者如何協作。

## Qiskit 基礎

```python
# 安裝：pip install qiskit pennylane
from qiskit import QuantumCircuit, Aer, execute

# 建立量子電路
qc = QuantumCircuit(2, 2)
qc.h(0)               # Hadamard 閘
qc.cx(0, 1)           # CNOT 閘
qc.measure([0, 1], [0, 1])

# 執行模擬
backend = Aer.get_backend('qasm_simulator')
result = execute(qc, backend, shots=1024).result()
counts = result.get_counts()
print(f"測量結果: {counts}")
```

## PennyLane 量子 ML

PennyLane 支援自動微分，可直接與 PyTorch 整合：

```python
import pennylane as qml
import numpy as np

# 定義量子裝置
dev = qml.device('default.qubit', wires=2)

@qml.qnode(dev)
def quantum_circuit(x, weights):
    """參數化量子電路"""
    qml.RY(x[0], wires=0)
    qml.RY(x[1], wires=1)
    qml.RX(weights[0], wires=0)
    qml.RX(weights[1], wires=1)
    qml.CNOT(wires=[0, 1])
    return qml.expval(qml.PauliZ(0))

# 自動微分
weights = np.array([0.5, -0.3])
x = np.array([0.8, 0.2])

energy = quantum_circuit(x, weights)
grad = qml.grad(quantum_circuit)(x, weights)
print(f"能量: {energy:.4f}")
print(f"梯度: {grad}")
```

## Qiskit + PennyLane 整合

```python
import pennylane as qml

# 使用 Qiskit 模擬器作為後端
dev = qml.device('qiskit.aer', wires=3, shots=1000)

@qml.qnode(dev)
def hybrid_circuit(x):
    for i in range(3):
        qml.RY(x[i], wires=i)
    qml.CNOT(wires=[0, 1])
    qml.CNOT(wires=[1, 2])
    return [qml.expval(qml.PauliZ(i)) for i in range(3)]

# 訓練資料
X_train = np.random.randn(10, 3)
y_train = np.random.randint(0, 2, 10)

# 使用梯度下降優化
opt = qml.AdamOptimizer(stepsize=0.1)
params = np.random.randn(3)

for step in range(50):
    params = opt.step(lambda p: hybrid_circuit(p)[0], params)
    if step % 10 == 0:
        print(f"Step {step}: {params}")
```

## 結語

Qiskit 提供完整的量子硬體模擬生態，PennyLane 則專注於量子 ML 的自動微分。兩者結合可實現從量子電路設計到混合模型訓練的完整工作流程。

---

**延伸閱讀**

- [Qiskit 文件](https://www.google.com/search?q=Qiskit+documentation+quantum+computing)
- [PennyLane 教學](https://www.google.com/search?q=PennyLane+quantum+machine+learning+tutorial)
- [Qiskit + PennyLane 整合](https://www.google.com/search?q=Qiskit+PennyLane+integration+hybrid)
