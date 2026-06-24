# 時間差分學習

## TD 學習概念

時間差分（Temporal Difference, TD）學習結合了蒙特卡羅和動態規劃的優點。

核心思想：**用估計更新估計**

TD 目標：r + γV(s')

TD 誤差：δ = r + γV(s') - V(s)

## TD(0)

最基本的 TD 方法，每步更新。

```python
def td_zero(env, n_episodes, alpha=0.1, gamma=0.99, epsilon=0.1):
    """
    TD(0) 學習狀態價值函數
    """
    n_states = env.observation_space.n
    V = np.zeros(n_states)

    for episode in range(n_episodes):
        state = env.reset()
        done = False

        while not done:
            # epsilon-greedy 選擇動作
            if random.random() < epsilon:
                action = env.action_space.sample()
            else:
                action = np.argmax(Q[state]) if 'Q' in dir() else 0

            next_state, reward, done, _ = env.step(action)

            # TD 更新
            V[state] += alpha * (reward + gamma * V[next_state] - V[state])

            state = next_state

    return V
```

## Sarsa（On-Policy TD 控制）

```python
class SarsaAgent:
    def __init__(self, n_states, n_actions, alpha=0.1, gamma=0.99, epsilon=0.1):
        self.Q = np.zeros((n_states, n_actions))
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

    def choose_action(self, state):
        if random.random() < self.epsilon:
            return random.randint(len(self.Q[state]))
        return np.argmax(self.Q[state])

    def update(self, state, action, reward, next_state, next_action):
        """Sarsa 更新"""
        td_target = reward + self.gamma * self.Q[next_state, next_action]
        td_error = td_target - self.Q[state, action]
        self.Q[state, action] += self.alpha * td_error

def train_sarsa(env, agent, n_episodes):
    for episode in range(n_episodes):
        state = env.reset()
        action = agent.choose_action(state)

        for t in range(1000):
            next_state, reward, done, _ = env.step(action)
            next_action = agent.choose_action(next_state)

            agent.update(state, action, reward, next_state, next_action)

            state = next_state
            action = next_action

            if done:
                break
```

## Q-Learning（Off-Policy TD 控制）

```python
class QLearningAgent:
    def __init__(self, n_states, n_actions, alpha=0.1, gamma=0.99, epsilon=0.1):
        self.Q = np.zeros((n_states, n_actions))
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

    def choose_action(self, state):
        if random.random() < self.epsilon:
            return random.randint(len(self.Q[state]))
        return np.argmax(self.Q[state])

    def update(self, state, action, reward, next_state):
        """Q-learning 更新"""
        best_next_action = np.argmax(self.Q[next_state])
        td_target = reward + self.gamma * self.Q[next_state, best_next_action]
        td_error = td_target - self.Q[state, action]
        self.Q[state, action] += self.alpha * td_error
```

## Sarsa vs Q-Learning

| | Sarsa | Q-Learning |
|---|---|---|
| 類型 | On-policy | Off-policy |
| 學習 | 從實際動作學習 | 從最佳動作學習 |
| 保守/大膽 | 保守（考慮探索） | 大膽 |

## TD(λ)

多步TD學習，使用λ加權。

```python
def td_lambda(env, n_episodes, alpha=0.1, gamma=0.99, epsilon=0.1, lam=0.8):
    """
    TD(λ) - 前視視圖
    使用 eligibility trace
    """
    n_states = env.observation_space.n
    V = np.zeros(n_states)
    E = np.zeros(n_states)  # eligibility trace

    for episode in range(n_episodes):
        state = env.reset()
        E.fill(0)

        for t in range(1000):
            action = np.argmax(V[state]) if random.random() > epsilon else random.randint(n_states)
            next_state, reward, done, _ = env.step(action)

            # TD 誤差
            td_error = reward + gamma * V[next_state] - V[state]

            # 更新 eligibility trace
            E[state] += 1

            # 更新價值函數
            V += alpha * td_error * E

            # 衰減 eligibility trace
            E *= gamma * lam

            state = next_state
            if done:
                break

    return V
```

## 資格跡（Eligibility Traces）

```python
def eligibility_trace_update(V, E, state, td_error, alpha, gamma, lam):
    """更新資格跡"""
    E[state] += 1  # 訪問標記
    V += alpha * td_error * E  # 對所有狀態更新
    E *= gamma * lam  # 衰減
```

## 比較：MC vs DP vs TD

| 方法 | 更新方式 | 樣本需求 |
|------|---------|----------|
| 蒙特卡羅 | 完整 episode | 多 |
| 動態規劃 | 模型需要 | 少 |
| TD | 單步 | 少 |

## 總結

TD 學習是強化學習的核心：
- TD(0)：單步 TD
- Sarsa：on-policy TD 控制
- Q-learning：off-policy TD 控制
- TD(λ)：結合多步 TD 的泛化