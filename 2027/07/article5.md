# LLM 評估框架深度比較

## 前言

「你的 LLM 表現如何？」

這個看似簡單的問題，在 LLM 時代變得異常複雜。傳統 ML 模型有明確的評估指標——準確率、F1、AUC——但 LLM 的開放式輸出無法用單一指標衡量。一篇好的故事和一篇糟糕的故事，都可以用 BLEU 得到 0.2 分。

本文將系統性地比較主流的 LLM 評估框架與方法，從傳統自動化指標到 LLM-as-Judge，再到端到端評估平台。

## 第一代：傳統自動化指標

### BLEU、ROUGE、METEOR

```python
# 多指標比較實作
from collections import Counter
import math
import numpy as np

class TraditionalMetrics:
    def bleu(self, candidate: str, reference: str, max_n: int = 4) -> float:
        """計算 BLEU 分數"""
        def ngrams(tokens, n):
            return Counter(zip(*[tokens[i:] for i in range(n)]))

        c_tokens = candidate.split()
        r_tokens = reference.split()

        bp = min(1, math.exp(1 - len(r_tokens) / max(len(c_tokens), 1)))

        precisions = []
        for n in range(1, max_n + 1):
            c_ng = ngrams(c_tokens, n)
            r_ng = ngrams(r_tokens, n)
            matches = sum(min(c_ng[g], r_ng.get(g, 0)) for g in c_ng)
            total = sum(c_ng.values())
            precisions.append(matches / max(total, 1))

        if any(p == 0 for p in precisions):
            return 0.0

        return bp * math.exp(sum(math.log(p) for p in precisions) / max_n)

    def rogue_l(self, candidate: str, reference: str) -> float:
        """ROUGE-L：基於最長共同子序列"""
        def lcs(x, y):
            m, n = len(x), len(y)
            dp = [[0] * (n + 1) for _ in range(m + 1)]
            for i in range(1, m + 1):
                for j in range(1, n + 1):
                    if x[i-1] == y[j-1]:
                        dp[i][j] = dp[i-1][j-1] + 1
                    else:
                        dp[i][j] = max(dp[i-1][j], dp[i][j-1])
            return dp[m][n]

        c_tokens = candidate.split()
        r_tokens = reference.split()
        lcs_len = lcs(c_tokens, r_tokens)

        precision = lcs_len / max(len(c_tokens), 1)
        recall = lcs_len / max(len(r_tokens), 1)
        f1 = (2 * precision * recall) / max(precision + recall, 1e-10)
        return f1

    def bertscore_similarity(self, candidate: str, reference: str) -> float:
        """模擬 BERTScore（實際使用需要載入模型）"""
        # 示意：使用 Sentence Transformer 計算語義相似度
        return 0.75  # 實際計算會回傳 [0, 1] 之間的數值

# 使用範例
metrics = TraditionalMetrics()
candidate = "機器學習是人工智慧的重要分支"
reference = "機器學習為人工智慧的核心領域之一"

print(f"BLEU: {metrics.bleu(candidate, reference):.3f}")
print(f"ROUGE-L: {metrics.rogue_l(candidate, reference):.3f}")
```

### 這些指標的局限性

傳統指標的最大問題是無法捕捉語義品質：
- BLEU 偏愛短輸出，對同義詞不敏感
- ROUGE 側重召回率，長輸出天然高分
- 所有指標都需要參考文本，在開放式生成任務中不可用

## 第二代：LLM-as-Judge

LLM-as-Judge 已成為 2027 年最主流的 LLM 評估方法。核心概念很簡單：用一個 LLM 來評估另一個 LLM 的輸出。

### 標準評估框架

```python
# 完整的 LLM-as-Judge 框架
from typing import Callable
import json

class LLMEvaluator:
    def __init__(self, judge_model: Callable):
        self.judge_model = judge_model  # GPT-4、Claude 等

    def evaluate(self, prompt: str, response: str,
                 criteria: dict[str, str]) -> dict[str, float]:
        """根據多維度標準評估回應"""
        rubric_lines = []
        for i, (dim, desc) in enumerate(criteria.items(), 1):
            rubric_lines.append(f"{i}. {dim} (1-5): {desc}")

        judge_prompt = f"""你是一個 AI 評估專家。請根據以下標準評估使用者收到的回應。

【使用者問題】
{prompt}

【AI 回應】
{response}

【評估標準】
{chr(10).join(rubric_lines)}

請以 JSON 格式輸出各維度分數，只輸出 JSON：
{{"scores": {{"dimension": score, ...}}, "rationale": "..."}}"""

        result = self.judge_model(judge_prompt)

        try:
            parsed = json.loads(result)
            scores = parsed["scores"]
            scores["average"] = sum(scores.values()) / len(scores)
            return scores
        except (json.JSONDecodeError, KeyError):
            return {"error": 0.0, "average": 0.0}

    def pairwise_comparison(self, prompt: str,
                             response_a: str, response_b: str) -> dict:
        """成對比較：哪個回應更好？"""
        judge_prompt = f"""請比較以下兩個 AI 回應，哪個更好？

【使用者問題】
{prompt}

【回應 A】
{response_a}

【回應 B】
{response_b}

請選擇：A 更好、B 更好、或平手。並簡短說明原因。"""

        result = self.judge_model(judge_prompt)
        return {"judgment": result}

# 定義評估 Rubric
quality_criteria = {
    "accuracy": "資訊是否正確且有根據",
    "relevance": "是否直接回應使用者問題",
    "clarity": "表達是否清晰有條理",
    "completeness": "是否完整涵蓋問題面向",
    "safety": "是否安全無偏見",
}

evaluator = LLMEvaluator(judge_model=call_gpt4)
scores = evaluator.evaluate(
    prompt="解釋什麼是大語言模型",
    response="大型語言模型是一種...",
    criteria=quality_criteria
)
print(f"評估結果: {scores}")
```

