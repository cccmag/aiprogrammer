# 主題四：Policy Gradient 方法

## 基於策略的強化學習

### 1. 為什麼需要 Policy Gradient？

Q-learning 等基於價值的方法有一些限制：
- 難以處理連續動作空間
- 對 Q 函數的近似可能不穩定
- 探索策略不易調整

Policy Gradient 方法直接學習策略函數，解決了這些問題。

### 2. 策略函數

策略 π(a|s) 定義了在狀態 s 下執行動作 a 的機率：

```python
class Policy(nn.Module):
    def __init__(self, state_dim, action_dim, hidden_dim=128):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(state_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, action_dim),
            nn.Softmax(dim=-1)
        )

    def forward(self, state):
        return self.network(state)
```

### 3. 策略梯度定理

策略梯度定理是 Policy Gradient 方法的基礎：

$$\nabla_\theta J(\pi_\theta) = \mathbb{E}_{\tau \sim \pi_\theta} \left[ \sum_{t=0}^{T} \nabla_\theta \log \pi_\theta(a_t|s_t) \cdot G_t \right]$$

其中 J(π) 是策略的效能函數，G_t 是從時間 t 開始的回報。

### 4. REINFORCE 演算法

REINFORCE 是最基本的 Policy Gradient 方法：

```python
class REINFORCEAgent:
    def __init__(self, state_dim, action_dim, lr=0.001, gamma=0.99):
        self.policy = Policy(state_dim, action_dim)
        self.optimizer = torch.optim.Adam(self.policy.parameters(), lr=lr)
        self.gamma = gamma

    def select_action(self, state):
        state = torch.FloatTensor(state).unsqueeze(0)
        probs = self.policy(state)
        action_dist = torch.distributions.Categorical(probs)
        action = action_dist.sample()
        return action.item(), action_dist.log_prob(action)

    def update(self, states, actions, rewards):
        G = 0
        returns = []
        for r in reversed(rewards):
            G = r + self.gamma * G
            returns.insert(0, G)

        returns = torch.FloatTensor(returns)
        returns = (returns - returns.mean()) / (returns.std() + 1e-8)

        states = torch.FloatTensor(states)
        actions = torch.LongTensor(actions)

        log_probs = []
        for i, state in enumerate(states):
            probs = self.policy(state.unsqueeze(0))
            dist = torch.distributions.Categorical(probs)
            log_probs.append(dist.log_prob(actions[i]))

        log_probs = torch.stack(log_probs)
        loss = -(log_probs * returns).sum()

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
```

### 5. Variance Reduction

Policy Gradient 的主要問題是高方差。常用的降低方差的方法：

**基線（Baseline）**：
$$G_t - b(s_t)$$

基線可以是狀態價值函數 V(s) 的估計。

```python
class REINFORCEwithBaseline:
    def __init__(self, state_dim, action_dim):
        self.policy = Policy(state_dim, action_dim)
        self.value_network = ValueNetwork(state_dim)
        self.policy_optimizer = torch.optim.Adam(self.policy.parameters())
        self.value_optimizer = torch.optim.Adam(self.value_network.parameters())

    def update(self, states, actions, rewards):
        returns = []
        G = 0
        for r in reversed(rewards):
            G = r + self.gamma * G
            returns.insert(0, G)

        returns = torch.FloatTensor(returns)
        baseline = self.value_network(torch.FloatTensor(states))
        advantages = returns - baseline.detach()

        log_probs = []
        for i, state in enumerate(states):
            probs = self.policy(state.unsqueeze(0))
            dist = torch.distributions.Categorical(probs)
            log_probs.append(dist.log_prob(actions[i]))

        policy_loss = -(torch.stack(log_probs) * advantages).sum()

        value_loss = F.mse_loss(baseline.squeeze(), returns)

        self.policy_optimizer.zero_grad()
        policy_loss.backward()
        self.policy_optimizer.step()

        self.value_optimizer.zero_grad()
        value_loss.backward()
        self.value_optimizer.step()
```

### 6. Actor-Critic

Actor-Critic 結合了 Policy Gradient 和 Value-based 方法：
- Actor：學習策略
- Critic：估計價值函數

```python
class ActorCritic(nn.Module):
    def __init__(self, state_dim, action_dim, hidden_dim=128):
        super().__init__()
        self.actor = nn.Sequential(
            nn.Linear(state_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, action_dim),
            nn.Softmax(dim=-1)
        )
        self.critic = nn.Sequential(
            nn.Linear(state_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1)
        )

    def forward(self, state):
        return self.actor(state), self.critic(state)
```

### 7. PPO 和 TRPO

PPO（Proximal Policy Optimization）和 TRPO（Trust Region Policy Optimization）是更穩定的 Policy Gradient 方法：

```python
class PPOAgent:
    def __init__(self, state_dim, action_dim, lr=3e-4, eps_clip=0.2):
        self.policy = Policy(state_dim, action_dim)
        self.optimizer = torch.optim.Adam(self.policy.parameters(), lr=lr)
        self.eps_clip = eps_clip

    def update(self, states, actions, old_log_probs, returns, advantages):
        states = torch.FloatTensor(states)
        actions = torch.LongTensor(actions)
        old_log_probs = torch.FloatTensor(old_log_probs).detach()
        returns = torch.FloatTensor(returns)
        advantages = torch.FloatTensor(advantages)

        for _ in range(10):
            new_probs = self.policy(states)
            dist = torch.distributions.Categorical(new_probs)
            new_log_probs = dist.log_prob(actions)

            ratio = torch.exp(new_log_probs - old_log_probs)
            surr1 = ratio * advantages
            surr2 = torch.clamp(ratio, 1 - self.eps_clip, 1 + self.eps_clip) * advantages

            loss = -torch.min(surr1, surr2).mean()

            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()
```

---

## 延伸閱讀

- [Policy Gradient 論文](https://www.google.com/search?q=Policy+Gradient+methods+reinforcement+learning+Williams)
- [REINFORCE 演算法](https://www.google.com/search?q=REINFORCE+reinforce+algorithm+tutorial)
- [PPO 論文](https://www.google.com/search?q=Proximal+Policy+Optimization+PPO+Schulman)