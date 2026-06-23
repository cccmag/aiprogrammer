# 去中心化算力市場

## 前言

大規模 AI 模型的訓練與推論需要巨量 GPU 算力，但集中式雲端供應商壟斷了市場。去中心化算力市場讓閒置 GPU 所有者出租算力，Agent 可以動態競標運算資源。本文探討這類市場的技術架構。

## 市場架構

去中心化算力市場涉及三個角色：**算力提供者**（出租 GPU）、**算力消費者**（Agent 或開發者）、**調度合約**（媒合供需）。

```python
import time, random
from dataclasses import dataclass, field

@dataclass
class ComputeOffer:
    provider_id: str
    gpu_type: str
    price_per_hour: float
    available_hours: int
    reliability: float  # 0-1
    location: str

class ComputeMarket:
    def __init__(self):
        self.offers: list[ComputeOffer] = []
        self.jobs: list[dict] = []
    def publish_offer(self, offer: ComputeOffer):
        self.offers.append(offer)
    def submit_job(self, job_id: str, gpu_req: str, budget: float, hours: int):
        self.jobs.append({"id": job_id, "gpu": gpu_req, "budget": budget, "hours": hours})
    def match_jobs(self):
        matches = []
        for job in self.jobs:
            candidates = [o for o in self.offers
                          if o.gpu_type == job["gpu"]
                          and o.price_per_hour * job["hours"] <= job["budget"]
                          and o.available_hours >= job["hours"]]
            if candidates:
                best = min(candidates, key=lambda o: o.price_per_hour)
                matches.append((job["id"], best.provider_id, best.price_per_hour))
                best.available_hours -= job["hours"]
        return matches
```

## 價格發現機制

算力價格由市場供需決定，而非集中式定價：

```python
def spot_price(market: ComputeMarket, gpu_type: str) -> float:
    offers = [o for o in market.offers if o.gpu_type == gpu_type]
    if not offers:
        return 0.0
    total_hours = sum(o.available_hours for o in offers)
    total_job_hours = sum(j["hours"] for j in market.jobs if j["gpu"] == gpu_type)
    utilization = total_job_hours / max(total_hours, 1)
    base = sum(o.price_per_hour for o in offers) / len(offers)
    return base * (1 + utilization)
```

## 參考資料

- https://www.google.com/search?q=decentralized+GPU+computing+market+2026
- https://www.google.com/search?q=peer+to+peer+compute+marketplace+blockchain
- https://www.google.com/search?q=spot+pricing+decentralized+computing
