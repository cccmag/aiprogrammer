# Gymnasium 環境設計

## 從 OpenAI Gym 到 Gymnasium

強化學習的第一站是環境。2016 年 OpenAI 釋出 Gym，2022 年社群 fork 出 Gymnasium 作為後繼專案。Gymnasium 提供了統一的 `Env` 介面，讓演算法可以無痛切換不同環境：

```python
import gymnasium as gym

env = gym.make("CartPole-v1", render_mode="rgb_array")
obs, info = env.reset()
for _ in range(100):
    action = env.action_space.sample()
    obs, reward, terminated, truncated, info = env.step(action)
    if terminated or truncated:
        obs, info = env.reset()
env.close()
```

## 核心介面設計

`gymnasium.Env` 定義了五個回傳值的 `step()`，其中 `terminated` 與 `truncated` 拆開是 Gymnasium 的重要改進——前者代表任務完成，後者代表時間超限。這讓演算法可以分別處理兩種結束原因。

## 自訂環境實作

實作一個自訂環境只需要繼承 `Env` 並實作 `__init__`、`reset`、`step`：

```python
import gymnasium as gym
from gymnasium import spaces
import numpy as np

class GridWorld(gym.Env):
    def __init__(self, size=5):
        super().__init__()
        self.size = size
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(
            low=0, high=size-1, shape=(2,), dtype=int)
        self.goal = np.array([size-1, size-1])

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.agent = np.array([0, 0])
        return self.agent, {}

    def step(self, action):
        moves = [(-1,0),(1,0),(0,-1),(0,1)]
        self.agent = np.clip(self.agent + moves[action],
                             0, self.size - 1)
        terminated = np.array_equal(self.agent, self.goal)
        reward = 1.0 if terminated else -0.01
        return self.agent, reward, terminated, False, {}
```

## Wrapper 系統

Gymnasium 的 Wrapper 機制讓環境功能可以疊加：

```python
from gymnasium.wrappers import TimeLimit, RecordEpisodeStatistics

env = GridWorld(size=5)
env = TimeLimit(env, max_episode_steps=50)
env = RecordEpisodeStatistics(env)
```

## 向量化環境

大規模 RL 訓練需要同時執行多個環境實例：

```python
from gymnasium.vector import SyncVectorEnv

def make_env():
    return GridWorld(size=5)

vec_env = SyncVectorEnv([make_env for _ in range(4)])
obs, _ = vec_env.reset()
actions = vec_env.action_space.sample()
obs, rewards, term, trunc, infos = vec_env.step(actions)
```

## 結語

Gymnasium 已成為 RL 環境的標準介面。無論是 Atari、MuJoCo 還是自訂模擬器，只要遵循 `Env` 協定，就能無縫接入 DQN、PPO 等演算法。


**延伸閱讀**
- [Gymnasium Documentation](https://www.google.com/search?q=Gymnasium+documentation+Farama)
- [OpenAI Gym 原始論文](https://www.google.com/search?q=OpenAI+Gym+paper)
- [Gymnasium Wrapper 指南](https://www.google.com/search?q=Gymnasium+wrappers+tutorial)
