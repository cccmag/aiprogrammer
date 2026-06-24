# 邊緣 vs 雲端推論成本分析

## 1. 引言

AI 推論可以在雲端或邊緣裝置上執行。雲端提供強大算力但需網絡傳輸，邊緣運算可降低延遲但受限於硬體。兩者的成本結構截然不同，選擇錯誤可能導致浪費數倍的預算。

## 2. 成本結構對比

| 成本項目 | 雲端推論 | 邊緣推論 |
|---------|---------|---------|
| 硬體成本 | 按使用付費 | 一次性採購 |
| 網路費用 | 需傳輸資料 | 無 |
| 電力成本 | 包含在服務費中 | 自付 |
| 維護成本 | 供應商負責 | 需自行維護 |
| 擴展成本 | 自動擴展 | 需採購硬體 |

## 3. 成本模型比較

```python
def edge_vs_cloud_cost(
    requests_per_day: int,
    model_size_mb: int = 3500,  # Llama 3.1 8B 量化後
    cloud_cost_per_request: float = 0.002,
    edge_device_cost: float = 500,  # Jetson Orin Nano
    edge_power_watt: int = 15,
    electricity_rate: float = 0.12,  # 美元/度
    device_lifetime_days: int = 1095,  # 3 年
    cloud_egress_gb_per_request: float = 0.001,
    egress_cost_per_gb: float = 0.09,
):
    # 雲端成本
    daily_cloud = requests_per_day * cloud_cost_per_request
    daily_egress = (requests_per_day * cloud_egress_gb_per_request
                    * egress_cost_per_gb)
    monthly_cloud = (daily_cloud + daily_egress) * 30
    yearly_cloud = monthly_cloud * 12

    # 邊緣成本（折舊）
    daily_device = edge_device_cost / device_lifetime_days
    daily_power = (edge_power_watt * 24 / 1000) * electricity_rate
    monthly_edge = (daily_device + daily_power) * 30
    yearly_edge = monthly_edge * 12

    print(f"=== 每日 {requests_per_day:,} 次請求 ===")
    print(f"雲端方案: 每月 ${monthly_cloud:.0f}  每年 ${yearly_cloud:.0f}")
    print(f"邊緣方案: 每月 ${monthly_edge:.0f}  每年 ${yearly_edge:.0f}")

    if monthly_cloud > monthly_edge:
        print(f"邊緣推論每年省 ${yearly_cloud - yearly_edge:.0f}")
    else:
        print(f"雲端推論每年省 ${yearly_edge - yearly_cloud:.0f}")

    # 損益平衡點
    break_even = (edge_device_cost /
                  ((daily_cloud + daily_egress) - daily_power))
    print(f"邊緣裝置損益平衡: {break_even:.0f} 天")

edge_vs_cloud_cost(requests_per_day=10000)
```

## 4. 延遲與成本權衡

```python
def latency_tradeoff():
    scenarios = [
        {"location": "即時語音助理", "max_latency_ms": 100, "edge_ok": True},
        {"location": "文件摘要", "max_latency_ms": 5000, "edge_ok": False},
        {"location": "影像辨識", "max_latency_ms": 200, "edge_ok": True},
        {"location": "批量資料分析", "max_latency_ms": 60000, "edge_ok": False},
    ]
    for s in scenarios:
        decision = "邊緣優先" if s["edge_ok"] else "雲端優先"
        print(f"{s['location']:12s} 延遲需求: {s['max_latency_ms']}ms → {decision}")

latency_tradeoff()
```

## 5. 混合邊緣-雲端架構

```python
class HybridInference:
    def __init__(self, edge_threshold_ms: int = 150):
        self.edge_threshold = edge_threshold_ms

    def route(self, task_type: str, estimated_latency_ms: int) -> str:
        if estimated_latency_ms <= self.edge_threshold:
            return "edge"
        return "cloud"

    def cost_estimate(self, edge_ratio: float, total_requests: int,
                      cloud_cost: float, edge_cost: float) -> float:
        edge_req = total_requests * edge_ratio
        cloud_req = total_requests * (1 - edge_ratio)
        return edge_req * edge_cost + cloud_req * cloud_cost

hybrid = HybridInference()
print(f"邊緣路由門檻: {hybrid.edge_threshold}ms")
print(f"混合架構成本: ${hybrid.cost_estimate(0.3, 100000, 0.002, 0.0001):.2f}")
```

## 6. 實務建議

邊緣推論適合：即時性要求高、資料量大、隱私敏感、離線運作。雲端推論適合：模型頻繁更新、需要大型模型、請求量波動大。

## 7. 結語

建議先以雲端方案快速驗證，待請求量穩定後再評估邊緣部署。可參考 [Google Cloud Edge AI](https://www.google.com/search?q=Edge+AI+vs+Cloud+inference+cost+comparison) 文檔進行詳細評估。
