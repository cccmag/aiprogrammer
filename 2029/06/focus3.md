# 多模態互動介面（2023-2029）

## 超越文字的互動

多模態介面（Multimodal Interface）整合文字、語音、影像、手勢等多種輸入輸出通道，讓使用者以最自然的方式與 AI 溝通。

### 多模態融合架構

```python
import json

class MultimodalInput:
    def __init__(self, text: str = "", image: str = "", audio: str = "", gesture: str = ""):
        self.modalities = {
            "text": text, "image": image,
            "audio": audio, "gesture": gesture
        }

class MultimodalFusion:
    def fuse(self, inputs: MultimodalInput) -> dict:
        intent = {"action": "unknown", "confidence": 0.0, "sources": []}

        if inputs.modalities["text"]:
            intent["action"] = self._analyze_text(inputs.modalities["text"])
            intent["sources"].append("text")
            intent["confidence"] += 0.4

        if inputs.modalities["image"]:
            visual_cue = self._analyze_image(inputs.modalities["image"])
            if visual_cue:
                intent["action"] = visual_cue
                intent["sources"].append("image")
                intent["confidence"] += 0.3

        if inputs.modalities["gesture"]:
            gesture_cmd = self._decode_gesture(inputs.modalities["gesture"])
            if gesture_cmd and intent["confidence"] < 0.7:
                intent["action"] = gesture_cmd
                intent["sources"].append("gesture")
                intent["confidence"] += 0.2

        intent["confidence"] = min(intent["confidence"], 1.0)
        return intent

    def _analyze_text(self, t: str) -> str:
        return "draw_diagram" if "畫" in t else "search"

    def _analyze_image(self, img: str) -> str | None:
        return "edit_photo" if "photo" in img.lower() else None

    def _decode_gesture(self, g: str) -> str | None:
        gestures = {"swipe_left": "delete", "pinch": "zoom", "point": "select"}
        return gestures.get(g)
```

參見：[多模態互動研究](https://www.google.com/search?q=multimodal+interaction+AI+2024)

### 模態同步策略

不同模態之間的時間同步是核心挑戰：

```python
class ModalitySync:
    def __init__(self):
        self.streams: dict[str, list[tuple[float, str]]] = {}

    def add_event(self, modality: str, timestamp: float, data: str):
        if modality not in self.streams:
            self.streams[modality] = []
        self.streams[modality].append((timestamp, data))

    def temporal_fusion(self, window: float = 1.0) -> list[dict]:
        events = []
        for mod, items in self.streams.items():
            for ts, data in items:
                events.append((ts, mod, data))
        events.sort(key=lambda x: x[0])

        fused = []
        i = 0
        while i < len(events):
            group = [events[i]]
            j = i + 1
            while j < len(events) and events[j][0] - events[i][0] <= window:
                group.append(events[j])
                j += 1
            fused.append({m: d for _, m, d in group})
            i = j
        return fused
```

### 應用場景

| 模態組合 | 應用 | 範例產品 |
|----------|------|----------|
| 語音 + 手勢 | 智慧家電控制 | 智慧音箱 + 手勢辨識 |
| 文字 + 影像 | 設計協作 | AI 輔助繪圖 |
| 語音 + 文字 | 會議輔助 | 即時翻譯與摘要 |
| 視線 + 語音 | 無障礙互動 | 眼動追蹤輸入 |

### 挑戰與未來方向

- **模態衝突**：不同模態傳遞矛盾訊息時如何處理？
- **認知負擔**：多模態是否反而增加使用者負擔？
- **個人化**：不同使用者偏好的模態組合不同

參見：
- [多模態 AI 架構](https://www.google.com/search?q=multimodal+AI+architecture+2025)
- [模態衝突解決](https://www.google.com/search?q=multimodal+conflict+resolution+HCI)
- [眼動追蹤互動](https://www.google.com/search?q=eye+tracking+multimodal+interaction)

## 結語

多模態互動的目標不是用越多模態越好，而是在正確的時刻使用最適合的模態。

---

*本篇文章為「AI 程式人雜誌 2026 年 9 月號」人機協作介面設計系列之三。*
