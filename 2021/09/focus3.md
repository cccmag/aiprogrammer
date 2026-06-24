# 主題三：Q-learning 與深度 Q 網路

## 基於價值的強化學習

### 1. Q-learning 簡介

Q-learning 是最經典的基於價值的強化學習演算法。它直接學習最優動作-價值函數 Q*(s,a)，而不需要學習環境模型。

### 2. Q-learning 演算法

```python
class QLearningAgent:
    def __init__(self, state_space, action_space, learning_rate=0.1, gamma=0.99, epsilon=1.0):
        self.Q = np.zeros((state_space, action_space))
        self.lr = learning_rate
        self.gamma = gamma
        self.epsilon = epsilon
        self.action_space = action_space

    def select_action(self, state):
        if random.random() < self.epsilon:
            return random.randint(0, self.action_space - 1)
        return np.argmax(self.Q[state])

    def update(self, state, action, reward, next_state, done):
        if done:
            target = reward
        else:
            target = reward + self.gamma * np.max(self.Q[next_state])

        self.Q[state, action] += self.lr * (target - self.Q[state, action])

    def decay_epsilon(self, decay_rate=0.995, min_epsilon=0.01):
        self.epsilon = max(self.epsilon * decay_rate, min_epsilon)
```

### 3. Q-learning 的更新規則

Q-learning 使用 TD（Temporal-Difference）學習：

$$Q(s,a) \leftarrow Q(s,a) + \alpha [r + \gamma \max_{a'} Q(s',a') - Q(s,a)]$$

其中：
- α 是學習率
- r 是即時獎勵
- γ 是折扣因子

### 4. Q 表

Q-learning 使用 Q 表存储每个状态-动作对的 Q 值：

```python
import numpy as np

class QTable:
    def __init__(self, state_dims, action_dim):
        self.table = np.zeros((*state_dims, action_dim))

    def get(self, state, action):
        return self.table[state][action]

    def update(self, state, action, value):
        self.table[state][action] = value

    def max_action(self, state):
        return np.argmax(self.table[state])
```

### 5. 深度 Q 網路 (DQN)

當狀態空間很大或連續時，Q 表不再適用。DQN 使用神經網路來近似 Q 函數：

```python
class DQN(nn.Module):
    def __init__(self, state_dim, action_dim, hidden_dim=128):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(state_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, action_dim)
        )

    def forward(self, state):
        return self.network(state)
```

### 6. 經驗回放 (Experience Replay)

DQN 使用經驗回放來打破樣本之間的相關性：

```python
from collections import deque
import random

class ReplayBuffer:
    def __init__(self, capacity=10000):
        self.buffer = deque(maxlen=capacity)

    def push(self, state, action, reward, next_state, done):
        self.buffer.append((state, action, reward, next_state, done))

    def sample(self, batch_size):
        batch = random.sample(self.buffer, batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)
        return (np.array(states), np.array(actions),
                np.array(rewards), np.array(next_states), np.array(dones))

    def __len__(self):
        return len(self.buffer)
```

### 7. 目標網路 (Target Network)

DQN 使用目標網路來穩定訓練：

```python
class DQNAgent:
    def __init__(self, state_dim, action_dim):
        self.q_network = DQN(state_dim, action_dim)
        self.target_network = DQN(state_dim, action_dim)
        self.target_network.load_state_dict(self.q_network.state_dict())

    def update_target(self):
        self.target_network.load_state_dict(self.q_network.state_dict())

    def compute_loss(self, states, actions, rewards, next_states, dones):
        current_q = self.q_network(states).gather(1, actions.unsqueeze(1)).squeeze()
        next_q = self.target_network(next_states).max(1)[0]
        target = rewards + (1 - dones) * self.gamma * next_q

        return F.mse_loss(current_q, target.detach())
```

### 8. 雙 DQN (Double DQN)

雙 DQN 解決 Q 值過估計的問題：

```python
def double_dqn_update(self, states, actions, rewards, next_states, dones):
    next_actions = self.q_network(next_states).argmax(1)
    next_q = self.target_network(next_states).gather(1, next_actions.unsqueeze(1)).squeeze()

    target = rewards + (1 - dones) * self.gamma * next_q
    current_q = self.q_network(states).gather(1, actions.unsqueeze(1)).squeeze()

    return F.mse_loss(current_q, target.detach())
```

---

## 延伸閱讀

- [DQN 論文](https://www.google.com/search?q=Playing+Atari+Deep+Reinforcement+Learning+Mnih)
- [Q-learning 教學](https://www.google.com/search?q=Q-learning+algorithm+tutorial+reinforcement+learning)
- [深度強化學習詳解](https://www.google.com/search?q=deep+Q+network+tutorial+pytorch)