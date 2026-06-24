# 深度 Q 網路與價值方法（2013-2028）

## 從 Q-Learning 到深度 Q 網路

傳統的 Q-Learning 使用表格儲存每個狀態-動作對的 Q 值。但當狀態空間連續（如圖像、感測器資料）時，表格方法完全不可行。

2013 年，DeepMind 的 Volodymyr Mnih 等人發表了 DQN（Deep Q-Network），用卷積神經網路來近似 Q 函數。DQN 的輸入是原始遊戲畫面（84×84 灰階圖），輸出是每個動作的 Q 值。

```
Q(s, a; θ) ≈ Q*(s, a)
```

其中 θ 是神經網路的參數。

## DQN 的兩大創新

### 經驗回放（Experience Replay）

DQN 將過去的經歷 (s, a, r, s') 存入回放記憶體，訓練時隨機取樣：

```python
import random
from collections import deque

class ReplayBuffer:
    def __init__(self, capacity=10000):
        self.buffer = deque(maxlen=capacity)

    def push(self, state, action, reward, next_state, done):
        self.buffer.append((state, action, reward, next_state, done))

    def sample(self, batch_size):
        return random.sample(self.buffer, min(batch_size, len(self.buffer)))

    def size(self):
        return len(self.buffer)
```

經驗回放打破樣本間的相關性，使訓練更穩定。

### 目標網路（Target Network）

DQN 使用兩個網路：在線網路 Q(s,a;θ) 和目標網路 Q(s,a;θ⁻)。目標網路的參數定期從在線網路複製：

```
Loss = (r + γ maxₐ' Q(s', a'; θ⁻) - Q(s, a; θ))²
```

## DQN 的演進（2015-2020）

### Double DQN (2015)

Hado van Hasselt 發現 DQN 傾向於高估 Q 值，因為 max 操作引入了正向偏差。Double DQN 使用在線網路選動作，目標網路算 Q 值：

```
Q_target = r + γ Q(s', argmaxₐ' Q(s', a'; θ); θ⁻)
```

### Prioritized Experience Replay (2016)

並非所有經驗同樣重要。優先級回放根據 TD-error 的絕對值分配取樣機率：

```python
class PrioritizedReplayBuffer:
    def __init__(self, capacity=10000, alpha=0.6):
        self.buffer = []
        self.priorities = []
        self.capacity = capacity
        self.alpha = alpha

    def push(self, state, action, reward, next_state, done, td_error):
        priority = (abs(td_error) + 1e-5) ** self.alpha
        if len(self.buffer) < self.capacity:
            self.buffer.append((state, action, reward, next_state, done))
            self.priorities.append(priority)
        else:
            self.buffer[self.pos] = (state, action, reward, next_state, done)
            self.priorities[self.pos] = priority
```

### Dueling DQN (2016)

將 Q 值分解為狀態價值 V(s) 和優勢函數 A(s,a)：

```
Q(s,a) = V(s) + A(s,a) - mean(A(s,:))
```

這種分解使網路能更有效地學習哪些狀態有價值，而不需考慮每個動作。

### Rainbow DQN (2017)

DeepMind 將六種 DQN 改進整合為單一演算法——Rainbow，在多項 Atari 遊戲上達到當時最佳表現。

## 從離散到連續控制（2018-2023）

DQN 只能處理離散動作空間。對於連續控制任務，研究者發展了基於價值的方法：

**DDPG（Deep Deterministic Policy Gradient）**：結合 DQN 和策略梯度，使用確定性策略：

```
Q(s,a) 的梯度指導策略 μ(s) 的更新
∇_θ J ≈ E[∇_a Q(s,a|θ^Q) · ∇_θ μ(s|θ^μ)]
```

**TD3（Twin Delayed DDPG, 2018）**：引入剪切雙 Q 學習、延遲策略更新和目標策略平滑，解決了 DDPG 的 Q 值高估問題。

**SAC（Soft Actor-Critic, 2018）**：在目標函數中增加熵項，鼓勵探索：

```
J(π) = E[ Σ_t r(s_t, a_t) + α H(π(·|s_t)) ]
```

SAC 在連續控制任務上表現出色，目前仍是主流演算法之一。

## 價值方法的應用（2023-2028）

2023 年後，價值方法在以下領域持續發展：

- **離線 RL**：從固定資料集中學習策略，無需與環境互動（CQL, IQL）
- **分佈式 RL**：學習回報的完整分佈而非期望值（C51, QR-DQN）
- **決策 Transformer**：將 RL 視為序列建模問題，使用 Transformer 架構

2028 年的價值方法趨勢是「隱式 Q 學習」（Implicit Q-Learning）和「分佈式決策模型」，在不與環境互動的情況下實現高效學習。

## 延伸閱讀

- [DQN 原始論文](https://www.google.com/search?q=Playing+Atari+with+Deep+Reinforcement+Learning+Mnih+2013)
- [Rainbow DQN](https://www.google.com/search?q=Rainbow+Combining+Improvements+in+Deep+Reinforcement+Learning)
- [SAC 演算法](https://www.google.com/search?q=Soft+Actor-Critic+Off-Policy+Maximum+Entropy+Deep+Reinforcement+Learning)

*本篇文章為「AI 程式人雜誌 2028 年 5 月號」強化學習系列之一。*
