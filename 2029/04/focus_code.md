# 程式實作：多模態 Agent 框架

## 簡介

本實作建構一個多模態 Agent 框架，支援文字、影像（標題）與語音（轉錄）三種模態的感知、推理與行動。完整程式碼在 `_code/mm_agent.py`。

## 核心元件

### 1. 多模態輸入

```python
@dataclass
class MultiModalInput:
    text: Optional[str] = None
    image_caption: Optional[str] = None
    audio_transcript: Optional[str] = None
```

### 2. 感知與推理

```python
agent = MultiModalAgent("VisionBot")
perception = agent.perceive(inp)
# 輸出: "Perceived: text(...), image(...), audio(...)"
action = agent.reason(perception)
# 返回 AgentAction(tool, params, reasoning)
```

### 3. 工具執行

```python
result = agent.execute(action)
# tools: search / respond
```

## 執行方式

```bash
cd _code
python3 mm_agent.py
```

## 延伸練習

1. **真實視覺模型**：用 CLIP 或 GPT-4V 替換模擬影像理解
2. **語音處理**：整合 Whisper 進行真實語音轉錄
3. **長期記憶**：用向量資料庫儲存多模態經驗
4. **多 Agent 協作**：讓視覺 Agent 與語音 Agent 協作完成任務
5. **螢幕 Agent**：實作螢幕截圖分析與 GUI 操作 Agent
