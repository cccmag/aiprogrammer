# 多模態 Agent（2024-2026）

## 從對話到行動

LLM 最初只是對話系統。真正的價值來自**行動**：操作電腦、使用工具、感知環境。多模態 Agent 能**看**、**聽**、**讀**、**說**、**做**。

## 標準架構

```
                    ┌──────────────────┐
                    │   User Input     │
                    │ (文字/語音/圖片) │
                    └────────┬─────────┘
                             ↓
                    ┌──────────────────┐
                    │   Perception     │
                    │ (VLM + ASR + OCR)│
                    └────────┬─────────┘
                             ↓
                    ┌──────────────────┐
                    │   Planner (LLM)  │
                    │ 思考 → 規劃步驟  │
                    └────────┬─────────┘
                             ↓
                    ┌──────────────────┐
                    │   Action Space   │
                    ├──────────────────┤
                    │ • 滑鼠/鍵盤操作  │
                    │ • API 呼叫       │
                    │ • 程式碼執行     │
                    │ • 檔案操作       │
                    │ • 語音輸出       │
                    └──────────────────┘
```

## Agent 核心循環：感知→規劃→行動

```python
def agent_loop(task, screenshot, audio=None):
    """感知→規劃→行動→觀察，遞迴直到完成"""
    state = {"screen": vlm_caption(screenshot)}
    if audio:
        state["transcript"] = whisper(audio)
    plan = llm(f"Task: {task}\nState: {state}\nAction?")
    if "click" in plan:    mouse_click(*parse_coords(plan))
    elif "type" in plan:   keyboard_type(extract_text(plan))
    elif "scroll" in plan: mouse_scroll()
    return agent_loop(task, capture_screen())
```

## 記憶與工具

```python
class MultimodalAgent:
    def __init__(self):
        self.memory, self.tools = [], {}
    def run(self, request):
        ctx = self.memory[-5:]
        plan = llm(request, capture_screen(), ctx, list(self.tools))
        for s in plan:
            self.memory.append(self.tools[s["tool"]](**s["args"]))
        return self._output(plan)
```

## 挑戰

| 挑戰 | 說明 |
|------|------|
| 可靠性 | 一步錯誤可能導致任務失敗 |
| 延遲 | 多模型串聯，回應長 |
| 安全性 | 操作權限控制 |
| 評估 | 開放式任務難以自動評測 |

| 年份 | 發展 |
|------|------|
| 2024 | 螢幕 Agent 原型（Apple Intelligence、Copilot） |
| 2025 | 多步驟自動化、API 整合 Agent |
| 2026 | 跨應用 Agent、自主學習 |

## 小結

多模態 Agent 代表 AI 從「被動回應」到「主動行動」的轉變。整合視覺、語音、文字與行動，讓 AI 在真實世界中執行任務。雖有可靠性、延遲、安全性挑戰，但這是 AI 應用的最終形態——能看、能聽、能說、能做的數字助手。

---

**回目錄**：[本期焦點](focus.md) | **程式實作**：[focus_code.md](focus_code.md)

## 延伸閱讀

- [Apple Intelligence 架構](https://www.google.com/search?q=Apple+Intelligence+on+device+AI+architecture)
- [Copilot Vision](https://www.google.com/search?q=Microsoft+Copilot+Vision+screen+understanding)
- [Agentic AI 設計模式](https://www.google.com/search?q=agentic+AI+design+patterns+autonomous+agents)
