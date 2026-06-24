# 多模態 Agent 架構設計

## 1. 為什麼需要多模態架構

人類透過視覺、聽覺、觸覺等多種感官理解世界。多模態 Agent 的目標也是如此——整合文字、圖像、語音、影片等不同類型的輸入，做出比單模態更準確的決策。架構設計決定了這些模態如何被融合與推理。

## 2. 三種主流架構

多模態 Agent 的核心挑戰在於整合視覺、語音、文字等異質模態。主流架構分為三類。

**早期融合**在輸入層拼接各模態特徵，交互充分但計算量大。**晚期融合**各模態獨立編碼後合併，效率高但跨模態資訊流失。

```python
import torch.nn as nn

class LateFusionAgent(nn.Module):
    def __init__(self, text_dim=768, vision_dim=512, hidden=256):
        super().__init__()
        self.te = nn.Linear(text_dim, hidden)
        self.ve = nn.Linear(vision_dim, hidden)
        self.fuse = nn.Linear(hidden*2, hidden)

    def forward(self, t, v):
        return self.fuse(torch.cat([t.relu(), v.relu()], dim=-1))
```

**以 LLM 為核心**的架構讓 LLM 作為中央控制器，各模態編碼器將輸入轉為 token 序列。**工具導向架構**將多模態能力封裝為工具，透過 ReAct 循環動態選擇。

```python
class ToolAgent:
    def __init__(self, llm):
        self.llm = llm
        self.tools = {"ocr": self.ocr, "tts": self.tts}

    def act(self, inp):
        resp = self.llm.chat(messages=[{"role":"user","content":inp}], tools=list(self.tools.keys()))
        if resp.get("tool_call"):
            return self.tools[resp["tool_call"]["name"]](**resp["tool_call"]["arguments"])
        return resp["content"]
```

## 2. 設計取捨

晚期融合的延遲最低，適合即時互動場景。LLM 為核心的架構推理能力最強，適合複雜決策任務。工具導向架構的擴展性最佳，適合需要動態整合外部 API 的應用。實務上大型系統常混合多種架構，在關鍵路徑使用晚期融合保證效能，在決策層使用 LLM 保證品質。

## 3. 結語

三種架構並非互斥，而是可以分層共存的。設計的關鍵在於釐清系統的延遲要求、推理深度和擴展需求，然後選擇合適的混合方案。

- https://www.google.com/search?q=multimodal+agent+architecture+survey
- https://www.google.com/search?q=early+fusion+vs+late+fusion+multimodal
