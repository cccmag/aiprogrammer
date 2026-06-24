# 程式碼範例

## Q-learning 基本實現

```python
#!/usr/bin/env python3
"""Q-learning 示範"""

import numpy as np

def q_learning_demo():
    print("=" * 50)
    print("Q-learning 示範")
    print("=" * 50)

    n_states = 5
    n_actions = 2
    Q = np.zeros((n_states, n_actions))

    alpha = 0.1
    gamma = 0.9
    epsilon = 0.3

    print(f"\n初始 Q 表:")
    print(Q)

    episodes = 10
    for ep in range(episodes):
        state = np.random.randint(n_states)
        done = False

        while not done:
            if np.random.random() < epsilon:
                action = np.random.randint(n_actions)
            else:
                action = np.argmax(Q[state])

            reward = np.random.choice([0, 1], p=[0.7, 0.3])

            next_state = (state + action) % n_states

            Q[state, action] += alpha * (
                reward + gamma * np.max(Q[next_state]) - Q[state, action]
            )

            state = next_state
            if np.random.random() < 0.1:
                done = True

        if ep < 3 or ep == episodes - 1:
            print(f"\nEpisode {ep+1} 後的 Q 表:")
            print(Q)

    print("\n最終 Q 表:")
    print(Q)
```

## 簡單 MDP 求解

```python
#!/usr/bin/env python3
""" MDP 價值迭代示範 """

import numpy as np

def value_iteration_demo():
    print("=" * 50)
    print(" MDP 價值迭代示範")
    print("=" * 50)

    n_states = 3
    n_actions = 2

    P = np.zeros((n_states, n_states, n_actions))
    R = np.zeros((n_states, n_actions, n_states))

    P[0, 1, 0] = 0.9
    P[0, 0, 1] = 0.9
    R[1, 0, 1] = 1.0
    R[0, 1, 0] = 1.0

    gamma = 0.9
    V = np.zeros(n_states)
    theta = 1e-6

    print("\n初始價值:")
    print(V)

    for iteration in range(100):
        V_old = V.copy()

        for s in range(n_states):
            q_values = []
            for a in range(n_actions):
                q = sum(P[s, sp, a] * (R[s, a, sp] + gamma * V_old[sp])
                       for sp in range(n_states))
                q_values.append(q)
            V[s] = max(q_values)

        if np.max(np.abs(V - V_old)) < theta:
            print(f"\n收斂於第 {iteration + 1} 次迭代")
            break

    print(f"\n最佳價值函數:")
    print(V)

    policy = np.zeros(n_states, dtype=int)
    for s in range(n_states):
        q_values = [sum(P[s, sp, a] * (R[s, a, sp] + gamma * V[sp])
                       for sp in range(n_states))
                    for a in range(n_actions)]
        policy[s] = np.argmax(q_values)

    print(f"\n最佳策略: {policy}")
```

## 簡單 Policy Gradient

```python
#!/usr/bin/env python3
""" Policy Gradient 概念示範 """

import numpy as np

def policy_gradient_demo():
    print("=" * 50)
    print("Policy Gradient 概念示範")
    print("=" * 50)

    state_dim = 4
    action_dim = 2

    policy_params = np.random.randn(state_dim, action_dim) * 0.1

    def softmax_policy(state, params):
        logits = state @ params
        exp_logits = np.exp(logits - np.max(logits))
        return exp_logits / exp_logits.sum()

    def get_action(state, params):
        probs = softmax_policy(state, params)
        return np.random.choice(action_dim, p=probs)

    def compute_return(rewards, gamma=0.99):
        G = 0
        returns = []
        for r in reversed(rewards):
            G = r + gamma * G
            returns.insert(0, G)
        return np.array(returns)

    states = []
    actions = []
    rewards = []

    state = np.random.randn(state_dim)

    for t in range(10):
        action = get_action(state, policy_params)
        reward = np.random.randn()

        states.append(state)
        actions.append(action)
        rewards.append(reward)

        state = np.random.randn(state_dim)

    returns = compute_return(rewards)
    returns = (returns - returns.mean()) / (returns.std() + 1e-8)

    print(f"\n產生的 {len(rewards)} 步:")
    print(f"動作: {actions}")
    print(f"獎賞: {[f'{r:.2f}' for r in rewards]}")
    print(f"回報: {[f'{g:.2f}' for g in returns]}")

    print("\n策略梯度更新概念:")
    print("grad = Σ ∇log π(a|s) * G")
```

## Exploration vs Exploitation

```python
#!/usr/bin/env python3
""" Exploration vs Exploitation """

import numpy as np

def exploration_demo():
    print("=" * 50)
    print("Exploration vs Exploitation")
    print("=" * 50)

    n_arms = 10
    true_rewards = np.random.randn(n_arms)

    estimated_rewards = np.zeros(n_arms)
    counts = np.zeros(n_arms)

    print(f"\n真正的獎賞分佈:")
    for i, r in enumerate(true_rewards):
        print(f"  Arm {i}: {r:.3f}")

    epsilon = 0.1
    n_pulls = 100

    for _ in range(n_pulls):
        if np.random.random() < epsilon:
            arm = np.random.randint(n_arms)
        else:
            arm = np.argmax(estimated_rewards)

        reward = true_rewards[arm] + np.random.randn() * 0.1
        counts[arm] += 1
        estimated_rewards[arm] += (reward - estimated_rewards[arm]) / counts[arm]

    print(f"\n{ n_pulls} 次拉動後估計:")
    for i in range(n_arms):
        print(f"  Arm {i}: 估計={estimated_rewards[i]:.3f}, 拉動={int(counts[i])}")

    print(f"\n最佳估計 arm: {np.argmax(estimated_rewards)}")
    print(f"真正最佳 arm: {np.argmax(true_rewards)}")
```

## OpenAI Gym 概念

```python
#!/usr/bin/env python3
""" Gym 環境概念 """

def gym_demo():
    print("=" * 50)
    print("OpenAI Gym 概念")
    print("=" * 50)

    print("\n1. 環境初始化:")
    print("   env = gym.make('CartPole-v0')")

    print("\n2. 環境互動:")
    print("   state = env.reset()")
    print("   action = env.action_space.sample()")
    print("   next_state, reward, done, info = env.step(action)")

    print("\n3. 回合循環:")
    print("   while not done:")
    print("       action = policy(state)")
    print("       state, reward, done, _ = env.step(action)")

    print("\n4. 離散動作空間:")
    print("   Discrete(2) - 2 個動作 (0, 1)")

    print("\n5. 連續動作空間:")
    print("   Box(shape=(1,), low=-1, high=1)")

    print("\n6. 離散觀察空間:")
    print("   Box(shape=(4,), low, high)")

if __name__ == "__main__":
    print("Q-learning 示範")
    q_learning_demo()

    print("\n" + "=" * 50)
    print("價值迭代示範")
    value_iteration_demo()

    print("\n" + "=" * 50)
    print("Policy Gradient 示範")
    policy_gradient_demo()

    print("\n" + "=" * 50)
    print("Exploration 示範")
    exploration_demo()

    print("\n" + "=" * 50)
    print("Gym 概念")
    gym_demo()
```