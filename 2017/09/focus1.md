# 強化學習概述

## 基本概念

強化學習涉及的核心元件：

- **Agent（代理人）**：學習並做決策的實體
- **Environment（環境）**：代理人所在的外部系統
- **State（狀態）**：當前環境的描述
- **Action（動作）**：代理人可執行的行為
- **Reward（獎賞）**：動作的好壞信號
- **Policy（策略）**：狀態到動作的映射

## 互動流程

```
時間步 t:
1. 代理人觀察狀態 s_t
2. 根據策略 π(a|s)，選擇動作 a_t
3. 環境接收動作，給予獎賞 r_t
4. 環境轉移到新狀態 s_{t+1}
5. 代理人更新策略

重複直到任務完成
```

## 回合（Episode）

強化學習任務通常分為多個 episode（回合）。

- **Terminal State**：任務結束的狀態
- **Starting State**：回合開始的初始狀態
- **Return**：一個回合的總獎賞

## 累積獎賞

代理人最大化的是未來獎賞的加权和。

### 有限時域回報

G_t = r_t + r_{t+1} + r_{t+2} + ... + r_T

### 無限時域折扣回報

G_t = r_t + γr_{t+1} + γ²r_{t+2} + ...

其中 γ ∈ [0, 1] 是折扣因子。

```python
def compute_return(rewards, gamma=0.9):
    """計算折扣回報"""
    G = 0
    for i, r in enumerate(rewards):
        G += (gamma ** i) * r
    return G

rewards = [1, 2, 3, 4, 5]
print(compute_return(rewards, gamma=0.9))
# = 1 + 0.9*2 + 0.81*3 + 0.729*4 + 0.6561*5
```

## 價值函數

### 狀態價值函數 V(s)

在狀態 s 開始，遵循策略 π 的預期回報：

V^π(s) = E_π[G_t | s_t = s]

### 動作價值函數 Q(s, a)

在狀態 s 執行動作 a，之後遵循策略 π 的預期回報：

Q^π(s, a) = E_π[G_t | s_t = s, a_t = a]

### 優勢函數

A(s, a) = Q(s, a) - V(s)

表示動作 a 相對於平均的好坏程度。

## 探索與利用

### 貪心策略（Greedy）

總是選擇最高 Q 值的動作，但容易陷入局部最優。

### E-greedy

以 ε 機率隨機選擇（探索），其餘選擇最佳動作（利用）。

```python
import random

def e_greedy(q_values, epsilon):
    if random.random() < epsilon:
        return random.randint(0, len(q_values) - 1)
    else:
        return q_values.index(max(q_values))
```

### Softmax / Boltzmann

根據機率分布選擇，溫度參數控制隨機性。

```python
import numpy as np

def softmax(q_values, temperature=1.0):
    q = np.array(q_values) / temperature
    exp_q = np.exp(q - np.max(q))  # 數值穩定化
    probs = exp_q / exp_q.sum()
    return np.random.choice(len(q_values), p=probs)
```

## 學習類型

### 基於模型（Model-based）

先學環境模型，再進行規劃。

```python
# 概念
class ModelBasedRL:
    def __init__(self):
        self.transition_model = {}  # P(s'|s,a)
        self.reward_model = {}      # R(s,a)

    def learn_model(self, experience):
        # 從經驗更新模型
        pass

    def plan(self, state):
        # 使用模型規劃
        pass
```

### 無模型（Model-free）

直接從經驗學習策略或價值。

```python
# Q-learning 是無模型方法
class ModelFreeRL:
    def update(self, state, action, reward, next_state):
        # 直接從(s,a,r,s')更新
        pass
```

## 多臂拉霸問題（Multi-Armed Bandit）

強化学習的入門問題。

```python
class Bandit:
    def __init__(self, n_arms):
        self.n_arms = n_arms
        self.true_rewards = [random.gauss(0, 1) for _ in range(n_arms)]

    def pull(self, arm):
        return self.true_rewards[arm] + random.gauss(0, 0.1)

def solve_bandit(n_arms, n_steps):
    bandit = Bandit(n_arms)

    estimated_rewards = [0] * n_arms
    counts = [0] * n_arms

    for _ in range(n_steps):
        epsilon = 0.1
        if random.random() < epsilon:
            arm = random.randint(0, n_arms - 1)
        else:
            arm = estimated_rewards.index(max(estimated_rewards))

        reward = bandit.pull(arm)
        counts[arm] += 1
        estimated_rewards[arm] += (reward - estimated_rewards[arm]) / counts[arm]

    return estimated_rewards
```

## 總結

強化學習的核心是代理人透過與環境互動學習最佳策略。關鍵概念包括：狀態、動作、獎賞、策略、價值函數。理解這些基礎對於學習後續的 Q-learning、DQN 等演算法至關重要。