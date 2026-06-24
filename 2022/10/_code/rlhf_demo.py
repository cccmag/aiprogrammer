#!/usr/bin/env python3
"""RLHF 完整流程模擬 — 從強化學習到人類反饋"""

import math
import random

# ─── 1. 虛擬環境 ──────────────────────────────────────────────

class VirtualEnv:
    """3 狀態, 2 動作。
    狀態: 0=起始, 1=中繼, 2=終端(+1獎勵)
    動作: 0=前進, 1=重置
    """
    def __init__(self):
        self.state = 0

    def reset(self):
        self.state = 0
        return self.state

    def step(self, a):
        s = self.state
        if s == 0:
            self.state = 1 if a == 0 else 0
        elif s == 1:
            self.state = 2 if a == 0 else 0
        else:
            self.state = 0
        r = 1.0 if self.state == 2 else 0.0
        return self.state, r, self.state == 2


# ─── 2. 策略網路 ──────────────────────────────────────────────

class PolicyNetwork:
    def __init__(self, n_states, n_actions):
        self.ns, self.na = n_states, n_actions
        self.logits = [[0.0] * n_actions for _ in range(n_states)]

    def probs(self, s):
        mx = max(self.logits[s])
        es = [math.exp(l - mx) for l in self.logits[s]]
        t = sum(es)
        return [e / t for e in es]

    def act(self, s):
        p = self.probs(s)
        r = random.random()
        for i, v in enumerate(p):
            r -= v
            if r <= 0: return i
        return len(p) - 1

    def logp(self, s, a):
        return math.log(self.probs(s)[a] + 1e-10)

    def copy(self):
        n = PolicyNetwork(self.ns, self.na)
        n.logits = [row[:] for row in self.logits]
        return n


# ─── 3. 獎勵模型 ──────────────────────────────────────────────

class RewardModel:
    def __init__(self, n_states):
        self.w = [0.0] * n_states

    def score(self, s):
        return self.w[s]

    def predict(self, s1, s2):
        d = self.w[s1] - self.w[s2]
        return 1.0 / (1.0 + math.exp(-d))

    def train(self, pairs, lr=0.5, epochs=200):
        losses = []
        for _ in range(epochs):
            total = 0.0
            for sw, sl in pairs:
                d = self.w[sw] - self.w[sl]
                p = 1.0 / (1.0 + math.exp(-d))
                total += -math.log(p + 1e-10)
                g = p - 1.0
                self.w[sw] -= lr * g
                self.w[sl] -= lr * (-g)
            losses.append(total / len(pairs))
        return losses[-1]


# ─── 4. PPO ────────────────────────────────────────────────────

class PPOTrainer:
    def __init__(self, pi, env, eps=0.2, beta=0.05, lr=0.1):
        self.pi = pi
        self.env = env
        self.eps = eps
        self.beta = beta
        self.lr = lr

    def rollout(self):
        s = self.env.reset()
        traj = []
        done = False
        while not done:
            a = self.pi.act(s)
            ns, r, done = self.env.step(a)
            traj.append((s, a, r, self.pi.logp(s, a)))
            s = ns
        return traj

    def normalize(self, xs):
        mu = sum(xs) / len(xs)
        sg = math.sqrt(sum((x - mu)**2 for x in xs) / len(xs) + 1e-8)
        return [(x - mu) / sg for x in xs]

    def discounted_returns(self, rewards, gamma=0.99):
        G = 0.0
        rets = []
        for r in reversed(rewards):
            G = r + gamma * G
            rets.insert(0, G)
        return self.normalize(rets)

    def step(self, traj, rm):
        rm_scores = [rm.score(s) for s, _, _, _ in traj]
        env_rews = [r for _, _, r, _ in traj]
        mixed = [r_rm + r_ev for r_rm, r_ev in zip(rm_scores, env_rews)]
        advs = self.discounted_returns(mixed)

        old = self.pi.copy()
        for (s, a, _, old_lp), A in zip(traj, advs):
            lp = self.pi.logp(s, a)
            ratio = math.exp(lp - old_lp)
            cr = max(min(ratio, 1.0 + self.eps), 1.0 - self.eps)
            L = min(ratio * A, cr * A)
            g = (1.0 - self.pi.probs(s)[a]) * (-L)
            self.pi.logits[s][a] -= self.lr * g

        kl = 0.0
        for s in range(self.pi.ns):
            kl += sum(p * math.log(p / (q + 1e-10) + 1e-10)
                     for p, q in zip(self.pi.probs(s), old.probs(s)))
        for s in range(self.pi.ns):
            for a in range(self.pi.na):
                self.pi.logits[s][a] -= self.lr * self.beta * kl
        return kl


