# DQN 從零實作

## Deep Q-Network 核心概念

DQN（Deep Q-Network）由 DeepMind 在 2013 年提出，首次將深度學習與 Q-learning 結合，在 Atari 遊戲上超越人類水準。核心公式是 Bellman 方程：

```
Q(s, a) = r + γ * max_a' Q(s', a')
```

## 從零實作 DQN

我們用 PyTorch 實作一個可在 CartPole 上運行的 DQN：

```python
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import gymnasium as gym
from collections import deque
import random

class DQN(nn.Module):
    def __init__(self, n_obs, n_actions):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(n_obs, 128), nn.ReLU(),
            nn.Linear(128, 128), nn.ReLU(),
            nn.Linear(128, n_actions))

    def forward(self, x):
        return self.net(x)

class ReplayBuffer:
    def __init__(self, capacity=10000):
        self.buffer = deque(maxlen=capacity)

    def push(self, state, action, reward, next_state, done):
        self.buffer.append((state, action, reward, next_state, done))

    def sample(self, batch_size):
        batch = random.sample(self.buffer, batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)
        return (np.array(states), np.array(actions),
                np.array(rewards, dtype=np.float32),
                np.array(next_states), np.array(dones))

    def __len__(self):
        return len(self.buffer)
```

## 訓練迴圈

DQN 的兩大關鍵技巧：**經驗回放**（Experience Replay）打破時間相關性；**目標網路**（Target Network）穩定訓練：

```python
env = gym.make("CartPole-v1")
n_obs = env.observation_space.shape[0]
n_actions = env.action_space.n

policy_net = DQN(n_obs, n_actions)
target_net = DQN(n_obs, n_actions)
target_net.load_state_dict(policy_net.state_dict())
optimizer = optim.Adam(policy_net.parameters(), lr=1e-3)
buffer = ReplayBuffer(10000)

epsilon = 1.0
gamma = 0.99
batch_size = 64

for episode in range(500):
    state, _ = env.reset()
    total_reward = 0
    for t in range(200):
        if random.random() < epsilon:
            action = env.action_space.sample()
        else:
            with torch.no_grad():
                q = policy_net(torch.FloatTensor(state))
                action = q.argmax().item()

        next_state, reward, done, _, _ = env.step(action)
        buffer.push(state, action, reward, next_state, done)
        state = next_state
        total_reward += reward

        if len(buffer) >= batch_size:
            states, actions, rewards, next_states, dones = buffer.sample(batch_size)
            states = torch.FloatTensor(states)
            actions = torch.LongTensor(actions)
            rewards = torch.FloatTensor(rewards)
            next_states = torch.FloatTensor(next_states)
            dones = torch.FloatTensor(dones)

            current_q = policy_net(states).gather(1, actions.unsqueeze(1))
            next_q = target_net(next_states).max(1)[0].detach()
            target_q = rewards + gamma * next_q * (1 - dones)

            loss = nn.MSELoss()(current_q.squeeze(), target_q)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        if done:
            break

    epsilon = max(0.01, epsilon * 0.995)
    if episode % 10 == 0:
        target_net.load_state_dict(policy_net.state_dict())
        print(f"Episode {episode}, Reward: {total_reward}")
```

## 結語

DQN 是深度強化學習的奠基之作。理解 DQN 後，進階演算法如 Double DQN、Dueling DQN、Rainbow 只是在此基礎上加入個別改良。


**延伸閱讀**
- [Playing Atari with Deep Reinforcement Learning](https://www.google.com/search?q=Playing+Atari+with+Deep+Reinforcement+Learning+Mnih+2013)
- [Human-level control through deep reinforcement learning](https://www.google.com/search?q=Nature+DQN+2015+Mnih)
- [Rainbow: Combining Improvements in Deep Reinforcement Learning](https://www.google.com/search?q=Rainbow+DQN+Hessel+2017)
