# 螢幕理解 Agent

## 1. GUI Agent 的興起

螢幕理解 Agent 直接「看」使用者介面操作電腦。從 Apple MM1 到 UI-TARS，這類 Agent 正在改變自動化測試與 RPA。

## 2. 螢幕解析

```python
from PIL import Image
import pytesseract

class ScreenParser:
    def parse(self, path):
        data = pytesseract.image_to_data(Image.open(path), output_type=pytesseract.Output.DICT)
        return [{"text": data["text"][i], "bbox": (data["left"][i], data["top"][i], data["width"][i], data["height"][i])}
                for i in range(len(data["text"])) if data["text"][i].strip()]
```

## 3. VLM 螢幕理解

```python
import base64
from openai import OpenAI

class VLMScreenAgent:
    def understand(self, path):
        with open(path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        r = OpenAI().chat.completions.create(model="gpt-4o", messages=[{
            "role": "user", "content": [
                {"type": "text", "text": "回傳 JSON 格式的 UI 元素列表"},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}}
            ]}])
        return r.choices[0].message.content
```

## 4. 動作執行

```python
import pyautogui, json

class GUIAgent:
    def __init__(self):
        self.vlm = VLMScreenAgent()

    def run(self, task, max_steps=10):
        for _ in range(max_steps):
            analysis = self.vlm.understand(self.screenshot())
            action = self.plan(task, analysis)
            if action["type"] == "done": return True
            self.execute(action)
        return False

    def screenshot(self):
        pyautogui.screenshot("screen.png"); return "screen.png"

    def execute(self, a):
        if a["type"] == "click": pyautogui.click(a["x"], a["y"])
        elif a["type"] == "type": pyautogui.write(a["text"])

    def plan(self, task, analysis):
        r = OpenAI().chat.completions.create(model="gpt-4o", messages=[{
            "role": "user", "content": f"任務：{task}\n畫面：{analysis}\n回傳 JSON 動作"}] )
        return json.loads(r.choices[0].message.content)
```

## 5. 結語

螢幕理解 Agent 代表從 API 驅動到視覺驅動自動化的轉變。跨平台 DOM 解析是關鍵挑戰。

- https://www.google.com/search?q=GUI+agent+screen+understanding+2025
- https://www.google.com/search?q=pyautogui+agent+automation
