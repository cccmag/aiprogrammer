# 開源 vs 閉源成本分析

## 1. 引言

開源模型（如 Llama、Mistral）與閉源模型（如 GPT-4o、Claude）各有優劣。開源模型無 API 使用費，但需要自建基礎設施；閉源模型按用量付費，但長期累積下來可能更昂貴。本文進行全面的成本比較。

## 2. 總持有成本（TCO）比較

```python
def tco_comparison(
    monthly_requests: int,
    avg_input_tokens: int = 500,
    avg_output_tokens: int = 200,
    months: int = 12,
):
    # 閉源方案
    closed_models = {
        "GPT-4o": {"input": 2.50, "output": 10.00},
        "GPT-4o-mini": {"input": 0.15, "output": 0.60},
    }
    # 開源方案（自部署硬體成本）
    open_source = {
        "Llama 3.1 70B": {
            "gpu_cost": 15000,   # 一次性 GPU 採購
            "power_monthly": 500,
            "hosting_monthly": 300,
            "ops_monthly": 1000,
        },
        "Mistral Large 2": {
            "gpu_cost": 12000,
            "power_monthly": 400,
            "hosting_monthly": 300,
            "ops_monthly": 1000,
        },
    }

    print("=== 閉源方案年成本 ===")
    for name, price in closed_models.items():
        per_request = (avg_input_tokens * price["input"] +
                       avg_output_tokens * price["output"]) / 1_000_000
        yearly = per_request * monthly_requests * 12
        print(f"{name:20s} ${yearly:,.0f}/年")

    print("\n=== 開源方案年成本（含折舊）===")
    for name, cost in open_source.items():
        depreciation = cost["gpu_cost"] / 36  # 3 年折舊
        monthly = (depreciation + cost["power_monthly"]
                   + cost["hosting_monthly"] + cost["ops_monthly"])
        yearly = monthly * 12
        per_request_cost = yearly / (monthly_requests * 12)
        print(f"{name:20s} ${yearly:,.0f}/年 (每請求 ${per_request_cost:.6f})")

tco_comparison(monthly_requests=500_000)
```

## 3. 損益平衡點計算

當請求量超過某個 threshold，自部署開源模型更划算：

```python
def break_even_point(
    api_price_per_request: float,
    fixed_hardware_cost: float,
    monthly_ops: float,
) -> int:
    """計算每月需要多少請求才能打平。"""
    monthly_fixed = fixed_hardware_cost / 36 + monthly_ops
    return int(monthly_fixed / api_price_per_request)

# GPT-4o-mini 每請求成本約 $0.00027
api_cost = (500 * 0.15 + 200 * 0.60) / 1_000_000
bep = break_even_point(api_cost, 15000, 1800)
print(f"損益平衡點: 每月 {bep:,} 次請求")
print(f"高於此數量，自部署 Llama 更划算")
```

## 4. 隱性成本比較

```python
hidden_costs = {
    "閉源方案": {
        "API 鎖定效應": "更換供應商需改程式碼",
        "資料隱私風險": "資料送至第三方",
        "價格波動": "供應商可隨時調漲",
    },
    "開源方案": {
        "維運人力": "需專人管理基礎設施",
        "模型更新": "需自行追蹤最新版本",
        "GPU 利用率": "硬體可能閒置",
    },
}
for category, items in hidden_costs.items():
    print(f"\n{category}:")
    for k, v in items.items():
        print(f"  - {k}: {v}")
```

## 5. 混合策略建議

```python
def hybrid_recommendation(sensitivity: str = "high"):
    """根據資料敏感度給出建議。"""
    recs = {
        "high": "核心資料用開源自部署，一般任務用閉源 API",
        "medium": "閉源為主，開源為輔以控制成本",
        "low": "全部使用閉源 API，最省維運心力",
    }
    return recs.get(sensitivity, "請評估資料類型")

print(hybrid_recommendation("high"))
```

## 6. 結語

開源與閉源不是二元選擇。建議採用混合架構：敏感資料使用自部署開源模型，大量簡單任務使用低價閉源 API，關鍵推理使用高品質閉源模型。詳見 [Google Cloud AI 方案](https://www.google.com/search?q=open+source+vs+closed+source+LLM+cost+comparison)。
