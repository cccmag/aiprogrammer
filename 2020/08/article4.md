# GPT-2 文字生成

## 前言

GPT-2 是 OpenAI 開發的強大文字生成模型。本文介紹如何使用 GPT-2 進行各種文字生成任務。

---

## 一、載入模型

```python
from transformers import GPT2LMHeadModel, GPT2Tokenizer

model_name = "gpt2"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)
```

---

## 二、基本生成

```python
import torch

# 輸入
input_text = "Once upon a time"
inputs = tokenizer(input_text, return_tensors="pt")

# 生成
with torch.no_grad():
    outputs = model.generate(
        inputs["input_ids"],
        max_length=50,
        num_return_sequences=1,
        temperature=0.7,
        top_k=50,
        top_p=0.95
    )

# 解碼
generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(generated_text)
```

---

## 三、生成參數

### Temperature

控制隨機性：
- 低 temperature（0.1-0.3）：確定性輸出
- 中 temperature（0.5-0.7）：平衡
- 高 temperature（0.9-1.0）：創意/隨機

```python
# 低溫度（保守）
outputs = model.generate(input_ids, temperature=0.1)

# 高溫度（創意）
outputs = model.generate(input_ids, temperature=1.0)
```

### Top-k 採樣

限制每次選擇前 k 個最可能的 token：

```python
outputs = model.generate(
    input_ids,
    top_k=50  # 只考慮前 50 個 token
)
```

### Top-p (Nucleus) 採樣

動態調整候選集合：

```python
outputs = model.generate(
    input_ids,
    top_p=0.92,  # 累積機率 92%
    top_k=0
)
```

---

## 四、創意寫作

```python
def creative_write(prompt, max_length=200):
    inputs = tokenizer(prompt, return_tensors="pt")
    
    outputs = model.generate(
        inputs["input_ids"],
        max_length=max_length,
        temperature=0.85,
        top_p=0.95,
        do_sample=True,
        num_return_sequences=3,
        pad_token_id=tokenizer.eos_token_id
    )
    
    for i, output in enumerate(outputs):
        text = tokenizer.decode(output, skip_special_tokens=True)
        print(f"\n--- Version {i+1} ---")
        print(text)

creative_write("The robot looked at the human and")
```

---

## 五、對話生成

```python
def chat(prompt, max_length=100):
    # 建構對話格式
    dialogue = f"Human: {prompt}\nAI:"
    inputs = tokenizer(dialogue, return_tensors="pt")
    
    outputs = model.generate(
        inputs["input_ids"],
        max_length=inputs["input_ids"].shape[1] + max_length,
        temperature=0.8,
        top_p=0.95,
        do_sample=True,
        pad_token_id=tokenizer.eos_token_id
    )
    
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    # 提取 AI 回應
    if "AI:" in response:
        response = response.split("AI:")[-1].strip()
    
    return response

print(chat("What is the meaning of life?"))
```

---

## 六、特定風格生成

```python
def style_transfer(prompt, style):
    styled_prompt = f"Write in the style of {style}: {prompt}"
    inputs = tokenizer(styled_prompt, return_tensors="pt")
    
    outputs = model.generate(
        inputs["input_ids"],
        max_length=100,
        temperature=0.7,
        top_p=0.9,
        do_sample=True
    )
    
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# 測試不同風格
print(style_transfer("The sun sets in the west.", "Shakespeare"))
print(style_transfer("The sun sets in the west.", "Technical documentation"))
```

---

## 七、程式碼生成

```python
def generate_code(description, language="python"):
    prompt = f"""
# {language} code for: {description}

def """
    
    inputs = tokenizer(prompt, return_tensors="pt")
    
    outputs = model.generate(
        inputs["input_ids"],
        max_length=150,
        temperature=0.3,  # 低溫度，更精確
        top_p=0.9,
        do_sample=True,
        pad_token_id=tokenizer.eos_token_id
    )
    
    code = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return code

print(generate_code("calculate fibonacci numbers"))
```

---

## 八、最佳實踐

### 1. 控制輸出長度

```python
# 設定 min_length 和 max_length
outputs = model.generate(
    input_ids,
    min_length=50,
    max_length=200
)
```

### 2. 避免重複

```python
outputs = model.generate(
    input_ids,
    repetition_penalty=1.2,  # 懲罰重複
    no_repeat_ngram_size=2    # 禁止 2-gram 重複
)
```

### 3. 批次生成

```python
prompts = ["Once upon a time", "In a galaxy far", "The magic of"]
inputs = tokenizer(prompts, return_tensors="pt", padding=True)

outputs = model.generate(
    inputs["input_ids"],
    attention_mask=inputs["attention_mask"],
    max_length=50,
    num_return_sequences=2
)
```

---

## 結語

GPT-2 是文字生成任務的強大工具。透過調整溫度、top-k、top-p 等參數，可以控制生成文字的創意程度和多樣性。

---

*延伸閱讀：[GPT-2+text+generation+tutorial](https://www.google.com/search?q=GPT-2+text+generation+tutorial+2020)*