# Policy Gradient 方法

## 為什麼需要 Policy Gradient？

Q-learning 和 DQN 等基於價值的方法有局限性：
- 連續動作空間難以處理
- 高度隨機策略難以學習
- 容易過估計 Q 值

Policy Gradient 直接優化策略 π(a|s)。

## 策略函數

策略 π(a|s, θ) 是由參數 θ 定義的機率分布。

```python
import numpy as np

class SoftmaxPolicy:
    def __init__(self, state_dim, action_dim, hidden_dim=128):
        self.model = tf.keras.Sequential([
            tf.keras.layers.Dense(hidden_dim, activation='relu', input_shape=(state_dim,)),
            tf.keras.layers.Dense(action_dim)
        ])

    def probs(self, state):
        logits = self.model(state)
        return tf.nn.softmax(logits)

    def action(self, state):
        probs = self.probs(state)
        return np.random.choice(len(probs), p=probs.numpy())
```

## 策略梯度定理

對於可微分的策略 π(a|s, θ)，策略梯度為：

∇_θ J(θ) = E_π [∇_θ log π(a|s,θ) · Q^π(s, a)]

其中 J(θ) 是目標函數（通常是初始狀態價值或平均獎賞）。

```python
def compute_policy_gradient_loss(states, actions, returns, policy):
    """計算策略梯度損失"""
    with tf.GradientTape() as tape:
        logits = policy.model(states)
        action_mask = tf.one_hot(actions, logits.shape[-1])
        log_probs = tf.reduce_sum(tf.nn.log_softmax(logits) * action_mask, axis=1)

        # 損失是負的加權對數機率（因為要最大化）
        loss = -tf.reduce_mean(log_probs * returns)

    return loss, tape.gradient(loss, policy.model.trainable_variables)
```

## REINFORCE 演算法

最基本的策略梯度方法。

```python
class REINFORCE:
    def __init__(self, state_dim, action_dim, lr=0.001):
        self.policy = SoftmaxPolicy(state_dim, action_dim)
        self.optimizer = tf.keras.optimizers.Adam(lr)

    def generate_episode(self, env):
        states, actions, rewards = [], [], []
        state = env.reset()

        done = False
        while not done:
            probs = self.policy.probs(state.reshape(1, -1)).numpy()[0]
            action = np.random.choice(len(probs), p=probs)

            states.append(state)
            actions.append(action)

            state, reward, done, _ = env.step(action)
            rewards.append(reward)

        return np.array(states), np.array(actions), np.array(rewards)

    def compute_returns(self, rewards, gamma=0.99):
        """計算折扣回報"""
        returns = []
        G = 0
        for r in reversed(rewards):
            G = r + gamma * G
            returns.insert(0, G)

        returns = np.array(returns)

        # 標準化（穩定訓練）
        returns = (returns - returns.mean()) / (returns.std() + 1e-8)
        return returns

    def update(self, env):
        states, actions, rewards = self.generate_episode(env)
        returns = self.compute_returns(rewards)

        # 策略梯度更新
        with tf.GradientTape() as tape:
            logits = self.policy.model(states)
            action_mask = tf.one_hot(actions, logits.shape[-1])
            log_probs = tf.reduce_sum(tf.nn.log_softmax(logits) * action_mask, axis=1)
            loss = -tf.reduce_mean(log_probs * returns)

        grads = tape.gradient(loss, self.policy.model.trainable_variables)
        self.optimizer.apply_gradients(zip(grads, self.policy.model.trainable_variables))

        return sum(rewards)
```

## Actor-Critic

結合策略梯度（Actor）與價值函數（Critic）。

