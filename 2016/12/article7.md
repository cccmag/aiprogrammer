# 強化學習的突破

## 前言

2016 年，強化學習取得了歷史性的突破——AlphaGo 擊敗了世界圍棋冠軍。本文探討強化學習的核心概念和 AlphaGo 背後的技術。

## 強化學習基礎

### Agent-Environment 互動

```python
class Agent:
    """強化學習 Agent"""
    def __init__(self):
        self.policy = {}  # 策略：狀態 -> 動作
        self.value = {}   # 值函式：狀態 -> 價值

    def select_action(self, state):
        """根據策略選擇動作"""
        if state in self.policy:
            return self.policy[state]
        return self.get_random_action()

    def update(self, state, action, reward, next_state):
        """更新策略和值函式"""
        pass


class Environment:
    """強化學習環境"""
    def __init__(self):
        self.state = None

    def reset(self):
        """重置環境"""
        self.state = self.get_initial_state()

    def step(self, action):
        """執行動作，返回 (next_state, reward, done)"""
        next_state = self.do_action(action)
        reward = self.get_reward(next_state)
        done = self.is_terminal(next_state)
        return next_state, reward, done
```

### 馬可夫決策過程（MDP）

```python
mdp_components = {
    'S': '狀態空間 (States)',
    'A': '動作空間 (Actions)',
    'P': '轉換機率 (Transition Probability)',
    'R': '獎勵函式 (Reward Function)',
    'gamma': '折扣因子 (Discount Factor)',
}

# MDP 示例：格子世界
def grid_world_mdp():
    """
    簡單的格子世界 MDP
    目標：從左上角走到右下角
    """
    states = [(i, j) for i in range(4) for j in range(4)]
    actions = ['up', 'down', 'left', 'right']

    # 轉換機率（確定性）
    transition = {
        'up': (0, 1),
        'down': (0, -1),
        'left': (-1, 0),
        'right': (1, 0),
    }

    return states, actions, transition
```

## Q-Learning

### Q 表學習

```python
import numpy as np

class QLearningAgent:
    def __init__(self, state_space, action_space, learning_rate=0.1, gamma=0.95):
        self.lr = learning_rate
        self.gamma = gamma
        self.q_table = np.zeros((state_space, action_space))

    def update(self, state, action, reward, next_state):
        """Q-Learning 更新規則"""
        best_next_action = np.argmax(self.q_table[next_state])
        td_target = reward + self.gamma * self.q_table[next_state][best_next_action]
        td_error = td_target - self.q_table[state][action]
        self.q_table[state][action] += self.lr * td_error

    def select_action(self, state, epsilon=0.1):
        """Epsilon-greedy 策略"""
        if np.random.random() < epsilon:
            return np.random.randint(len(self.q_table[state]))
        return np.argmax(self.q_table[state])


def train_q_learning(episodes=1000):
    agent = QLearningAgent(state_space=16, action_space=4)

    for episode in range(episodes):
        state = 0  # 初始狀態
        done = False

        while not done:
            action = agent.select_action(state)
            next_state, reward, done = env.step(action)
            agent.update(state, action, reward, next_state)
            state = next_state

    return agent.q_table
```

## Deep Q-Network (DQN)

### 用深度學習近似 Q 函式

```python
import tensorflow as tf

class DQN:
    def __init__(self, state_size, action_size):
        self.model = tf.keras.Sequential([
            tf.keras.layers.Dense(24, activation='relu', input_shape=(state_size,)),
            tf.keras.layers.Dense(24, activation='relu'),
            tf.keras.layers.Dense(action_size, activation='linear')
        ])
        self.model.compile(optimizer=tf.keras.optimizers.Adam(0.001),
                          loss='mse')

    def predict(self, state):
        return self.model.predict(state)

    def train(self, states, targets):
        self.model.fit(states, targets, epochs=1, verbose=0)


class ReplayBuffer:
    """經驗回放記憶"""
    def __init__(self, capacity=10000):
        self.buffer = []
        self.capacity = capacity

    def add(self, experience):
        self.buffer.append(experience)
        if len(self.buffer) > self.capacity:
            self.buffer.pop(0)

    def sample(self, batch_size):
        return np.random.choice(len(self.buffer), batch_size, replace=False)
```

