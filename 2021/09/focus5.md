# 主題五：Actor-Critic 架構

## 結合價值與策略

### 1. Actor-Critic 的基本原理

Actor-Critic 結合了兩種方法的優點：

**Actor（演員）**：
- 學習策略 π(a|s)
- 根據 Critic 的反饋更新策略

**Critic（評論家）**：
- 估計價值函數 V(s) 或 Q(s,a)
- 為 Actor 提供基於價值的梯度估計

### 2. 優勢

- 相比純 Policy Gradient：更低方差
- 相比純 Value-based：更好的收斂性
- 可以處理連續和離散動作空間

### 3. Advantage Actor-Critic (A2C)

A2C 使用 Advantage 函數來減少方差：

$$A(s,a) = Q(s,a) - V(s) \approx r + \gamma V(s') - V(s)$$

```python
class A2CAgent:
    def __init__(self, state_dim, action_dim, lr=3e-4, gamma=0.99):
        self.actor = Policy(state_dim, action_dim)
        self.critic = ValueNetwork(state_dim)
        self.actor_optimizer = torch.optim.Adam(self.actor.parameters(), lr=lr)
        self.critic_optimizer = torch.optim.Adam(self.critic.parameters(), lr=lr)
        self.gamma = gamma

    def update(self, states, actions, rewards, next_states, dones):
        states = torch.FloatTensor(states)
        actions = torch.LongTensor(actions)
        rewards = torch.FloatTensor(rewards)
        next_states = torch.FloatTensor(next_states)
        dones = torch.FloatTensor(dones)

        values = self.critic(states)
        next_values = self.critic(next_states)
        targets = rewards + self.gamma * next_values * (1 - dones)
        advantages = targets - values.detach()

        probs = self.actor(states)
        dist = torch.distributions.Categorical(probs)
        log_probs = dist.log_prob(actions)

        actor_loss = -(log_probs * advantages).mean()
        critic_loss = F.mse_loss(values.squeeze(), targets.detach())

        self.actor_optimizer.zero_grad()
        actor_loss.backward()
        self.actor_optimizer.step()

        self.critic_optimizer.zero_grad()
        critic_loss.backward()
        self.critic_optimizer.step()
```

### 4. Asynchronous Advantage Actor-Critic (A3C)

A3C 使用多個並行環境來加速訓練：

```python
import multiprocessing as mp

class A3CAgent:
    def __init__(self, state_dim, action_dim, num_workers=4):
        self.global_agent = ActorCritic(state_dim, action_dim)
        self.num_workers = num_workers

    def worker(self, worker_id, env):
        local_agent = ActorCritic(state_dim, action_dim)
        local_agent.load_state_dict(self.global_agent.state_dict())

        while True:
            states, actions, rewards = [], [], []
            state = env.reset()

            for _ in range(100):
                action = local_agent.select_action(state)
                next_state, reward, done = env.step(action)

                states.append(state)
                actions.append(action)
                rewards.append(reward)

                if done:
                    break

                state = next_state

            local_agent.update(states, actions, rewards)

            self.global_agent.load_state_dict(local_agent.state_dict())
```

### 5. Generalised Advantage Estimation (GAE)

GAE 提供了更好的優勢估計：

$$A_{GAE}(t) = \sum_{l=0}^{\infty} (\gamma \lambda)^l \delta_{t+l}$$

其中 δ_t = r_t + γV(s_{t+1}) - V(s_t)

```python
def compute_gae(rewards, values, next_values, dones, gamma=0.99, lambda_=0.95):
    advantages = []
    gae = 0

    for t in reversed(range(len(rewards))):
        if t == len(rewards) - 1:
            next_value = 0
        else:
            next_value = next_values[t]

        delta = rewards[t] + gamma * next_value * (1 - dones[t]) - values[t]
        gae = delta + gamma * lambda_ * (1 - dones[t]) * gae
        advantages.insert(0, gae)

    return torch.FloatTensor(advantages)
```

### 6. Soft Actor-Critic (SAC)

SAC 是一種最大熵強化學習方法：

```python
class SACAgent:
    def __init__(self, state_dim, action_dim):
        self.actor = SquashedGaussianPolicy(state_dim, action_dim)
        self.critic1 = QNetwork(state_dim, action_dim)
        self.critic2 = QNetwork(state_dim, action_dim)
        self.value_network = ValueNetwork(state_dim)
        self.target_value_network = ValueNetwork(state_dim)

        self.alpha = torch.tensor(1.0, requires_grad=True)

    def update(self, states, actions, rewards, next_states, dones):
        next_action, next_log_prob = self.actor.sample(next_states)
        target_q = torch.min(
            self.critic1(next_states, next_action),
            self.critic2(next_states, next_action)
        )
        target_value = target_q - self.alpha * next_log_prob

        value_loss = F.mse_loss(self.value_network(states), target_value.detach())

        q1 = self.critic1(states, actions)
        q2 = self.critic2(states, actions)
        q_loss = F.mse_loss(q1, target_value.detach()) + F.mse_loss(q2, target_value.detach())
```

### 7. TD3 (Twin Delayed DDPG)

TD3 是 DDPG 的改進版本：

- 雙 Q 網路（減少過估計）
- 延遲策略更新
- 目標策略平滑正則化

```python
class TD3Agent:
    def __init__(self, state_dim, action_dim):
        self.actor = DDPGPolicy(state_dim, action_dim)
        self.critic1 = QNetwork(state_dim, action_dim)
        self.critic2 = QNetwork(state_dim, action_dim)
        self.target_actor = DDPGPolicy(state_dim, action_dim)
        self.target_critic1 = QNetwork(state_dim, action_dim)
        self.target_critic2 = QNetwork(state_dim, action_dim)

    def update(self, states, actions, rewards, next_states, dones, policy_delay=2):
        with torch.no_grad():
            next_action = self.target_actor(next_states)
            noise = torch.randn_like(actions) * 0.2
            next_action = (next_action + noise).clamp(-1, 1)

            target_q = torch.min(
                self.target_critic1(next_states, next_action),
                self.target_critic2(next_states, next_action)
            )
            target_q = rewards + (1 - dones) * 0.99 * target_q

        current_q1 = self.critic1(states, actions)
        current_q2 = self.critic2(states, actions)
        critic_loss = F.mse_loss(current_q1, target_q) + F.mse_loss(current_q2, target_q)

        if update_step % policy_delay == 0:
            actor_loss = -self.critic1(states, self.actor(states)).mean()
```

---

## 延伸閱讀

- [A3C 論文](https://www.google.com/search?q=Asynchronous+Methods+Deep+Reinforcement+Learning+Mnih)
- [SAC 論文](https://www.google.com/search?q=Soft+Actor-Critic+off-policy+maximum+entropy+deep+RL+Haarnoja)
- [TD3 論文](https://www.google.com/search?q=Addressing+function+approximation+error+in+Actor-Critic+methods+TD3)