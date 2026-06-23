# RL 在推薦系統

## 推薦系統的困境

傳統推薦系統（協同過濾、內容推薦、深度學習 CTR 預估）都屬於監督式學習——預測使用者點擊率，選擇分數最高的物品。但這種模式存在根本問題：

- **即時回饋 vs 長期價值**：點擊不代表滿意，短期點擊率最佳化可能損害長期留存
- **探索 vs 利用**：只推薦已知高分物品會導致資訊繭房
- **動態變化**：使用者偏好會隨時間改變，監督模型難以適應

RL 的序列決策框架天然適合解決這些問題。

## 將推薦建模為 MDP

在推薦 RL 中，每個元素對應到 MDP 的組件：

| MDP 組件 | 推薦系統對應 |
|---------|------------|
| 狀態 s | 使用者歷史行為序列、使用者畫像、上下文 |
| 動作 a | 推薦的物品列表（slate） |
| 獎勵 r | 點擊、停留時間、購買、轉換 |
| 轉移 P | 使用者狀態因推薦而改變的動態 |

## 深度 Q 網路推薦

用 DQN 解決推薦的探索-利用困境：

```python
import torch
import torch.nn as nn
import numpy as np

class RecDQN(nn.Module):
    def __init__(self, n_users, n_items, embed_dim=64):
        super().__init__()
        self.user_emb = nn.Embedding(n_users, embed_dim)
        self.item_emb = nn.Embedding(n_items, embed_dim)
        self.net = nn.Sequential(
            nn.Linear(embed_dim * 2, 128), nn.ReLU(),
            nn.Linear(128, 64), nn.ReLU(),
            nn.Linear(64, 1))

    def forward(self, user_id, item_ids):
        user_vec = self.user_emb(user_id)
        item_vec = self.item_emb(item_ids)
        features = torch.cat([user_vec.expand_as(item_vec), item_vec], dim=-1)
        return self.net(features).squeeze(-1)

    def recommend(self, user_id, candidate_items, epsilon=0.1):
        if np.random.random() < epsilon:
            return np.random.choice(candidate_items)
        with torch.no_grad():
            q_values = self.forward(
                torch.tensor([user_id]),
                torch.tensor(candidate_items))
        return candidate_items[q_values.argmax().item()]
```

## 獎勵塑造（Reward Shaping）

推薦系統的獎勵往往稀疏——使用者可能瀏覽 50 個物品才點擊一次。獎勵塑造可以緩解這個問題：

```python
def shaped_reward(click, dwell_time, session_depth):
    # 即時獎勵
    immediate = 1.0 if click else 0.0
    # 停留時間獎勵
    dwell_reward = min(dwell_time / 60.0, 2.0) if click else 0.0
    # 多樣性獎勵（鼓勵探索新類別）
    diversity_bonus = 0.1 if explored_new_category else -0.05
    # 長度懲罰（避免無限瀏覽）
    length_penalty = -0.01 * session_depth

    return immediate + dwell_reward + diversity_bonus + length_penalty
```

## Top-K 推薦與 SlateQ

一次推薦多個物品時，動作空間是指數級的。SlateQ 將 slate 推薦分解為每個物品的 Q 值計算，再考慮 slate 內物品間的互相影響：

```python
def slate_q_value(item_q_values, item_similarities, slate_size=5):
    """Compute slate-level Q value with diversity penalty"""
    base = item_q_values.sum()
    # Penalize similarity within slate
    diversity_penalty = 0
    for i in range(slate_size):
        for j in range(i+1, slate_size):
            diversity_penalty += item_similarities[i][j]
    return base - 0.1 * diversity_penalty
```

## 結語

RL 為推薦系統帶來了長期價值最佳化、動態探索、即時適應等能力。YouTube、Netflix、TikTok 等平台已在生產環境中部署了 RL 推薦系統。聯合訓練（Offline RL + Online RL）是目前的主流架構。


**延伸閱讀**
- [Deep Reinforcement Learning for Page-wise Recommendations](https://www.google.com/search?q=DRL+for+page-wise+recommendations+Zhao+2018)
- [Top-K Off-Policy Correction for a REINFORCE Recommender System](https://www.google.com/search?q=Top+K+off+policy+correction+REINFORCE+recommender+Chen+2019)
- [SlateQ: A Tractable Decomposition for RL with Recommendation Sets](https://www.google.com/search?q=SlateQ+recommendation+RL+Je+2019)
