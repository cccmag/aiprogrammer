# VQE 演算法實作

## 前言

變分量子本徵求解器（VQE）是量子化學與量子 ML 的標竿演算法，利用變分原理尋找 Hamiltonian 的基態能量。

## VQE 原理

VQE 採用混合量子-經典架構：量子計算機準備參數化量子電路 $|\psi(\theta)\rangle$，經典計算機優化參數 $\theta$ 以最小化能量期望值 $E(\theta) = \langle\psi(\theta)|H|\psi(\theta)\rangle$。

## Python 實作

以下使用簡單的模擬來展示 VQE 的核心流程：

```python
import numpy as np
from scipy.optimize import minimize

def hamiltonian(params):
    """簡單的 Hamiltonian：H = aZ₀Z₁ + bX₀"""
    a, b = 0.5, 0.3
    return a * params[0] * params[1] + b * params[0]

def ansatz(theta):
    """參數化量子電路： Ry 旋轉 + CNOT 糾纏 """
    return np.array([np.cos(theta/2), 0, 0, np.sin(theta/2)])

def energy(theta):
    state = ansatz(theta)
    # 期望值近似
    return -np.cos(theta) + 0.5 * np.sin(theta)**2

# 經典優化
result = minimize(energy, x0=0.0, method='Nelder-Mead')
print(f"最佳參數: {result.x[0]:.4f}")
print(f"基態能量: {result.fun:.4f}")
```

## 完整流程

實際 VQE 包含以下步驟：

1. 定義問題的 Hamiltonian
2. 選擇參數化量子電路（ansatz）
3. 在量子計算機上測量能量期望值
4. 使用經典優化器更新參數

```python
from functools import partial

def vqe_loop(hamiltonian, ansatz, optimizer, n_iters=100):
    theta = np.random.random()
    history = []
    
    for i in range(n_iters):
        # 量子部分：計算能量
        E = energy(theta)
        history.append(E)
        
        # 經典部分：更新參數
        res = minimize(energy, theta, method='COBYLA')
        theta = res.x[0]
        
        if i % 20 == 0:
            print(f"Iter {i}: E = {E:.4f}")
    
    return theta, history

best_theta, energies = vqe_loop(None, None, None)
```

## 結語

VQE 展示了量子計算在近期的實用價值。它是量子 ML 中變分方法的基石，為量子神經網路等進階演算法奠定了基礎。

---

**延伸閱讀**

- [VQE 文獻](https://www.google.com/search?q=Variational+Quantum+Eigensolver+VQE)
- [變分量子演算法綜述](https://www.google.com/search?q=variational+quantum+algorithms+review)
- [Qiskit VQE 教學](https://www.google.com/search?q=Qiskit+VQE+tutorial+example)
