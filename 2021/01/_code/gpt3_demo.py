#!/usr/bin/env python3
"""GPT-3 API Demo: Few-shot learning and prompt engineering examples"""

import json
from typing import Optional

class GPT3Demo:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or "demo-key"
        self.model = "text-davinci-003"

    def call_api(self, prompt: str, max_tokens: int = 100) -> str:
        print(f"\n[API Call]")
        print(f"Prompt: {prompt[:50]}...")
        print(f"Max tokens: {max_tokens}")
        simulated_response = self._simulate_response(prompt)
        return simulated_response

    def _simulate_response(self, prompt: str) -> str:
        if "翻譯" in prompt or "translation" in prompt.lower():
            if "你好" in prompt:
                return "Hello"
            elif "謝謝" in prompt:
                return "Thank you"
            elif "對不起" in prompt:
                return "Sorry"
            elif "我愛你" in prompt:
                return "I love you"
        if "摘要" in prompt or "summary" in prompt.lower():
            return "Python is a versatile programming language."
        if "Python" in prompt and ("什麼是" in prompt or "is" in prompt):
            return "Python 是一種高階程式語言，適合初學者學習。"
        if "翻轉" in prompt:
            return "[::-1]"
        return "這是模擬的回應結果。"

    def few_shot_translation(self) -> str:
        prompt = """將中文翻譯�成英文：

範例：
"你好" → "Hello"
"謝謝" → "Thank you"
"對不起" → "Sorry"

待翻譯：
"我愛你" →"""
        return self.call_api(prompt)

    def sentiment_classification(self) -> str:
        prompt = """判斷以下評論的情感（正面/負面）：

範例：
"這家餐廳非常好吃！" → 正面
"服務態度太差了" → 負面

待判斷：
"食物一般，但環境不錯" →"""
        return self.call_api(prompt)

    def code_explanation(self) -> str:
        prompt = """解釋以下 Python 程式碼的功能：

```python
print("Hello, World!")
```

解釋："""
        return self.call_api(prompt)

    def summarize(self) -> str:
        prompt = """請用一句話總結以下文字：

Python 是一種廣泛使用的高階程式語言，由 Guido van Rossum 於 1991 年創造。Python 強調程式碼的可讀性和簡潔的語法，讓開發者能夠用更少的程式碼表達想法。

摘要："""
        return self.call_api(prompt)

    def math_reasoning(self) -> str:
        prompt = """計算：7 × 8 = ?

請逐步思考："""
        return self.call_api(prompt, max_tokens=50)

    def json_format(self) -> str:
        prompt = """將以下資訊以 JSON 格式輸出：

姓名：小明
年齡：25
職業：工程師

JSON："""
        return self.call_api(prompt, max_tokens=50)


def demo():
    print("=" * 60)
    print("GPT-3 API Demo - Few-shot Learning Examples")
    print("=" * 60)

    demo_obj = GPT3Demo()

    print("\n" + "=" * 40)
    print("1. Few-shot 翻譯")
    print("=" * 40)
    result = demo_obj.few_shot_translation()
    print(f"Result: {result}")

    print("\n" + "=" * 40)
    print("2. Few-shot 情感分類")
    print("=" * 40)
    result = demo_obj.sentiment_classification()
    print(f"Result: {result}")

    print("\n" + "=" * 40)
    print("3. 程式碼解釋")
    print("=" * 40)
    result = demo_obj.code_explanation()
    print(f"Result: {result}")

    print("\n" + "=" * 40)
    print("4. 文字摘要")
    print("=" * 40)
    result = demo_obj.summarize()
    print(f"Result: {result}")

    print("\n" + "=" * 40)
    print("5. 數學推理")
    print("=" * 40)
    result = demo_obj.math_reasoning()
    print(f"Result: {result}")

    print("\n" + "=" * 40)
    print("6. JSON 格式輸出")
    print("=" * 40)
    result = demo_obj.json_format()
    print(f"Result: {result}")

    print("\n" + "=" * 60)
    print("All demos completed!")
    print("=" * 60)


if __name__ == '__main__':
    demo()