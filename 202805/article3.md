# PPO 演算法深入

## 為何需要 PPO？

Policy Gradient 方法直接最佳化策略，但樣本效率低且訓練不穩定。TRPO（Trust Region Policy Optimization）透過 KL 散度約束來穩定更新，但計算複雜。PPO（Proximal Policy Optimization）在 2017 年由 OpenAI 提出，用 clip 機制簡化 TRPO，成為 RL 的事實標準。

## PPO-Clip 核心公式

PPO 的核心是限制策略更新的幅度：

```python
ratio = π_new(a|s) / π_old(a|s)
L_clip = min(ratio * A, clip(ratio, 1-ε, 1+ε) * A)
```

其中 `A` 是優勢函數（Advantage Function），`ε` 是裁剪範圍。

## 從零實作 PPO

```python
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import gymnasium as gym

class ActorCritic(nn.Module):
    def __init__(self, n_obs, n_actions):
        super().__init__()
        self.shared = nn.Sequential(
            nn.Linear(n_obs, 64), nn.Tanh(),
            nn.Linear(64, 64), nn.Tanh())
        self.actor = nn.Linear(64, n_actions)
        self.critic = nn.Linear(64, 1)

    def forward(self, x):
        features = self.shared(x)
        logits = self.actor(features)
        value = self.critic(features)
        return logits, value

    def get_action(self, obs, action=None):
        logits, value = self.forward(obs)
        probs = torch.distributions.Categorical(logits=logits)
        if action is None:
            action = probs.sample()
        log_prob = probs.log_prob(action)
        entropy = probs.entropy()
        return action, log_prob, entropy, value
```

## GAE：廣義優勢估計

PPO 使用 GAE（Generalized Advantage Estimation）計算優勢函數，平衡偏差與方差：

```python
def compute_gae(rewards, values, dones, gamma=0.99, lam=0.95):
    advantages = []
    gae = 0
    for t in reversed(range(len(rewards))):
        if t == len(rewards) - 1:
            next_value = 0
        else:
            next_value = values[t + 1] * (1 - dones[t])
        delta = rewards[t] + gamma * next_value - values[t]
        gae = delta + gamma * lam * (1 - dones[t]) * gae
        advantages.insert(0, gae)
    returns = [adv + val for adv, val in zip(advantages, values)]
    return advantages, returns
```

## 完整訓練迴圈

```python
env = gym.make("CartPole-v1")
model = ActorCritic(4, 2)
optimizer = optim.Adam(model.parameters(), lr=3e-4)

for iteration in range(1000):
    states, actions, rewards, dones = [], [], [], []
    state, _ = env.reset()
    ep_reward = 0

    for _ in range(2048):
        state_t = torch.FloatTensor(state).unsqueeze(0)
        action, log_prob, _, value = model.get_action(state_t)
        next_state, reward, done, _, _ = env.step(action.item())

        states.append(state)
        actions.append(action.item())
        rewards.append(reward)
        dones.append(done)
        state = next_state
        ep_reward += reward
        if done:
            state, _ = env.reset()

    states = torch.FloatTensor(np.array(states))
    actions = torch.LongTensor(actions)
    _, _, _, values = model.get_action(states)
    advantages, returns = compute_gae(
        rewards, values.squeeze().detach().numpy(), dones)

    for _ in range(10):
        _, log_probs, entropies, values = model.get_action(states, actions)
        ratios = torch.exp(log_probs - log_probs.detach())
        advantages_t = torch.FloatTensor(advantages)
        advantages_t = (advantages_t - advantages_t.mean()) / (advantages_t.std() + 1e-8)

        surr1 = ratios * advantages_t
        surr2 = torch.clamp(ratios, 0.8, 1.2) * advantages_t
        actor_loss = -torch.min(surr1, surr2).mean()
        critic_loss = nn.MSELoss()(values.squeeze(),
                                   torch.FloatTensor(returns))
        entropy_loss = -entropies.mean() * 0.01
        loss = actor_loss + critic_loss + entropy_loss

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
```

## 結語

PPO 的簡潔與穩定使其成為 RL 的首選演算法。無論是機器人控制、遊戲 AI 還是 LLM 訓練（RLHF 的 PPO 階段），PPO 都扮演著核心角色。


**延伸閱讀**
- [Proximal Policy Optimization Algorithms](https://www.google.com/search?q=PPO+Schulman+2017+OpenAI)
- [High-Continuous Control Using Deep Reinforcement Learning](https://www.google.com/search?q=TRPO+Schulman+2015)
- [GAE: Generalized Advantage Estimation](https://www.google.com/search?q=Generalized+Advantage+Estimation+Schulman+2015)
