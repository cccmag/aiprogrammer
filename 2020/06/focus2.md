# 2. Few-shot Learning 機制

## 什麼是 Few-shot Learning？

Few-shot Learning 是指模型在給定少量任務示範後，能夠完成新任務的能力，無需進行梯度更新。這種能力是 GPT-3 最引人注目的特點之一。

## 與傳統方法的比較

| 方法 | 需要標註資料 | 需要微調 | 推論速度 |
|------|-------------|---------|---------|
| 傳統監督學習 | 數千至數萬 | 是 | 快 |
| 遷移學習 (BERT) | 數百至數千 | 是 | 快 |
| Few-shot (GPT-3) | 0-100 | 否 | 慢 |
| Zero-shot (GPT-3) | 0 | 否 | 慢 |

## Few-shot Prompt 範例

```
任務：翻譯英文為法文

範例：
English: Hello
French: Bonjour

English: Good morning
French: Bonjour

English: Thank you
French:

預測：Merci
```

## Prompt Engineering

Few-shot Learning 的效果高度依賴 Prompt 的設計：

```python
def create_prompt(task_description, examples, input_text):
    prompt = f"{task_description}\n\n"
    for example_input, example_output in examples:
        prompt += f"Input: {example_input}\n"
        prompt += f"Output: {example_output}\n"
    prompt += f"Input: {input_text}\n"
    prompt += "Output:"
    return prompt
```

## 影響 Few-shot 效果的因素

1. **範例數量**：通常 10-100 個範例效果較好
2. **範例多樣性**：涵蓋不同情況的範例效果更好
3. **範例順序**：從簡單到複雜的排序通常較好
4. **格式一致性**：輸入輸出格式需要一致

## 情境學習（In-context Learning）

GPT-3 的 Few-shot 能力被稱為「情境學習」，因為模型是在推理時透過上下文中的示範來學習任務，而不是真的在更新權重。

這種學習方式與傳統的監督學習有本質不同：
- 不需要梯度計算
- 學習速度極快
- 但泛化能力可能有限

## 局限性

Few-shot Learning 也有一些限制：
- 每次推理都需要傳遞範例，增加計算成本
- 模型仍可能生成不合理輸出
- 對某些任務效果不佳

## 參考資源

- https://www.google.com/search?q=GPT-3+few-shot+learning+in-context+learning+prompt+tutorial+2020
- https://www.google.com/search?q=few-shot+one-shot+zero-shot+language+model+comparison+performance
- https://www.google.com/search?q=prompt+engineering+GPT-3+few-shot+examples+design+best+practices