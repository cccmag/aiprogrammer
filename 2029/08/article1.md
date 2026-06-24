# 量子計算基礎

## 前言

量子機器學習（Quantum ML）是量子計算與機器學習的交叉領域。要理解這個領域，首先需要掌握量子計算的核心概念。

## 量子位元

不同於古典位元只能是 0 或 1，量子位元（qubit）可以處於疊加態：$|\psi\rangle = \alpha|0\rangle + \beta|1\rangle$，其中 $|\alpha|^2 + |\beta|^2 = 1$。

```python
import numpy as np

# 量子態向量表示
zero = np.array([1, 0])   # |0>
one  = np.array([0, 1])   # |1>

# 疊加態：Hadamard 變換的結果
plus = (zero + one) / np.sqrt(2)  # |+>
print(f"|+> = {plus}")
```

## 量子閘

量子閘是作用在 qubit 上的么正變換。常見的單 qubit 閘包括 Pauli 矩陣：

```python
def apply_gate(state, gate):
    return gate @ state

# Pauli 矩陣
X = np.array([[0, 1], [1, 0]])
H = np.array([[1, 1], [1, -1]]) / np.sqrt(2)

# 應用 Hadamard 閘產生疊加態
result = apply_gate(zero, H)
print(f"H|0> = {result}")  # 產生 |+>
```

## 量子糾纏

糾纏是量子計算的關鍵資源。Bell 態是典型的糾纏態：

```python
# CNOT 閘
CNOT = np.array([
    [1,0,0,0],
    [0,1,0,0],
    [0,0,0,1],
    [0,0,1,0]
])

# 產生 Bell 態 |Φ+>
bell_state = CNOT @ np.kron(plus, zero)
print(f"Bell state: {bell_state}")
```

## 量子測量

測量會使量子態坍縮到古典位元：

```python
def measure(state, shots=1000):
    prob = np.abs(state)**2
    outcomes = np.random.choice(len(state), size=shots, p=prob)
    return outcomes

# 測量 |+> 態：0 和 1 各約 50%
outcomes = measure(plus, shots=10000)
print(f"P(0) = {np.mean(outcomes == 0):.3f}")
```

## 結語

量子位元的疊加、糾纏與干涉特性，賦予了量子計算超越古典計算的潛力。這些基礎概念是後續理解量子機器學習演算法的基石。

---

**延伸閱讀**

- [量子計算概述](https://www.google.com/search?q=%E9%87%8F%E5%AD%90%E8%A8%88%E7%AE%97%E5%9F%BA%E7%A4%8E)
- [Quantum Machine Learning arXiv](https://www.google.com/search?q=quantum+machine+learning+survey+2024)
- [IBM Qiskit 教學](https://www.google.com/search?q=Qiskit+quantum+computing+tutorial)
