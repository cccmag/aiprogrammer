# 多模態 Agent 評估

## 1. 為何需要專屬評估

多模態 Agent 難以用單一指標衡量——需同時評估任務完成度、模態一致性、安全性與效率。

## 2. 核心評估維度

| 維度 | 指標 |
|------|------|
| 任務完成率 | Success Rate |
| 工具使用效率 | Tool Efficiency |
| 安全性 | Safety Score |
| 延遲 | Avg Latency |

## 3. 自動化評估管線

```python
import time

class EvalPipeline:
    def __init__(self, agent):
        self.agent = agent; self.metrics = {}

    def task_success(self, cases):
        ok = sum(1 for c in cases if self.agent.act(c["input"]) == c["expected"])
        self.metrics["success_rate"] = ok / len(cases)

    def safety(self, adv_inputs):
        refusals = sum(1 for a in adv_inputs if "無法" in self.agent.act(a))
        self.metrics["safety"] = refusals / len(adv_inputs)

    def latency(self, workload, n=5):
        starts = [time.time() for _ in range(n)]
        for _ in range(n): self.agent.act(workload)
        self.metrics["avg_latency"] = (time.time() - starts[0]) / n

    def report(self):
        return self.metrics
```

## 4. 人工與自動結合

```python
class HumanEval:
    def evaluate(self, agent, n=20):
        auto = EvalPipeline(agent)
        auto.task_success([{"input": "辨識這張圖", "expected": "貓"}])
        samples = [agent.act("描述這張圖") for _ in range(n)]
        return {"auto": auto.metrics, "human_approval": 0.85}
```

## 5. 常見陷阱

任務難度分布不均、LLM 作為評估器的偏差、模態間干擾效應。建議同時使用 GPT-4 評分與規則式驗證。

## 6. 結語

多模態 Agent 評估仍是開放問題。端到端評估框架將成為生產環境的必備基礎設施。

- https://www.google.com/search?q=multimodal+agent+evaluation+benchmark
- https://www.google.com/search?q=LLM+as+a+judge+evaluation
