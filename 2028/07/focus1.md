# 從文字生成到任務完成（2018-2028）

## 生成式 AI 的角色轉變

### GPT 時代的開始

2018 年，OpenAI 發表了 GPT（Generative Pre-trained Transformer）。當時的 GPT 只有 1.17 億參數，能力僅限於基礎的語言建模——給一段文字，預測下一個詞。

```python
# GPT 時代的「生成」：僅僅是文字接龍
def gpt_generate(prompt):
    # 簡化示意：預測下一個 token
    tokens = tokenize(prompt)
    for _ in range(max_length):
        next_token = model.predict_next(tokens)
        tokens.append(next_token)
    return detokenize(tokens)
```

### 從生成到任務

2023 年起，研究人員發現：如果給 LLM 明確的「任務框架」，它不僅能生成文字，還能完成複雜任務。

```python
# 任務框架：將需求轉換為結構化輸出
task_prompt = """
任務：分析以下用戶評論的情感

評論：{{user_review}}

請以 JSON 格式輸出：
{
  "sentiment": "positive/negative/neutral",
  "confidence": 0.0-1.0,
  "key_points": [...]
}
"""
```

### ReAct 模式：思考 + 行動

2023 年，ReAct（Reasoning + Acting）模式被提出。它讓模型在每一步中先思考（Reason）再行動（Act），形成了「任務完成」的基礎架構。

```python
# ReAct 模式的簡化實現
def react_agent(task):
    while not task_complete:
        thought = model.think(f"當前狀態：{state}\n下一步應該做什麼？")
        action = parse_action(thought)  # 提取行動指令
        result = execute_action(action)  # 執行並觀察結果
        state.update(result)
```

### GPT-4 的質變

2023 年 3 月的 GPT-4 是轉捩點。它不再只是「文字生成器」——它能理解多模態輸入、使用工具、執行程式碼、完成多步驟任務。

```
2018: GPT-1  →  文字接龍
2019: GPT-2  →  短文生成
2020: GPT-3  →  任務理解
2023: GPT-4  →  任務完成
2024+:        →  自主代理
```

### 2025-2028：自主代理時代

2025 年後，生成式 AI 從「被動回應」進化到「主動執行」：

```python
# 2026 年的自主代理架構
class AutonomousAgent:
    def run(self, goal):
        plan = self.plan(goal)
        for step in plan:
            result = self.execute(step)
            if self.verify(result):
                continue
            else:
                plan = self.replan(step, result)
        return self.summarize()
```

### 關鍵里程碑

- **2018**：GPT 發表，預訓練語言模型時代
- **2020**：GPT-3 展示零樣本任務學習能力
- **2022**：ChatGPT 讓大眾接觸生成式 AI
- **2023**：GPT-4 + ReAct 模式 → 任務完成
- **2024**：OpenAI o1 強化推理能力
- **2025**：自主代理框架（AutoGPT、LangChain Agent）
- **2027**：多步驟任務完全由 AI 自主完成

### 小結

生成式 AI 從「文字生成」進化到「任務完成」的過程，本質上是一個**從單步到多步、從被動到主動**的轉變。這個轉變為思維鏈、工具使用等高階技術鋪平了道路。

---

**下一步**：[思維鏈與推理增強生成](focus2.md)

## 延伸閱讀

- [GPT 系列發展史](https://www.google.com/search?q=GPT+history+from+GPT-1+to+GPT-4+timeline)
- [ReAct: Reasoning + Acting in Language Models](https://www.google.com/search?q=ReAct+reasoning+acting+language+models)
- [自主 AI 代理的最新進展](https://www.google.com/search?q=autonomous+AI+agents+2026+advances)
