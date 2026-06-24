# 生成結果驗證框架

## 為什麼需要驗證

LLM 可能產生幻覺、格式錯誤或邏輯矛盾。自動化驗證是將生成式 AI 導入生產環境的關鍵。

## 驗證層級

1. **語法驗證**：檢查 JSON/YAML 格式
2. **邏輯驗證**：檢查事實一致性
3. **語意驗證**：使用 embedding 相似度比對
4. **功能驗證**：執行測試案例

## 驗證框架實作

```python
from typing import Any
import json
import jsonschema

class ValidationPipeline:
    def __init__(self):
        self.validators = []

    def add(self, validator):
        self.validators.append(validator)
        return self

    def validate(self, output: Any) -> dict:
        results = {"passed": [], "failed": []}
        for v in self.validators:
            try:
                v(output)
                results["passed"].append(v.__name__)
            except Exception as e:
                results["failed"].append({"name": v.__name__, "error": str(e)})
        return results

def json_schema_validator(schema):
    def validate(output):
        if isinstance(output, str):
            output = json.loads(output)
        jsonschema.validate(output, schema)
    return validate

def fact_check_validator(llm):
    def validate(output):
        prompt = f"以下陳述是否包含事實錯誤？\n{output}"
        verdict = llm.generate(prompt)
        if "錯誤" in verdict:
            raise ValueError(f"事實錯誤：{verdict}")
    return validate
```

## 自動修正循環

```python
class SelfCorrectingGenerator:
    def __init__(self, llm, pipeline):
        self.llm = llm
        self.pipeline = pipeline

    def generate(self, prompt, max_retry=3):
        for i in range(max_retry):
            output = self.llm.generate(prompt)
            result = self.pipeline.validate(output)
            if not result["failed"]:
                return output
            prompt += f"\n請修正以下問題：{result['failed']}"
        raise RuntimeError("超過重試次數")
```

## 評估指標

使用 BLEU、ROUGE、BERTScore 等指標，結合人工抽樣檢查。詳見 https://www.google.com/search?q=LLM+output+validation+framework。
