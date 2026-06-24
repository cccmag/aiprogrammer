# 主題二：馬可夫決策過程

## MDP 與價值函數

### 1. 馬可夫決策過程簡介

馬可夫決策過程（Markov Decision Process，MDP）是強化學習的數學框架。MDP 假設系統的未來只與當前狀態有關，與過去歷史無關，這就是所謂的「馬可夫性」。

### 2. MDP 的組成要素

MDP 由以下要素組成：

**狀態空間（State Space）S**：
- 環境可能處的所有狀態集合
- 可以是離散的或連續的

**動作空間（Action Space）A**：
- 智能體可以執行的所有動作集合
- 離散的或連續的

**轉移函數（Transition Function）P**：
- P(s'|s,a) = 在狀態 s 執行動作 a 後轉移到 s' 的機率

**獎勵函數（Reward Function）R**：
- R(s,a,s') = 執行動作後得到的獎勵
- R(s,a) 或 R(s) 也是常見形式

**折扣因子（Discount Factor）γ**：
- 0 ≤ γ < 1
- 控制未來獎勵的重要性

### 3. 策略（Policy）

策略定義了在每個狀態下應該選擇什麼動作：

```python
class Policy:
    def select_action(self, state):
        """根據狀態返回動作"""
        raise NotImplementedError
```

**確定性策略**：π(s) = a
**隨機策略**：π(a|s) = P(a|s)

### 4. 軌跡與回報

**軌跡（Trajectory）**：
τ = (s₀, a₀, r₀, s₁, a₁, r₁, ...)

**回報（Return）**：
$$G_t = r_t + \gamma r_{t+1} + \gamma^2 r_{t+2} + ... = \sum_{k=0}^{\infty} \gamma^k r_{t+k}$$

折扣因子 γ 的作用：
- γ = 0：只關注即時獎勵
- γ = 1：平等對待所有獎勵
- 0 < γ < 1：折扣未來獎勵，確保總和收斂

### 5. 價值函數

價值函數衡量某個狀態或狀態-動作對的「好壞」：

**狀態價值函數 V^π(s)**：
$$V^\pi(s) = \mathbb{E}_\pi [G_t | s_t = s]$$

在策略 π 下，從狀態 s 開始的期望回報。

**動作價值函數 Q^π(s,a)**：
$$Q^\pi(s,a) = \mathbb{E}_\pi [G_t | s_t = s, a_t = a]$$

在狀態 s 執行動作 a，然後遵循策略 π 的期望回報。

### 6. Bellman 方程

價值函數滿足 Bellman 方程：

**V^π 的 Bellman 方程**：
$$V^\pi(s) = \sum_a \pi(a|s) \sum_{s'} P(s'|s,a) [R(s,a,s') + \gamma V^\pi(s')]$$

**Q^π 的 Bellman 方程**：
$$Q^\pi(s,a) = \sum_{s'} P(s'|s,a) [R(s,a,s') + \gamma \sum_{a'} \pi(a'|s') Q^\pi(s',a')]$$

### 7. 最優策略

強化學習的目標是找到最優策略 π*：

$$V^*(s) = \max_\pi V^\pi(s)$$
$$Q^*(s,a) = \max_\pi Q^\pi(s,a)$$

**Bellman 最優方程**：
$$V^*(s) = \max_a \sum_{s'} P(s'|s,a) [R(s,a,s') + \gamma V^*(s')]$$

$$Q^*(s,a) = \sum_{s'} P(s'|s,a) [R(s,a,s') + \gamma \max_{a'} Q^*(s',a')]$$

### 8. Python 實現簡單 MDP

```python
import numpy as np

class SimpleMDP:
    def __init__(self):
        self.states = [0, 1, 2, 3, 4]
        self.actions = [0, 1]  # 0: 左, 1: 右
        self.P = {
            (0, 0): {0: (0.9, 0, 0.0), 1: (0.1, 4, 0.0)},
            (0, 1): {0: (0.9, 1, 0.0), 1: (0.1, 4, 0.0)},
            (1, 0): {0: (0.9, 0, 0.0), 1: (0.1, 2, 0.0)},
            (1, 1): {0: (0.9, 0, 0.0), 1: (0.1, 2, 0.0)},
            (2, 0): {0: (0.9, 1, 0.0), 1: (0.1, 3, 0.0)},
            (2, 1): {0: (0.9, 1, 0.0), 1: (0.1, 3, 0.0)},
            (3, 0): {0: (0.9, 2, 0.0), 1: (0.1, 4, 0.0)},
            (3, 1): {0: (0.9, 2, 0.0), 1: (0.1, 4, 0.0)},
            (4, 0): {0: (1.0, 4, 1.0), 1: (0.1, 0, 0.0)},
            (4, 1): {0: (0.1, 0, 0.0), 1: (1.0, 4, 1.0)},
        }

    def step(self, state, action):
        transitions = self.P[(state, action)]
        probs = [t[0] for t in transitions.values()]
        next_states = list(transitions.keys())
        idx = np.random.choice(len(probs), p=probs)
        next_state, reward = transitions[next_states[idx]][1], transitions[next_states[idx]][2]
        return next_state, reward
```

---

## 延伸閱讀

- [MDP 教學](https://www.google.com/search?q=Markov+decision+process+tutorial+reinforcement+learning)
- [動態規劃與強化學習](https://www.google.com/search?q=dynamic+programming+reinforcement+learning+Sutton)
- [價值迭代與策略迭代](https://www.google.com/search?q=value+iteration+policy+iteration+MDP)