# 多模態工具使用

## 1. 工具驅動的 Agent

多模態 Agent 不僅能理解圖像語音，還能主動呼叫工具——拍照、截圖、OCR、播放音訊——完成複雜任務。

## 2. 工具定義

```python
class Tool:
    def __init__(self, name, desc, fn, params):
        self.name = name; self.desc = desc; self.fn = fn; self.params = params

    def to_openai(self):
        return {"type": "function", "function": {"name": self.name, "description": self.desc, "parameters": self.params}}
```

## 3. 常見多模態工具

```python
import cv2, pytesseract

def capture_photo():
    cap = cv2.VideoCapture(0); ret, f = cap.read(); cap.release()
    if ret: cv2.imwrite("photo.jpg", f); return "photo.jpg"

def ocr_image(path):
    return pytesseract.image_to_string(cv2.imread(path), lang="chi_tra+eng").strip()

tools = {
    "photo": Tool("capture_photo", "拍照", capture_photo, {"type": "object", "properties": {}, "required": []}),
    "ocr": Tool("ocr_image", "圖片文字辨識", ocr_image, {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}),
}
```

## 4. 動態執行

```python
import json
from openai import OpenAI

class ToolExecutor:
    def __init__(self, tools):
        self.tools = tools; self.llm = OpenAI()

    def run(self, prompt):
        msgs = [{"role": "user", "content": prompt}]
        resp = self.llm.chat.completions.create(model="gpt-4o", messages=msgs, tools=[t.to_openai() for t in tools.values()])
        msg = resp.choices[0].message
        if msg.tool_calls:
            for tc in msg.tool_calls:
                r = self.tools[tc.function.name].fn(**json.loads(tc.function.arguments))
                msgs.append({"role": "tool", "tool_call_id": tc.id, "content": json.dumps(r)})
            return self.llm.chat.completions.create(model="gpt-4o", messages=msgs).choices[0].message.content
        return msg.content
```

## 5. 結語

工具使用是 Agent 從「被動回應」到「主動執行」的關鍵。錯誤處理穩定性是生產環境的核心挑戰。

- https://www.google.com/search?q=function+calling+multimodal+agent
- https://www.google.com/search?q=OpenAI+tool+use+vision+agent
