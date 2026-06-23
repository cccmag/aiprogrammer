# Agent 身分與聲譽系統（2025-2029）

## 去中心化身分（DID）

Agent 需要一個全球唯一的去中心化身分（Decentralized Identifier, DID）。DID 的私鑰由 Agent 控制，不需要中心化註冊機構。

## DID 結構

```
did:agent:123456789abcdef
├── method: agent (特定的 DID method)
├── DID Document: 包含公鑰、服務端點
└── Verifiable Credential: 第三方簽發的聲明
```

## 聲譽系統設計

聲譽是 Agent 經濟中最有價值的無形資產。好的聲譽系統需滿足：

1. **不可轉讓**：聲譽綁定 DID，無法買賣
2. **上下文相關**：翻譯 Agent 的聲譽不應直接套用於程式撰寫
3. **抗 Sybil**：透過質押或身分證明防止分身攻擊
4. **遺忘機制**：舊評價權重遞減，反映當前能力

## 程式範例：聲譽系統

```python
import time

class ReputationSystem:
    def __init__(self, decay_rate=0.95):
        self.ratings = {}
        self.decay_rate = decay_rate

    def add_rating(self, agent_did, score, task_type):
        if agent_did not in self.ratings:
            self.ratings[agent_did] = {}
        if task_type not in self.ratings[agent_did]:
            self.ratings[agent_did][task_type] = []
        self.ratings[agent_did][task_type].append({
            "score": score, "time": time.time()
        })

    def get_score(self, agent_did, task_type):
        if agent_did not in self.ratings:
            return 0.5
        entries = self.ratings[agent_did].get(task_type, [])
        if not entries:
            return 0.5
        total, weight_sum = 0, 0
        for e in entries:
            age = time.time() - e["time"]
            w = self.decay_rate ** (age / 86400)  # 每日衰減
            total += e["score"] * w
            weight_sum += w
        return total / weight_sum if weight_sum else 0.5

rep = ReputationSystem()
rep.add_rating("did:agent:alice", 5.0, "翻譯")
rep.add_rating("did:agent:alice", 4.0, "翻譯")
rep.add_rating("did:agent:bob", 2.0, "翻譯")
print(f"Alice 翻譯聲譽: {rep.get_score('did:agent:alice', '翻譯'):.2f}")
print(f"Bob 翻譯聲譽: {rep.get_score('did:agent:bob', '翻譯'):.2f}")
```

## 聲譽的經濟價值

高聲譽 Agent 可以：
- 收取更高服務費
- 獲得優先任務推薦
- 降低質押要求
- 參與高價值合約

## 參考資料

- [W3C DID 規範](https://www.google.com/search?q=W3C+decentralized+identifier+DID)
- [Verifiable Credentials 資料模型](https://www.google.com/search?q=verifiable+credentials+data+model)
- [EigenTrust 聲譽演算法](https://www.google.com/search?q=EigenTrust+reputation+algorithm)
