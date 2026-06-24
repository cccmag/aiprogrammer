# 主題六：AlphaGo 與圍棋 AI

## 深度強化學習的勝利

### 1. AlphaGo 的歷史性勝利

2016 年 3 月，AlphaGo 以 4-1 擊敗世界冠軍李世石，標誌著人工智慧在圍棋領域的重大突破。這是 AI 首次在這個被認為是 AI 最終挑戰的遊戲中戰勝頂級人類選手。

### 2. AlphaGo 的技術架構

AlphaGo 結合了深度神經網路和蒙特卡羅樹搜索（MCTS）：

**策略網路（Policy Network）**：
- 預測下一步的最佳動作
- 減少搜索空間

**價值網路（Value Network）**：
- 評估當前棋局的勝率
- 減少搜索深度

```python
class AlphaGoNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(17, 192, 3, padding=1)
        self.conv2 = nn.Conv2d(192, 192, 3, padding=1)
        self.conv3 = nn.Conv2d(192, 192, 3, padding=1)
        self.conv4 = nn.Conv2d(192, 192, 3, padding=1)
        self.conv5 = nn.Conv2d(192, 192, 3, padding=1)
        self.conv6 = nn.Conv2d(192, 192, 3, padding=1)
        self.conv7 = nn.Conv2d(192, 192, 3, padding=1)
        self.conv8 = nn.Conv2d(192, 192, 3, padding=1)
        self.conv9 = nn.Conv2d(192, 192, 3, padding=1)
        self.conv10 = nn.Conv2d(192, 192, 3, padding=1)
        self.conv11 = nn.Conv2d(192, 192, 3, padding=1)
        self.conv12 = nn.Conv2d(192, 192, 3, padding=1)

        self.policy_head = nn.Sequential(
            nn.Conv2d(192, 2, 1),
            nn.ReLU(),
            nn.Linear(2 * 19 * 19, 19 * 19)
        )

        self.value_head = nn.Sequential(
            nn.Conv2d(192, 1, 1),
            nn.ReLU(),
            nn.Linear(19 * 19, 256),
            nn.ReLU(),
            nn.Linear(256, 1),
            nn.Tanh()
        )

    def forward(self, x):
        x = F.relu(self.conv1(x))
        for i in range(2, 13):
            x = F.relu(getattr(self, f'conv{i}')(x))

        policy = self.policy_head(x)
        value = self.value_head(x)

        return policy, value
```

### 3. 蒙特卡羅樹搜索 (MCTS)

MCTS 是 AlphaGo 的核心規劃算法：

```python
class MCTS:
    def __init__(self, policy_network, value_network, num_simulations=1000):
        self.policy = policy_network
        self.value = value_network
        self.num_simulations = num_simulations
        self.Q = {}
        self.N = {}

    def select_action(self, state):
        for _ in range(self.num_simulations):
            self.simulate(state.copy(), 0)

        legal_moves = state.get_legal_moves()
        visit_counts = [self.N.get((state, a), 0) for a in legal_moves]
        return legal_moves[np.argmax(visit_counts)]

    def simulate(self, state, depth):
        if state.is_game_over():
            return -state.get_result()

        state_hash = state.get_hash()
        if (state_hash, 0) not in self.Q:
            policy, value = self.get_network_output(state)
            self.Q[(state_hash, 0)] = value
            return -value

        legal_moves = state.get_legal_moves()
        best_score = -float('inf')
        best_move = None

        for move in legal_moves:
            p = self.policy.get_move_probability(state, move)

            next_state = state.copy()
            next_state.play(move)

            if (next_state.get_hash(), depth + 1) not in self.Q:
                policy, value = self.get_network_output(next_state)
                self.Q[(next_state.get_hash(), depth + 1)] = value
                score = -value
            else:
                score = -self.Q[(next_state.get_hash(), depth + 1)]

            u = score + 1.4 * p * np.sqrt(np.log(self.N.get((state_hash, 0), 1)) / (1 + self.N.get((next_state.get_hash(), depth + 1), 0)))

            if u > best_score:
                best_score = u
                best_move = move

        next_state = state.copy()
        next_state.play(best_move)
        value = self.simulate(next_state, depth + 1)

        self.N[(state_hash, 0)] = self.N.get((state_hash, 0), 0) + 1
        self.N[(next_state.get_hash(), depth + 1)] = self.N.get((next_state.get_hash(), depth + 1), 0) + 1
        self.Q[(state_hash, 0)] = (self.N[(state_hash, 0)] - 1) / self.N[(state_hash, 0)] * self.Q[(state_hash, 0)] + value / self.N[(state_hash, 0)]

        return -value
```

### 4. AlphaGo 的訓練過程

**第一階段：監督學習**：
- 從人類圍棋高手的棋譜中學習
- 訓練策略網路預測人類落子

**第二階段：強化學習**：
- 使用 Policy Gradient 改進策略網路
- 與之前的版本對弈

**第三階段：價值估計**：
- 訓練價值網路評估棋局
- 使用自我對弈的資料

### 5. AlphaGo Zero 的創新

2017 年，AlphaGo Zero 完全從零開始學習，不需要人類棋譜：

**主要創新**：
- 完全從自我對弈中學習
- 使用殘差網路
- 合併策略和價值頭

```python
class AlphaGoZeroNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(17, 256, 3, padding=1)
        self.residual_towers = nn.ModuleList([
            ResidualBlock(256) for _ in range(40)
        ])
        self.policy_head = nn.Sequential(
            nn.Conv2d(256, 2, 1),
            nn.ReLU(),
            nn.Linear(2 * 19 * 19, 19 * 19 + 1)
        )
        self.value_head = nn.Sequential(
            nn.Conv2d(256, 1, 1),
            nn.ReLU(),
            nn.Linear(19 * 19, 256),
            nn.ReLU(),
            nn.Linear(256, 1),
            nn.Tanh()
        )
```

### 6. AlphaZero

AlphaZero 將 AlphaGo Zero 的方法推廣到其他遊戲（西洋棋、將棋），同樣從零開始學習，達到超越人類的水準。

### 7. 影響與啟示

AlphaGo 的成功帶來了深遠的影響：

**技術層面**：
- 展示了深度強化學習的潛力
- 推动了 RL + 深度學習的發展
- 促進了 MCTS 的研究

**應用層面**：
- 啟發了其他領域的 AI 應用
- 推動了晶片和硬體發展
- 促進了 AI 倫理討論

---

## 延伸閱讀

- [AlphaGo 論文](https://www.google.com/search?q=Mastering+the+game+of+Go+deep+neural+networks+Silver)
- [AlphaGo Zero 論文](https://www.google.com/search?q=Mastering+the+game+of+Go+without+human+knowledge+Silver)
- [蒙特卡羅樹搜索](https://www.google.com/search?q=Monte+Carlo+tree+search+AI+games)