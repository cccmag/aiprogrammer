# 量子優化演算法

## 前言

量子優化是量子計算最有前景的應用之一，與機器學習中的超參數調優、特徵選擇、神經網路結構搜尋等問題緊密相關。

## QAOA

量子近似優化演算法（QAOA）是解決組合優化問題的變分方法：

```python
import numpy as np

class QAOA:
    def __init__(self, n_qubits, p_layers=1):
        self.n = n_qubits
        self.p = p_layers
    
    def cost_hamiltonian(self, x):
        """Max-Cut 哈密頓量"""
        # 簡單環狀圖
        cost = 0
        for i in range(self.n):
            j = (i + 1) % self.n
            cost += x[i] * (1 - x[j]) + x[j] * (1 - x[i])
        return -cost
    
    def mixer_hamiltonian(self, x):
        """混合哈密頓量：σx"""
        return np.sum(1 - 2*x)
    
    def circuit(self, gamma, beta):
        """QAOA 電路模擬"""
        # 簡化模擬：直接計算期望值
        best_state = None
        best_cost = float('inf')
        
        for _ in range(100):
            # 隨機初始態
            state = np.random.choice([0, 1], size=self.n)
            
            # 交替演化
            for _ in range(self.p):
                # 問題哈密頓量演化
                cost = self.cost_hamiltonian(state)
                # 混合哈密頓量演化
                for i in range(self.n):
                    if np.random.random() < beta:
                        state[i] = 1 - state[i]
            
            c = self.cost_hamiltonian(state)
            if c < best_cost:
                best_cost = c
                best_state = state
        
        return best_state, best_cost

# 求解 Max-Cut
qaoa = QAOA(n_qubits=6, p_layers=2)
best_state, best_cost = qaoa.circuit(0.5, 0.3)
print(f"最佳分割: {best_state}")
print(f"成本: {best_cost:.1f}")
```

## 量子退火

```python
class QuantumAnnealing:
    def __init__(self, n_spins, T_max=10, steps=1000):
        self.n = n_spins
        self.T_max = T_max
        self.steps = steps
    
    def schedule(self, t):
        """退火排程：線性降溫"""
        return self.T_max * (1 - t / self.steps)
    
    def anneal(self, J, h):
        """量子退火模擬"""
        state = np.random.choice([-1, 1], size=self.n)
        
        for step in range(self.steps):
            T = self.schedule(step)
            # 隨機挑選 spin
            i = np.random.randint(self.n)
            
            # 計算翻轉能量差
            delta_E = 2 * state[i] * (h[i] + np.sum(J[i] * state))
            
            # Metropolis 接受準則
            if delta_E < 0 or np.random.random() < np.exp(-delta_E / T):
                state[i] *= -1
        
        return state

# 範例：Ising 模型
n = 8
J = np.random.randn(n, n) * 0.1
J = (J + J.T) / 2  # 對稱
np.fill_diagonal(J, 0)
h = np.random.randn(n) * 0.05

qa = QuantumAnnealing(n_spins=n)
result = qa.anneal(J, h)
print(f"最低能量配置: {result}")
```

## 在 ML 中的應用

量子優化可解決以下 ML 問題：

1. **特徵選擇**：最大化資訊同時最小化冗餘
2. **聚類**：K-means 初始化優化
3. **神經架構搜尋**：搜尋最佳網路結構
4. **強化學習**：策略搜尋

## 結語

QAOA 和量子退火為 ML 中的 NP-hard 問題提供了新的求解思路。雖然當前硬體規模有限，但隨著量子處理器的發展，量子優化在 ML 中的應用將持續擴大。

---

**延伸閱讀**

- [QAOA 原始論文](https://www.google.com/search?q=Quantum+Approximate+Optimization+Algorithm+Farhi)
- [量子退火 vs QAOA](https://www.google.com/search?q=quantum+annealing+vs+QAOA+comparison)
- [量子優化在 ML 中的應用](https://www.google.com/search?q=quantum+optimization+machine+learning+applications)
