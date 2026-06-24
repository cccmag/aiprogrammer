# Actor-Critic 架構

## 為什麼需要 Actor-Critic？

純策略梯度（REINFORCE）方差高。
純價值方法（Q-learning）可能不穩定。

Actor-Critic 結合兩者優點：
- **Actor**：策略網路，輸出動作
- **Critic**：價值網路，評估動作

## 基本 Actor-Critic

```python
class ActorCritic:
    def __init__(self, state_dim, action_dim, hidden_dim=64, lr=0.001, gamma=0.99):
        self.gamma = gamma

        # Actor：策略網路
        self.actor = self.build_network(state_dim, action_dim)
        self.actor_optimizer = tf.keras.optimizers.Adam(lr)

        # Critic：價值網路
        self.critic = self.build_value_network(state_dim)
        self.critic_optimizer = tf.keras.optimizers.Adam(lr)

    def build_network(self, state_dim, action_dim):
        return tf.keras.Sequential([
            tf.keras.layers.Dense(64, activation='relu', input_shape=(state_dim,)),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(action_dim)
        ])

    def build_value_network(self, state_dim):
        return tf.keras.Sequential([
            tf.keras.layers.Dense(64, activation='relu', input_shape=(state_dim,)),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(1)
        ])

    def choose_action(self, state):
        probs = tf.nn.softmax(self.actor(state.reshape(1, -1)))
        return np.random.choice(len(probs[0]), p=probs.numpy()[0])

    def update(self, state, action, reward, next_state, done):
        state = state.reshape(1, -1)
        next_state = next_state.reshape(1, -1)

        with tf.GradientTape() as tape:
            # Critic 更新
            v = self.critic(state)[0, 0]
            v_next = self.critic(next_state)[0, 0]
            td_target = reward + self.gamma * v_next * (1 - done)
            td_error = td_target - v
            critic_loss = td_error ** 2

        critic_grads = tape.gradient(critic_loss, self.critic.trainable_variables)
        self.critic_optimizer.apply_gradients(zip(critic_grads, self.critic.trainable_variables))

        # Actor 更新（使用 TD 誤差作為優勢）
        with tf.GradientTape() as tape:
            logits = self.actor(state)
            log_probs = tf.nn.log_softmax(logits)
            action_log_prob = log_probs[0, action]
            actor_loss = -action_log_prob * td_error

        actor_grads = tape.gradient(actor_loss, self.actor.trainable_variables)
        self.actor_optimizer.apply_gradients(zip(actor_grads, self.actor.trainable_variables))
```

## Advantage Actor-Critic (A2C)

使用優勢函數替代簡單 TD 誤差。

```python
class A2C:
    def update(self, states, actions, rewards, next_states, dones):
        """
        A2C 更新
        """
        # 計算優勢 A(s,a) = Q(s,a) - V(s)
        # 使用 TD 誤差近似：A ≈ r + γV(s') - V(s)

        values = self.critic(states).numpy().flatten()
        next_values = self.critic(next_states).numpy().flatten()

        # TD 目標
        td_targets = rewards + self.gamma * next_values * (1 - dones)
        advantages = td_targets - values

        # Critic 更新（MSE 損失）
        with tf.GradientTape() as tape:
            value_pred = self.critic(states)
            critic_loss = tf.reduce_mean((td_targets - value_pred) ** 2)

        # Actor 更新（策略梯度）
        with tf.GradientTape() as tape:
            logits = self.actor(states)
            log_probs = tf.nn.log_softmax(logits)
            action_log_probs = tf.reduce_sum(log_probs * tf.one_hot(actions, self.action_dim), axis=1)
            actor_loss = -tf.reduce_mean(action_log_probs * advantages)

        # ... 應用梯度
```

## A3C（非同步優勢演員-評論家）

使用多個並行的 worker 加速訓練。

```python
import multiprocessing as mp

class A3CWorker(mp.Process):
    def __init__(self, global_agent, worker_id):
        super().__init__()
        self.global_agent = global_agent
        self.worker_id = worker_id

    def run(self):
        local_agent = ActorCritic(state_dim, action_dim)

        while True:
            # 收集經驗
            states, actions, rewards = self.collect_experience()

            # 異步更新全局 agent
            self.global_agent.update(states, actions, rewards)
```

## PPO（Proximal Policy Optimization）

穩定的策略梯度方法。

```python
class PPO:
    def __init__(self, policy, old_policy, clip_ratio=0.2, lr=3e-4):
        self.policy = policy
        self.old_policy = old_policy
        self.clip_ratio = clip_ratio
        self.optimizer = tf.keras.optimizers.Adam(lr)

    def compute_ppo_loss(self, states, actions, advantages, old_log_probs):
        # 新的 log 機率
        new_log_probs = self.policy.log_prob(states, actions)

        # 比率
        ratio = tf.exp(new_log_probs - old_log_probs)

        # 裁剪
        clipped = tf.clip_by_value(ratio, 1 - self.clip_ratio, 1 + self.clip_ratio)

        # PPO 目標
        surrogate = tf.minimum(ratio * advantages, clipped * advantages)

        return -tf.reduce_mean(surrogate)

    def update(self, states, actions, advantages, old_log_probs):
        with tf.GradientTape() as tape:
            loss = self.compute_ppo_loss(states, actions, advantages, old_log_probs)

        grads = tape.gradient(loss, self.policy.trainable_variables)
        self.optimizer.apply_gradients(zip(grads, self.policy.trainable_variables))
```

## GAE（Generalized Advantage Estimation）

平滑的優勢估計。

```python
def compute_gae(rewards, values, next_values, dones, gamma=0.99, lam=0.95):
    """
    GAE: 優勢估計的加權平均
    """
    advantages = []
    gae = 0

    for t in reversed(range(len(rewards))):
        delta = rewards[t] + gamma * next_values[t] * (1 - dones[t]) - values[t]
        gae = delta + gamma * lam * (1 - dones[t]) * gae
        advantages.insert(0, gae)

    return np.array(advantages)
```

## 實用技巧

### 熵正則化

```python
def entropy_loss(logits):
    """鼓勵探索"""
    probs = tf.nn.softmax(logits)
    log_probs = tf.nn.log_softmax(logits)
    entropy = -tf.reduce_sum(probs * log_probs, axis=-1)
    return entropy

# 總損失
total_loss = policy_loss - beta * entropy_loss
```

### 梯度裁剪

```python
# 防止梯度爆炸
gradients = tape.gradient(loss, model.trainable_variables)
gradients, _ = tf.clip_by_global_norm(gradients, max_norm=0.5)
optimizer.apply_gradients(zip(gradients, model.trainable_variables))
```

## 總結

Actor-Critic 架構結合了：
- **Actor**：學習策略（策略梯度）
- **Critic**：評估價值（降低方差）

A2C、A3C、PPO 是實際應用中的主流方法。