# PPO 截斷目標

## 1. 引言

PPO（Proximal Policy Optimization）是目前最流行的策略梯度演算法之一。它的核心創新在於使用截斷（clipping）機制來限制每次策略更新的大小，從而實現穩定且高效的訓練。本文將深入分析 PPO 的截斷目標函數。

## 2. 問題背景

標準的策略梯度方法有兩個主要問題：

1. **樣本效率低**：每次更新後，舊樣本就無法使用
2. **訓練不穩定**：步長過大會導致策略崩潰

TRPO（Trust Region Policy Optimization）透過 KL 散度約束解決了第二個問題，但計算複雜。PPO 用簡單的截斷達到了類似效果。

## 3. 重要性採樣關鍵

PPO 的核心是重要性採樣（Importance Sampling），允許使用舊策略 π_old 的樣本估計新策略 π_θ 的梯度：

```
J(θ) = E_{a~π_old}[ (π_θ(a|s) / π_old(a|s)) * A^{π_old}(s, a) ]
```

定義重要性採樣比 r_t(θ)：

```
r_t(θ) = π_θ(a_t|s_t) / π_old(a_t|s_t)
```

當 r_t(θ) > 1 時，新策略更傾向於該動作；當 r_t(θ) < 1 時則相反。

## 4. 截斷目標

PPO 的截斷目標函數：

```
L^CLIP(θ) = E[ min( r_t(θ) * A_t, clip(r_t(θ), 1-ε, 1+ε) * A_t ) ]
```

### 分情況分析

**情況 1：A_t > 0（好動作）**
- 未截斷的目標：r_t(θ) * A_t（希望增加 r_t）
- 截斷後的目標：min(r_t, 1+ε) * A_t（限制增加幅度）
- 當 r_t > 1+ε，梯度為 0，停止增加

**情況 2：A_t < 0（壞動作）**
- 未截斷的目標：r_t(θ) * A_t（希望降低 r_t）
- 截斷後的目標：max(r_t, 1-ε) * A_t（限制降低幅度）
- 當 r_t < 1-ε，梯度為 0，停止降低

```
PPO 目標示意圖：
                    L_CLIP
                     ↑
  壞動作(A<0)        |        好動作(A>0)
  ─────────          |         ─────────
                     |
  不更新             |        不更新
  (r < 1-ε)         |        (r > 1+ε)
                     |
  ──── 更新 ────     |     ──── 更新 ────
                     |
              r=1 (舊策略)
```

## 5. 完整損失函數

PPO 的完整損失函數包含三個部分：

```python
def ppo_loss(old_log_probs, log_probs, advantages, values, returns):
    # 策略損失
    ratio = exp(log_probs - old_log_probs)
    surr1 = ratio * advantages
    surr2 = clamp(ratio, 1-eps, 1+eps) * advantages
    policy_loss = -min(surr1, surr2)

    # 值函數損失
    value_loss = MSE(values, returns)

    # 熵獎勵（鼓勵探索）
    entropy_loss = -entropy(log_probs)

    return policy_loss + vf_coef * value_loss - entropy_coef * entropy_loss
```

## 6. ε 的調節

ε 控制截斷範圍，典型值為 0.2：

- ε 過小（如 0.05）：更新過慢，訓練效率低
- ε 過大（如 0.5）：更新過快，可能不穩定
- ε = 0.2 在多數場景中表現良好

## 7. 為什麼 PPO 有效？

PPO 的截斷機制創造了一個「安全區間」：
- 策略可以在區間內自由最佳化
- 一旦超出區間，梯度被截斷，防止進一步偏離
- 這種軟約束比 TRPO 的硬約束更簡單、更高效

## 8. 在 RLHF 中的應用

RLHF 的 PPO 階段完全基於截斷目標。此外，還加入了 KL 懲罰項：

```
L_RLHF = L_CLIP - β * KL(π_θ, π_SFT)
```

這雙重保護（截斷 + KL）確保語言模型在最佳化獎勵的同時，不會喪失語言能力。

## 9. 結語

PPO 的截斷目標是「簡單而優雅」的設計。它不需要計算 KL 散度或 Hessian 矩陣，卻能達到與 TRPO 相當的穩定性。這種設計哲學——用簡單機制解決複雜問題——值得每個工程師學習。

## 延伸閱讀

- [PPO 原始論文](https://www.google.com/search?q=PPO+schulman+proximal+policy+optimization)
- [PPO 實作教學](https://www.google.com/search?q=PPO+implementation+guide+python)