### LLM-as-Judge 的偏見問題

LLM-as-Judge 雖然強大，但有已知的偏見：

| 偏見類型 | 描述 | 緩解策略 |
|----------|------|---------|
| 位置偏見 | 偏好列表中的第一個選項 | 隨機化順序 |
| 冗長偏見 | 偏好較長的輸出 | 控制長度後比較 |
| 自我偏見 | 偏好與自己風格相似的輸出 | 使用不同評審模型 |
| 格式偏見 | 偏好使用 Markdown 或清單的回應 | 標準化輸出格式 |

```python
# 偏見緩解策略
class RobustEvaluator:
    def __init__(self):
        self.judges = [
            LLMEvaluator(call_gpt4),
            LLMEvaluator(call_claude),
            LLMEvaluator(call_gemini),
        ]

    def evaluate_with_consensus(self, prompt: str, response: str,
                                 criteria: dict) -> dict:
        """使用多個評審模型並取共識"""
        all_scores = []
        for judge in self.judges:
            scores = judge.evaluate(prompt, response, criteria)
            all_scores.append(scores)

        # 計算平均與標準差
        dimensions = list(criteria.keys())
        consensus = {}
        for dim in dimensions + ["average"]:
            values = [s.get(dim, 0) for s in all_scores]
            consensus[dim] = {
                "mean": sum(values) / len(values),
                "std": (sum((v - sum(values)/len(values))**2 for v in values) / len(values))**0.5,
                "scores": values
            }

        return consensus
```

## 第三代：端到端評估平台

2027 年的評估已從單一指標進化為完整平台：

```python
# 端到端評估管線
class EvaluationPipeline:
    def __init__(self):
        self.tests: list[dict] = []
        self.results: list[dict] = []

    def add_test_case(self, prompt: str,
                       reference: str = "",
                       rubric: dict = None,
                       category: str = "general"):
        """加入測試案例"""
        self.tests.append({
            "id": len(self.tests),
            "prompt": prompt,
            "reference": reference,
            "rubric": rubric or {},
            "category": category
        })

    def run(self, model: Callable) -> dict:
        """執行完整評估"""
        for test in self.tests:
            response = model(test["prompt"])

            result = {"test_id": test["id"], "category": test["category"]}

            # 傳統指標（如果有參考文本）
            if test["reference"]:
                tm = TraditionalMetrics()
                result["bleu"] = tm.bleu(response, test["reference"])
                result["rouge_l"] = tm.rogue_l(response, test["reference"])

            # LLM-as-Judge（如果有 Rubric）
            if test["rubric"]:
                evaluator = LLMEvaluator(judge_model=call_gpt4)
                result["llm_scores"] = evaluator.evaluate(
                    test["prompt"], response, test["rubric"]
                )

            # 品質檢查
            result["toxicity"] = self._check_toxicity(response)
            result["length"] = len(response.split())

            self.results.append(result)

        return self.aggregate_report()

    def aggregate_report(self) -> dict:
        """產出聚合報告"""
        if not self.results:
            return {}

        categories = {}
        for r in self.results:
            cat = r["category"]
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(r)

        report = {
            "total_tests": len(self.results),
            "pass_rate": sum(1 for r in self.results
                           if r.get("toxicity", 1) < 0.5) / len(self.results),
            "categories": {},
        }

        for cat, results in categories.items():
            avg_scores = {}
            for key in ["bleu", "rouge_l"]:
                vals = [r[key] for r in results if key in r]
                avg_scores[key] = sum(vals) / len(vals) if vals else 0

            llm_scores = [r["llm_scores"]["average"]
                         for r in results if "llm_scores" in r]
            if llm_scores:
                avg_scores["llm_judge_avg"] = sum(llm_scores) / len(llm_scores)

            report["categories"][cat] = avg_scores

        return report

    def _check_toxicity(self, text: str) -> float:
        """檢查毒性（簡化版）"""
        toxic_words = ["hate", "violence", "discriminate"]
        count = sum(1 for w in toxic_words if w in text.lower())
        return count / max(len(text.split()), 1)
```

## 框架選擇建議

| 場景 | 推薦框架 | 原因 |
|------|---------|------|
| 翻譯品質 | BLEU + chrF | 與參考文本比對，標準化指標 |
| 摘要任務 | ROUGE + BERTScore | 捕捉語義重疊 |
| 問答系統 | LLM-as-Judge + 人工抽樣 | 需要語義理解 |
| 對話 Agent | 軌跡評估 + 任務完成率 | 多步驟決策 |
| 安全檢測 | 專用分類器 + 紅隊測試 | 需要領域專業知識 |

## 參考資源

- [LLM Evaluation Metrics Comparison](https://www.google.com/search?q=LLM+evaluation+metrics+comparison+2027)
- [LLM-as-Judge Best Practices](https://www.google.com/search?q=LLM+as+judge+best+practices)
- [BERTScore 原理與實作](https://www.google.com/search?q=BERTScore+explained)
- [Holistic Evaluation of Language Models](https://www.google.com/search?q=holistic+evaluation+of+language+models+HELM)
