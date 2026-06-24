# 多模態 Agent 導論（2024-2029）

## 從語言模型到多模態 Agent

2024 年是「多模態 Agent」元年。GPT-4V、Gemini、Claude 3 等模型開始同時處理文字、圖像與音訊，讓 AI Agent 不再只是「聊天機器人」，而是能感知世界的智慧體。多模態 Agent 的定義：一個能夠接收多種模態輸入（文字、圖片、語音、影片），透過大型多模態模型（LMM）進行推理，並輸出動作或決策的自主系統。

## 核心架構

典型的多模態 Agent 包含五層：感知層（編碼各模態輸入）、理解層（多模態 LLM 推理）、規劃層（分解任務為子步驟）、執行層（呼叫工具或 API）與記憶層（跨模態儲存與檢索）。

```
使用者輸入 → 模態編碼器 → 多模態 LLM → 規劃器 → 工具呼叫 → 執行
     ↑                                              │
     └──────────── 多模態記憶 ──────────────────────┘
```

Python 簡易實作：

```python
import openai, base64

class MultimodalAgent:
    def __init__(self, model="gpt-4o"):
        self.model = model
        self.memory = []

    def encode_image(self, image_path):
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()

    def act(self, text, image_path=None):
        msg = [{"role": "user", "content": [{"type": "text", "text": text}]}]
        if image_path:
            msg[0]["content"].append({
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{self.encode_image(image_path)}"}
            })
        resp = openai.chat.completions.create(model=self.model, messages=msg)
        return resp.choices[0].message.content
```

## 關鍵差異：多模態感知 vs 多模態生成

- **多模態感知**：模型理解圖像、語音、影片內容
- **多模態生成**：模型輸出圖像、語音、影片

2024-2025 年間的主流 Agent 以感知為主，2026 年後開始出現具備生成能力的雙向多模態 Agent。

## 發展里程碑

- 2024/03: GPT-4V 開放 API，多模態 Agent 開始普及
- 2024/12: Gemini 2.0 支援原生多模態輸出
- 2025/06: 首個開源多模態 Agent 框架 (OpenMMAgent)
- 2026/01: Agent 能同時處理 6 種以上模態輸入
- 2027: 預計端側多模態推理達到可商用水準

## 參考資源

- https://www.google.com/search?q=multimodal+agent+survey+2024
- https://www.google.com/search?q=GPT-4V+agent+system+architecture
- https://www.google.com/search?q=multimodal+foundation+models+2025
