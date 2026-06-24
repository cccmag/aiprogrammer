# Q-Learning 與 DQN

## 1. 引言

在強化學習中，除了直接最佳化策略（策略梯度方法），另一條路線是透過學習值函數來間接得到最佳策略。Q-Learning 是這條路線的經典演算法，而 DQN（Deep Q-Network）則將其擴展到深度學習時代。

## 2. Q-Learning 基礎

Q-Learning 的目標是學習最優動作值函數 Q*(s, a)，表示在狀態 s 採取動作 a 後，按照最優策略行動所能獲得的期望累積獎勵。

### Q 表更新公式

```
Q(s, a) ← Q(s, a) + α [ r + γ max_a' Q(s', a') - Q(s, a) ]
```

其中：
- α：學習率
- r：即時獎勵
- γ：折扣因子
- max_a' Q(s', a')：下一狀態的最優 Q 值估計

### 離策略學習

Q-Learning 是離策略（off-policy）演算法——它可以從其他策略產生的資料中學習。這意味著 Q-Learning 可以重複使用歷史經驗，提高樣本效率。

## 3. 從 Q 表到深度網路

傳統 Q-Learning 使用 Q 表儲存每個 (s, a) 的 Q 值。但當狀態空間很大（如圖像、文字）時，Q 表不可行。DQN 使用神經網路近似 Q 函數：

```
Q(s, a; θ) ≈ Q*(s, a)
```

### DQN 的關鍵技巧

**經驗回放（Experience Replay）**：
儲存過去的經驗 (s, a, r, s') 到回放緩衝區，訓練時隨機取樣。這打破了時間關聯性，穩定訓練。

```
回放緩衝區：[e_1, e_2, ..., e_N]
訓練取樣：隨機批次
```

**目標網路（Target Network）**：
使用一個定期更新的目標網路計算 TD 目標，減少訓練震盪：

```
L(θ) = E[ (r + γ max_a' Q(s', a'; θ_target) - Q(s, a; θ))^2 ]
```

## 4. DQN 的架構

```python
class DQN:
    def __init__(self):
        self.q_network = QNetwork()      # 主網路
        self.target_network = QNetwork() # 目標網路
        self.replay_buffer = []          # 經驗回放
        self.epsilon = 1.0               # 探索率

    def act(self, state):
        if random() < self.epsilon:  # 探索
            return random_action()
        return argmax(self.q_network(state))  # 利用

    def train(self, batch):
        states, actions, rewards, next_states = batch
        targets = rewards + gamma * max(self.target_network(next_states))
        loss = MSE(self.q_network(states)[actions], targets)
        # 更新 q_network
        # 定期同步 target_network = q_network
```

## 5. DQN 的變體

- **Double DQN**：解耦動作選擇和評估，減少 Q 值過高估計
- **Dueling DQN**：分離狀態值和動作優勢的估計
- **PER（Prioritized Experience Replay）**：優先取樣重要經驗

## 6. 為什麼 RLHF 不使用 DQN？

RLHF 選擇 PPO 而非 DQN，有幾個關鍵原因：

1. **動作空間**：語言模型的動作是詞元（離散且超大），DQN 需要計算 max_a Q(s, a)，對超大動作空間不可行
2. **序列生成**：詞元序列的聯合動作空間是指數級，Q-Learning 難以處理
3. **策略隨機性**：語言模型需要隨機性（溫度採樣），而 DQN 天生是確定性策略

## 7. 結語

Q-Learning 和 DQN 在值函數為基礎的 RL 中佔有重要地位，特別是在遊戲和機器人控制等領域。但在語言模型的場景中，基於策略的方法（如 PPO）更加適合。理解 DQN 有助於理解 Actor-Critic 架構的設計動機。

## 延伸閱讀

- [DQN 原始論文](https://www.google.com/search?q=playing+atari+with+deep+reinforcement+learning)
- [Q-Learning 教學](https://www.google.com/search?q=Q+learning+tutorial+python)
