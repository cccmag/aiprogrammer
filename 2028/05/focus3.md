# 策略梯度與 Actor-Critic（2014-2028）

## 為什麼需要策略梯度？

價值方法（如 DQN）先學 Q 函數，再根據 Q 值選擇動作。策略梯度方法則直接學習策略 π(a|s; θ)，不需要中間的價值函數。

策略梯度的核心思想：增加好動作的機率，減少壞動作的機率。這個直覺可以用下面的梯度公式表示：

```
∇_θ J(θ) = E[ ∇_θ log π(a|s; θ) · R ]
```

其中 R 是累積獎勵。這個公式被稱為 REINFORCE 演算法，由 Ronald Williams 於 1992 年提出，但直到深度學習時代才展現威力。

## 簡單的 REINFORCE 實作

```python
import numpy as np

class REINFORCE:
    def __init__(self, policy_net, lr=0.001, gamma=0.99):
        self.policy = policy_net
        self.lr = lr
        self.gamma = gamma

    def update(self, trajectory):
        # trajectory: list of (s, a, r)
        T = len(trajectory)
        returns = np.zeros(T)

        # 計算折扣回報 G_t
        G = 0
        for t in reversed(range(T)):
            G = trajectory[t][2] + self.gamma * G
            returns[t] = G

        # 策略梯度更新
        loss = 0
        for t in range(T):
            s, a, _ = trajectory[t]
            log_prob = self.policy.log_prob(s, a)
            loss += -log_prob * returns[t]

        loss.backward()
        self.policy.step(self.lr)
```

REINFORCE 的問題是高方差：同一策略的多次執行可能得到完全不同的回報，導致學習不穩定。

## Actor-Critic：減小方差

Actor-Critic 同時學習策略（Actor）和價值函數（Critic）。Critic 評估當前狀態的好壞，減少回報估計的方差：

```
∇_θ J(θ) = E[ ∇_θ log π(a|s; θ) · A(s,a) ]
```

A(s,a) = Q(s,a) - V(s) 是優勢函數，表示動作 a 相對於平均水準的好壞。

```python
class ActorCritic:
    def __init__(self, actor_net, critic_net, lr_a=0.001, lr_c=0.01, gamma=0.99):
        self.actor = actor_net
        self.critic = critic_net
        self.lr_a = lr_a
        self.lr_c = lr_c
        self.gamma = gamma

    def update(self, s, a, r, s_next, done):
        # Critic 更新：最小化 TD-error
        V_next = 0 if done else self.critic(s_next).item()
        td_target = r + self.gamma * V_next
        V_cur = self.critic(s)
        critic_loss = (td_target - V_cur) ** 2
        critic_loss.backward()
        self.critic.step(self.lr_c)

        # Actor 更新：最大化優勢
        advantage = td_target - V_cur.item()
        log_prob = self.actor.log_prob(s, a)
        actor_loss = -log_prob * advantage
        actor_loss.backward()
        self.actor.step(self.lr_a)
```

## A3C 與 A2C（2016）

2016 年，DeepMind 發表了 A3C（Asynchronous Advantage Actor-Critic），使用多個平行 worker 同時與環境互動：

```
Worker 1 → 環境 1 → 梯度 → 全域網路 ← 梯度 ← Worker 2 → 環境 2
Worker 3 → 環境 3 → 梯度 → 全域網路 ← 梯度 ← Worker 4 → 環境 4
```

A3C 的非同步訓練打破了樣本相關性，不需要經驗回放。後來的 A2C（Advantage Actor-Critic）使用同步版本，效果相當且實現更簡單。

## PPO：最穩定的策略梯度（2017）

PPO（Proximal Policy Optimization）迄今仍是使用最廣泛的 RL 演算法之一，也是 RLHF 和 LLM 訓練的核心。

PPO 的核心思想：每次更新不要偏離舊策略太遠，使用剪切損失函數：

```python
def ppo_loss(old_log_prob, new_log_prob, advantage, epsilon=0.2):
    ratio = new_log_prob - old_log_prob.exp()
    surr1 = ratio * advantage
    surr2 = torch.clamp(ratio, 1-epsilon, 1+epsilon) * advantage
    return -torch.min(surr1, surr2)
```

PPO 的優勢：
- 訓練穩定，學習率超參數不敏感
- 適用於離散和連續動作空間
- 適合大規模並行訓練

## 策略梯度在 LLM 時代（2023-2028）

2023 年後，策略梯度方法在 LLM 訓練中發揮了關鍵作用：

- **RLHF**：使用 PPO 微調語言模型，獎勵來自人類偏好模型
- **GRPO（2025）**：Google 提出的 Group Relative Policy Optimization，無需 Critic 網路，透過組內比較計算優勢
- **RLOO**：在線上輸出的基礎上進行強化學習，適用於 LLM 推理

2028 年的趨勢是「可擴展策略梯度」——讓策略梯度方法能夠在數十億參數模型和超大規模分散式環境中高效運行。

## 延伸閱讀

- [PPO 論文](https://www.google.com/search?q=PPO+Proximal+Policy+Optimization+Algorithms+Schulman+2017)
- [A3C 論文](https://www.google.com/search?q=Asynchronous+Methods+for+Deep+Reinforcement+Learning+Mnih+2016)
- [GRPO 論文](https://www.google.com/search?q=GRPO+Group+Relative+Policy+Optimization+DeepSeek+Math)

*本篇文章為「AI 程式人雜誌 2028 年 5 月號」強化學習系列之一。*
