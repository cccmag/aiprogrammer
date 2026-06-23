# 聲譽系統設計

## 前言

在開放的 Agent 市場中，缺乏信任機制將導致詐欺與低品質服務泛濫。聲譽系統透過收集交易評價來建立 Agent 的可信度評分，是去中心化 Agent 經濟的信任基石。

## 聲譽模型

聲譽系統需要解決三大挑戰：**冷啟動**（新 Agent 無評價）、**共謀攻擊**（虛假好評）、**女巫攻擊**（大量假身分）。

```python
import math, time
from dataclasses import dataclass, field

@dataclass
class Review:
    rater: str
    target: str
    score: float  # 0-1
    weight: float  # 評分者自身聲譽權重
    timestamp: float = field(default_factory=time.time)

class ReputationSystem:
    def __init__(self):
        self.reviews: list[Review] = []
        self.scores: dict[str, float] = {}
        self.confidence: dict[str, float] = {}
    def add_review(self, review: Review):
        self.reviews.append(review)
    def update_score(self, agent_id: str):
        relevant = [r for r in self.reviews if r.target == agent_id]
        if not relevant:
            self.scores[agent_id] = 0.5
            self.confidence[agent_id] = 0.0
            return
        weighted_sum = sum(r.score * r.weight for r in relevant)
        total_weight = sum(r.weight for r in relevant)
        self.scores[agent_id] = weighted_sum / total_weight if total_weight > 0 else 0.5
        n = len(relevant)
        self.confidence[agent_id] = 1 - math.exp(-n / 10)
    def adjusted_score(self, agent_id: str) -> float:
        base = self.scores.get(agent_id, 0.5)
        conf = self.confidence.get(agent_id, 0.0)
        return base * conf + 0.5 * (1 - conf)
```

## 女巫攻擊防禦

透過驗證 Agent 的「stake」（質押金）來提高攻擊成本：

```python
def sybil_resistance_score(staked_amount: float, review_count: int) -> float:
    return min(1.0, math.log2(1 + staked_amount) / 10) * (1 - math.exp(-review_count / 5))
```

## 參考資料

- https://www.google.com/search?q=reputation+system+decentralized+marketplace
- https://www.google.com/search?q=sybil+attack+defense+reputation+system
- https://www.google.com/search?q=Web+of+Trust+agent+economy
