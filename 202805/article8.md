# 安全 RL

## 當 RL 遇到安全問題

強化學習的最大目標是最大化累積獎勵，但這可能導致危險行為——機器人為了快速完成任務而過度磨損關節、自動駕駛為了節省時間而違反交通規則、聊天機器人為了取悅使用者而說出有害內容。**安全 RL** 就是在最佳化獎勵的同時，確保行為滿足安全約束。

## Constrained MDP

安全 RL 的理論基礎是 Constrained MDP（CMDP），在標準 MDP 的基礎上加入了成本函數 `C(s, a)` 和約束閾值 `d`：

```
max  E[ Σ γ^t R(s_t, a_t) ]
s.t. E[ Σ γ^t C(s_t, a_t) ] ≤ d
```

## Lagrangian 方法

最直觀的做法是用 Lagrangian 對偶法將約束懲罰納入目標：

```python
class LagrangianPPO:
    def __init__(self, env):
        self.actor_critic = ActorCritic(env.observation_space.shape[0],
                                        env.action_space.n)
        self.lagrangian = nn.Parameter(torch.tensor(0.0))

    def update(self, trajectories):
        # Standard PPO loss
        pi_loss = self.compute_ppo_loss(trajectories)
        # Cost constraint
        cost = trajectories["cost"].mean()
        # Lagrangian dual
        lag_loss = (self.lagrangian * (cost - cost_limit)).mean()

        total_loss = pi_loss + lag_loss
        total_loss.backward()

        # Clip lagrangian multiplier to be non-negative
        self.lagrangian.data.clamp_(min=0)
```

## 安全盾牌（Safety Shield）

安全盾牌是一種即時干預機制，當 RL 策略選擇的動作會導致不安全狀態時，安全盾牌會 override 該動作：

```python
class SafetyShield:
    def __init__(self, safety_monitor):
        self.monitor = safety_monitor

    def safe_action(self, state, proposed_action):
        next_state = self.predict_next_state(state, proposed_action)
        if self.monitor.is_safe(next_state):
            return proposed_action
        # Fallback to safest action
        safe_actions = self.get_safe_actions(state)
        return self.select_best_safe_action(state, safe_actions)

class VelocityMonitor:
    def is_safe(self, state):
        velocity = state[1]  # assume velocity at index 1
        return velocity < 2.0  # max safe velocity
```

## CPO：受約束的策略最佳化

CPO（Constrained Policy Optimization）是 TRPO 的安全版本，在 KL 約束之外再加入成本約束：

```python
def cpo_update(policy, trajectories):
    # Compute policy gradient and constraint gradient
    pi_grad = compute_policy_grad(trajectories)
    cost_grad = compute_cost_grad(trajectories)

    # Solve dual problem
    # Project gradient onto feasible direction
    if is_feasible(trajectories):
        # Maximize reward while satisfying cost constraint
        update_dir = project_onto_KL_and_cost_constraints(
            pi_grad, cost_grad)
    else:
        # Recover feasibility first
        update_dir = -cost_grad

    policy.update(update_dir)
```

## 實務最佳實踐

安全 RL 不只是理論問題，實務上需要多層防護：

1. **模擬器驗證**：在部署前進行大量模擬測試，覆蓋邊界案例
2. **漸進式部署**：先從低風險情境開始，逐步放寬限制
3. **人類監督**：在關鍵時刻保留人類介入的能力
4. **安全包絡**：用傳統控制器（如 PID）作為最終安全網

```python
def deploy_with_safeguard(policy, env, safety_shield):
    obs, _ = env.reset()
    while True:
        action = policy.act(obs)
        action = safety_shield.safe_action(obs, action)
        obs, reward, term, trunc, _ = env.step(action)
        if term or trunc:
            break
```

## 結語

安全 RL 是 RL 從實驗室走向生產的必經之路。CMDP、Lagrangian 方法、安全盾牌和 CPO 是目前最主要的技術路線。對於自動駕駛、醫療診斷等安全關鍵領域，安全約束與獎勵最佳化同等重要。


**延伸閱讀**
- [Constrained Policy Optimization](https://www.google.com/search?q=Constrained+Policy+Optimization+Achiam+2017)
- [Benchmarking Safe Exploration in Deep RL](https://www.google.com/search?q=safe+exploration+benchmark+RL+Ray+2019)
- [A Lyapunov-based Approach to Safe Reinforcement Learning](https://www.google.com/search?q=Lyapunov+safe+RL+Chow+2018)
