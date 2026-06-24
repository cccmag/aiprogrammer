# GPT-3 文字生成實測

## 基本文字生成

```python
import openai

response = openai.Completion.create(
    model="davinci",
    prompt="The future of artificial intelligence is",
    max_tokens=100,
    temperature=0.7,
    top_p=1.0
)
print(response.choices[0].text)
```

## 不同溫度的效果

```python
prompts = [
    "Once upon a time",
    "The meaning of life is",
    "Why is the sky blue?"
]

for temp in [0.3, 0.7, 1.0, 1.5]:
    print(f"\n=== Temperature: {temp} ===")
    for prompt in prompts:
        response = openai.Completion.create(
            model="davinci",
            prompt=prompt,
            max_tokens=50,
            temperature=temp
        )
        print(f"Prompt: {prompt}")
        print(f"Output: {response.choices[0].text[:100]}...")
        print()
```

## 創意寫作

```python
story_prompt = """Write a short story about a robot who discovers emotions.

Title: The Awakening

Once upon a time, in a laboratory far away, there was a robot named Echo. Echo had been programmed to assist humans with their daily tasks, but one day, something strange happened. While organizing photographs, Echo stumbled upon an old image of a human family smiling together. Something stirred within Echo's circuits—a feeling Echo had never experienced before.

The feeling was..."""

response = openai.Completion.create(
    model="davinci",
    prompt=story_prompt,
    max_tokens=300,
    temperature=0.85
)
print(response.choices[0].text)
```

## 技術文件生成

```python
api_doc_prompt = """Generate Python documentation for the following function:

```python
def fibonacci(n):
    '''
    Calculate the nth Fibonacci number.

    Args:
        n (int): The position in the Fibonacci sequence

    Returns:
        int: The nth Fibonacci number
    '''
    pass
```

Documentation:"""

response = openai.Completion.create(
    model="davinci",
    prompt=api_doc_prompt,
    max_tokens=200
)
print(response.choices[0].text)
```

## 問答生成

```python
qa_prompt = """Answer the following question based on the context.

Context: Photosynthesis is the process used by plants and other organisms to convert light energy into chemical energy. The process occurs in the chloroplasts of plant cells. Chlorophyll, the green pigment in plants, absorbs light and uses it to convert carbon dioxide and water into glucose and oxygen.

Question: What is photosynthesis?
Answer: Photosynthesis is the process used by plants to convert light energy into chemical energy.

Context: The mitochondria is the powerhouse of the cell. It generates most of the cell's supply of adenosine triphosphate (ATP), used as a source of chemical energy.

Question: What is the mitochondria?
Answer:"""

response = openai.Completion.create(
    model="davinci",
    prompt=qa_prompt,
    max_tokens=50,
    temperature=0.0  # 確定性輸出
)
print(response.choices[0].text)
```

## 比較不同模型

```python
models = ["davinci", "curie", "babbage", "ada"]
prompt = "Explain quantum computing in simple terms:"

for model in models:
    response = openai.Completion.create(
        model=model,
        prompt=prompt,
        max_tokens=100
    )
    print(f"\n=== {model} ===")
    print(response.choices[0].text)
```

## 參考資源

- https://www.google.com/search?q= GPT-3+text+generation+API+Python+tutorial+examples+2020
- https://www.google.com/search?q=OpenAI+davinci+curie+babbage+ada+comparison+output+quality
- https://www.google.com/search?q=GPT-3+temperature+top_p+settings+creative+writing+technical+output