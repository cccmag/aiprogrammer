# 主題一：強化學習概述

## 從經驗中學習的 AI

### 1. 什麼是強化學習？

強化學習（Reinforcement Learning，RL）是機器學習的一個分支，專注於如何讓智能體（Agent）通過與環境的互動來學習決策策略。

與監督學習不同，強化學習不需要標註好的資料，而是通過「試錯」（trial-and-error）的方式學習。智能體從自己的經驗中學習，逐漸改進其決策策略。

### 2. 強化學習的基本框架

強化學習的核心是智能體與環境的互動：

```python
class Agent:
    def select_action(self, state):
        """根據當前狀態選擇動作"""
        raise NotImplementedError

    def update(self, state, action, reward, next_state, done):
        """根據經驗更新策略"""
        raise NotImplementedError

class Environment:
    def reset(self):
        """重置環境到初始狀態"""
        raise NotImplementedError

    def step(self, action):
        """執行動作，返回下一狀態、獎勵、是否結束"""
        raise NotImplementedError
```

### 3. 互動循環

強化學習的基本互動循環：

```
for episode in range(num_episodes):
    state = env.reset()

    for step in range(max_steps):
        action = agent.select_action(state)
        next_state, reward, done = env.step(action)

        agent.update(state, action, reward, next_state, done)

        state = next_state

        if done:
            break
```

### 4. 探索與利用的平衡

強化學習面臨一個核心問題：**探索（Exploration）與利用（Exploitation）的平衡**。

**利用（Exploitation）**：
- 選擇已知能帶來高獎勵的動作
- 最大化當前策略的期望回報

**探索（Exploration）**：
- 嘗試新的動作
- 可能發現更好的策略

**常見策略**：
- Epsilon-Greedy：以 epsilon 機率隨機探索
- Softmax/Thompson Sampling：根據機率選擇動作
- Upper Confidence Bound (UCB)：平衡均值和不确定性

```python
def epsilon_greedy(Q, state, epsilon):
    """Epsilon-Greedy 策略"""
    if random.random() < epsilon:
        return random.randint(0, len(Q[state]) - 1)
    else:
        return argmax(Q[state])
```

### 5. 獎勵信號

獎勵（Reward）是強化學習的核心：

- 每個步驟提供即時的回報
- 引導智能體學習正確的行為
- 可以是人為設計的，也可以是學習的

設計良好的獎勵函數是強化學習成功的關鍵。

### 6. 強化學習的特點

**與監督學習的比較**：

| 特性 | 監督學習 | 強化學習 |
|------|----------|----------|
| 學習方式 | 從標註資料學習 | 從經驗學習 |
| 反饋類型 | 即時標籤 | 延遲獎勵 |
| 決策序列 | 獨立 | 相互影響 |
| 探索 | 不需要 | 需要 |

### 7. 應用場景

強化學習廣泛應用於：
- **遊戲**：圍棋、Atari 遊戲、星際爭霸
- **機器人控制**：運動控制、導航
- **自動駕駛**：路徑規劃、決策
- **推薦系統**：動態推薦策略
- **資源管理**：資料中心冷卻、網路路由

---

## 延伸閱讀

- [強化學習經典教材 - Sutton & Barto](https://www.google.com/search?q=Reinforcement+Learning+An+Introduction+Sutton+Barto)
- [OpenAI Gym 環境](https://www.google.com/search?q=OpenAI+Gym+reinforcement+learning+environments)
- [深度強化學習概述](https://www.google.com/search?q=deep+reinforcement+learning+survey+2021)