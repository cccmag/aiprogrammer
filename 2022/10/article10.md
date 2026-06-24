# DPO 直接偏好最佳化

## 1. 引言

直接偏好最佳化（Direct Preference Optimization, DPO）是 2023 年由史丹佛大學提出的 RLHF 替代方案。DPO 的核心洞察：繞過顯式的獎勵模型訓練，直接從人類偏好中最佳化策略。本文將介紹 DPO 的數學原理和實務應用。

## 2. 核心思想

RLHF 的標準流程是：
```
人類偏好 → 獎勵模型 → PPO 最佳化 → 對齊策略
```

DPO 將這個流程簡化為：
```
人類偏好 → 直接最佳化 → 對齊策略
```

DPO 的洞察：在 RLHF 中，最佳策略可以從獎勵函數中推導出來。反過來，獎勵函數也可以從最佳策略中推導。DPO 利用這個對偶關係，繞過顯式獎勵模型。

## 3. 數學推導

### 步驟 1：RLHF 的最佳策略

在 KL 正則化的 RLHF 中，最佳策略 π* 滿足：

```
π*(y|x) ∝ π_ref(y|x) * exp(r(x, y) / β)
```

其中 r(x, y) 是獎勵函數，β 是 KL 係數。

### 步驟 2：獎勵函數表示

從上式可以反解獎勵函數：

```
r(x, y) = β * log(π*(y|x) / π_ref(y|x)) + β * Z(x)
```

其中 Z(x) 是歸一化常數。

### 步驟 3：偏好機率

將獎勵函數代入 Bradley-Terry 模型：

```
P(y_1 > y_2) = σ( β * log(π*(y_1|x)/π_ref(y_1|x)) - β * log(π*(y_2|x)/π_ref(y_2|x)) )
```

這就是 DPO 的關鍵公式！

### 步驟 4：DPO 損失函數

```
L_DPO(θ) = -E[ log σ( β * log(π_θ(y_w|x)/π_ref(y_w|x)) - β * log(π_θ(y_l|x)/π_ref(y_l|x)) ) ]
```

## 4. DPO 的實作

```python
def dpo_loss(policy_logps, ref_logps, chosen, rejected, beta):
    # 偏好和拒絕回應的 log 機率
    policy_chosen_logps = policy_logps[chosen]
    policy_rejected_logps = policy_logps[rejected]
    ref_chosen_logps = ref_logps[chosen]
    ref_rejected_logps = ref_logps[rejected]

    # 計算 log 機率比
    chosen_ratio = policy_chosen_logps - ref_chosen_logps
    rejected_ratio = policy_rejected_logps - ref_rejected_logps

    # DPO 損失
    logits = beta * (chosen_ratio - rejected_ratio)
    loss = -log(sigmoid(logits)).mean()
    return loss
```

## 5. DPO vs RLHF 比較

| 特性 | RLHF | DPO |
|------|------|-----|
| 獎勵模型 | 需要訓練 | 不需要 |
| 訓練階段 | 3 階段 | 1 階段 |
| PPO | 需要 | 不需要 |
| 穩定性 | 敏感 | 穩定 |
| 記憶體 | 4 個模型 | 2 個模型 |
| 偏好資料 | 需要 | 需要 |

## 6. DPO 的優勢

1. **簡潔**：不需要訓練獎勵模型，不需要 PPO
2. **穩定**：沒有 PPO 的超參數調節問題
3. **高效**：只需要策略模型和參考模型
4. **有效**：在許多任務上與 RLHF 效果相當或更好

## 7. DPO 的局限性

1. **隱式獎勵限制**：不能直接控制獎勵函數的形式
2. **分佈外問題**：對訓練分佈外的提示效果不確定
3. **未解決的對齊問題**：只是簡化 RLHF，不是對齊問題的最終解決方案

## 8. DPO 的變體

- **IPO（Identity Preference Optimization）**：修改 DPO 損失，提高穩定性
- **KTO**：使用單一標籤而非配對
- **ORPO**：在 SFT 階段直接加入偏好損失
- **SimPO**：使用簡單的機率比代替複雜的公式

## 9. 結語

DPO 代表了 RLHF 的重要簡化方向。它證明了顯式的獎勵模型可能不是必要的——人類偏好可以直接驅動策略最佳化。DPO 的簡潔性和有效性使其成為 RLHF 的重要替代方案，特別適合預算有限的團隊。

## 延伸閱讀

- [DPO 原始論文](https://www.google.com/search?q=direct+preference+optimization+your+language+model)
- [DPO 實作教學](https://www.google.com/search?q=DPO+implementation+tutorial+TRL)
