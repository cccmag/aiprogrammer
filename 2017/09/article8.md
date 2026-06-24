# 蒙地卡羅方法

## 隨機模擬

蒙地卡羅方法使用隨機抽樣解決數學問題。

## 估計 π

```python
import random

def estimate_pi(n_samples):
    inside = 0

    for _ in range(n_samples):
        x = random.random()
        y = random.random()

        if x**2 + y**2 <= 1:
            inside += 1

    return 4 * inside / n_samples

print(estimate_pi(1000000))  # ≈ 3.14159
```

## 積分估計

```python
def monte_carlo_integral(f, a, b, n_samples=100000):
    """
    估計 ∫_a^b f(x) dx
    使用均值估計：∫f ≈ (b-a) * mean(f(x_i))
    """
    total = 0
    for _ in range(n_samples):
        x = random.uniform(a, b)
        total += f(x)

    return (b - a) * total / n_samples

import math
result = monte_carlo_integral(math.sin, 0, math.pi, 100000)
print(f"∫sin(x) dx from 0 to π ≈ {result:.4f}")  # ≈ 2
```

## 蒙地卡羅樹搜索（MCTS）

用於遊戲決策的搜索算法。

```python
class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = {}
        self.visits = 0
        self.wins = 0

def uct(node, exploration=1.41):
    """UCB1 for tree search"""
    if node.visits == 0:
        return float('inf')

    avg_value = node.wins / node.visits
    return avg_value + exploration * np.sqrt(np.log(node.parent.visits) / node.visits)

def mcts(root, n_iterations=1000):
    for _ in range(n_iterations):
        node = select(root, uct)
        if not node.is_terminal():
            node = expand(node)
        reward = simulate(node)
        backpropagate(node, reward)

    return root.best_child()
```

## 重要性採樣

```python
def importance_sampling(f, p, q, n_samples=10000):
    """
    估計 E_p[f(X)] = ∫ f(x) p(x) dx
    = ∫ f(x) p(x)/q(x) q(x) dx ≈ (1/n) Σ f(x_i) p(x_i)/q(x_i)
    其中 x_i ~ q
    """
    total = 0
    for _ in range(n_samples):
        x = q.sample()
        total += f(x) * p.pdf(x) / q.pdf(x)

    return total / n_samples
```

## 蒙地卡羅积分的變異數減少

### 對偶變數

```python
def antithetic_integral(f, a, b, n_samples=50000):
    """使用對偶變數減少變異數"""
    total = 0
    half_samples = n_samples // 2

    for _ in range(half_samples):
        u = random.random()
        x1 = a + (b - a) * u
        x2 = a + (b - a) * (1 - u)  # 對偶變數

        total += f(x1) + f(x2)

    return (b - a) * total / n_samples
```

## 馬可夫鏈蒙地卡羅（MCMC）

```python
def metropolis_hastings(target_pdf, proposal_std=1, n_samples=10000):
    """Metropolis-Hastings 採樣"""
    samples = []
    x = 0  # 起始點

    for _ in range(n_samples):
        # 提議分佈（常態）
        x_proposed = random.gauss(x, proposal_std)

        # 接受概率
        alpha = target_pdf(x_proposed) / target_pdf(x)

        if random.random() < alpha:
            x = x_proposed

        samples.append(x)

    return samples
```

## 在強化學習中的應用

### 蒙地卡羅控制

```python
def mc_control(env, n_episodes, gamma=0.99, epsilon=0.1):
    """
    蒙地卡羅控制（epsilon-greedy 策略）
    """
    n_states = env.observation_space.n
    n_actions = env.action_space.n

    Q = np.zeros((n_states, n_actions))
    returns_sum = np.zeros((n_states, n_actions))
    returns_count = np.zeros((n_states, n_actions))

    for episode in range(n_episodes):
        state = env.reset()
        episode_history = []

        # 產生 episode
        done = False
        while not done:
            if random.random() < epsilon:
                action = env.action_space.sample()
            else:
                action = np.argmax(Q[state])

            next_state, reward, done, _ = env.step(action)
            episode_history.append((state, action, reward))
            state = next_state

        # 計算回報
        G = 0
        for state, action, reward in reversed(episode_history):
            G = reward + gamma * G
            returns_sum[state, action] += G
            returns_count[state, action] += 1
            Q[state, action] = returns_sum[state, action] / returns_count[state, action]

    return Q
```

## 總結

蒙地卡羅方法應用廣泛：
- 數值積分
- 機率估計
- 遊戲 AI（MCTS）
- 採樣（MCMC）
- 強化學習（MC 學習）