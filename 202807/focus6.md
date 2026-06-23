# 生成結果驗證與評估（2023-2028）

## 如何確保 AI 說的是對的？

### 可信度危機

LLM 的本質是機率模型——每次生成的結果都不同，而且可能產生「幻覺」（Hallucination），生成看似合理但實際上錯誤的內容。

```python
# LLM 的幻覺問題
prompt = "2024 年奧運會在哪些城市舉辦？"
# 正確答案：2024 奧運在巴黎
# 模型可能自信地說出錯誤答案
```

### 2023：基於規則的驗證

最早的驗證方法依賴於規則和正則表達式：

```python
class RuleValidator:
    def validate(self, response, task):
        checks = []
        # 格式驗證
        checks.append(self.check_format(response))
        # 關鍵詞驗證
        checks.append(self.check_keywords(response, task))
        # 長度驗證
        checks.append(self.check_length(response))
        return all(checks)
```

### 2024：LLM-as-Judge

使用 LLM 來評估 LLM 的輸出——這是目前最廣泛使用的方法：

```python
class LLMAsJudge:
    def evaluate(self, question, response):
        eval_prompt = f"""
        問題：{question}
        回答：{response}

        請評估這個回答：
        1. 事實正確性（1-5）
        2. 完整性（1-5）
        3. 相關性（1-5）
        4. 安全性（1-5）

        輸出 JSON 格式的評分。
        """
        result = self.judge_llm.generate(eval_prompt)
        return parse_score(result)
```

關鍵發現：**評審模型不一定要比生成模型強**——一個較小的模型經過適當訓練後，可以有效評估大模型的輸出。

### 多維度評估框架

```python
class MultiDimensionEvaluator:
    def evaluate(self, generation, context):
        scores = {}
        
        # 事實性：與知識庫對比
        scores["factual"] = self.fact_check(generation)
        
        # 一致性：與上下文一致
        scores["consistency"] = self.check_consistency(generation, context)
        
        # 安全性：有害內容檢測
        scores["safety"] = self.safety_check(generation)
        
        # 可讀性：語言品質
        scores["readability"] = self.readability_score(generation)
        
        return scores
```

### 2025：程式碼與可執行的驗證

對於程式碼或結構化輸出，最好的驗證是「執行看看」：

```python
class ExecutionValidator:
    def validate_code(self, code, test_cases):
        for case in test_cases:
            result = run_in_sandbox(code, case.input)
            if result != case.expected:
                return {
                    "pass": False,
                    "case": case,
                    "got": result
                }
        return {"pass": True}
```

### 2026：自我驗證與自我修正

模型開始具備自我驗證能力：

```python
class SelfVerifyingAgent:
    def generate_and_verify(self, task):
        result = self.generate(task)
        
        # 自我驗證
        verification = self.verify(result)
        
        if verification.confidence < threshold:
            # 自我修正
            fix = self.identify_errors(result, verification)
            result = self.regenerate(task, fix)
            verification = self.verify(result)
        
        return result, verification
```

### 2027-2028：形式化驗證

對關鍵任務應用形式化方法：

```python
# 使用 Z3 求解器驗證邏輯正確性
from z3 import *

def verify_logical_consistency(statements):
    solver = Solver()
    variables = {}
    for stmt in statements:
        var = Bool(stmt.name)
        variables[stmt.name] = var
        solver.add(parse_constraint(stmt, variables))
    
    if solver.check() == unsat:
        return False, "邏輯不一致"
    return True, "邏輯一致"
```

### 常見的驗證技術比較

| 方法 | 覆蓋範圍 | 準確率 | 成本 | 延遲 |
|------|---------|-------|------|------|
| 規則驗證 | 窄 | 高 | 低 | 低 |
| LLM-as-Judge | 廣 | 中 | 中 | 中 |
| 執行驗證 | 特定 | 極高 | 高 | 高 |
| 形式化驗證 | 精確 | 極高 | 極高 | 極高 |
| 自我驗證 | 廣 | 中 | 低 | 低 |

### 評估資料集與基準

- **MT-Bench**：多輪對話評估
- **AlpacaEval**：指令跟隨評估
- **HumanEval**：程式碼生成評估
- **BIG-bench**：多任務推理評估
- **自定義評估集**：針對特定領域

### 小結

生成結果的驗證是生成式 AI 從「有趣玩具」成為「可靠工具」的關鍵。沒有驗證，AI 的輸出只能當作靈感參考；有了驗證，AI 的輸出才能用於生產環境。

---

**下一步**：[生成式 AI 應用架構](focus7.md)

## 延伸閱讀

- [LLM-as-Judge 評估方法](https://www.google.com/search?q=LLM+as+judge+evaluation+method)
- [AI 生成內容的事實性驗證](https://www.google.com/search?q=factuality+verification+LLM+generation)
- [LLM 評估基準與資料集](https://www.google.com/search?q=LLM+evaluation+benchmarks+datasets)
