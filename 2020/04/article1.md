# GPT-2 文字生成實戰

## 安裝依賴

```bash
pip install torch transformers
```

## 基本使用

```python
from transformers import GPT2LMHeadModel, GPT2Tokenizer

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

def generate_text(prompt, max_length=50, temperature=1.0):
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(
        **inputs,
        max_length=max_length,
        temperature=temperature,
        do_sample=True,
        top_k=50
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

prompt = "Artificial intelligence is"
result = generate_text(prompt, max_length=50)
print(result)
```

## 溫度參數

溫度控制輸出的隨機性：
- 低溫度（0.1-0.5）：輸出更穩定、確定性更高
- 中溫度（0.7-1.0）：平衡創造性與穩定性
- 高溫度（1.0+）：輸出更隨機、多樣性更高

## Top-k 與 Top-p 採樣

```python
# Top-k 採樣：只從機率最高的 k 個詞中選擇
outputs = model.generate(**inputs, max_length=50, do_sample=True, top_k=50)

# Top-p (nucleus) 採樣：選擇累積機率達到 p 的最小詞集合
outputs = model.generate(**inputs, max_length=50, do_sample=True, top_p=0.95)
```

## 批次生成

```python
prompts = [
    "The future of AI is",
    "In the year 2025,",
    "Machine learning allows"
]

inputs = tokenizer(prompts, return_tensors="pt", padding=True)
outputs = model.generate(**inputs, max_length=50, do_sample=True)
```

## 儲存與載入本地模型

```python
# 儲存模型
tokenizer.save_pretrained("./my_gpt2")
model.save_pretrained("./my_gpt2")

# 載入模型
tokenizer = GPT2Tokenizer.from_pretrained("./my_gpt2")
model = GPT2LMHeadModel.from_pretrained("./my_gpt2")
```

## 參考資源

- https://www.google.com/search?q=GPT-2+Hugging+Face+text+generation+Python+tutorial+2020
- https://www.google.com/search?q=transformers+GPT2LMHeadModel+generate+function+parameters
- https://www.google.com/search?q=top-k+top-p+nucleus+sampling+language+model+explained