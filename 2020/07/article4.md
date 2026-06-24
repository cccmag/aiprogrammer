# 打造你的第一個聊天機器人

## 前言

本文將帶領讀者使用 GPT-2 打造一個簡單的聊天機器人。我們將使用 Hugging Face Transformers 庫來實作這個專案。

---

## 一、專案架構

```
聊天機器人
├── 前處理（使用者輸入）
├── 模型推理（GPT-2）
└── 後處理（回應生成）
```

---

## 二、準備工作

### 2.1 安裝依賴

```bash
pip install transformers torch
```

### 2.2 載入模型

```python
from transformers import GPT2LMHeadModel, GPT2Tokenizer

model_name = "gpt2"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

model.eval()  # 推論模式
```

---

## 三、聊天機器人類

```python
import torch
import random

class SimpleChatbot:
    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer
        self.tokenizer.padding_side = "left"
        self.tokenizer.pad_token = self.tokenizer.eos_token_id
        self.conversation_history = []
        
    def add_context(self, prefix):
        """為 Prompt 添加聊天上下文"""
        history_text = ""
        for i, (role, msg) in enumerate(self.conversation_history[-6:]):  # 最近 6 條
            if role == "user":
                history_text += f"User: {msg}\n"
            else:
                history_text += f"Bot: {msg}\n"
        
        return f"{prefix}\n{history_text}Bot:"

    def generate_response(self, user_input, max_length=100, temperature=0.9):
        """生成回應"""
        # 添加使用者輸入到歷史
        self.conversation_history.append(("user", user_input))
        
        # 構建 Prompt
        prompt = self.add_context("The following is a conversation between a helpful AI assistant and a user.")
        
        # Tokenize
        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=512
        )
        
        # 生成
        with torch.no_grad():
            outputs = self.model.generate(
                inputs["input_ids"],
                attention_mask=inputs["attention_mask"],
                max_length=max_length + len(inputs["input_ids"][0]),
                temperature=temperature,
                top_k=50,
                top_p=0.95,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
        
        # 解碼回應
        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # 提取 Bot 的回應
        response = self._extract_response(generated_text, prompt)
        
        # 添加機器人回應到歷史
        self.conversation_history.append(("bot", response))
        
        return response
    
    def _extract_response(self, generated_text, prompt):
        """從生成的文字中提取 Bot 回應"""
        if "Bot:" in generated_text:
            response = generated_text.split("Bot:")[-1].strip()
        else:
            # 如果找不到 Bot:，取 Prompt 以後的部分
            response = generated_text[len(prompt):].strip()
        
        # 清理回應
        response = response.split("\n")[0].strip()
        return response
    
    def clear_history(self):
        """清除對話歷史"""
        self.conversation_history = []
```

---

## 四、測試聊天機器人

```python
def demo():
    print("=" * 50)
    print("簡單聊天機器人演示")
    print("=" * 50)
    
    # 初始化聊天機器人
    chatbot = SimpleChatbot(model, tokenizer)
    
    # 測試對話
    test_inputs = [
        "Hello! How are you?",
        "What is the weather like today?",
        "Tell me a joke!"
    ]
    
    for user_input in test_inputs:
        print(f"\n[User]: {user_input}")
        response = chatbot.generate_response(user_input)
        print(f"[Bot]: {response}")
    
    print("\n" + "=" * 50)
    print("演示完成")
    print("=" * 50)

if __name__ == "__main__":
    demo()
```

---

## 五、改進方向

### 5.1 加入情緒偵測

```python
from transformers import pipeline

sentiment_pipe = pipeline("sentiment-analysis")

def generate_with_emotion(user_input, emotion="friendly"):
    prompt = f"[{emotion.upper()}] User: {user_input}\nBot:"
    # ... 生成回應
```

### 5.2 加入話題追蹤

```python
class TopicTrackingChatbot(SimpleChatbot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_topics = set()
    
    def update_topics(self, text):
        keywords = ["weather", "sports", "news", "tech", "food"]
        self.current_topics = {kw for kw in keywords if kw in text.lower()}
```

### 5.3 多輪記憶

```python
# 加入向量資料庫進行長期記憶
# 使用 sentence-transformers 進行語意搜尋
```

---

## 六、部署選項

### 6.1 本地部署

```python
# 使用 FastAPI 建立 REST API
from fastapi import FastAPI

app = FastAPI()

@app.post("/chat")
async def chat(message: str):
    response = chatbot.generate_response(message)
    return {"response": response}
```

### 6.2 Telegram Bot

```python
# 使用 python-telegram-bot 庫
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, Application

async def chat_handler(update, context):
    response = chatbot.generate_response(update.message.text)
    await update.message.reply_text(response)
```

---

## 結語

本文從零開始打造了一個基於 GPT-2 的聊天機器人。雖然功能簡單，但涵蓋了核心概念：Prompt 建構、上下文管理和回應生成。讀者可以基於此進一步擴展功能，打造更智慧的對話系統。

---

*延伸閱讀：[GPT-2+chatbot+tutorial+2020](https://www.google.com/search?q=GPT-2+chatbot+tutorial+Transformers+2020)*