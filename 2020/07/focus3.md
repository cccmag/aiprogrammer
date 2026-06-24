# Prompt Engineering：引導語言模型的新方法

## Prompt 的崛起

### 什麼是 Prompt？

Prompt（提示）是引導語言模型產生預期輸出的輸入文字。

```
Prompt: "Translate to French: Hello, how are you?"
Output: "Bonjour, comment allez-vous?"
```

### Prompt Engineering 的興起

隨著 GPT-3 的發布，一個新的領域誕生了：**Prompt Engineering**

研究者開始系統性地研究如何設計更好的提示，以獲得更好的模型輸出。

---

## Prompt 設計原則

### 1. 明確的任務描述

不好的 Prompt：
```
Write about AI.
```

好的 Prompt：
```
Write a 500-word essay about the impact of artificial intelligence on healthcare, 
focusing on diagnosis accuracy and patient outcomes.
```

### 2. 使用格式範例

GPT-3 學會從格式中推斷任務：

```
Prompt:
"Apple -> fruit
Banana -> fruit
Car -> [你的輸出]"
```

### 3. Chain-of-Thought Prompting

2020 年，研究者提出了 Chain-of-Thought 提示：

```
Prompt:
"Q: John has 5 apples. He gives 2 to Mary. How many does he have?
A: He has 5 - 2 = 3 apples.

Q: If you have 3 chickens and you buy 2 more, how many do you have?"
```

模型開始展示推理能力。

---

## Prompt 技術分類

### Zero-shot Prompting

不提供任何範例，只描述任務：

```
"Analyze the sentiment of this review: 'This product is amazing!'"
```

### Few-shot Prompting

提供少量範例：

```
"Sentiment analysis examples:
Review: 'Great food!' -> Positive
Review: 'Terrible service' -> Negative
Review: 'It was okay' -> [模型輸出]"
```

### Prefix Prompting

在輸入前加入前綴，引導模型：

```
"TL;DR: " + 文章內容 -> 摘要
```

### Structure Prompting

使用結構化格式：

```
{
  "task": "translation",
  "source_lang": "English",
  "target_lang": "Spanish", 
  "text": "Hello world"
}
```

---

## Prompt Tuning vs Fine-tuning

### 傳統 Fine-tuning

修改模型權重，適用於每個任務需要獨立模型。

### Prompt Tuning

只改變 Prompt，保持模型權重不變。2020 年的研究顯示：

- **Prefix Tuning**：在輸入前加入可學習的前綴
- **Prompt Tuning**（2021）：學習一組 soft prompts

### 比較

| 方法 | 需要更新權重 | 需要任務資料 |
|------|------------|------------|
| Fine-tuning | 是 | 大量 |
| Prompt Tuning | 只更新 Prompt | 少量 |
| In-context Learning | 否 | 零 |

---

## 實用技巧

### 1. 溫度設定

- 溫度 0：確定性輸出
- 溫度 0.7：創意寫作
- 溫度 1.0+：高度隨機

### 2. Top-p 採樣

控制輸出多樣性：
- top_p=0.9：考慮累积機率 90% 的詞
- top_p=1.0：考慮所有詞

### 3. 限制輸出長度

使用明確的長度指令：
```
"Write a summary in exactly 50 words."
```

---

**下一步**：[GPT-3 的架構與訓練](focus4.md)

## 延伸閱讀

- [Prompt+Engineering+guide+2020](https://www.google.com/search?q=prompt+engineering+language+models+2020)
- [Chain-of-Thought+Prompting+2020](https://www.google.com/search?q=chain+of+thought+prompting+paper+2020)
- [Prefix+Tuning+Prompt+Tuning](https://www.google.com/search?q=prefix+tuning+prompt+tuning+NLP)