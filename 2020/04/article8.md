# GPT-2 與對話系統

## 對話系統類型

1. **任務導向對話**：預約餐廳、客服等
2. **社交對話**：閒聊、情感支援
3. **知識問答**：回答問題、解釋概念

## 基礎對話生成

```python
from transformers import GPT2LMHeadModel, GPT2Tokenizer

model = GPT2LMHeadModel.from_pretrained("gpt2")
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

def chat(prompt, max_length=100):
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(
        **inputs,
        max_length=max_length,
        do_sample=True,
        temperature=0.8,
        top_p=0.95
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

response = chat("User: What is Python?\nAssistant:")
print(response)
```

## 對話格式

將對話格式化為模型可理解的形式：

```python
def format_conversation(history, current_input):
    prompt = ""
    for user, assistant in history:
        prompt += f"User: {user}\nAssistant: {assistant}\n"
    prompt += f"User: {current_input}\nAssistant:"
    return prompt

history = [
    ("Hello", "Hi! How can I help you?"),
    ("What is AI?", "AI stands for Artificial Intelligence...")
]

prompt = format_conversation(history, "Tell me more about it")
response = chat(prompt)
```

## 對話狀態追蹤

```python
class DialogueState:
    def __init__(self):
        self.history = []
        self.context = {}
    
    def add_turn(self, user_input, assistant_response):
        self.history.append((user_input, assistant_response))
    
    def get_context(self):
        return "\n".join([
            f"User: {u}\nAssistant: {a}"
            for u, a in self.history
        ])

state = DialogueState()
state.add_turn("I want to book a flight", "Where would you like to go?")
state.add_turn("Paris", "When would you like to fly to Paris?")
```

## 回覆選擇

從多個候選中選擇最佳回覆：

```python
def generate_candidates(prompt, n=5):
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(
        **inputs,
        max_length=100,
        do_sample=True,
        temperature=0.9,
        top_p=0.95,
        num_return_sequences=n
    )
    return [tokenizer.decode(o, skip_special_tokens=True) for o in outputs]

def select_best_response(candidates, criteria_fn):
    scored = [(c, criteria_fn(c)) for c in candidates]
    return max(scored, key=lambda x: x[1])[0]
```

## 安全性過濾

```python
BLOCKED_WORDS = ["violence", "hack", "illegal"]

def is_safe_response(response):
    for word in BLOCKED_WORDS:
        if word.lower() in response.lower():
            return False
    return True

def safe_chat(prompt):
    response = chat(prompt)
    if is_safe_response(response):
        return response
    return "I'm sorry, I can't respond to that."
```

## 參考資源

- https://www.google.com/search?q=GPT-2+chatbot+conversation+system+Python+tutorial+2020
- https://www.google.com/search?q=dialogue+state+tracking+conversation+AI+implementation
- https://www.google.com/search?q=conversational+AI+response+selection+safety+filtering+GPT-2