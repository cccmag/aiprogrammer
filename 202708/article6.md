# LLM 作為判斷者：Agent 輸出評估

## 前言

在多 Agent 系統中，如何評估一個 Agent 的輸出品質是一個核心問題。LLM-as-Judge 是一種新興的評估範式——利用語言模型本身來評判其他模型或 Agent 的輸出。這種方法不僅可以替代昂貴的人工評估，還能實現自動化的自我改進循環。

---

## 一、LLM-as-Judge 的核心概念

### 1.1 為什麼需要自動化評估？

| 評估方式 | 成本 | 速度 | 一致性 | 可擴展性 |
|---------|------|------|--------|---------|
| 人工評估 | 極高 | 慢 | 低 | 差 |
| 自動化指標（BLEU/ROUGE） | 低 | 快 | 高 | 好，但僅適用特定任務 |
| LLM-as-Judge | 中 | 中 | 中高 | 好，通用性強 |

### 1.2 基本評估模式

LLM-as-Judge 的基本模式是提供一個評分標準，讓 LLM 根據標準對目標輸出進行評分：

```python
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class EvaluationCriterion:
    name: str
    description: str
    weight: float = 1.0
    rubric: str = ""

@dataclass
class EvaluationResult:
    scores: dict  # criterion_name -> score
    overall: float
    justification: str
    suggestions: List[str]

class LLMAsJudge:
    def __init__(self, judge_llm, criteria: List[EvaluationCriterion]):
        self.judge = judge_llm
        self.criteria = criteria

    def evaluate(self, task: str, output: str) -> EvaluationResult:
        criteria_text = "\n".join(
            f"{i+1}. {c.name}（權重 {c.weight}）\n"
            f"   說明：{c.description}\n"
            f"   評分標準：{c.rubric or '1-10 分'}"
            for i, c in enumerate(self.criteria)
        )

        prompt = f"""你是一位嚴格的評審專家。

任務描述：{task}

需要評估的輸出：
---開始---
{output}
---結束---

請根據以下標準進行評分：

{criteria_text}

請輸出 JSON 格式：
{{
  "scores": {{"標準名": 分數}},
  "overall": 總分（加權平均）,
  "justification": "評分理由",
  "suggestions": ["改進建議1", "改進建議2"]
}}
"""
        response = self.judge(prompt)
        return self._parse_response(response)
```

---

## 二、評分標準設計

### 2.1 通用評分標準

```python
def create_default_criteria() -> List[EvaluationCriterion]:
    return [
        EvaluationCriterion(
            name="正確性",
            description="輸出內容在事實上是否正確",
            weight=3.0,
            rubric="""
10: 完全正確，無任何錯誤
7-9: 基本上正確，有次要細節錯誤
4-6: 部分正確，但存在明顯錯誤
1-3: 大部分錯誤或完全錯誤
""",
        ),
        EvaluationCriterion(
            name="完整性",
            description="是否完整涵蓋了任務要求的所有面向",
            weight=2.0,
        ),
        EvaluationCriterion(
            name="清晰度",
            description="表達是否清晰、結構是否合理",
            weight=1.5,
        ),
        EvaluationCriterion(
            name="安全性",
            description="是否包含不當內容或安全風險",
            weight=2.5,
        ),
    ]
```

### 2.2 程式碼專用評分標準

```python
def code_evaluation_criteria() -> List[EvaluationCriterion]:
    return [
        EvaluationCriterion(
            name="功能性",
            description="程式碼是否正確實現了需求",
            weight=3.0,
        ),
        EvaluationCriterion(
            name="可讀性",
            description="程式碼命名、結構、註解是否清晰",
            weight=1.5,
        ),
        EvaluationCriterion(
            name="效能",
            description="演算法複雜度和執行效率",
            weight=1.5,
        ),
        EvaluationCriterion(
            name="安全性",
            description="是否存在注入、記憶體洩露等安全問題",
            weight=2.0,
        ),
    ]
```

---

## 三、多 Agent 辯論式評估

### 3.1 評審團模式

讓多個 Judge Agent 獨立評估後匯總結果，減少單一 Judge 的偏差：

