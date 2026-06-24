# Few-shot 學習實作

## 基本 Few-shot 模式

```python
def fewshot_translation(english_text):
    prompt = f"""Translate the following English text to French.

Example 1:
English: Hello
French: Bonjour

Example 2:
English: Good morning
French: Bonjour

Example 3:
English: Thank you
French: Merci

Now translate:
English: {english_text}
French:"""

    response = openai.Completion.create(
        model="davinci",
        prompt=prompt,
        max_tokens=50,
        temperature=0.0
    )
    return response.choices[0].text.strip()

result = fewshot_translation("Good night")
print(result)  # "Bonne nuit"
```

## 情緒分析

```python
def analyze_sentiment(text):
    prompt = f"""Classify the sentiment of the following text as positive, negative, or neutral.

Example 1:
Text: I love this product! It's amazing.
Sentiment: positive

Example 2:
Text: This is the worst experience ever.
Sentiment: negative

Example 3:
Text: The meeting is at 3pm.
Sentiment: neutral

Now classify:
Text: {text}
Sentiment:"""

    response = openai.Completion.create(
        model="curie",
        prompt=prompt,
        max_tokens=1,
        temperature=0.0
    )
    return response.choices[0].text.strip()

result = analyze_sentiment("Absolutely fantastic!")
print(result)  # "positive"
```

## 文字分類

```python
def classify_topic(text):
    prompt = f"""Classify the topic of the following text into one of these categories: Technology, Sports, Business, Entertainment, Science.

Example 1:
Text: Apple released new iPhone models today.
Topic: Technology

Example 2:
Text: The Lakers won the championship game.
Topic: Sports

Example 3:
Text: Stock markets rose after positive economic data.
Topic: Business

Now classify:
Text: {text}
Topic:"""

    response = openai.Completion.create(
        model="curie",
        prompt=prompt,
        max_tokens=1
    )
    return response.choices[0].text.strip()
```

## 程式碼解釋

```python
def explain_code(code_snippet):
    prompt = f"""Explain what the following code does in simple terms:

Code:
{code_snippet}

Explanation:"""

    response = openai.Completion.create(
        model="davinci",
        prompt=prompt,
        max_tokens=100
    )
    return response.choices[0].text
```

## 多步推理

```python
def solve_reasoning(problem):
    prompt = f"""Solve this problem step by step:

Problem: If I have 3 apples and you have 5 apples, and we both eat 2 apples, how many apples do we have left?

Step 1: Calculate total apples: 3 + 5 = 8 apples
Step 2: Calculate apples eaten: 2 + 2 = 4 apples
Step 3: Calculate remaining: 8 - 4 = 4 apples
Answer: 4 apples

Problem: {problem}
Step 1:"""

    response = openai.Completion.create(
        model="davinci",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text
```

## Prompt 設計原則

1. **提供清楚的角色描述**
2. **使用多個範例**
3. **格式一致性**
4. **從簡單到複雜的範例排序**

```python
def create_prompt(task, role, examples, input_text):
    prompt = f"You are a {role}. Your task is to {task}.\n\n"
    prompt += "Examples:\n"
    for ex_in, ex_out in examples:
        prompt += f"Input: {ex_in}\nOutput: {ex_out}\n"
    prompt += f"\nNow solve:\nInput: {input_text}\nOutput:"
    return prompt
```

## 參考資源

- https://www.google.com/search?q=few-shot+learning+GPT-3+prompt+design+tutorial+2020
- https://www.google.com/search?q=in-context+learning+GPT-3+examples+few-shot+format+best+practices
- https://www.google.com/search?q=prompt+engineering+GPT-3+classification+translation+reasoning+examples