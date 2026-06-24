# 多語言能力分析

## GPT-3 的語言支援

GPT-3 的訓練資料涵蓋多種語言，表現差異：

| 語言類型 | 表現 |
|---------|------|
| 英語 | 最佳 |
| 西歐語言（法、德、西） | 良好 |
| 日語、韓語 | 中等 |
| 中文 | 中等 |
| 其他語言 | 有限 |

## 多語言生成

```python
def translate_multilingual(text, target_lang):
    prompt = f"""Translate to {target_lang}:
{text}

Translation:"""
    response = openai.Completion.create(
        model="curie",
        prompt=prompt,
        max_tokens=200
    )
    return response.choices[0].text

# 測試
french = translate_multilingual("Hello, how are you?", "French")
japanese = translate_multilingual("Hello, how are you?", "Japanese")
```

## 多語言問答

```python
def multilingual_qa(question, lang="English"):
    prompt = f"""Answer this question in {lang}:

Question: {question}

Answer in {lang}:"""
    response = openai.Completion.create(
        model="davinci",
        prompt=prompt,
        max_tokens=100
    )
    return response.choices[0].text
```

## Few-shot 多語言

```python
# 用英語範例指導其他語言任務
prompt = """Translate English to French:
English: Hello -> French: Bonjour
English: Good morning -> French: Bonjour
English: Thank you -> French: Merci
English: {input} -> French:"""
```

## 語言檢測

```python
def detect_language(text):
    prompt = f"""Detect the language of this text:
"{text}"

Language:"""
    response = openai.Completion.create(
        model="curie",
        prompt=prompt,
        max_tokens=20,
        temperature=0.0
    )
    return response.choices[0].text.strip()
```

## 跨語言遷移

GPT-3 能用英語 Few-shot 示範來完成其他語言的任務，這是一種跨語言遷移能力。

## 限制與建議

1. **資源較少的語言**：表現較差
2. **複雜語法**：如匈牙利語、芬蘭語
3. **翻譯品質**：可能不如專業翻譯模型

## 參考資源

- https://www.google.com/search?q=GPT-3+multilingual+capabilities+languages+performance+comparison+2020
- https://www.google.com/search?q=GPT-3+non-English+languages+translation+accuracy+analysis
- https://www.google.com/search?q=large+language+model+cross-lingual+transfer+zero-shot+multilingual