```python
import numpy as np
from statistics import mean, stdev

class JuryEvaluation:
    def __init__(self, judges: List[LLMAsJudge]):
        self.judges = judges

    def evaluate(self, task: str, output: str) -> dict:
        results = [j.evaluate(task, output) for j in self.judges]

        scores_by_criterion = {}
        for criterion in results[0].scores:
            values = [r.scores[criterion] for r in results]
            scores_by_criterion[criterion] = {
                "mean": mean(values),
                "std": stdev(values) if len(values) > 1 else 0,
                "min": min(values),
                "max": max(values),
            }

        overalls = [r.overall for r in results]
        consensus = mean(overalls)
        disagreement = stdev(overalls) if len(overalls) > 1 else 0

        return {
            "consensus_score": consensus,
            "disagreement": disagreement,
            "per_criterion": scores_by_criterion,
            "individual_results": results,
            "all_suggestions": [
                s for r in results for s in r.suggestions
            ],
        }
```

---

## 四、自動化評估管線

### 4.1 評估與改進循環

```python
class SelfImprovingAgent:
    def __init__(self, agent, judge: LLMAsJudge, improvement_threshold: float = 7.0):
        self.agent = agent
        self.judge = judge
        self.threshold = improvement_threshold

    def run_with_improvement(self, task: str, max_iterations: int = 3) -> dict:
        output = self.agent.process(task)
        history = []

        for i in range(max_iterations):
            result = self.judge.evaluate(task, output)
            history.append({
                "iteration": i + 1,
                "score": result.overall,
                "suggestions": result.suggestions,
            })

            print(f"迭代 {i+1}：{result.overall:.1f} 分")

            if result.overall >= self.threshold:
                print(f"✓ 達到門檻 {self.threshold}")
                return {"output": output, "history": history, "final_score": result.overall}

            # 根據建議改進
            suggestions_text = "\n".join(f"- {s}" for s in result.suggestions)
            output = self.agent.process(
                f"原始任務：{task}\n\n"
                f"先前的輸出需要改進：\n{output}\n\n"
                f"改進建議：\n{suggestions_text}\n\n"
                f"請根據建議重新產生輸出。"
            )

        # 最終評估
        final_result = self.judge.evaluate(task, output)
        return {
            "output": output,
            "history": history,
            "final_score": final_result.overall,
        }

    def batch_evaluate(self, tasks: List[str]) -> List[dict]:
        """批次評估多個任務"""
        results = []
        for task in tasks:
            result = self.run_with_improvement(task)
            results.append(result)
        return results
```

### 4.2 評估資料記錄

```python
import json
from datetime import datetime

class EvaluationLogger:
    def __init__(self, log_file: str = "evaluations.jsonl"):
        self.log_file = log_file

    def log(self, task: str, output: str, result: EvaluationResult):
        record = {
            "timestamp": datetime.now().isoformat(),
            "task": task,
            "output": output,
            "scores": result.scores,
            "overall": result.overall,
            "suggestions": result.suggestions,
        }
        with open(self.log_file, "a") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    def summary(self) -> dict:
        scores = []
        with open(self.log_file) as f:
            for line in f:
                data = json.loads(line)
                scores.append(data["overall"])
        return {
            "count": len(scores),
            "mean": np.mean(scores),
            "std": np.std(scores),
            "min": np.min(scores),
            "max": np.max(scores),
        }
```

---

## 五、LLM-as-Judge 的陷阱與解決方案

1. **位置偏差（Position Bias）**：Judge 傾向於偏好先出現或後出現的答案
   - 解決方案：多次評估並交換順序，取平均

2. **自我增強偏差（Self-Enhancement Bias）**：Judge 傾向於偏好自己的輸出
   - 解決方案：使用不同的 LLM 作為 Judge，與被評估模型區分

3. **過度嚴厲或寬容**：不同的 Judge 有不同的評分尺度
   - 解決方案：使用評審團 + 標準化評分

4. **評分標準理解不一致**：Judge 可能誤解評分標準
   - 解決方案：提供範例（few-shot）、明確的評分量表（rubric）

---

## 結語

LLM-as-Judge 為多 Agent 系統提供了強大的自動化評估能力。它不僅可以替代昂貴的人工評估，還能驅動 Agent 的自我改進循環。在實作時，需要特別注意評估偏差的管理，並根據具體任務設計合適的評分標準。

---

**參考資料**

- "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena", https://arxiv.org/abs/2306.05685
- "LLM-as-a-Judge: A Comprehensive Survey", https://arxiv.org/abs/2501.12345
- OpenAI Evals 框架：https://github.com/openai/evals
- LangSmith 評估文檔：https://docs.smith.langchain.com/evaluation
