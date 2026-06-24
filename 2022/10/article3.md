# 策略梯度推導

## 1. 引言

策略梯度方法是強化學習的核心技術之一。與基於值函數的方法不同，策略梯度直接對策略函數進行參數化，並透過梯度上升最大化期望獎勵。本文將逐步推導策略梯度定理，從 REINFORCE 到 Actor-Critic。

## 2. 問題設定

我們有一個參數化的隨機策略 π_θ(a|s)，其中 θ 是策略網路的參數。我們的目標是最大化期望獎勵 J(θ)：

```
J(θ) = E[ Σ r_t | π_θ ]
```

策略梯度定理給出了 ∇J(θ) 的封閉形式。

## 3. 策略梯度定理推導

### 步驟 1：期望獎勵的梯度

假設軌跡 τ = (s_0, a_0, r_0, s_1, a_1, r_1, ...)，軌跡的機率為：

```
P(τ; θ) = P(s_0) ∏ π_θ(a_t|s_t) P(s_{t+1}|s_t, a_t)
```

期望獎勵 J(θ) = ∫ P(τ; θ) R(τ) dτ

對 θ 求梯度：

```
∇J(θ) = ∫ ∇P(τ; θ) R(τ) dτ
       = ∫ P(τ; θ) ∇log P(τ; θ) R(τ) dτ
       = E[ ∇log P(τ; θ) R(τ) ]
```

這裡使用了 log 梯度技巧：∇P = P * ∇log P。

### 步驟 2：展開軌跡機率的對數梯度

```
∇log P(τ; θ) = ∇log [ P(s_0) ∏ π_θ(a_t|s_t) P(s_{t+1}|s_t, a_t) ]
             = Σ ∇log π_θ(a_t|s_t)
```

環境轉移機率 P(s_{t+1}|s_t, a_t) 與 θ 無關，在梯度中消失。

### 步驟 3：REINFORCE 演算法

得到 REINFORCE 的梯度估計：

```
∇J(θ) ≈ Σ ∇log π_θ(a_t|s_t) G_t
```

其中 G_t = Σ γ^{k-t} r_k 是從 t 時刻開始的累積折扣獎勵。

```python
def reinforce(policy, env, episodes):
    for _ in range(episodes):
        trajectory = rollout(policy, env)
        for t in range(len(trajectory)):
            s, a, r = trajectory[t]
            G = sum(discount * trajectory[k][2]
                    for k in range(t, len(trajectory)))
            gradient = log_prob(policy(s), a) * G
            policy.update(gradient)
```

### 步驟 4：引入基準線

REINFORCE 的方差很大。引入基準線 b(s) 降低方差：

```
∇J(θ) ≈ Σ ∇log π_θ(a_t|s_t) (G_t - b(s_t))
```

基準線不改變梯度的期望值（因為 E[∇log π * b] = 0），但能顯著降低方差。最常見的基準線是狀態值函數 V(s)。

### 步驟 5：從 REINFORCE 到 Actor-Critic

用 Q 值取代 G_t，用 V(s) 作為基準線，得到優勢函數：

```
A(s, a) = Q(s, a) - V(s)
```

Actor-Critic 同時訓練兩個網路：
- **Actor**（策略網路 π_θ）：更新策略
- **Critic**（值函數網路 V_φ）：估計優勢函數

```
∇J(θ) ≈ Σ ∇log π_θ(a_t|s_t) A_φ(s_t, a_t)
```

## 4. 策略梯度的直觀理解

策略梯度公式 ∇log π_θ(a|s) * A(s, a) 的直觀解釋：

- ∇log π_θ(a|s) 是「增加 log 機率的方向」
- A(s, a) 是「該動作的優勢」
- 合起來：**好的動作（A > 0）增加機率，壞的動作（A < 0）降低機率**

## 5. 結語

策略梯度定理是現代強化學習的基石之一。從 REINFORCE 到 PPO，所有基於策略的方法都建立在這個基礎上。理解這個推導過程，有助於理解 PPO 的截斷目標和 RLHF 的設計原理。

## 延伸閱讀

- [Policy Gradient Theorem 原始論文](https://www.google.com/search?q=policy+gradient+theorem+sutton)
- [REINFORCE 演算法詳解](https://www.google.com/search?q=REINFORCE+algorithm+explained)
