# 決策 Transformer

## 將決策視為序列建模

傳統 RL 用價值函數或策略梯度解決決策問題。Decision Transformer（DT）在 2021 年由 Chen 等人提出，將 RL 重新定義為 **序列建模問題**——給定過去回傳、狀態與動作序列，預測下一個動作。

## 核心架構

DT 使用 GPT 風格的 Transformer，輸入格式為三元組序列 `(R_t, s_t, a_t)`：

```python
import torch
import torch.nn as nn
import math

class DecisionTransformer(nn.Module):
    def __init__(self, state_dim, act_dim, max_ep_len=1000,
                 n_blocks=6, embed_dim=128, n_heads=4):
        super().__init__()
        self.embed_dim = embed_dim

        self.state_encoder = nn.Linear(state_dim, embed_dim)
        self.action_encoder = nn.Linear(act_dim, embed_dim)
        self.return_encoder = nn.Linear(1, embed_dim)
        self.pos_encoder = nn.Embedding(max_ep_len * 3, embed_dim)

        self.transformer = nn.TransformerEncoder(
            nn.TransformerEncoderLayer(
                d_model=embed_dim, nhead=n_heads,
                dim_feedforward=4*embed_dim, dropout=0.1),
            num_layers=n_blocks)

        self.action_pred = nn.Linear(embed_dim, act_dim)

    def forward(self, states, actions, returns_to_go, timesteps):
        batch_size, seq_len = states.shape[:2]

        # Embed each modality
        state_emb = self.state_encoder(states)
        action_emb = self.action_encoder(actions)
        return_emb = self.return_encoder(returns_to_go.unsqueeze(-1))

        # Interleave: R, s, a, R, s, a, ...
        stacked = []
        for i in range(seq_len):
            stacked.extend([
                return_emb[:, i:i+1] + self.pos_encoder(timesteps[:, i]*3),
                state_emb[:, i:i+1] + self.pos_encoder(timesteps[:, i]*3+1),
                action_emb[:, i:i+1] + self.pos_encoder(timesteps[:, i]*3+2)])

        x = torch.cat(stacked, dim=1)
        x = self.transformer(x)

        # Extract action predictions (at state positions)
        action_logits = self.action_pred(
            x[:, 1::3])  # positions of state embeddings
        return action_logits
```

## 訓練方式

不同於傳統 RL 的 TD 誤差，DT 用簡單的動作預測損失來訓練：

```python
def train_step(model, batch, optimizer):
    states, actions, rewards, dones = batch
    batch_size, seq_len = states.shape[:2]

    # Compute returns-to-go
    returns_to_go = torch.zeros(batch_size, seq_len)
    for i in range(seq_len - 1, -1, -1):
        returns_to_go[:, i] = rewards[:, i] + (
            returns_to_go[:, i+1] if i < seq_len - 1 else 0)

    timesteps = torch.arange(seq_len).unsqueeze(0).expand(batch_size, -1)
    # Causal mask: each position only sees past
    action_preds = model(states, actions, returns_to_go, timesteps)

    loss = nn.MSELoss()(action_preds[:, :-1], actions[:, 1:])
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    return loss.item()
```

## DT v.s. 傳統 RL

DT 的優勢在於簡單——不需要 Bellman 更新、不需要優勢估計、不需要目標網路。但代價是樣本效率較低，且難以處理連續動作空間中的高精度控制。

## 結語

Decision Transformer 打開了「用序列模型做決策」的新思路。後續的 Trajectory Transformer、Online DT、以及將 Transformer 應用於 RL 的各項研究，都證明了序列建模視角的強大潛力。


**延伸閱讀**
- [Decision Transformer: Reinforcement Learning via Sequence Modeling](https://www.google.com/search?q=Decision+Transformer+Chen+2021)
- [Offline Reinforcement Learning as One Big Sequence Modeling Problem](https://www.google.com/search?q=Trajectory+Transformer+Janner+2021)
- [Online Decision Transformer](https://www.google.com/search?q=Online+Decision+Transformer+Zheng+2022)
