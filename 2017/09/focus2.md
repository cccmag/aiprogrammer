# 馬可夫決策過程

## MDP 定義

馬可夫決策過程（Markov Decision Process, MDP）是強化學習的數學框架。

一個 MDP 由四元組定義：**(S, A, P, R)**

- **S**：狀態空間（所有可能狀態的集合）
- **A**：動作空間（所有可能動作的集合）
- **P**：轉移機率 P(s'|s, a)
- **R**：獎賞函數 R(s, a, s')

## 馬可夫性質

未來只依賴於當前狀態，與過去歷史無關。

P(s_{t+1} | s_t, a_t, s_{t-1}, a_{t-1}, ...) = P(s_{t+1} | s_t, a_t)

這就是所謂的「無記憶」性質。

## 轉移機率

P(s'|s, a) 表示在狀態 s 執行動作 a 後，轉移到狀態 s' 的機率。

```python
import numpy as np

# 狀態數量
n_states = 3
n_actions = 2

# 轉移機率矩陣 P[s, s', a]
# P[s, s', a] = P(s' | s, a)
P = np.zeros((n_states, n_states, n_actions))

# 範例：簡單的 3 狀態 MDP
# 狀態 0: 左
# 狀態 1: 中
# 狀態 2: 右

# 動作 0: 向左
P[0, 0, 0] = 0.8  # 向左後停留在左側（邊界）
P[0, 1, 0] = 0.2  # 向左後移動到中間

# 動作 1: 向右
P[2, 2, 1] = 0.8  # 向右後停留在右側（邊界）
P[2, 1, 1] = 0.2  # 向右後移動到中間
```

## 獎賞函數

R(s, a, s') 或 R(s, a) 表示在狀態 s 執行動作 a 後（可能轉移到 s'）獲得的獎賞。

```python
# R(s, a, s') 形式
R = np.zeros((n_states, n_actions, n_states))

# 範例：
# 到達狀態 2（右側邊界）給予 +1 獎賞
R[1, 1, 2] = 1.0  # 從中間向右到右側

# 到達狀態 0（左側邊界）給予 -1 獎賞（懲罰）
R[1, 0, 0] = -1.0  # 從中間向左到左側

# 其他狀態無獎賞
```

## 策略（Policy）

策略 π(a|s) 是在狀態 s 選擇動作 a 的機率分布。

### 確定性策略

π(a|s) = 1 對於某個特定動作

```python
# 確定性策略：始終選擇最大 Q 值的動作
def greedy_policy(Q, state):
    return Q[state].index(max(Q[state]))
```

### 隨機策略

π(a|s) 可以是多個動作的機率分布

```python
# 隨機策略
def stochastic_policy(Q, state, epsilon=0.1):
    n_actions = len(Q[state])
    probs = [epsilon / n_actions] * n_actions
    best_action = Q[state].index(max(Q[state]))
    probs[best_action] += 1 - epsilon
    return np.random.choice(n_actions, p=probs)
```

## 價值函數的貝爾曼方程

### 狀態價值函數

V^π(s) = Σ_a π(a|s) Σ_{s'} P(s'|s,a) [R(s,a,s') + γV^π(s')]

### 動作價值函數

Q^π(s,a) = Σ_{s'} P(s'|s,a) [R(s,a,s') + γ Σ_{a'} π(a'|s') Q^π(s',a')]

## 求解 MDP

### 價值迭代（Value Iteration）

```python
def value_iteration(P, R, n_states, n_actions, gamma=0.9, theta=1e-8, max_iterations=1000):
    V = np.zeros(n_states)

    for _ in range(max_iterations):
        V_old = V.copy()

        for s in range(n_states):
            q_values = []
            for a in range(n_actions):
                # Q(s,a) = Σ_s' P(s'|s,a)[R(s,a,s') + γV(s')]
                q = sum(P[s, s_prime, a] * (R[s, a, s_prime] + gamma * V_old[s_prime])
                       for s_prime in range(n_states))
                q_values.append(q)

            V[s] = max(q_values)

        # 收斂檢查
        if np.max(np.abs(V - V_old)) < theta:
            break

    # 提取最佳策略
    policy = np.zeros(n_states, dtype=int)
    for s in range(n_states):
        q_values = [sum(P[s, s_prime, a] * (R[s, a, s_prime] + gamma * V[s_prime])
                       for s_prime in range(n_states))
                   for a in range(n_actions)]
        policy[s] = np.argmax(q_values)

    return V, policy
```

### 策略迭代（Policy Iteration）

```python
def policy_iteration(P, R, n_states, n_actions, gamma=0.9, max_iterations=1000):
    # 初始隨機策略
    policy = np.random.randint(0, n_actions, n_states)

    for _ in range(max_iterations):
        # 策略評估
        V = policy_evaluation(policy, P, R, n_states, n_actions, gamma)

        # 策略改進
        policy_stable = True
        for s in range(n_states):
            old_action = policy[s]

            q_values = [sum(P[s, s_prime, a] * (R[s, a, s_prime] + gamma * V[s_prime])
                        for s_prime in range(n_states))
                       for a in range(n_actions)]
            policy[s] = np.argmax([sum(q) for q in q_values])

            if old_action != policy[s]:
                policy_stable = False

        if policy_stable:
            break

    return V, policy

def policy_evaluation(policy, P, R, n_states, n_actions, gamma, theta=1e-8):
    V = np.zeros(n_states)

    while True:
        V_old = V.copy()

        for s in range(n_states):
            a = policy[s]
            V[s] = sum(P[s, s_prime, a] * (R[s, a, s_prime] + gamma * V_old[s_prime])
                      for s_prime in range(n_states))

        if np.max(np.abs(V - V_old)) < theta:
            break

    return V
```

## 舉例：機器人導航

```python
# 5x5 格子世界
# 狀態：25 個格子 (0-24)
# 動作：上下左右 (0,1,2,3)
# 目標：到達右上角 (+1 獎賞)
# 陷阱：左上角 (-1 獎賞)

n_states = 25
n_actions = 4
grid_size = 5

# 轉移與獎賞
P = np.zeros((n_states, n_states, n_actions))
R = np.zeros((n_states, n_actions, n_states))

goal_state = 24  # 右上角
trap_state = 0   # 左上角

for s in range(n_states):
    row, col = s // grid_size, s % grid_size

    for a in range(n_actions):
        # 定義轉移（這裡省略邊界處理）
        pass

# 求解
V, policy = value_iteration(P, R, n_states, n_actions)
print(f"Optimal Value Function: {V}")
print(f"Optimal Policy: {policy}")
```

## 總結

MDP 提供了強化學習的數學框架。價值迭代和策略迭代是求解 MDP 的經典方法。理解 MDP 的四元組 (S, A, P, R) 和貝爾曼方程是學習 Q-learning 的基礎。