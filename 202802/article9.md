# 成本 vs 延遲權衡

## 每毫秒都有價格

即時 AI 系統的延遲最佳化不是免費的。使用更快的 GPU、更大的批次、更低的精度——每一個決策都在成本和延遲之間取捨。本文建立一套量化框架幫助你做決策。

## 延遲分解分析

```python
class LatencyProfiler:
    def __init__(self):
        self.breakdown = {
            'preprocess': 0,
            'model_inference': 0,
            'postprocess': 0,
            'network_transfer': 0,
        }

    def profile(self, pipeline, sample):
        for stage in pipeline:
            start = time.perf_counter()
            stage(sample)
            self.breakdown[stage.name] += time.perf_counter() - start

    def report(self):
        total = sum(self.breakdown.values())
        print("延遲分佈：")
        for name, latency in self.breakdown.items():
            print(f"  {name}: {latency*1000:.1f}ms "
                  f"({latency/total*100:.1f}%)")
```

## 模型大小 vs 準確度

```python
import pandas as pd

models = [
    {'name': 'Llama-3-8B', 'params_B': 8,  'latency_ms': 45,
     'cost_per_1M': 0.20, 'accuracy': 0.89},
    {'name': 'Llama-3-70B', 'params_B': 70, 'latency_ms': 280,
     'cost_per_1M': 1.60, 'accuracy': 0.93},
    {'name': 'Mistral-7B', 'params_B': 7,   'latency_ms': 38,
     'cost_per_1M': 0.17, 'accuracy': 0.87},
    {'name': 'GPT-4o-mini', 'params_B': 8,  'latency_ms': 30,
     'cost_per_1M': 0.15, 'accuracy': 0.91},
]

df = pd.DataFrame(models)
# 經濟效益 = 準確度 / (延遲 * 成本)
df['efficiency'] = (df['accuracy'] * 1000) / (
    df['latency_ms'] * df['cost_per_1M'])
```

## 硬體成本模型

```python
class CostModel:
    def __init__(self, gpu_hourly, requests_per_sec):
        self.gpu_hourly = gpu_hourly
        self.rps = requests_per_sec
        self.gpu_cost_per_second = gpu_hourly / 3600

    def cost_per_request(self, latency_ms, batch_size):
        # GPU 時間成本
        gpu_time_s = latency_ms * batch_size / 1000
        compute_cost = gpu_time_s * self.gpu_cost_per_second

        # 延遲懲罰（SLA 違約）
        if latency_ms > 200:
            penalty = 0.01  # 每次違約 $0.01
        else:
            penalty = 0

        return compute_cost + penalty

    def break_even(self, latency_a, latency_b):
        """兩種配置的成本平衡點"""
        price_diff = abs(self.gpu_hourly_a - self.gpu_hourly_b)
        latency_diff = abs(latency_a - latency_b)
        return {
            'price_per_ms_saved': price_diff / latency_diff,
            'recommendation': (
                'high_perf_gpu' if latency_a < latency_b
                else 'cost_optimized'
            )
        }
```

## 量化經濟學

量化的成本效益分析：

| 精度 | 延遲 | GPU 記憶體 | GPU 成本/時 | 準確度損失 |
|------|------|-----------|-----------|----------|
| FP16 | 1.0x | 16 GB | $3.00 | 0% |
| INT8 | 0.6x | 8 GB | $1.50 | 0.5% |
| INT4 | 0.4x | 4 GB | $0.75 | 1.5% |

## SLA 導向的配置選擇

```python
class SLABasedSelector:
    def __init__(self, latency_sla_ms=200, accuracy_min=0.85):
        self.latency_sla = latency_sla_ms
        self.accuracy_min = accuracy_min

    def select_config(self, candidates):
        valid = [
            c for c in candidates
            if c['p99_latency'] <= self.latency_sla
            and c['accuracy'] >= self.accuracy_min
        ]
        if not valid:
            return None  # 無法滿足 SLA
        return min(valid, key=lambda c: c['cost_per_request'])
```

## 動態路由決策

根據當下負載和預算動態選擇模型：

```python
class AdaptiveRouter:
    def __init__(self, models_with_cost):
        self.models = models_with_cost

    async def route(self, request, budget_percent=100):
        if request.priority == 'high':
            return await models['premium'].infer(request)

        if budget_percent < 50:
            return await models['quantized'].infer(request)

        if self.queue_depth > 100:
            return await models['fast'].infer(request)

        return await models['balanced'].infer(request)
```

## 延伸閱讀

- [GPU 成本比較](https://www.google.com/search?q=A100+vs+H100+pricing+comparison+2026)
- [模型推論成本計算](https://www.google.com/search?q=LLM+inference+cost+estimation)
- [SLA 設計模式](https://www.google.com/search?q=latency+SLA+design+for+ML+systems)
