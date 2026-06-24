# 強化學習：從遊戲到現實

## 前言

2017 年強化學習在遊戲領域取得重大突破，同時開始向現實世界應用擴展。

## AlphaGo 系列

### AlphaGo 擊敗柯潔

```python
# AlphaGo 的關鍵技術

class AlphaGo:
    def __init__(self):
        self.policy_network = PolicyNetwork()  # 策略網路
        self.value_network = ValueNetwork()    # 價值網路
        self.mcts = MCTS()                     # 蒙特卡羅樹搜索

    def select_move(self, board_state):
        # 使用 MCTS 選擇最佳動作
        search_results = self.mcts.search(
            board_state,
            self.policy_network,
            self.value_network,
            num_simulations=1600
        )
        return search_results.best_move()
```

### AlphaGo Zero

```python
# AlphaGo Zero 的創新：從零學習

class AlphaGoZero:
    def __init__(self):
        self.network = DualNetwork()  # 合併策略和價值

    def self_play(self):
        """完全自我對弈學習"""
        game_history = []

        state = initial_state()
        while not state.is_terminal():
            # MCTS + Neural Network
            move_probs = self.mcts.search(state, self.network)

            game_history.append({
                'state': state,
                'probs': move_probs,
                'player': state.current_player
            })

            state = state.step(move_probs)

        # 計算遊戲結果
        game_result = state.game_result()

        # 更新網路
        return game_history, game_result
```

## DeepMind DQN

```python
# 經典 DQN 用於 Atari 遊戲

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
    def __init__(self, capacity=100000):
        self.buffer = deque(maxlen=capacity)

    def push(self, *args):
        self.buffer.append(Transition(*args))

    def sample(self, batch_size):
        return random.sample(self.buffer, batch_size)
```

## Policy Gradient 方法

```python
# REINFORCE 演算法

class PolicyGradient:
    def update(self, states, actions, rewards):
        # 計算回報
        returns = self.compute_returns(rewards)

        # 計算策略梯度
        log_probs = self.policy(states).log_prob(actions)
        loss = -(log_probs * returns).mean()

        loss.backward()
        self.optimizer.step()

        return loss.item()

    def compute_returns(self, rewards, gamma=0.99):
        """計算折扣回報"""
        returns = []
        running_return = 0

        for r in reversed(rewards):
            running_return = r + gamma * running_return
            returns.insert(0, running_return)

        returns = torch.tensor(returns)
        returns = (returns - returns.mean()) / (returns.std() + 1e-8)

        return returns
```

## 實際應用

```
┌─────────────────────────────────────────────────────────┐
│              強化學習應用領域                            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  遊戲:                                                │
│  - 圍棋、象棋                                         │
│  - Atari 遊戲                                         │
│  - StarCraft (AlphaStar, 2019)                         │
│                                                         │
│  機器人:                                              │
│  - 運動控制                                            │
│  - 抓取物體                                            │
│                                                         │
│  資源管理:                                            │
│  - 資料中心冷卻 (DeepMind)                             │
│  - 網路路由                                            │
│                                                         │
│  金融:                                               │
│  - 交易策略                                            │
│  - 投資組合優化                                        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 2018 年展望

強化學習的未來方向：
- 樣本效率提升
- 多代理強化學習
- 實際機器人應用
- 安全性與可解釋性

---

**延伸閱讀**

- [DeepMind Publications](https://www.google.com/search?q=DeepMind+publications+rl)
- [Reinforcement Learning Book](https://www.google.com/search?q=reinforcement+learning+sutton+barto)

---

*本篇文章為「AI 程式人雜誌 2017 年 12 月號」年終回顧系列之一。*