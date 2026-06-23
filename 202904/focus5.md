# 工具使用與多模態 API（2025-2029）

## Function Calling 的多模態擴展

2023 年 OpenAI 推出 function calling，讓 LLM 能呼叫外部 API。到了 2025 年，function calling 擴展到多模態——模型可以根據圖片內容決定呼叫哪個工具。例如，看到使用者上傳的發票圖片，自動選擇 OCR 工具、計算工具與記帳工具。

```python
import openai, json

class ToolUsingMultimodalAgent:
    def __init__(self):
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "analyze_image",
                    "description": "分析圖片中的物體與場景",
                    "parameters": {"type": "object", "properties": {}}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "search_web",
                    "description": "搜尋網路資訊",
                    "parameters": {
                        "type": "object",
                        "properties": {"query": {"type": "string"}}
                    }
                }
            }
        ]
```

## 視覺觸發的工具選擇

視覺觸發是 2025 年最重要的 Agent 模式之一。使用者不需要告訴 Agent「先 OCR 再搜尋」，Agent 看到圖片後自動決定工具鏈：

```python
def process_receipt(image_path):
    agent = ToolUsingMultimodalAgent()
    result = agent.act("請處理這張發票", image_path)
    return result
```

## 多模態 API 生態

各大平台推出多模態 API，開發者可以自由組合：

- **OpenAI GPT-4o**：文字 + 圖像 + 音訊輸入，支援 streaming
- **Google Gemini**：文字 + 圖像 + 音訊 + 影片，原生多模態設計
- **Anthropic Claude 3.5**：文字 + 圖像，強調安全性
- **ElevenLabs**：語音合成 API，支援情感控制

Gemini 多模態 API 範例：

```python
import google.generativeai as genai
model = genai.GenerativeModel("gemini-2.0-flash")
response = model.generate_content([
    "請描述這張圖片中的場景",
    genai.upload_file("photo.jpg")
])
```

## Agent 工具鏈的自動組合

2026 年後的趨勢是「動態工具組合」。Agent 根據任務需求即時生成工具呼叫圖，而非預先寫死的順序。這需要 Agent 具備工具規劃與錯誤復原能力：

```python
tools_pipeline = [
    ("vision", screenshot),
    ("ocr", vision_result),
    ("search", ocr_result),
    ("summarize", search_result)
]
```

## 參考資源

- https://www.google.com/search?q=multimodal+function+calling+2025
- https://www.google.com/search?q=GPT-4o+vision+tool+use
- https://www.google.com/search?q=Gemini+multimodal+API+tool+integration
