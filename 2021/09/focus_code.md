# 程式：Q-learning 與 Policy Gradient 實作

## 基礎 RL 演算法實現

### 1. 經典 Q-learning

```python
import numpy as np
import random


class QLearningAgent:
    def __init__(self, state_space, action_space, learning_rate=0.1, gamma=0.99, epsilon=1.0, epsilon_decay=0.995, min_epsilon=0.01):
        self.Q = np.zeros((state_space, action_space))
        self.lr = learning_rate
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.min_epsilon = min_epsilon
        self.action_space = action_space

    def select_action(self, state):
        if random.random() < self.epsilon:
            return random.randint(0, self.action_space - 1)
        return np.argmax(self.Q[state])

    def update(self, state, action, reward, next_state, done):
        if done:
            target = reward
        else:
            target = reward + self.gamma * np.max(self.Q[next_state])

        self.Q[state, action] += self.lr * (target - self.Q[state, action])

    def decay_epsilon(self):
        self.epsilon = max(self.epsilon * self.epsilon_decay, self.min_epsilon)


class SimpleEnv:
    def __init__(self, num_states=5, num_actions=2):
        self.num_states = num_states
        self.num_actions = num_actions
        self.state = 0

    def reset(self):
        self.state = random.randint(0, self.num_states - 1)
        return self.state

    def step(self, action):
        if action == 1:
            self.state = min(self.state + 1, self.num_states - 1)

        reward = 1.0 if self.state == self.num_states - 1 else 0.0
        done = self.state == self.num_states - 1

        return self.state, reward, done
```

### 2. Policy Gradient (REINFORCE)

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np


class PolicyNetwork(nn.Module):
    def __init__(self, state_dim, action_dim, hidden_dim=128):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(state_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, action_dim),
            nn.Softmax(dim=-1)
        )

    def forward(self, state):
        return self.network(state)


class REINFORCEAgent:
    def __init__(self, state_dim, action_dim, lr=0.001, gamma=0.99):
        self.policy = PolicyNetwork(state_dim, action_dim, lr)
        self.optimizer = torch.optim.Adam(self.policy.parameters(), lr=lr)
        self.gamma = gamma

    def select_action(self, state):
        state = torch.FloatTensor(state).unsqueeze(0)
        probs = self.policy(state)
        dist = torch.distributions.Categorical(probs)
        action = dist.sample()
        return action.item(), dist.log_prob(action)

    def update(self, states, actions, rewards):
        G = 0
        returns = []
        for r in reversed(rewards):
            G = r + self.gamma * G
            returns.insert(0, G)

        returns = torch.FloatTensor(returns)

        states = torch.FloatTensor(np.array(states))
        actions = torch.LongTensor(actions)

        log_probs = []
        for i, state in enumerate(states):
            probs = self.policy(state.unsqueeze(0))
            dist = torch.distributions.Categorical(probs)
            log_probs.append(dist.log_prob(actions[i]))

        log_probs = torch.stack(log_probs)
        loss = -(log_probs * returns).sum()

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
```

### 3. CartPole 環境模擬

```python
import gym

def train_cartpole():
    env = gym.make('CartPole-v1')
    state_dim = env.observation_space.shape[0]
    action_dim = env.action_space.n

    agent = REINFORCEAgent(state_dim, action_dim, lr=0.002)

    num_episodes = 500
    max_steps = 500
    rewards_history = []

    for episode in range(num_episodes):
        state = env.reset()
        states, actions, rewards = [], [], []

        for step in range(max_steps):
            action, log_prob = agent.select_action(state)
            next_state, reward, done, _ = env.step(action)

            states.append(state)
            actions.append(action)
            rewards.append(reward)

            if done:
                break

            state = next_state

        agent.update(states, actions, rewards)
        rewards_history.append(sum(rewards))

        if episode % 50 == 0:
            avg_reward = np.mean(rewards_history[-50:])
            print(f"Episode {episode}: Average Reward = {avg_reward:.1f}")

        if np.mean(rewards_history[-50:]) >= 450:
            print(f"Solved at episode {episode}!")
            break

    env.close()
    return rewards_history
```

### 4. 測試函數

```python
def demo():
    print("=== Q-learning 與 Policy Gradient 示範 ===\n")

    print("--- Q-learning ---")
    env = SimpleEnv(num_states=10, num_actions=2)
    agent = QLearningAgent(10, 2, learning_rate=0.1, gamma=0.99)

    for episode in range(100):
        state = env.reset()
        total_reward = 0

        for step in range(100):
            action = agent.select_action(state)
            next_state, reward, done = env.step(action)
            agent.update(state, action, reward, next_state, done)
            total_reward += reward

            if done:
                break

            state = next_state

        agent.decay_epsilon()

        if episode % 20 == 0:
            print(f"Episode {episode}: Total Reward = {total_reward}")

    print("\n--- REINFORCE (CartPole) ---")
    print("Training REINFORCE on CartPole-v1...")
    print("(Install gym to run: pip install gym)")

    try:
        train_cartpole()
    except ImportError:
        print("gym not installed, skipping CartPole training")


if __name__ == "__main__":
    demo()