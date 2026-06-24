# Deep Q-Network (DQN)

## 深度學習遇見強化學習

DQN (2013) 將深度學習應用於強化學習，使用神經網路近似 Q 函數，處理高維度狀態空間（如影像）。

## DQN 的挑戰

強化學習與深度學習結合面臨的問題：

1. **非穩態分佈**：資料分佈隨策略變化
2. **樣本相關性**：相鄰時間步的樣本高度相關
3. **目標不穩定**：Q 值估計的目標持續變化

## 解決方案：經驗回放與目標網路

### 經驗回放（Experience Replay）

將交互經驗存入 replay buffer，隨機取樣打斷時間相關性。

```python
import numpy as np
from collections import deque
import random

class ReplayBuffer:
    def __init__(self, capacity=10000):
        self.buffer = deque(maxlen=capacity)

    def push(self, state, action, reward, next_state, done):
        self.buffer.append((state, action, reward, next_state, done))

    def sample(self, batch_size):
        batch = random.sample(self.buffer, batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)
        return (np.array(states), np.array(actions),
                np.array(rewards), np.array(next_states),
                np.array(dones))

    def __len__(self):
        return len(self.buffer)
```

### 目標網路（Target Network）

使用延遲更新的目標網路計算 TD 目標。

```python
import copy

class DQN:
    def __init__(self, state_dim, action_dim, hidden_dim=128, lr=0.001):
        self.action_dim = action_dim

        # 線上網路（用於選擇動作）
        self.q_network = self.build_network(state_dim, action_dim, hidden_dim)

        # 目標網路（用於計算 TD 目標）
        self.target_network = self.build_network(state_dim, action_dim, hidden_dim)
        self.target_network.set_weights(self.q_network.get_weights())

        self.optimizer = tf.keras.optimizers.Adam(lr)

    def build_network(self, state_dim, action_dim, hidden_dim):
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(hidden_dim, activation='relu', input_shape=(state_dim,)),
            tf.keras.layers.Dense(hidden_dim, activation='relu'),
            tf.keras.layers.Dense(action_dim)
        ])
        return model

    def update_target(self):
        self.target_network.set_weights(self.q_network.get_weights())
```

## DQN 演算法

```python
def train_dqn(agent, env, replay_buffer, n_episodes=500, batch_size=32,
              gamma=0.99, epsilon=1.0, epsilon_decay=0.995, epsilon_min=0.01,
              target_update_freq=10):

    for episode in range(n_episodes):
        state = env.reset()
        total_reward = 0
        done = False

        while not done:
            # epsilon-greedy 選擇動作
            if np.random.random() < epsilon:
                action = env.action_space.sample()
            else:
                action = np.argmax(agent.q_network.predict(state))

            next_state, reward, done, _ = env.step(action)

            # 儲存經驗
            replay_buffer.push(state, action, reward, next_state, done)

            # 從 replay buffer 取樣訓練
            if len(replay_buffer) >= batch_size:
                batch = replay_buffer.sample(batch_size)
                states, actions, rewards, next_states, dones = batch

                # 計算 TD 目標
                next_q_values = agent.target_network.predict(next_states)
                max_next_q = np.max(next_q_values, axis=1)
                targets = rewards + gamma * max_next_q * (1 - dones)

                # 計算損失並更新
                with tf.GradientTape() as tape:
                    current_q = agent.q_network(states)
                    action_mask = tf.one_hot(actions, agent.action_dim)
                    current_q = tf.reduce_sum(current_q * action_mask, axis=1)
                    loss = tf.reduce_mean((targets - current_q) ** 2)

                grads = tape.gradient(loss, agent.q_network.trainable_variables)
                agent.optimizer.apply_gradients(zip(grads, agent.q_network.trainable_variables))

            state = next_state
            total_reward += reward

        # 更新目標網路
        if episode % target_update_freq == 0:
            agent.update_target()

        # epsilon 衰減
        epsilon = max(epsilon * epsilon_decay, epsilon_min)

        if episode % 50 == 0:
            print(f"Episode {episode}, Reward: {total_reward}, Epsilon: {epsilon:.3f}")
```

