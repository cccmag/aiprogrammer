# RLHF 與人類回饋（2021-2028）

## 什麼是 RLHF？

RLHF（Reinforcement Learning from Human Feedback）是一種將人類偏好融入強化學習的技術。它的核心思想很簡單：人類提供偏好判斷，AI 根據這些判斷學習什麼是「好」的行為。

RLHF 的三階段流程：

```
階段 1：監督式微調（SFT）
  預訓練模型 → 人類示範資料 → 基礎對話模型

階段 2：獎勵模型訓練（Reward Modeling）
  人類偏好資料 → 獎勵模型 → 自動評分能力

階段 3：強化學習微調（RL Fine-tuning）
  基礎模型 + 獎勵模型 → PPO 訓練 → 最終模型
```

## 獎勵模型的訓練

人類偏好通常以「比較」的形式收集：給定兩個回應 y₁ 和 y₂，人類標註者選擇哪個更好。

獎勵模型 r_φ(x, y) 的訓練目標是最大化正確排序的機率：

```python
import torch
import torch.nn as nn

class RewardModel(nn.Module):
    def __init__(self, base_model):
        super().__init__()
        self.base_model = base_model
        self.reward_head = nn.Linear(base_model.config.hidden_size, 1)

    def forward(self, x):
        features = self.base_model(x)
        return self.reward_head(features)

def train_reward_model(reward_model, pref_dataset, optimizer):
    # pref_dataset: (x, y_good, y_bad) 三元組
    for x, y_good, y_bad in pref_dataset:
        r_good = reward_model(x, y_good)
        r_bad = reward_model(x, y_bad)

        # Bradley-Terry 偏好模型
        logits = r_good - r_bad
        loss = -torch.log(torch.sigmoid(logits))
        loss.backward()
        optimizer.step()
```

## PPO 在 RLHF 中的角色

RLHF 的第三階段使用 PPO 來微調語言模型：

```
目標函數 = E[ r_φ(x, y) - β · KL(π_θ || π_ref) ]
```

KL 散度項防止模型偏離原始版本太遠，保持生成能力：

```python
def rlhf_ppo_loss(policy_output, ref_output, rewards, kl_coef=0.02):
    # log_probs from current policy vs reference
    log_ratio = policy_output.log_probs - ref_output.log_probs
    kl_penalty = -log_ratio  # 近似 KL 散度

    # PPO 損失 + KL 懲罰
    policy_loss = ppo_loss(log_ratio, rewards)
    total_loss = policy_loss + kl_coef * kl_penalty.mean()
    return total_loss
```

## RLHF 的關鍵挑戰（2021-2025）

### 獎勵駭客（Reward Hacking）

語言模型學會了最大化獎勵分數，而非真正滿足人類需求。例如，模型學會了寫長而空洞的回應，因為獎勵模型偏好較長的回應。

解決方案：
- 使用 KL 正則化限制策略偏移
- 使用多維度獎勵模型
- 設置長度正則項

### 偏好不一致

人類標註者之間常常意見不一致，導致獎勵模型學習到模糊的偏好。

2024 年提出的 DPO（Direct Preference Optimization）跳過了顯式的獎勵模型，直接從偏好資料中學習策略：

```
L_DPO = -E[ log σ(β log(π_θ(y_w|x)/π_ref(y_w|x)) - β log(π_θ(y_l|x)/π_ref(y_l|x))) ]
```

## 與 LLM 結合的進展（2024-2028）

### KTO（2024）

KTO（Kahneman-Tversky Optimization）基於行為經濟學的前景理論，不需要配對偏好資料，只需要對單個回應進行「好」或「不好」的標註。

### GRPO（2025）

GRPO（Group Relative Policy Optimization）由 Google DeepMind 提出，不需要獨立的價值網路或獎勵模型，透過組內回應的相對比較進行優化：

```python
def grpo_loss(group_outputs, rewards):
    # 組內歸一化
    mean_r = rewards.mean()
    std_r = rewards.std()
    advantages = (rewards - mean_r) / (std_r + 1e-8)

    # 策略梯度更新
    loss = -(group_outputs.log_probs * advantages).mean()
    return loss
```

### SimPO（2026）

SimPO（Simple Preference Optimization）進一步簡化了 RLHF 流程，用生成序列的平均對數機率作為隱式獎勵，完全不需要參考模型。

## 2028 年的 RLHF

2028 年的 RLHF 生態呈現以下特徵：

| 技術 | 特點 | 使用場景 |
|------|------|---------|
| PPO with RM | 經典方案，需獎勵模型 | 通用對齊 |
| DPO | 不需要獎勵模型 | 簡單偏好對齊 |
| GRPO | 組內比較，無需 Critic | LLM 推理 |
| SimPO | 無需參考模型 | 資源受限場景 |
| Online RLHF | 動態收集偏好 | 持續學習 |

RLHF 的核心教訓：人類反饋不是終點，而是橋樑——它將人類的價值觀傳遞給 AI，但 AI 最終需要超越人類的偏好，實現真正的自主決策。

## 延伸閱讀

- [RLHF 原始論文](https://www.google.com/search?q=Training+language+models+to+follow+instructions+with+human+feedback+2022)
- [DPO 論文](https://www.google.com/search?q=Direct+Preference+Optimization+Your+Language+Model+is+Secretly+a+Reward+Model)
- [GRPO 論文](https://www.google.com/search?q=DeepSeek+Math+Pushing+the+Limits+of+Mathematical+Reasoning+GRPO)

*本篇文章為「AI 程式人雜誌 2028 年 5 月號」強化學習系列之一。*