## AlphaGo 的架構

### 兩個神經網路

```python
alpha_go_components = """
AlphaGo 核心元件：

1. 策略網路 (Policy Network)
   - 輸入：當前棋盤狀態
   - 輸出：每個動作的機率
   - 訓練：監督學習 + 強化學習

2. 價值網路 (Value Network)
   - 輸入：當前棋盤狀態
   - 輸出：當前玩家獲勝的機率
   - 訓練：監督學習

3. Monte Carlo Tree Search (MCTS)
   - 結合策略網路和價值網路
   - 模擬大量對局
   - 選擇最高價值的動作
"""
```

### 監督學習預訓練

```python
class PolicyNetwork:
    def __init__(self):
        self.model = tf.keras.Sequential([
            tf.keras.layers.Conv2D(64, 3, activation='relu', input_shape=(19, 19, 17)),
            tf.keras.layers.Conv2D(64, 3, activation='relu'),
            tf.keras.layers.Conv2D(64, 3, activation='relu'),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(362, activation='softmax')  # 19x19 + pass = 362
        ])

    def train(self, states, moves):
        """使用人類專家棋譜訓練"""
        self.model.compile(optimizer='adam', loss='categorical_crossentropy')
        self.model.fit(states, moves, epochs=1)

class ValueNetwork:
    def __init__(self):
        self.model = tf.keras.Sequential([
            tf.keras.layers.Conv2D(64, 3, activation='relu', input_shape=(19, 19, 17)),
            tf.keras.layers.Conv2D(64, 3, activation='relu'),
            tf.keras.layers.Conv2D(64, 3, activation='relu'),
            tf.keras.layers.Conv2D(1, 1, activation='relu'),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(256, activation='relu'),
            tf.keras.layers.Dense(1, activation='tanh')
        ])
```

## Policy Gradient

### REINFORCE 算法

```python
class PolicyGradientAgent:
    def __init__(self, state_size, action_size):
        self.model = tf.keras.Sequential([
            tf.keras.layers.Dense(24, activation='relu', input_shape=(state_size,)),
            tf.keras.layers.Dense(action_size, activation='softmax')
        ])
        self.optimizer = tf.keras.optimizers.Adam(0.01)

    def select_action(self, state):
        probs = self.model.predict(state)
        return np.random.choice(len(probs[0]), p=probs[0])

    def train(self, states, actions, rewards):
        """Policy Gradient 更新"""
        with tf.GradientTape() as tape:
            action_probs = self.model(states)
            action_masks = tf.one_hot(actions, depth=len(action_probs[0]))
            masked_probs = action_probs * action_masks
            selected_log_probs = tf.reduce_sum(masked_probs, axis=1)
            loss = -tf.reduce_mean(selected_log_probs * rewards)

        gradients = tape.gradient(loss, self.model.trainable_variables)
        self.optimizer.apply_gradients(zip(gradients, self.model.trainable_variables))
```

## 强化學習的應用

```python
rl_applications = {
    '遊戲': 'Atari 遊戲、圍棋、象棋',
    '機器人': '運動控制、導航',
    '推薦系統': '動態推薦',
    '自動駕駛': '路徑規劃',
    '資源管理': '資料中心冷源管理',
    '金融': '交易策略',
}
```

## 小結

2016 年是強化學習的突破年。AlphaGo 的成功展示了深度強化學習在複雜策略遊戲中的潛力。從 Q-Learning 到 DQN，再到 AlphaGo 的策略網路和價值網路，強化學習演算法正在不斷進化，應用範圍也越來越廣泛。

---

**延伸閱讀**

- [DeepMind AlphaGo Paper](https://www.google.com/search?q=AlphaGo+Nature+2016+paper)
- [Reinforcement Learning: An Introduction](https://www.google.com/search?q=reinforcement+learning+Sutton+Barto)
- [DQN Tutorial](https://www.google.com/search?q=deep+Q+network+tutorial)