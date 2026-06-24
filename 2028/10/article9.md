# AI 服務定價策略

## 1. 引言

當你建立了一個 AI 產品，如何定價將直接影響市場競爭力與利潤率。AI 服務的定價與傳統軟體不同，因為變動成本（每次推論）佔比極高。本文探討三種主流的 AI 定價模型。

## 2. 三種定價模型

### 2.1 按量計價（Pay-as-you-go）

最直接的模式，客戶按使用量付費。優點是門檻低，缺點是營收波動大。

### 2.2 訂閱制（Subscription）

每月固定費用，通常包含一定的用量上限。提供可預測的營收流。

### 2.3 混合制（Hybrid）

固定月費 + 超額按量計價，結合兩者優點。

## 3. 定價計算引擎

```python
def pricing_strategy(
    cost_per_request: float,
    target_margin: float = 0.7,
    monthly_fixed_cost: float = 10000,
    expected_monthly_requests: int = 100000,
):
    # 按量計價
    payg_price = cost_per_request / (1 - target_margin)

    # 訂閱制：假設平均用量，提供 20% 折扣
    avg_monthly_cost = expected_monthly_requests * cost_per_request
    sub_price = avg_monthly_cost * 0.8 / (1 - target_margin)

    return {
        "payg_per_request": round(payg_price, 4),
        "payg_monthly_avg": round(payg_price * expected_monthly_requests, 0),
        "subscription_monthly": round(sub_price, 0),
        "margin": target_margin,
    }

# 假設每次推論成本 $0.003
result = pricing_strategy(0.003)
print(f"按量計價: ${result['payg_per_request']:.4f}/次 "
      f"(月均 ${result['payg_monthly_avg']:,.0f})")
print(f"訂閱制: ${result['subscription_monthly']:,.0f}/月")
```

## 4. 成本結構分析

```python
class CostStructure:
    def __init__(self):
        self.costs = {}

    def add_cost(self, name: str, fixed: float, variable_per_request: float):
        self.costs[name] = {"fixed": fixed, "variable": variable_per_request}

    def total_cost(self, requests: int) -> float:
        fixed = sum(c["fixed"] for c in self.costs.values())
        variable = sum(c["variable"] for c in self.costs.values())
        return fixed + variable * requests

    def breakeven_analysis(self, price_per_request: float, requests: int):
        total = self.total_cost(requests)
        revenue = price_per_request * requests
        profit = revenue - total
        print(f"請求數: {requests:,}")
        print(f"總成本: ${total:,.0f}")
        print(f"營收: ${revenue:,.0f}")
        print(f"利潤: ${profit:,.0f}")
        return profit

cs = CostStructure()
cs.add_cost("GPU 推論", 2000, 0.001)
cs.add_cost("API Gateway", 500, 0.0001)
cs.add_cost("頻寬", 300, 0.00005)
cs.add_cost("人員維運", 5000, 0)

print("=== 成本結構 ===")
for name, c in cs.costs.items():
    print(f"{name:12s} 固定 ${c['fixed']:>5.0f} + 變動 ${c['variable']:.5f}/次")

cs.breakeven_analysis(price_per_request=0.01, requests=50000)
```

## 5. 分級定價設計

```python
tiers = [
    {"name": "Free",     "monthly_price": 0,    "requests": 100,   "features": "基本功能"},
    {"name": "Starter",  "monthly_price": 29,    "requests": 5000,  "features": "標準功能"},
    {"name": "Pro",      "monthly_price": 99,    "requests": 50000, "features": "進階功能 + API"},
    {"name": "Enterprise", "monthly_price": 499, "requests": 500000, "features": "自訂模型 + SLA"},
]

print("=== 定價方案 ===")
for t in tiers:
    extra_cost = max(0, t["requests"]) * 0.003
    margin = (t["monthly_price"] - extra_cost) / max(t["monthly_price"], 1)
    print(f"{t['name']:12s} ${t['monthly_price']:>4.0f}/月 "
          f"({t['requests']:,} 次) 利潤率 {margin:.0%}")
```

## 6. 動態定價

```python
def dynamic_pricing(
    base_price: float,
    current_load: float,
    max_capacity: float,
) -> float:
    """根據系統負載調整價格。"""
    utilization = current_load / max_capacity
    if utilization > 0.8:
        surge = 1 + (utilization - 0.8) * 2  # 最多漲 40%
        return base_price * surge
    elif utilization < 0.3:
        discount = 1 - (0.3 - utilization) * 0.5  # 最多打 65 折
        return base_price * discount
    return base_price

print("動態定價範例:")
for load in [0.2, 0.5, 0.85, 0.95]:
    price = dynamic_pricing(0.01, load, 1.0)
    print(f"  負載 {load:.0%} → ${price:.4f}/次")
```

## 7. 結語

AI 定價沒有萬能公式，關鍵在於理解你的成本結構與客戶價值感知。建議從小規模測試開始，根據數據持續優化。更多資訊請搜尋 [AI 服務定價策略](https://www.google.com/search?q=AI+service+pricing+strategy+2026)。
