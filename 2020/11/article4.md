# Ray 分散式執行框架

## 前言

Ray 是 UC Berkeley RISELab 開發的分散式執行框架，專為 AI 和強化學習設計，支援大規模平行計算。

## Ray 核心概念

```python
import ray

ray.init()

@ray.remote
def compute_function(x):
    return x * x

# 分散式執行
results = ray.get([compute_function.remote(i) for i in range(100)])
```

## Actor 模型

```python
@ray.remote
class Counter:
    def __init__(self):
        self.count = 0
    
    def increment(self):
        self.count += 1
        return self.count

# 使用 Actor
counter = Counter.remote()
for _ in range(10):
    counter.increment.remote()

print(ray.get(counter.increment.remote()))  # 11
```

## Ray 與強化學習

```python
# Ray RLlib 用於強化學習
from ray import tune

tune.run(
    "PPO",
    config={
        "env": "CartPole-v0",
        "num_workers": 4,
        "lr": tune.grid_search([0.001, 0.01])
    },
    stop={"episode_reward_mean": 200},
    num_samples=2
)
```

## 延伸閱讀

- [Ray 官方網站](https://www.google.com/search?q=Ray+distributed+execution+framework)

---

*本篇文章為「AI 程式人雜誌 2020 年 11 月號」文章集錦之一。*