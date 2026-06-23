# LLM 生成訓練資料實戰

## 1. 引言

大型語言模型（LLM）不僅可以用來回答問題，更能反過來生成高品質的訓練資料。這種「以模型訓練模型」的自舉方法，正成為 AI 開發中的重要策略。本文將探討如何使用 LLM 生成結構化訓練資料，並以 Python 實作示範。

## 2. 為什麼需要 LLM 生成資料？

真實世界標註資料的取得成本高昂，且往往涉及隱私問題。LLM 生成資料的優勢在於：

- **低成本**：不需要人工標註
- **可擴展**：能大量產生多樣化資料
- **快速迭代**：即時調整語意範圍

## 3. 實作：使用 OpenAI API 生成問答資料

以下 Python 程式碼示範如何利用 LLM 生成指定主題的問答對：

```python
import json
from openai import OpenAI

client = OpenAI()

def generate_qa_pairs(topic: str, n: int = 5) -> list:
    prompt = f"""請為主題「{topic}」產生 {n} 組問答對。
每組包含：
- question: 中文提問
- answer: 簡潔的中文回答
- difficulty: 難度 (easy/medium/hard)

以 JSON 陣列格式輸出。"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
    )
    data = json.loads(response.choices[0].message.content)
    return data.get("qa_pairs", [])

# 生成「機器學習」主題的問答資料
pairs = generate_qa_pairs("機器學習", n=3)
for p in pairs:
    print(f"Q: {p['question']}")
    print(f"A: {p['answer']} ({p['difficulty']})\n")
```

## 4. 品質過濾策略

LLM 生成的資料需要經過品質把關。常見策略包括：

```python
def filter_low_quality(pairs: list, threshold: float = 0.8) -> list:
    filtered = []
    for p in pairs:
        score = evaluate_quality(p["question"], p["answer"])
        if score >= threshold:
            filtered.append(p)
    return filtered

def evaluate_quality(question: str, answer: str) -> float:
    # 使用另一個 LLM 評估品質
    prompt = f"""評估以下問答對的品質：
問題：{question}
答案：{answer}
請給出 0-1 之間的分數。"""
    return float(client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
    ).choices[0].message.content)
```

## 5. 常見陷阱

- **模式坍縮**：生成結果過度相似，缺乏多樣性。解決方案是在 prompt 中加入隨機種子與風格要求。
- **幻覺知識**：模型可能生成看似合理但錯誤的答案。建議導入事實驗證機制。
- **偏見放大**：LLM 本身的偏見會反映在生成資料中，需要搭配去偏見策略。

## 6. 結語

LLM 生成訓練資料是一把雙面刃：它大幅降低了資料獲取的成本，但也帶來了品質控管的新挑戰。實務上建議採用「人機協作」模式——由 LLM 大量生成，再由人工抽樣驗證。

## 延伸閱讀

- [OpenAI Prompt Engineering Guide](https://www.google.com/search?q=OpenAI+prompt+engineering+guide)
- [Synthetic Data Generation with LLMs](https://www.google.com/search?q=synthetic+data+generation+with+large+language+models)
