# Q-learning 演算法

## 基於價值的強化學習

Q-learning 是一種無模型的強化學習算法，學習動作價值函數 Q(s, a)。

核心思想：
- 估計 Q(s, a)：在狀態 s 執行動作 a 的長期價值
- 選擇最高 Q 值的動作

## Q 表

對於小型狀態空間，可以使用表格存储 Q 值。

```python
import numpy as np

# 離散狀態空間：10 個狀態
# 離散動作空間：4 個動作
n_states = 10
n_actions = 4

# Q 表
Q = np.zeros((n_states, n_actions))

def choose_action(state, epsilon=0.1):
    if np.random.random() < epsilon:
        return np.random.randint(n_actions)
    else:
        return np.argmax(Q[state])
```

## Q-learning 更新規則

Q(s, a) ← Q(s, a) + α [r + γ max_{a'} Q(s', a') - Q(s, a)]

- α：學習率
- γ：折扣因子
- r：當前獎賞
- s'：下一狀態

```python
def q_update(Q, state, action, reward, next_state, alpha=0.1, gamma=0.9):
    """Q-learning 更新"""
    best_next_action = np.argmax(Q[next_state])
    td_target = reward + gamma * Q[next_state, best_next_action]
    td_error = td_target - Q[state, action]
    Q[state, action] += alpha * td_error

# 等價寫法
def q_update_v2(Q, state, action, reward, next_state, alpha=0.1, gamma=0.9):
    Q[state, action] += alpha * (reward + gamma * np.max(Q[next_state]) - Q[state, action])
```

## 完整的 Q-learning 代理

```python
class QLearningAgent:
    def __init__(self, n_states, n_actions, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.n_states = n_states
        self.n_actions = n_actions
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.Q = np.zeros((n_states, n_actions))

    def choose_action(self, state):
        if np.random.random() < self.epsilon:
            return np.random.randint(self.n_actions)
        return np.argmax(self.Q[state])

    def learn(self, state, action, reward, next_state):
        self.Q[state, action] += self.alpha * (
            reward + self.gamma * np.max(self.Q[next_state]) - self.Q[state, action]
        )

    def decay_epsilon(self, decay_rate=0.99, min_epsilon=0.01):
        self.epsilon = max(self.epsilon * decay_rate, min_epsilon)
```

## 示範：懸浮桿問題（CartPole）

```python
import gym

env = gym.make('CartPole-v0')
n_states = env.observation_space.n
n_actions = env.action_space.n

agent = QLearningAgent(n_states, n_actions)

# 訓練
n_episodes = 1000

for episode in range(n_episodes):
    state = env.reset()

    for t in range(100):
        action = agent.choose_action(state)
        next_state, reward, done, _ = env.step(action)

        agent.learn(state, action, reward, next_state)
        state = next_state

        if done:
            break

    if episode % 100 == 0:
        print(f"Episode {episode}: steps = {t+1}")

env.close()
```

## 連續狀態空間的離散化

現實問題的狀態空間通常是連續的，需要離散化處理。

```python
class Discretizer:
    def __init__(self, n_bins, low, high):
        self.n_bins = n_bins
        self.low = low
        self.high = high

    def discretize(self, state):
        # 將連續狀態映射到離散箱子
        bins = (state - self.low) / (self.high - self.low) * self.n_bins
        bins = np.clip(bins, 0, self.n_bins - 1).astype(int)
        return tuple(bins)

# 使用
low = env.observation_space.low
high = env.observation_space.high
discretizer = Discretizer(n_bins=10, low=low, high=high)

state = env.reset()
discrete_state = discretizer.discretize(state)
```

## 示範：懸浮桿（連續狀態）

```python
import gym

class SARSAAgent:
    def __init__(self, n_bins, n_actions, alpha=0.1, gamma=0.99, epsilon=0.1):
        self.n_bins = n_bins
        self.n_actions = n_actions
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.Q = np.zeros([n_bins] * 4 + [n_actions])

    def discretize(self, state, low, high, n_bins):
        bins = (state - low) / (high - low) * n_bins
        return tuple(np.clip(bins.astype(int), 0, n_bins - 1))

    def choose_action(self, state):
        if np.random.random() < self.epsilon:
            return np.random.randint(self.n_actions)
        return np.argmax(self.Q[state])

    def learn(self, state, action, reward, next_state):
        next_action = self.choose_action(next_state)
        self.Q[state + (action,)] += self.alpha * (
            reward + self.gamma * self.Q[next_state + (next_action,)] -
            self.Q[state + (action,)]
        )

# 訓練 CartPole
env = gym.make('CartPole-v0')
n_actions = env.action_space.n

# 觀察空間的範圍
low = env.observation_space.low
high = env.observation_space.high

agent = SARSAAgent(n_bins=10, n_actions=n_actions)

for episode in range(500):
    state = agent.discretize(env.reset(), low, high, 10)
    action = agent.choose_action(state)

    for t in range(200):
        next_state_raw, reward, done, _ = env.step(action)
        next_state = agent.discretize(next_state_raw, low, high, 10)

        agent.learn(state, action, reward, next_state)

        state = next_state
        action = agent.choose_action(state) if not done else None

        if done:
            break

    if episode % 50 == 0:
        print(f"Episode {episode}: {t+1} steps")

env.close()
```

## Sarsa（另一種 TD 學習）

Sarsa 與 Q-learning 的差異：
- Sarsa 使用實際選擇的下一動作更新
- Q-learning 使用最大 Q 值的動作更新（離策略）

```python
class SarsaAgent:
    def learn(self, state, action, reward, next_state, next_action):
        self.Q[state, action] += self.alpha * (
            reward + self.gamma * self.Q[next_state, next_action] -
            self.Q[state, action]
        )
```

## Q-learning vs Sarsa

| | Q-learning | Sarsa |
|---|---|---|
| 類型 | 離策略（off-policy） | 在策略（on-policy） |
| 更新 | 使用最佳下一動作 | 使用實際選擇的下一動作 |
| 收斂 | 更直接 | 可能更保守 |
| 應用 | 理論分析較易 | 實際訓練較穩 |

## 總結

Q-learning 是強化學習的核心算法之一：
- 學習動作價值函數 Q(s, a)
- 使用 TD 學習從樣本中更新
- 透過 epsilon-greedy 平衡探索與利用
- 適用於離散狀態空間的問題