# ─── 5. 人類標註模擬 ──────────────────────────────────────────

def simulate_preference(s1, s2):
    """人類標註：給定兩個狀態，偏好哪個？
    S2 (+1 獎勵) > S1 (可達 S2) > S0 (最遠)
    """
    value = {0: 0, 1: 1, 2: 2}
    v1, v2 = value[s1], value[s2]
    if v1 > v2: return 0
    if v2 > v1: return 1
    return None


# ─── 6. 主流程 ────────────────────────────────────────────────

def demo():
    print("=" * 52)
    print("  RLHF 完整流程模擬")
    print("  Reinforcement Learning from Human Feedback")
    print("=" * 52)

    env = VirtualEnv()
    pi = PolicyNetwork(3, 2)
    rm = RewardModel(3)

    # ── Phase 1: 偏好資料收集 ──
    print("\n[Phase 1] 收集人類偏好資料")
    pairs = []
    for _ in range(500):
        s1 = random.randint(0, 2)
        s2 = random.randint(0, 2)
        if s1 == s2: continue
        pref = simulate_preference(s1, s2)
        if pref == 0: pairs.append((s1, s2))
        elif pref == 1: pairs.append((s2, s1))
    random.shuffle(pairs)
    print(f"  收集 {len(pairs)} 個偏好配對")

    # ── Phase 2: 獎勵模型訓練 ──
    print("\n[Phase 2] 訓練獎勵模型 (Bradley-Terry)")
    loss = rm.train(pairs, lr=0.3, epochs=200)
    print(f"  最終損失: {loss:.6f}")
    print(f"  獎勵分數: S0={rm.score(0):+.3f}  S1={rm.score(1):+.3f}  S2={rm.score(2):+.3f}")

    # ── Phase 3: PPO 策略最佳化 ──
    print("\n[Phase 3] PPO 策略最佳化")
    trainer = PPOTrainer(pi, env, eps=0.2, beta=0.05, lr=0.15)

    for ep in range(40):
        traj = trainer.rollout()
        kl = trainer.step(traj, rm)
        env_r = sum(t[2] for t in traj)
        if ep % 5 == 0:
            p0 = [round(x, 3) for x in pi.probs(0)]
            p1 = [round(x, 3) for x in pi.probs(1)]
            print(f"  Ep {ep:2d}: env_R={env_r:.1f}  KL={kl:.4f}  π0={p0}  π1={p1}")

    # ── Phase 4: 最終評估 ──
    print("\n[Phase 4] 最終評估")
    ok = 0
    total_steps = 0
    for _ in range(1000):
        s = env.reset()
        done = False
        while not done:
            a = pi.act(s)
            s, _, done = env.step(a)
            total_steps += 1
        if s == 2: ok += 1

    policies = [[round(x, 3) for x in pi.probs(s)] for s in range(3)]
    print(f"  成功率: {ok}/1000 ({100*ok//1000}%)")
    print(f"  平均步數: {total_steps/1000:.2f}")
    print(f"  最終策略: {policies}")
    print(f"  獎勵模型: S0={rm.score(0):+.3f}  S1={rm.score(1):+.3f}  S2={rm.score(2):+.3f}")

    fwd_s0 = pi.probs(0)[0]
    fwd_s1 = pi.probs(1)[0]
    print(f"\n  S0 前進機率: {fwd_s0:.1%}  S1 前進機率: {fwd_s1:.1%}")
    print("\n" + "=" * 52)
    print("  模擬完成")
    print("=" * 52)


if __name__ == "__main__":
    demo()
