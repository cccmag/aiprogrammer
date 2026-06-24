# A/B 測試與模型評估

## 前言

AI 應用中模型的更換或提示詞調整可能對使用者體驗產生重大影響。A/B 測試與系統化評估是確保變更帶來正向效果的唯一方法。

## A/B 測試架構

```python
import random
from datetime import datetime
from typing import Any

class ABTest:
    def __init__(self, experiment_name: str, variants: list[str],
                 traffic_split: list[float] | None = None):
        self.name = experiment_name
        self.variants = variants
        self.traffic_split = traffic_split or [1.0 / len(variants)] * len(variants)
        self.results: dict[str, list[dict]] = {v: [] for v in variants}

    def assign(self, user_id: str) -> str:
        seed = hash(f"{self.name}:{user_id}") % 10000
        cumulative = 0
        for i, (variant, split) in enumerate(zip(self.variants, self.traffic_split)):
            cumulative += split * 10000
            if seed < cumulative:
                return variant
        return self.variants[-1]

    def record(self, variant: str, metrics: dict):
        self.results[variant].append({
            "timestamp": datetime.now(),
            **metrics,
        })

    def summary(self) -> dict[str, Any]:
        result = {}
        for variant, records in self.results.items():
            if not records:
                result[variant] = {}
                continue
            latencies = [r.get("latency_ms", 0) for r in records]
            result[variant] = {
                "count": len(records),
                "avg_latency_ms": sum(latencies) / len(latencies),
                "avg_score": sum(r.get("score", 0) for r in records) / len(records),
            }
        return result
```

## 評估指標

```python
class ResponseEvaluator:
    async def evaluate(self, prompt: str, response: str, expected: str = "") -> dict:
        eval_prompt = (
            f"評估以下回答，請給出各項指標的 0-1 分數：\n\n"
            f"問題：{prompt}\n回答：{response}\n"
            f"請以 JSON 格式回傳相關性、正確性、流暢度分數"
        )
        result = await call_llm(eval_prompt, model="gpt-4o")
        import json
        return json.loads(result.content)

    def latency_metric(self, start: datetime, end: datetime) -> float:
        return (end - start).total_seconds() * 1000

evaluator = ResponseEvaluator()

async def ab_test_call(exp: ABTest, user_id: str, prompt: str) -> str:
    variant = exp.assign(user_id)
    start = datetime.now()
    response = await call_llm(prompt, model=variant)
    latency = evaluator.latency_metric(start, datetime.now())

    quality = await evaluator.evaluate(prompt, response)
    exp.record(variant, {"latency_ms": latency, "score": quality.get("相關性", 0)})
    return response
```

## 離線評估

```python
class OfflineEvaluator:
    def __init__(self, test_cases: list[dict]):
        self.test_cases = test_cases

    async def benchmark(self, model: str) -> dict:
        scores = []
        for case in self.test_cases:
            response = await call_llm(case["prompt"], model=model)
            eval_result = await evaluator.evaluate(case["prompt"], response, case.get("expected"))
            scores.append(eval_result)
        return {
            "model": model,
            "avg_relevance": sum(s.get("相關性", 0) for s in scores) / len(scores),
            "avg_accuracy": sum(s.get("正確性", 0) for s in scores) / len(scores),
            "avg_fluency": sum(s.get("流暢度", 0) for s in scores) / len(scores),
        }
```

## 自動化回歸測試

```python
class RegressionTest:
    def __init__(self):
        self.golden: list[dict] = []

    def add_golden(self, prompt: str, expected_keywords: list[str]):
        self.golden.append({"prompt": prompt, "keywords": expected_keywords})

    async def run(self, model: str) -> list[dict]:
        failures = []
        for case in self.golden:
            response = await call_llm(case["prompt"], model=model)
            missing = [kw for kw in case["keywords"] if kw not in response]
            if missing:
                failures.append({
                    "prompt": case["prompt"],
                    "missing_keywords": missing,
                    "response_preview": response[:100],
                })
        return failures
```

## 結語

A/B 測試和系統化評估是 AI 應用持續改善的基礎。建立離線基準、上線實驗和回歸測試的完整流程，確保每次模型或提示詞變更都有數據支撑。

---

**延伸閱讀**

- [LLM A/B 測試方法](https://www.google.com/search?q=LLM+A-B+testing+methodology)
- [模型評估指標](https://www.google.com/search?q=LLM+evaluation+metrics)
- [回歸測試策略](https://www.google.com/search?q=LLM+regression+testing+strategy)
