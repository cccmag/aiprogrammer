# 強化學習成就：AlphaGo 與 DeepMind 的其他成就

## 前言

2017 年是強化學習領域的突破年。AlphaGo 的歷史性勝利和 AlphaGo Zero 的創新，以及 DeepMind 在其他領域的成就，都標誌著強化學習的成熟。

## AlphaGo 系列

### AlphaGo 的成功

2017 年 5 月戰勝柯潔，10 月 AlphaGo Zero 從零學習。

## 其他 DeepMind 成就

### 1. WaveNet (2017)

原始音訊生成的神經網路，用於語音合成：

```python
# WaveNet 的dilated causal convolutions
class WaveNetBlock(nn.Module):
    def __init__(self, dilation, residual_channels, skip_channels):
        super().__init__()
        self.filter_conv = nn.Conv1d(
            residual_channels, residual_channels * 2,
            kernel_size=2 * dilation, dilation=dilation
        )
        self.gate_conv = nn.Conv1d(
            residual_channels, residual_channels * 2,
            kernel_size=2 * dilation, dilation=dilation
        )
        self.residual_conv = nn.Conv1d(residual_channels, residual_channels, 1)
        self.skip_conv = nn.Conv1d(residual_channels, skip_channels, 1)

    def forward(self, x):
        # 擴展視角
        filter_out = torch.tanh(self.filter_conv(x))
        gate_out = torch.sigmoid(self.gate_conv(x))

        gated = filter_out * gate_out

        residual = self.residual_conv(gated) + x
        skip = self.skip_conv(gated)

        return residual, skip
```

### 2. Atari 遊戲大師

DeepMind 的DQN在 Atari 遊戲上達到超人水平：

```python
# DQN 核心
class DQN(nn.Module):
    def __init__(self, input_shape, num_actions):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(input_shape[0], 32, 8, stride=4),
            nn.ReLU(),
            nn.Conv2d(32, 64, 4, stride=2),
            nn.ReLU(),
            nn.Conv2d(64, 64, 3, stride=1),
            nn.ReLU()
        )
        self.fc = nn.Sequential(
            nn.Linear(3136, 512),
            nn.ReLU(),
            nn.Linear(512, num_actions)
        )

    def forward(self, x):
        conv_out = self.conv(x).view(x.size(0), -1)
        return self.fc(conv_out)

# Experience Replay
class ReplayBuffer:
    def __init__(self, capacity):
        self.buffer = deque(maxlen=capacity)

    def push(self, state, action, reward, next_state, done):
        self.buffer.append((state, action, reward, next_state, done))

    def sample(self, batch_size):
        return random.sample(self.buffer, batch_size)
```

### 3. AlphaFold (雛形)

蛋白質結構預測的早期工作，後來在 2018/2020 取得突破。

## 強化學習基本概念

```python
# 強化學習基本框架
class RLAgent:
    def __init__(self, state_space, action_space):
        self.state_space = state_space
        self.action_space = action_space
        self.policy = self.build_policy()
        self.value = self.build_value()

    def choose_action(self, state, epsilon=0.1):
        """Epsilon-greedy 策略"""
        if random.random() < epsilon:
            return random.randint(0, self.action_space - 1)
        else:
            q_values = self.policy(state)
            return q_values.argmax().item()

    def update(self, state, action, reward, next_state, done):
        """Q-Learning 更新"""
        current_q = self.policy(state)[action]
        next_q = 0 if done else self.value(next_state).max()
        td_error = reward + 0.99 * next_q - current_q
        # 更新網路
```

## Policy Gradient 方法

```python
class PolicyGradient(nn.Module):
    def __init__(self, state_dim, action_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(state_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, action_dim),
            nn.Softmax(dim=-1)
        )

    def forward(self, state):
        return self.net(state)

    def update(self, states, actions, rewards):
        """Policy Gradient 更新 (REINFORCE)"""
        policy = self(states)
        log_probs = torch.log(policy.gather(1, actions.unsqueeze(1)))

        # 計算回報
        returns = self.compute_returns(rewards)

        # Policy Gradient 損失
        loss = -(log_probs * returns).mean()

        loss.backward()
```

## Actor-Critic

```python
class ActorCritic(nn.Module):
    def __init__(self, state_dim, action_dim):
        self.actor = nn.Sequential(
            nn.Linear(state_dim, 128),
            nn.ReLU(),
            nn.Linear(128, action_dim),
            nn.Softmax()
        )
        self.critic = nn.Sequential(
            nn.Linear(state_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 1)
        )

    def forward(self, state):
        return self.actor(state), self.critic(state)

    def update(self, states, actions, rewards, next_states, dones):
        # Critic 更新
        current_value = self.critic(states)
        next_value = self.critic(next_states).detach()
        target = rewards + 0.99 * next_value * (1 - dones)
        critic_loss = F.mse_loss(current_value, target)

        # Actor 更新
        policy, _ = self.forward(states)
        log_prob = torch.log(policy.gather(1, actions))
        advantage = (target - current_value).detach()
        actor_loss = -(log_prob * advantage).mean()

        return critic_loss + actor_loss
```

## 強化學習應用領域

```
┌─────────────────────────────────────────────────────────┐
│              強化學習應用領域                            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  遊戲:                                                │
│  - 圍棋 (AlphaGo)                                      │
│  - Atari (DQN)                                         │
│  - StarCraft (AlphaStar, 2019)                         │
│                                                         │
│  機器人:                                              │
│  - 運動控制                                            │
│  - 物體操作                                            │
│  - 自主導航                                          │
│                                                         │
│  資源管理:                                            │
│  - 資料中心冷卻                                        │
│  - 網路路由                                            │
│  - 記憶體管理                                          │
│                                                         │
│  金融:                                               │
│  - 交易策略                                            │
│  - 風險管理                                           │
│  - 投資組合優化                                        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 2017 年強化學習重要事件

| 時間 | 事件 |
|------|------|
| 1月 | AlphaGo 自我對弈版本升級 |
| 5月 | AlphaGo 擊敗柯潔 |
| 6月 | DeepMind 發布 WaveNet |
| 10月 | AlphaGo Zero 發布 |

## 總結

2017 年強化學習的特點：

1. **AlphaGo 的突破**展示了深度強化學習的潛力
2. **自我學習**（AlphaGo Zero）開創新範式
3. **DQN 持續成功**在 Atari 遊戲上保持領先
4. **應用擴展**從遊戲到現實世界的各種領域

---

**延伸閱讀**

- [DeepMind Publications](https://www.google.com/search?q=DeepMind+publications+2017)
- [Reinforcement Learning Tutorial](https://www.google.com/search?q=reinforcement+learning+tutorial)

---

*本篇文章為「AI 程式人雜誌 2017 年 12 月號」年終回顧系列之一。*