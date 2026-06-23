# 去中心化訓練協定

## 前言

大型 AI 模型的訓練需要大量資料與算力。去中心化訓練協定讓多個參與方在不共享原始資料的前提下協同訓練模型，同時透過加密經濟學激勵貢獻者。

## 聯邦學習基礎

聯邦學習（Federated Learning）是去中心化訓練的核心技術。參與者在本地訓練模型，只上傳梯度而非原始資料：

```python
import random, json
from dataclasses import dataclass, field

@dataclass
class GradientUpdate:
    node_id: str
    model_version: str
    gradient_hash: str
    samples_count: int
    accuracy: float

class FederatedTrainingProtocol:
    def __init__(self, min_nodes: int = 3):
        self.nodes: dict[str, float] = {}  # node_id -> stake
        self.updates: list[GradientUpdate] = []
        self.min_nodes = min_nodes
        self.global_accuracy = 0.0
    def register_node(self, node_id: str, stake: float):
        self.nodes[node_id] = stake
    def submit_update(self, update: GradientUpdate):
        if update.node_id not in self.nodes:
            return False
        self.updates.append(update)
        return True
    def aggregate(self) -> bool:
        recent = self.updates[-self.min_nodes:]
        if len(recent) < self.min_nodes:
            return False
        weighted_acc = sum(u.accuracy * self.nodes.get(u.node_id, 0) for u in recent)
        total_stake = sum(self.nodes.get(u.node_id, 0) for u in recent)
        self.global_accuracy = weighted_acc / total_stake if total_stake > 0 else 0
        return True
```

## 激勵機制

貢獻訓練資源的節點應獲得獎勵。使用基於貢獻度的分配模型：

```python
def compute_reward(update: GradientUpdate, total_stake: float, reward_pool: float) -> float:
    contribution = update.samples_count * update.accuracy
    return reward_pool * (contribution / max(total_stake, 1))
```

## 參考資料

- https://www.google.com/search?q=federated+learning+decentralized+training+protocol
- https://www.google.com/search?q=incentive+mechanism+federated+learning+blockchain
- https://www.google.com/search?q=distributed+model+training+reward+distribution