## Double DQN

傳統 DQN 對 Q 值過度估計。Double DQN 使用兩個網路分離動作選擇與價值估計。

```python
def double_dqn_update(agent, states, actions, rewards, next_states, dones):
    # 使用線上網路選擇動作
    next_actions = np.argmax(agent.q_network.predict(next_states), axis=1)

    # 使用目標網路估計價值
    next_q_values = agent.target_network.predict(next_states)
    next_q_values = next_q_values[np.arange(len(next_actions)), next_actions]

    # 計算目標
    targets = rewards + gamma * next_q_values * (1 - dones)

    # 更新線上網路
    with tf.GradientTape() as tape:
        current_q = agent.q_network(states)
        action_mask = tf.one_hot(actions, agent.action_dim)
        current_q = tf.reduce_sum(current_q * action_mask, axis=1)
        loss = tf.reduce_mean((targets - current_q) ** 2)

    grads = tape.gradient(loss, agent.q_network.trainable_variables)
    agent.optimizer.apply_gradients(zip(grads, agent.q_network.trainable_variables))
```

## DQN 變體

### 優先經驗回放（Prioritized Experience Replay）

根據 TD 誤差大小給予抽樣優先權。

```python
class PrioritizedReplayBuffer:
    def __init__(self, capacity=10000, alpha=0.6):
        self.capacity = capacity
        self.alpha = alpha
        self.priorities = np.zeros(capacity)
        self.buffer = deque(maxlen=capacity)
        self.position = 0

    def push(self, state, action, reward, next_state, done):
        max_priority = self.priorities.max() if self.buffer else 1.0
        self.buffer.append((state, action, reward, next_state, done))
        self.priorities[self.position] = max_priority
        self.position = (self.position + 1) % self.capacity

    def sample(self, batch_size, beta=0.4):
        if len(self.buffer) == self.capacity:
            priorities = self.priorities
        else:
            priorities = self.priorities[:self.position]

        probabilities = priorities ** self.alpha
        probabilities /= probabilities.sum()

        indices = np.random.choice(len(self.buffer), batch_size, p=probabilities)
        weights = (len(self.buffer) * probabilities[indices]) ** (-beta)
        weights /= weights.max()

        batch = [self.buffer[i] for i in indices]
        states, actions, rewards, next_states, dones = zip(*batch)

        return states, actions, rewards, next_states, dones, indices, weights
```

### Dueling DQN

分離價值函數與優勢函數。

```
Q(s,a) = V(s) + A(s,a)
```

```python
def build_dueling_network(state_dim, action_dim):
    inputs = tf.keras.layers.Input(shape=(state_dim,))
    x = tf.keras.layers.Dense(128, activation='relu')(inputs)
    x = tf.keras.layers.Dense(128, activation='relu')(x)

    # 價值函數
    v = tf.keras.layers.Dense(1)(x)

    # 優勢函數
    a = tf.keras.layers.Dense(action_dim)(x)
    a = a - tf.reduce_mean(a, axis=1, keepdims=True)

    # Q = V + A
    q = v + a

    return tf.keras.Model(inputs=inputs, outputs=q)
```

## Atari 遊戲中的 DQN

```python
# 典型的 Atari DQN 配置
config = {
    'state_dim': (84, 84, 4),  # 連續 4 幀，84x84 灰階
    'action_dim': 4,           # 4 個遊戲動作
    'replay_capacity': 1000000,
    'batch_size': 32,
    'gamma': 0.99,
    'epsilon_start': 1.0,
    'epsilon_end': 0.1,
    'epsilon_decay_steps': 1000000,
    'target_update_freq': 10000,
    'learning_freq': 4,
}
```

## 總結

DQN 開創了深度強化學習的時代：
- 使用神經網路逼近 Q 函數
- 經驗回放解決樣本相關性
- 目標網路解決非穩態問題
- 後續有多種改進：Double DQN、Prioritized ER、Dueling DQN 等