```python
class ActorCritic:
    def __init__(self, state_dim, action_dim, hidden_dim=128, lr=0.001, gamma=0.99):
        self.gamma = gamma

        # Actor：策略網路
        self.actor = tf.keras.Sequential([
            tf.keras.layers.Dense(hidden_dim, activation='relu', input_shape=(state_dim,)),
            tf.keras.layers.Dense(action_dim)
        ])

        # Critic：價值網路
        self.critic = tf.keras.Sequential([
            tf.keras.layers.Dense(hidden_dim, activation='relu', input_shape=(state_dim,)),
            tf.keras.layers.Dense(1)
        ])

        self.actor_optimizer = tf.keras.optimizers.Adam(lr)
        self.critic_optimizer = tf.keras.optimizers.Adam(lr)

    def choose_action(self, state):
        probs = tf.nn.softmax(self.actor(state.reshape(1, -1))).numpy()[0]
        return np.random.choice(len(probs), p=probs)

    def update(self, state, action, reward, next_state, done):
        state = state.reshape(1, -1)
        next_state = next_state.reshape(1, -1)

        # Critic 更新：用 TD 目標計算價值損失
        with tf.GradientTape() as tape:
            v = self.critic(state)[0, 0]
            v_next = self.critic(next_state)[0, 0]
            td_target = reward + self.gamma * v_next * (1 - done)
            td_error = td_target - v
            critic_loss = td_error ** 2

        critic_grads = tape.gradient(critic_loss, self.critic.trainable_variables)
        self.critic_optimizer.apply_gradients(zip(critic_grads, self.critic.trainable_variables))

        # Actor 更新：用 TD 誤差加權的策略梯度
        with tf.GradientTape() as tape:
            logits = self.actor(state)
            log_probs = tf.nn.log_softmax(logits)
            action_log_prob = log_probs[0, action]
            actor_loss = -action_log_prob * td_error

        actor_grads = tape.gradient(actor_loss, self.actor.trainable_variables)
        self.actor_optimizer.apply_gradients(zip(actor_grads, self.actor.trainable_variables))
```

## Advantage Actor-Critic (A2C)

使用優勢函數替代 TD 誤差。

```python
class A2C:
    def update(self, states, actions, rewards, next_states, dones, gamma=0.99, lam=0.95):
        """
        使用 GAE (Generalized Advantage Estimation) 計算優勢估計
        """
        advantages = []
        returns = []

        # 從後向前計算
        G = 0
        for t in reversed(range(len(rewards))):
            G = rewards[t] + gamma * G * (1 - dones[t])
            returns.insert(0, G)

            # 簡單的優勢估計
            advantage = G - self.critic(states[t:t+1])[0, 0]
            advantages.insert(0, advantage)

        advantages = np.array(advantages)
        returns = np.array(returns)

        # 標準化優勢
        advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)

        # 同時更新 Actor 和 Critic
        self.train_step(states, actions, advantages, returns)
```

## 連續動作空間

用於機器人控制等連續動作問題。

```python
class GaussianPolicy:
    def __init__(self, state_dim, action_dim, hidden_dim=128):
        self.mean_network = tf.keras.Sequential([
            tf.keras.layers.Dense(hidden_dim, activation='relu', input_shape=(state_dim,)),
            tf.keras.layers.Dense(action_dim * 2)  # mean 和 log_std
        ])

    def get_action(self, state):
        output = self.mean_network(state.reshape(1, -1))[0]
        mean, log_std = output[:action_dim], output[action_dim:]
        std = tf.exp(log_std)

        action = tf.random.normal([action_dim], mean, std)
        return action.numpy()

    def log_prob(self, state, action):
        output = self.mean_network(state.reshape(1, -1))[0]
        mean, log_std = output[:action_dim], output[action_dim:]
        std = tf.exp(log_std)

        # 高斯分佈的對數機率
        diff = action - mean
        log_prob = -0.5 * tf.reduce_sum((diff / std) ** 2 + 2 * log_std + np.log(2 * np.pi), axis=-1)
        return log_prob
```

## PPO（Proximal Policy Optimization）

目前最流行的策略梯度方法之一，2017 年提出。

```python
class PPO:
    def __init__(self, policy, old_policy, clip_ratio=0.2, lr=0.0003):
        self.policy = policy
        self.old_policy = old_policy
        self.clip_ratio = clip_ratio

    def update(self, states, actions, advantages, old_log_probs):
        with tf.GradientTape() as tape:
            # 計算新的 log 機率
            new_log_probs = self.policy.log_prob(states, actions)

            # 比率
            ratio = tf.exp(new_log_probs - old_log_probs)

            # 裁剪
            clipped_ratio = tf.clip_by_value(ratio, 1 - self.clip_ratio, 1 + self.clip_ratio)

            # PPO 目標
            surrogate = tf.minimum(ratio * advantages, clipped_ratio * advantages)
            loss = -tf.reduce_mean(surrogate)

        grads = tape.gradient(loss, self.policy.model.trainable_variables)
        self.optimizer.apply_gradients(zip(grads, self.policy.model.trainable_variables))
```

## 總結

Policy Gradient 直接優化策略：
- **REINFORCE**：基礎的策略梯度方法
- **Actor-Critic**：結合價值估計降低方差
- **A2C/PPO**：穩定且高效的實際應用方法

與基於價值的方法比較，Policy Gradient 更適合連續動作空間和高度隨機的環境。