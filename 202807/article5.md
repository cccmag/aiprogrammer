# 多模型路由策略

## 為什麼需要路由

不同 LLM 各有擅長：小模型速度快成本低，大模型推理能力強。路由策略根據任務特性動態選擇最佳模型，平衡成本與品質。

## 路由器設計

```python
class ModelRouter:
    def __init__(self):
        self.models = {
            "fast": {"model": "gpt-4o-mini", "cost": 0.15, "suited_for": ["分類", "摘要"]},
            "reasoning": {"model": "o1", "cost": 2.0, "suited_for": ["數學", "程式"]},
            "code": {"model": "claude-3-opus", "cost": 1.5, "suited_for": ["程式碼生成"]}
        }

    def route(self, task):
        if self._needs_reasoning(task):
            return self.models["reasoning"]
        elif self._is_code_task(task):
            return self.models["code"]
        return self.models["fast"]

    def _needs_reasoning(self, task):
        keywords = ["證明", "推導", "數學", "邏輯"]
        return any(k in task for k in keywords)
```

## 快取與 Fallback

```python
class SmartRouter(ModelRouter):
    def __init__(self):
        super().__init__()
        self.cache = {}

    def execute(self, task):
        if task in self.cache:
            return self.cache[task]

        model = self.route(task)
        try:
            result = call_llm(model["model"], task)
            self.cache[task] = result
            return result
        except Exception as e:
            fallback = self.models["reasoning"]
            return call_llm(fallback["model"], task)
```

## 混合策略

進階路由可結合 classifier 模型，先將任務分類再路由。也可使用「並行投票」：同時呼叫多個小模型，取多數決結果。

## 成本優化

定期統計各模型表現，動態調整路由閾值。詳見 https://www.google.com/search?q=LLM+model+routing+strategy。
