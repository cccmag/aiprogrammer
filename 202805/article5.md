# 多智能體 RL

## 從單一到大規模協作

真實世界的決策很少只有一個智能體。自動駕駛需要與其他車輛互動，機器人需要協作搬運，遊戲 AI 需要團隊配合。多智能體強化學習（MARL）處理的就是這類場景。

## MARL 的分類

根據智能體之間的關係，MARL 可分為三類：

- **完全合作**：所有智能體共享同一獎勵函數
- **完全競爭**：零和遊戲，一方所得即另一方所失
- **混合動機**：既有合作又有競爭，如橋牌、麻將

## 集中訓練分散執行（CTDE）

CTDE 是 MARL 的主流框架——訓練時可以使用全域資訊，執行時每個智能體只能看到局部觀察：

```python
import torch
import torch.nn as nn

class CentralizedCritic(nn.Module):
    """訓練時可以看到所有智能體的狀態與動作"""
    def __init__(self, n_agents, obs_dim, action_dim):
        super().__init__()
        input_dim = n_agents * (obs_dim + action_dim)
        self.net = nn.Sequential(
            nn.Linear(input_dim, 256), nn.ReLU(),
            nn.Linear(256, 128), nn.ReLU(),
            nn.Linear(128, 1))

    def forward(self, all_obs, all_actions):
        x = torch.cat([all_obs.flatten(1),
                       all_actions.flatten(1)], dim=-1)
        return self.net(x)

class DecentralizedActor(nn.Module):
    """執行時只看自己的局部觀察"""
    def __init__(self, obs_dim, action_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(obs_dim, 128), nn.ReLU(),
            nn.Linear(128, action_dim))

    def forward(self, obs):
        return self.net(obs)
```

## MADDPG：多智能體 DDPG

MADDPG（Multi-Agent DDPG）是 CTDE 的代表作。每個智能體有自己的 Actor，但 Critic 可以看到所有智能體的資訊：

```python
class MADDPG:
    def __init__(self, n_agents, obs_dim, action_dim):
        self.actors = [DecentralizedActor(obs_dim, action_dim)
                       for _ in range(n_agents)]
        self.critics = [CentralizedCritic(n_agents, obs_dim, action_dim)
                        for _ in range(n_agents)]

    def update(self, replay_buffer, batch_size=256):
        batch = replay_buffer.sample(batch_size)
        for i in range(self.n_agents):
            # Centralized critic update
            target_q = self._compute_target_q(batch, i)
            current_q = self.critics[i](batch.all_obs, batch.all_actions)
            critic_loss = nn.MSELoss()(current_q, target_q)

            # Actor update
            actions = list(batch.all_actions)
            actions[i] = self.actors[i](batch.all_obs[:, i])
            actor_loss = -self.critics[i](batch.all_obs,
                                          torch.cat(actions, dim=-1)).mean()

            self._update_networks(i, critic_loss, actor_loss)
```

## 簡單協作環境實例

用 PettingZoo 建立一個簡單的協作環境：

```python
from pettingzoo.mpe import simple_spread_v3
import numpy as np

env = simple_spread_v3.parallel_env(
    N=3, max_cycles=100, continuous_actions=False)

obs, _ = env.reset()
for step in range(100):
    actions = {agent: env.action_space(agent).sample()
               for agent in env.agents}
    obs, rewards, term, trunc, infos = env.step(actions)
    if any(term.values()) or any(trunc.values()):
        break
```

## 結語

MARL 是 RL 從玩具問題走向真實世界的關鍵。自動駕駛、群體機器人、即時策略遊戲都是 MARL 的應用場景。PettingZoo 與 Mava 等框架讓 MARL 研究的門檻大幅降低。


**延伸閱讀**
- [Multi-Agent Actor-Critic for Mixed Cooperative-Competitive](https://www.google.com/search?q=MADDPG+Lowe+2017)
- [PettingZoo: Gym for Multi-Agent RL](https://www.google.com/search?q=PettingZoo+MARL+library)
- [QMIX: Monotonic Value Function Factorisation](https://www.google.com/search?q=QMIX+MARL+Rashid+2018)
