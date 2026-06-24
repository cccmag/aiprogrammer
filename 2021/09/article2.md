# OpenAI Gym 入門

OpenAI Gym 是強化學習的標準環境框架。

## 1. 基本使用

```python
import gym

env = gym.make('CartPole-v1')
state = env.reset()

for episode in range(10):
    state = env.reset()
    total_reward = 0

    for step in range(200):
        action = env.action_space.sample()
        state, reward, done, _ = env.step(action)
        total_reward += reward

        if done:
            break

    print(f"Episode {episode}: Total Reward = {total_reward}")
```

## 2. 常見環境

- **CartPole**：平衡杆經典控制問題
- **MountainCar**：爬上山丘
- **Atari**：雅達利遊戲
- **MuJoCo**：物理模擬

## 3. 定義觀察和動作空間

```python
from gym import spaces

class CustomEnv(gym.Env):
    def __init__(self):
        self.observation_space = spaces.Box(low=-1, high=1, shape=(4,))
        self.action_space = spaces.Discrete(2)
```

---

## 延伸閱讀

- [OpenAI Gym GitHub](https://www.google.com/search?q=OpenAI+Gym+GitHub+reinforcement+learning)
- [Gym 環境列表](https://www.google.com/search?q=gym+environments+list+cartpole+mountaincar)