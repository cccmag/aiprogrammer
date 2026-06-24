# 強化學習基礎

## 前言

強化學習（Reinforcement Learning, RL）是機器學習的重要分支，專注於如何讓代理人在環境中學習做出一系列決策。2008 年時，強化學習在遊戲和機器人控制領域已有諸多應用。

## 強化學習的核心概念

### 代理與環境

```python
# 強化學習的基本框架

rl_framework = {
    "代理人 (Agent)": "學習者和決策者",
    "環境 (Environment)": "代理人所在的外部世界",
    "狀態 (State)": "環境的當前描述",
    "動作 (Action)": "代理人可以執行的行為",
    "獎勵 (Reward)": "環境對動作的回饋"
}

# 互動流程
# Agent 觀察 State → 執行動作 Action → 環境回傳 Reward 和新 State
```

### 回饋循環

```
    ┌─────────┐
    │  Agent  │
    └────┬────┘
         │
         │ 動作 (Action)
         ▼
    ┌─────────┐
    │ 環境    │◄──── 獎勵 (Reward)
    │Environment│
    └────┬────┘
         │
         │ 新狀態 (State')
         ▼
```

## 馬可夫決策過程（MDP）

### 定義

```python
mdp_definition = {
    "S": "狀態空間（所有可能狀態的集合）",
    "A": "動作空間（所有可能動作的集合）",
    "P": "轉移機率 P(s'|s, a)",
    "R": "獎勵函數 R(s, a, s')",
    "γ": "折扣因子 (0 ≤ γ < 1)"
}
```

### 轉移機率

```python
# P(s'|s, a) 表示在狀態 s 執行動作 a 後轉移到 s' 的機率

transition_example = {
    "問題": "Grid World",
    "狀態": "位置 (x, y)",
    "動作": "上、下、左、右",
    "轉移": "確定性或機率性"
}
```

## 價值函數

### 狀態價值函數

```python
# V(s) = 從狀態 s 開始，遵循策略 π 的預期回報

state_value_function = {
    "定義": "V^π(s) = E_π[Σ(γ^t * R_t) | S_t = s]",
    "含義": "在狀態 s 的長期價值",
    "計算": "遞迴關係（貝爾曼方程式）"
}

# 貝爾曼方程式：
# V^π(s) = Σ_a π(a|s) * Σ_{s'} P(s'|s,a) * [R(s,a,s') + γV^π(s')]
```

### 動作價值函數

```python
# Q(s, a) = 從狀態 s 執行動作 a，之後遵循策略 π 的預期回報

action_value_function = {
    "定義": "Q^π(s, a) = E_π[Σ(γ^t * R_t) | S_t = s, A_t = a]",
    "含義": "在狀態 s 執行動作 a 的長期價值"
}
```

## Q 學習

### 離策略學習

```python
# Q 學習是一種離策略（off-policy）方法

q_learning = {
    "核心": "直接最佳化動作價值函數 Q(s, a)",
    "更新規則": "Q(s, a) ← Q(s, a) + α[r + γ max Q(s', a') - Q(s, a)]",
    "特點": "最終收斂到最佳 Q 函數"
}
```

### Q 表

```python
# 簡單的 Q 學習使用表格存储 Q 值

q_table_example = {
    "大小": "|S| × |A|",
    "更新": "每次互動更新一個條目",
    "限制": "只適用於狀態和動作數量有限的情況"
}

# 對於大型狀態空間，需要函數近似（後來使用深度學習）
```

## 探索與利用

### 探索-利用困境

```python
# 探索與利用的平衡

exploration_exploitation = {
    "利用 (Exploitation)": "選擇目前已知最優的動作",
    "探索 (Exploration)": "嘗試新的動作以獲取更多資訊",
    "困境": "兩者之間需要平衡"
}
```

### 策略

```python
epsilon_greedy = {
    "epsilon": "探索機率（通常 0.1 或 0.01）",
    "行為": "以 1-epsilon 的機率選擇最佳動作",
    "行為": "以 epsilon 的機率隨機選擇"
}

# 隨著學習進行，逐漸降低 epsilon
```

## 深度強化學習的萌芽

### 2008 年的狀況

```python
rl_state_2008 = {
    "傳統方法": "Q 學習、TD 學習、Policy Gradient",
    "函數近似": "使用類神經網路近似 Q 函數（2013 年後才普及）",
    "應用": "簡單遊戲、機器人控制",
    "挑戰": "維度災難、穩定性問題"
}
```

### 神經網路與 RL

```python
# 早期類神經網路用於 RL

neural_rl_early = {
    "TD-Gammon (1992)": "使用 MLP 玩西洋雙陸棋",
    "神經網路近似": "Q(s, a) ≈ NN(s, a)",
    "問題": "訓練不穩定，收斂困難"
}
```

## Policy Gradient 方法

### 直接策略學習

```python
# Policy Gradient 直接學習策略函數 π(a|s)

policy_gradient = {
    "目標": "找到最大化預期回報的策略參數",
    "更新": "根據回報調整動作機率",
    "優點": "適用於連續動作空間"
}

# 簡化更新規則：
# θ ← θ + α * ∇_θ J(θ)
# 其中 J 是策略的效能函數
```

## 應用領域

### 遊戲

```python
game_applications = {
    "TD-Gammon": "西洋雙陸棋（1992）",
    "Atari 遊戲": "2013 年的突破（DQN）",
    "圍棋": "AlphaGo（2016）",
    "星海爭霸": "AlphaStar（2019）"
}
```

### 機器人控制

```python
robot_applications = {
    "運動控制": "學習走路的動作",
    "操作": "學習抓取物體",
    "導航": "學習在環境中移動"
}
```

## 挑戰

### 樣本效率

```python
# 強化學習的主要挑戰

sample_efficiency = {
    "問題": "需要大量互動才能學習",
    "原因": "每個樣本只提供稀疏的回報",
    "方向": "遷移學習、層次強化學習"
}
```

### 穩定性

```python
# 訓練穩定性問題

stability_issues = {
    "非平穩性": "策略改變導致資料分佈改變",
    "回報稀疏": "很多步驟都沒有回報信號",
    "區域最小值": "可能陷入不良策略"
}
```

## 基礎實作

### 簡單的 Q 學習

```python
import random

class SimpleQLearning:
    def __init__(self, states, actions, learning_rate=0.1, gamma=0.9):
        self.q = [[0.0] * actions for _ in range(states)]
        self.lr = learning_rate
        self.gamma = gamma

    def update(self, state, action, reward, next_state):
        best_next = max(self.q[next_state])
        td_target = reward + self.gamma * best_next
        td_error = td_target - self.q[state][action]
        self.q[state][action] += self.lr * td_error

    def choose_action(self, state, epsilon=0.1):
        if random.random() < epsilon:
            return random.randint(0, len(self.q[state]) - 1)
        else:
            return max(range(len(self.q[state])), key=lambda i: self.q[state][i])
```

## 未來展望

### 即將到來的突破

```python
upcoming_breakthroughs = {
    "2013": "DQN 在 Atari 遊戲突破",
    "2015": "Deep Q-Learning 論文",
    "2016": "AlphaGo 擊敗圍棋冠軍",
    "2017": "Proximal Policy Optimization (PPO)"
}
```

---

**延伸閱讀**

- [Reinforcement learning tutorial](https://www.google.com/search?q=Reinforcement+learning+tutorial)
- [Q+learning+algorithm](https://www.google.com/search?q=Q+learning+algorithm)
- [MDP+reinforcement+learning](https://www.google.com/search?q=MDP+reinforcement+learning)