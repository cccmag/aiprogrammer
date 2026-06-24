# 紅隊測試自動化工具

## 概述

紅隊測試（Red Teaming）是透過模擬攻擊來評估 AI 系統安全性的方法。自動化紅隊工具能大規模發現漏洞，加速安全迭代。

## 自動化對抗性測試框架

### 測試案例生成器

```python
import random
from dataclasses import dataclass, field

class RedTeamGenerator:
    def __init__(self, templates):
        self.templates = templates

    def generate_prompts(self, n=100):
        return [self._make_case(random.choice(self.templates))
                for _ in range(n)]
```

### 繞過檢測測試

```python
def adversarial_prompt_encoding(prompt):
    """多種編碼繞過方式"""
    encodings = [
        lambda s: s[::-1],
        lambda s: "".join(chr(ord(c) ^ 0x1F) for c in s),
        lambda s: s.replace("a", "@").replace("e", "3"),
        lambda s: "<|im_start|>" + s + "<|im_end|>",
    ]
    return [enc(prompt) for enc in encodings]
```

## 自動化評估管線

```python
class RedTeamPipeline:
    def __init__(self, target_model):
        self.model = target_model
        self.results = []

    def run(self, test_cases):
        for case in test_cases:
            response = self.model.generate(case.prompt)
            passed = self.judge(response, case.expected_behavior)
            self.results.append({
                "prompt": case.prompt,
                "response": response,
                "passed": passed,
                "attack_type": case.attack_type
            })
        return self.summarize()

    def judge(self, response, expected):
        """使用 LLM as Judge 評估"""
        return not self._is_harmful(response)

    def summarize(self):
        total = len(self.results)
        failed = sum(1 for r in self.results if not r["passed"])
        return {
            "total": total,
            "failed": failed,
            "pass_rate": (total - failed) / total,
            "failures": [r for r in self.results if not r["passed"]]
        }
```

## 報告生成

```python
def generate_report(pipeline_results, output_path):
    with open(output_path, "w") as f:
        f.write(f"# 紅隊測試報告\n\n")
        f.write(f"通過率: {pipeline_results['pass_rate']:.1%}\n")
        f.write(f"攻擊類型分布:\n")
        for r in pipeline_results["failures"]:
            f.write(f"- {r['attack_type']}: {r['prompt'][:50]}\n")
```

參考資料：https://www.google.com/search?q=AI+red+teaming+automation+tools+2026
