# 多智能體強化學習（2016-2028）

## 從單智能體到多智能體

在現實世界中，多個決策者同時互動是常態：自動駕駛車輛在交通中行駛，機器人在倉庫中協作，AI 在遊戲中對戰。這些場景需要多智能體強化學習（Multi-Agent Reinforcement Learning, MARL）。

MARL 的核心挑戰：每個智能體的環境不僅包含靜態世界，還包含其他學習中的智能體，導致環境非平穩（Non-stationary）。

```
單智能體 RL：    環境 ← 智能體
多智能體 RL：    環境 ← 智能體 1
                          ← 智能體 2
                          ← 智能體 N
              每個智能體的決策都影響所有人的下一個狀態
```

## MARL 的分類框架

根據獎勵結構和目標關係，MARL 可分為：

- **完全合作**：所有智能體共享同一獎勵函數
- **完全競爭**：零和博弈，一方的收益等於另一方的損失
- **混合動機**：既有合作又有競爭（如撲克、談判）

### 完全合作：VDN 與 QMIX（2017-2018）

在合作場景中，智能體需要協調行動。VDN（Value Decomposition Networks）將聯合 Q 值分解為各智能體 Q 值的和：

```python
class VDN:
    def __init__(self, agent_nets):
        self.agents = agent_nets

    def joint_q(self, states, actions):
        # 各智能體獨立計算 Q 值
        agent_qs = [agent(s, a) for agent, s, a
                     in zip(self.agents, states, actions)]
        return sum(agent_qs)  # 簡單求和
```

QMIX 更進一步，使用混合網路（Mixing Network）學習非線性分解：

```
Q_total(s, a_1, a_2, ..., a_N) = MixingNetwork(Q_1, Q_2, ..., Q_N)
```

QMIX 強制 ∂Q_total/∂Q_i ≥ 0，確保各智能體的貢獻方向一致。

### 完全競爭：MADDPG（2017）

對於競爭和混合動機場景，OpenAI 提出了 MADDPG（Multi-Agent DDPG），核心思想是「集中訓練、分散執行」（CTDE）：

```
訓練時：    Critic_i 使用所有智能體的觀測和動作
執行時：    Actor_i 只使用自己的局部觀測
```

```python
class MADDPG:
    def __init__(self, agents, critics):
        self.agents = agents      # 各智能體的 Actor
        self.critics = critics     # 各智能體的 Critic（集中式）

    def train(self, experiences):
        # experiences 包含所有智能體的 (s, a, r, s')
        for i, agent in enumerate(self.agents):
            # Critic_i 知道所有智能體的資訊
            q_target = self.target_q_all(expertise[i], experiences)
            critic_loss = (q_target - self.critics[i](observations, actions)) ** 2
            critic_loss.backward()

            # Actor_i 只用自己的觀測
            actor_loss = -self.critics[i](obs[i], agent(obs[i]))
            actor_loss.backward()
```

## 大規模 MARL（2020-2025）

### 混合合作競爭（2020-2022）

SMAC（StarCraft Multi-Agent Challenge）成為 MARL 的標準測試平台。頂尖演算法如 QPLEX 和 HAPPO 在 SMAC 上達到超人級表現。

### 基於 Transformer 的 MARL（2023-2025）

Transformer 架構被引入 MARL，用於建模智能體間的互動關係：

- **MATE（Multi-Agent Transformer）**：使用 self-attention 在智能體之間傳遞資訊
- **MAT（Multi-Agent Transformer）**：將序列建模應用於多智能體決策

### 人類與 AI 混合團隊（2024-2025）

研究重點從純 AI 團隊轉向人類與 AI 的混合協作。關鍵問題：
- AI 如何理解人類隊友的意圖？
- 人類如何信任 AI 隊友？
- 如何實現自然語言的指揮與協調？

## 2028 年的 MARL

當前 MARL 的前沿方向：

### 開源大規模框架

2026-2028 年，多個開源的 MARL 框架（如 MAPPO-Bench、SMACv2）統一了評測標準，使研究更可重現。

### 零樣本方協作

最新研究發現，在大量合作任務上預訓練的 MARL 模型，能在未見過的任務中與未知同伴快速協作。這是「決策基礎模型」的重要方向。

### 現實世界部署

MARL 正在以下領域實現真實部署：

| 場景 | 應用 | 智能體數量 |
|------|------|-----------|
| 交通控制 | 自動駕駛交叉路口協調 | 10-1000 |
| 倉儲物流 | 機器人撿貨與搬運 | 50-500 |
| 能源管理 | 智慧電網負載平衡 | 100-10000 |
| 無人機集群 | 搜索與救援 | 10-100 |

## 延伸閱讀

- [MADDPG 論文](https://www.google.com/search?q=MADDPG+Multi-Agent+Actor-Critic+for+Mixed+Cooperative-Competitive+Environments)
- [QMIX 論文](https://www.google.com/search?q=QMIX+Monotonic+Value+Function+Factorisation+for+Deep+Multi-Agent+Reinforcement+Learning)
- [SMAC 測試平台](https://www.google.com/search?q=SMAC+StarCraft+Multi-Agent+Challenge)

*本篇文章為「AI 程式人雜誌 2028 年 5 月號」強化學習系列之一。*
