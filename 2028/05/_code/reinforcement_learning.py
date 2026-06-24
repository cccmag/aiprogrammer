"""
從零實作強化學習 — Q-Learning, Policy Gradient, RLHF 模擬
"""

import math
import random
from dataclasses import dataclass, field
from typing import Optional


# --- 1. 環境: 簡單迷宮 ---

class GridWorld:
    """Simple 4x4 grid world with goal"""

    def __init__(self, size: int = 4):
        self.size = size
        self.goal = (size - 1, size - 1)
        self.obstacles = {(1, 1), (2, 2)}
        self.reset()

    def reset(self):
        self.agent = (0, 0)
        return self.agent

    def step(self, action: int) -> tuple[tuple, float, bool]:
        """action: 0=up, 1=down, 2=left, 3=right"""
        x, y = self.agent
        moves = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        nx, ny = moves[action]

        # Check bounds
        if 0 <= nx < self.size and 0 <= ny < self.size:
            if (nx, ny) not in self.obstacles:
                self.agent = (nx, ny)

        # Check goal
        done = self.agent == self.goal
        reward = 1.0 if done else -0.01
        return self.agent, reward, done


# --- 2. Q-Learning ---

class QLearning:
    """Tabular Q-Learning"""

    def __init__(self, state_size: int, action_size: int, lr: float = 0.1, gamma: float = 0.9):
        self.lr = lr
        self.gamma = gamma
        self.q_table: dict[tuple, list[float]] = {}

    def _get_q(self, state: tuple) -> list[float]:
        if state not in self.q_table:
            self.q_table[state] = [0.0] * 4
        return self.q_table[state]

    def choose_action(self, state: tuple, epsilon: float) -> int:
        if random.random() < epsilon:
            return random.randint(0, 3)
        q = self._get_q(state)
        return q.index(max(q))

    def update(self, state: tuple, action: int, reward: float,
               next_state: tuple):
        q = self._get_q(state)
        next_q = self._get_q(next_state)
        td_target = reward + self.gamma * max(next_q)
        q[action] += self.lr * (td_target - q[action])


# --- 3. Policy Gradient (REINFORCE) ---

class PolicyGradient:
    """Simple policy gradient with softmax policy"""

    def __init__(self, n_states: int = 16, n_actions: int = 4, lr: float = 0.01):
        self.n_states = n_states
        self.n_actions = n_actions
        self.lr = lr
        self.weights = [[random.gauss(0, 0.1) for _ in range(n_actions)]
                        for _ in range(n_states)]

    def _softmax(self, state_idx: int) -> list[float]:
        vals = self.weights[state_idx]
        exp = [math.exp(v) for v in vals]
        total = sum(exp)
        return [e / total for e in exp]

    def choose_action(self, state: tuple) -> int:
        state_idx = state[0] * 4 + state[1]
        probs = self._softmax(state_idx)
        return random.choices(range(self.n_actions), weights=probs)[0]

    def update(self, episode: list[tuple]):
        # REINFORCE: for each step, update weights
        for t, (state, action, reward) in enumerate(episode):
            state_idx = state[0] * 4 + state[1]
            probs = self._softmax(state_idx)
            gradient = probs[:]
            gradient[action] -= 1
            for a in range(self.n_actions):
                self.weights[state_idx][a] -= self.lr * gradient[a] * reward


# --- 4. RLHF 模擬 ---

class RLHFSimulator:
    """Simulate RLHF preference learning"""

    def __init__(self):
        self.preference_model: dict[str, float] = {}
        self.policy: dict[str, list[str]] = {}

    def collect_preference(self, prompt: str, response_a: str, response_b: str,
                           preferred: str) -> None:
        """Record human preference"""
        if prompt not in self.preference_model:
            self.preference_model[prompt] = 0.5
        reward_a = 1.0 if preferred == "a" else -1.0
        self.preference_model[prompt] += 0.1 * reward_a

    def get_reward(self, prompt: str, response: str) -> float:
        base = self.preference_model.get(prompt, 0.5)
        noise = random.gauss(0, 0.1)
        return max(-1.0, min(1.0, base + noise))


# --- Demo ---

def run_qlearning(episodes: int = 200) -> float:
    env = GridWorld()
    agent = QLearning(state_size=16, action_size=4)
    total_rewards = []

    for ep in range(episodes):
        state = env.reset()
        epsilon = max(0.05, 1.0 - ep / 100)
        total_reward = 0
        done = False
        steps = 0

        while not done and steps < 100:
            action = agent.choose_action(state, epsilon)
            next_state, reward, done = env.step(action)
            agent.update(state, action, reward, next_state)
            state = next_state
            total_reward += reward
            steps += 1
        total_rewards.append(total_reward)

    return sum(total_rewards[-20:]) / 20  # avg of last 20


def demo():
    print("=== Reinforcement Learning from Scratch ===\n")

    # 1. Q-Learning
    print("1. Q-Learning on GridWorld:")
    avg_reward = run_qlearning(200)
    print(f"  Avg reward (last 20 eps): {avg_reward:.3f}")
    print(f"  Goal reached: {avg_reward > 0.5}")

    # 2. Policy Gradient
    print("\n2. Policy Gradient (REINFORCE):")
    env = GridWorld()
    pg = PolicyGradient()
    for ep in range(50):
        state = env.reset()
        episode = []
        done = False
        steps = 0
        while not done and steps < 100:
            action = pg.choose_action(state)
            next_state, reward, done = env.step(action)
            episode.append((state, action, reward))
            state = next_state
            steps += 1
        pg.update(episode)
    print(f"  Trained for 50 episodes")

    # 3. RLHF Simulation
    print("\n3. RLHF Preference Learning:")
    rlhf = RLHFSimulator()
    prompts = ["Write a poem", "Explain quantum computing", "Tell a joke"]
    for prompt in prompts:
        rlhf.collect_preference(prompt, "short version", "long version",
                                random.choice(["a", "b"]))
        reward = rlhf.get_reward(prompt, "short version")
        print(f"  Prompt: '{prompt}' -> reward: {reward:.3f}")

    print("\n=== Demo Complete ===")


if __name__ == "__main__":
    demo()
