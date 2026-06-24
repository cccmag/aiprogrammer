# 視覺-語言模型整合

## 1. 為何需要 VLM

純文字 LLM 無法理解圖像。視覺-語言模型（VLM）結合視覺編碼器與 LLM，讓 Agent 能讀取圖表、辨識物體、理解場景。

## 2. 核心架構

VLM 由三部分組成：視覺編碼器（ViT）、投影層、LLM 主幹。投影層將視覺特徵映射到 LLM 的 embedding 空間：

```python
import torch.nn as nn

class VLMConnector(nn.Module):
    def __init__(self, vdim=1024, ldim=4096, nq=64):
        super().__init__()
        self.queries = nn.Parameter(torch.randn(1, nq, vdim))
        self.attn = nn.MultiheadAttention(vdim, 8, batch_first=True)
        self.proj = nn.Linear(vdim, ldim)

    def forward(self, vfeat):
        q = self.queries.expand(vfeat.shape[0], -1, -1)
        o, _ = self.attn(q, vfeat, vfeat)
        return self.proj(o)
```

## 3. 螢幕理解

Agent 透過截圖理解 GUI，定位按鈕並執行操作：

```python
import base64
from openai import OpenAI

def describe_screen(path):
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    c = OpenAI()
    r = c.chat.completions.create(model="gpt-4o", messages=[{
        "role": "user", "content": [
            {"type": "text", "text": "描述所有可點擊元素及其位置"},
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}}
        ]}])
    return r.choices[0].message.content
```

## 4. 圖表推理

VLM 對圖表推理的應用日漸重要。Agent 可將 DataFrame 視覺化為圖表，再讓 VLM 分析趨勢、提取數據點，實現從「看圖」到「讀圖」的跨越。這對財務報表分析與科學數據解讀特別有用。

## 5. 結語

VLM 讓 Agent 從「只能讀文字」進化到「能看世界」。投影層設計與訓練數據品質是關鍵瓶頸。隨著模型體積縮小，行動端多模態 Agent 正在成為現實。

- https://www.google.com/search?q=vision+language+model+architecture
- https://www.google.com/search?q=GUI+agent+screen+understanding
