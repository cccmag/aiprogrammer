# Python 模擬環境

Python 可以用於建立簡單的強化學習模擬環境。

## 1. 基本環境結構

```python
class GridWorldEnv:
    def __init__(self, width=5, height=5):
        self.width = width
        self.height = height
        self.state = (0, 0)

    def reset(self):
        self.state = (0, 0)
        return self.state

    def step(self, action):
        x, y = self.state
        if action == 0:  # up
            y = min(y + 1, self.height - 1)
        elif action == 1:  # down
            y = max(y - 1, 0)
        elif action == 2:  # left
            x = max(x - 1, 0)
        elif action == 3:  # right
            x = min(x + 1, self.width - 1)

        self.state = (x, y)
        reward = 1.0 if self.state == (self.width - 1, self.height - 1) else 0.0
        done = self.state == (self.width - 1, self.height - 1)
        return self.state, reward, done
```

## 2. 互動迴圈

```python
env = GridWorldEnv()
state = env.reset()

for episode in range(10):
    state = env.reset()
    for step in range(100):
        action = agent.select_action(state)
        next_state, reward, done = env.step(action)
        agent.update(state, action, reward, next_state, done)
        state = next_state
        if done:
            break
```

---

## 延伸閱讀

- [OpenAI Gym 文档](https://www.google.com/search?q=OpenAI+Gym+documentation+python)
- [強化學習環境設計](https://www.google.com/search?q=reinforcement+learning+environment+design+python)