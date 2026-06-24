# OpenAI Gym 入門

## Gym 簡介

OpenAI Gym 是強化學習的標準環境庫，提供各種任務環境，用於開發和比較強化學習演算法。

```bash
pip install gym
```

## 基本使用

```python
import gym

# 創建環境
env = gym.make('CartPole-v0')

# 重置環境
state = env.reset()

# 環境互動
for _ in range(1000):
    env.render()  # 顯示環境

    action = env.action_space.sample()  # 隨機動作
    state, reward, done, info = env.step(action)  # 執行動作

    if done:
        state = env.reset()  # 回合結束，重置

env.close()
```

## 環境結構

```python
# 觀察空間
print(env.observation_space)
# Box(4,) - 4 維連續空間

print(env.observation_space.low)   # 觀察空間下界
print(env.observation_space.high)  # 觀察空間上界

# 動作空間
print(env.action_space)
# Discrete(2) - 2 個離散動作

print(env.action_space.n)  # 動作數量
```

## 離散動作環境

### CartPole

平衡桿子：
- 動作：0（向左推）、1（向右推）
- 觀察：位置、速度、角度、角速度
- 獎賞：每步 +1
- 結束：角度過大或超出邊界

```python
import gym

env = gym.make('CartPole-v0')
n_episodes = 10

for episode in range(n_episodes):
    state = env.reset()
    total_reward = 0

    for t in range(200):
        action = env.action_space.sample()  # 或使用學習到的策略
        state, reward, done, _ = env.step(action)
        total_reward += reward

        if done:
            print(f"Episode {episode+1}: {t+1} steps, reward = {total_reward}")
            break

env.close()
```

### Atari 遊戲

```python
import gym

# 安裝依賴後可以使用 Atari
# pip install gym[atari]
env = gym.make('SpaceInvaders-v0')

state = env.reset()
for _ in range(1000):
    env.render()
    action = env.action_space.sample()  # 隨機或學習到的策略
    state, reward, done, _ = env.step(action)

    if done:
        state = env.reset()

env.close()
```

## 連續動作環境

### MountainCarContinuous

連續動作空間：

```python
env = gym.make('MountainCarContinuous-v0')
print(env.action_space)
# Box(1,) - 1 維連續空間，範圍 [-1, 1]
```

### 執行連續動作

```python
state = env.reset()
action = env.action_space.sample()  # 陣列，如 [0.15]
next_state, reward, done, _ = env.step(action)
```

## 自定義環境

```python
import gym
from gym import spaces
import numpy as np

class MyEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super().__init__()
        self.observation_space = spaces.Box(low=0, high=1, shape=(4,))
        self.action_space = spaces.Discrete(2)

    def reset(self):
        self.state = np.random.rand(4)
        return self.state

    def step(self, action):
        self.state += np.random.randn(4) * 0.1
        reward = np.sum(self.state)
        done = np.sum(self.state) > 10
        info = {}
        return self.state, reward, done, info

    def render(self, mode='human'):
        print(f"State: {self.state}")

    def close(self):
        pass
```

## 常用環境列表

| 環境 | 類型 | 說明 |
|------|------|------|
| CartPole-v0 | 離散 | 平衡桿子 |
| MountainCar-v0 | 離散 | 上山坡 |
| Pendulum-v0 | 連續 | 擺錘 |
| Acrobot-v1 | 連散 | 雙擺 |
| LunarLander-v2 | 離散 | 登月著陸 |
| BipedalWalker-v2 | 連續 | 步行機器人 |
| Ant-v2 | 離散 |螞蟻機器人 |
| Humanoid-v2 | 連續 | 人形機器人 |

## 包裝器（Wrapper）

用於修改環境行為：

```python
import gym
from gym import wrappers

# 錄影
env = gym.make('CartPole-v0')
env = wrappers.Monitor(env, './video', force=True)

# 影像化獎賞
from gym.wrappers import AtariPreprocessing
env = AtariPreprocessing(env)

# 框擾亂
from gym.wrappers import FrameStack
env = FrameStack(env, num_stack=4)
```

## 監控與記錄

```python
import gym
from gym.wrappers import Monitor

env = gym.make('CartPole-v0')
env = Monitor(env, './results', force=True)

for episode in range(100):
    state = env.reset()
    for t in range(200):
        action = env.action_space.sample()
        state, reward, done, _ = env.step(action)
        if done:
            break

env.close()

# 上傳結果到 OpenAI 伺服器
# gym.upload('./results', api_key='your-api-key')
```

## CartPole 完整訓練範例

```python
import numpy as np
import gym

class QLearningAgent:
    def __init__(self, n_states, n_actions, alpha=0.1, gamma=0.99, epsilon=1.0, epsilon_decay=0.995, epsilon_min=0.01):
        self.n_states = n_states
        self.n_actions = n_actions
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.Q = np.zeros((n_states, n_actions))

    def discretize(self, state, bins):
        return tuple(int(np.clip(np.digitize(x, b), 0, n-1)) for x, b, n in zip(state, bins, [10, 10, 10, 10]))

    def choose_action(self, state):
        if np.random.random() < self.epsilon:
            return np.random.randint(self.n_actions)
        return np.argmax(self.Q[state])

    def learn(self, state, action, reward, next_state):
        self.Q[state, action] += self.alpha * (
            reward + self.gamma * np.max(self.Q[next_state]) - self.Q[state, action]
        )
        self.epsilon = max(self.epsilon * self.epsilon_decay, self.epsilon_min)

# 訓練
env = gym.make('CartPole-v0')
n_actions = env.action_space.n

# 觀察空間離散化
obs_low = env.observation_space.low
obs_high = env.observation_space.high
bins = [
    np.linspace(obs_low[i], obs_high[i], 10) for i in range(4)
]

agent = QLearningAgent(n_states=(10, 10, 10, 10), n_actions=n_actions)

n_episodes = 500
max_steps = 200

for episode in range(n_episodes):
    state_raw = env.reset()
    state = agent.discretize(state_raw, bins)

    for step in range(max_steps):
        action = agent.choose_action(state)
        next_state_raw, reward, done, _ = env.step(action)
        next_state = agent.discretize(next_state_raw, bins)

        agent.learn(state, action, reward, next_state)
        state = next_state

        if done:
            break

    if episode % 50 == 0:
        print(f"Episode {episode}: {step+1} steps, epsilon = {agent.epsilon:.3f}")

env.close()
```

## 總結

OpenAI Gym 提供了統一的強化學習環境介面：
- 支援離散與連續動作空間
- 涵蓋遊戲、機器人等多種任務
- 可自定義環境與使用包裝器
- 是 RL 研究與實驗的標準工具