#!/usr/bin/env python3
"""強化學習基礎演算法示範"""

import numpy as np
import random
import torch
import torch.nn as nn
import torch.nn.functional as F


class QLearningAgent:
    def __init__(self, state_space, action_space, lr=0.1, gamma=0.99, epsilon=1.0, decay=0.995, min_eps=0.01):
        self.Q = np.zeros((state_space, action_space))
        self.lr = lr
        self.gamma = gamma
        self.epsilon = epsilon
        self.decay = decay
        self.min_epsilon = min_eps
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
        self.epsilon = max(self.epsilon * self.decay, self.min_epsilon)


class SimpleGridEnv:
    def __init__(self, size=5):
        self.size = size
        self.state = 0

    def reset(self):
        self.state = random.randint(0, self.size - 1)
        return self.state

    def step(self, action):
        if action == 1:
            self.state = min(self.state + 1, self.size - 1)
        reward = 1.0 if self.state == self.size - 1 else 0.0
        done = self.state == self.size - 1
        return self.state, reward, done


class PolicyNet(nn.Module):
    def __init__(self, state_dim, action_dim, hidden=64):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(state_dim, hidden),
            nn.ReLU(),
            nn.Linear(hidden, hidden),
            nn.ReLU(),
            nn.Linear(hidden, action_dim),
            nn.Softmax(dim=-1)
        )

    def forward(self, state):
        return self.net(state)


def demo():
    print("=== Q-learning 與 Policy Gradient 示範 ===\n")

    print("--- Q-learning on Grid World ---")
    env = SimpleGridEnv(size=10)
    agent = QLearningAgent(10, 2, lr=0.1, gamma=0.99)

    for ep in range(200):
        state = env.reset()
        total = 0
        for _ in range(100):
            action = agent.select_action(state)
            next_state, reward, done = env.step(action)
            agent.update(state, action, reward, next_state, done)
            total += reward
            if done:
                break
            state = next_state
        agent.decay_epsilon()
        if ep % 50 == 0:
            print(f"Episode {ep}: Reward={total:.0f}, Epsilon={agent.epsilon:.3f}")

    print("\n--- Policy Gradient (PyTorch) ---")
    policy = PolicyNet(state_dim=4, action_dim=2)
    optimizer = torch.optim.Adam(policy.parameters(), lr=0.01)

    states = [[0.1, 0.2, 0.3, 0.4] for _ in range(10)]
    actions = [random.randint(0, 1) for _ in range(10)]
    returns = [random.random() * 10 for _ in range(10)]

    states_t = torch.FloatTensor(states)
    actions_t = torch.LongTensor(actions)
    returns_t = torch.FloatTensor(returns)

    probs = policy(states_t)
    dists = torch.distributions.Categorical(probs)
    log_probs = dists.log_prob(actions_t)
    loss = -(log_probs * returns_t).sum()

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    print(f"Policy Gradient update completed. Loss={loss.item():.4f}")


if __name__ == "__main__":
    demo()