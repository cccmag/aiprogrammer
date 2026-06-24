# 圍棋 AI 的突破：AlphaGo 與 AlphaGo Zero

## 前言

2017 年 5 月，AlphaGo 在中國烏鎮擊敗世界冠軍柯潔；同年 10 月，AlphaGo Zero 從零開始学习，達到了更高的水平。這兩件事標誌著人工智慧在策略遊戲領域的重大突破。

## AlphaGo 的勝利

### 對局背景

2017 年 5 月 23-27 日，AlphaGo 與世界排名第一的中國圍棋棋士柯潔在中國烏鎮進行了三番棋對弈。最終 AlphaGo 以 3:0 獲勝。

```
┌─────────────────────────────────────────────────────────┐
│              AlphaGo vs 柯潔 對局摘要                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  比賽時間：2017 年 5 月 23-27 日                        │
│  比賽地點：中國烏鎮                                      │
│  對局結果：AlphaGo 3:0 柯潔                             │
│                                                         │
│  第二局第 121 手被譽為「神之一手」                      │
│  這手棋展示了 AlphaGo 的創造性思維                      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### AlphaGo 的技術架構

```python
# AlphaGo 的神經網路架構
class AlphaGoNetwork(nn.Module):
    def __init__(self):
        # 共享特徵提取器
        self.conv_block = ResidualBlocks(12)

        # 策略頭 (Policy Head)
        # 輸出每個位置的走法機率
        self.policy_head = nn.Sequential(
            nn.Conv2d(256, 2, 1),
            nn.Linear(361 * 2, 361)
        )

        # 價值頭 (Value Head)
        # 輸出當前局面的勝率
        self.value_head = nn.Sequential(
            nn.Conv2d(256, 1, 1),
            nn.Linear(361, 256),
            nn.ReLU(),
            nn.Linear(256, 1),
            nn.Tanh()
        )

    def forward(self, x):
        features = self.conv_block(x)
        policy = self.policy_head(features)  # (batch, 361) log probabilities
        value = self.value_head(features)   # (batch, 1) win probability
        return policy, value
```

### 蒙特卡羅樹搜索 (MCTS)

AlphaGo 使用 MCTS 結合神經網路進行搜索：

```python
class MCTS:
    def __init__(self, network):
        self.network = network
        self.Q_values = {}  # 存储 Q(s,a)
        self.N_visits = {}  # 存储 N(s,a)
        self.Prior = {}     # 存储 P(s,a)

    def search(self, state, num_simulations=1600):
        """
        執行 MCTS 搜索

        每個模擬包含：
        1. 選擇 (Selection)
        2. 擴展 (Expansion)
        3. 評估 (Evaluation)
        4. 回溯 (Backup)
        """
        for _ in range(num_simulations):
            self.simulate(state.clone())

        # 返回訪問次數最多的動作
        state_key = self.get_state_key(state)
        best_action = max(self.N_visits[state_key].items(),
                         key=lambda x: x[1])[0]
        return best_action
```

## AlphaGo Zero 的創新

### 從零開始學習

AlphaGo Zero 的最大創新是完全不需要人類棋譜：

```
┌─────────────────────────────────────────────────────────┐
│              AlphaGo 演進對比                            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  版本           訓練資料         能力水平              │
│  ─────────────────────────────────────────────────────  │
│  AlphaGo Fan    16萬人類棋譜     业餘高手              │
│  AlphaGo Lee    16萬人類棋譜     職業水平               │
│  AlphaGo Master 16萬人類棋譜     超人類                  │
│  AlphaGo Zero   無（純自我對弈） 超人類                  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### AlphaGo Zero 的架構

```python
class AlphaGoZeroNetwork(nn.Module):
    def __init__(self):
        # 更深的骨幹網路
        self.backbone = ResidualBlocks(40)

        # 合併的策略頭和價值頭
        self.policy_head = nn.Conv2d(256, 2, 1)
        self.value_head = nn.Conv2d(256, 1, 1)

    def forward(self, x):
        features = self.backbone(x)

        # 策略：19x19+1 個動作的 log probabilities
        policy_logits = self.policy_head(features).view(-1, 362)

        # 價值：局面評估 [-1, 1]
        value = self.value_head(features).view(-1, 1)

        return policy_logits, value

class SelfPlay:
    """
    AlphaGo Zero 的自我對弈學習
    """
    def generate_game_data(self, network, temperature=1.0):
        states = []
        policies = []
        values = []

        state = initial_state()

        while not state.is_terminal():
            # MCTS 搜索
            mcts = MCTS(network)
            action_probs = mcts.search(state, num_simulations=1600)

            # 記錄
            states.append(state)
            policies.append(action_probs)

            # 執行動作
            state = state.step(action_probs)

        # 計算遊戲結果
        game_result = state.game_result()

        # 所有局面的價值是遊戲結果
        values = [-game_result for _ in states]

        return states, policies, values
```

### 訓練流程

```python
def train_alpha_go_zero():
    """
    AlphaGo Zero 的完整訓練流程
    """
    network = AlphaGoZeroNetwork()
    optimizer = torch.optim.Adam(network.parameters(), lr=0.01)

    for iteration in range(700):
        # 1. 自我對弈生成資料
        game_data = self_play(network)

        # 2. 更新網路
        for epoch in range:
            states, policies, values = game_data

            policy_logits, value = network(states)
            policy_loss = F.cross_entropy(policy_logits, policies)
            value_loss = F.mse_loss(value.squeeze(), values)
            loss = policy_loss + value_loss

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
```

## 為什麼這重要？

### 1. 樣本效率

```
傳統方法：需要數百萬個人類棋譜
AlphaGo Zero：只靠自我對弈，40天超越所有人類知識
```

### 2. 泛化能力

AlphaGo Zero 的方法可以推廣到其他領域：
- 蛋白質結構預測 (AlphaFold)
- 數學定理證明
- 通用遊戲 AI

### 3. 科學意義

展示了「智慧可以在沒有先驗知識的情況下產生」

## 對 AI 領域的影響

```python
# AlphaFold (2018-) - 蛋白質折疊預測
# 基於 AlphaGo Zero 的思想

# Muzero (2020) - 通用強化學習
# 完全無模型的強化學習

# AlphaCode (2022) - 程式設計
# 程式設計競賽達到人類水準
```

## 結論

AlphaGo 和 AlphaGo Zero 的成就不僅是圍棋領域的突破，更是人工智慧發展的重要里程碑。它們展示了深度強化學習的巨大潛力，為未來 AI 研究指明了方向。

---

**延伸閱讀**

- [AlphaGo Paper (Silver et al., 2016)](https://www.google.com/search?q=AlphaGo+Silver+2016+paper)
- [AlphaGo Zero Paper (Silver et al., 2017)](https://www.google.com/search?q=AlphaGo+Zero+2017+paper)
- [DeepMind AlphaGo Page](https://www.google.com/search?q=DeepMind+AlphaGo)

---

*本篇文章為「AI 程式人雜誌 2017 年 12 月號」年終回顧系列之一。*