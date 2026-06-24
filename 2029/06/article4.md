# 多模態輸入處理

## 前言

人機協作不應僅限於鍵盤與滑鼠。多模態輸入（Multimodal Input）整合語音、手勢、視線、觸控等多種通道，讓使用者以最自然的方式與 AI 溝通。本文探討如何設計與實作多模態融合系統。

## 多模態融合架構

### 通道抽象層

統一的輸入抽象層是整合多種模態的基礎：

```python
import enum
import time
from typing import Any, Dict, List
from dataclasses import dataclass

class Modality(enum.Enum):
    TEXT = "text"
    SPEECH = "speech"
    GESTURE = "gesture"
    GAZE = "gaze"
    TOUCH = "touch"

@dataclass
class ModalityInput:
    modality: Modality
    content: Any
    confidence: float
    timestamp: float
    metadata: Dict = None

class MultimodalFusion:
    def __init__(self):
        self.input_queue: List[ModalityInput] = []
        self.fusion_window = 0.5

    def add_input(self, inp: ModalityInput):
        self.input_queue.append(inp)
        self.input_queue.sort(key=lambda x: x.timestamp)

    def fuse(self) -> Dict[Modality, Any]:
        now = time.time()
        recent = [
            inp for inp in self.input_queue
            if now - inp.timestamp <= self.fusion_window
        ]
        result = {}
        for inp in recent:
            if inp.confidence > 0.6:
                result[inp.modality] = inp.content
        return result
```

## 語音輸入處理

### 語音轉文字與意圖

語音是最高效的輸入通道之一，但需要處理雜訊和口音：

```python
class SpeechProcessor:
    def __init__(self):
        self.vocab = {"新增", "刪除", "修改", "查詢", "顯示"}

    def transcribe(self, audio_signal: str) -> str:
        return audio_signal.lower()

    def extract_command(self, text: str) -> tuple:
        words = set(text.split())
        verbs = words & self.vocab
        if verbs:
            verb = list(verbs)[0]
            rest = text.replace(verb, "").strip()
            return verb, rest
        return None, text

    def confidence_score(self, audio_quality: float) -> float:
        return min(1.0, max(0.0, audio_quality))

sp = SpeechProcessor()
text = sp.transcribe("新增一個備忘錄")
cmd, args = sp.extract_command(text)
print(f"指令={cmd}, 參數={args}")
```

## 手勢與視線融合

### 多通道互補

當一個模態不可靠時，另一個模態可以補充：

```python
class GestureGazeFusion:
    def __init__(self):
        self.gestures = {"point": "select", "swipe_left": "next", "swipe_right": "prev"}
        self.gaze_targets = {}

    def process_gesture(self, gesture: str) -> str:
        return self.gestures.get(gesture, "unknown")

    def process_gaze(self, gaze_coords: tuple, screen_elements: Dict) -> str:
        x, y = gaze_coords
        for elem_id, bounds in screen_elements.items():
            if bounds["x"] <= x <= bounds["x"] + bounds["w"]:
                if bounds["y"] <= y <= bounds["y"] + bounds["h"]:
                    return elem_id
        return None

    def fuse(self, gesture: str, gaze: tuple, elements: Dict) -> str:
        action = self.process_gesture(gesture)
        target = self.process_gaze(gaze, elements)
        if action and target:
            return f"對 {target} 執行 {action}"
        return None

fg = GestureGazeFusion()
elems = {"button_save": {"x": 10, "y": 20, "w": 80, "h": 30}}
print(fg.fuse("swipe_left", (50, 35), elems))
```

## 觸控與語音協作

### 補充式多模態

觸控選取範圍 + 語音指定動作：

```python
class TouchSpeechCoordination:
    def __init__(self):
        self.selected_region = None
        self.voice_command = None

    def touch_select(self, region: tuple):
        self.selected_region = region
        return f"已選取區域 {region}"

    def speech_command(self, command: str):
        self.voice_command = command
        return f"語音指令：{command}"

    def execute_combined(self) -> str:
        if self.selected_region and self.voice_command:
            result = f"在區域 {self.selected_region} 執行 {self.voice_command}"
            self.selected_region = None
            self.voice_command = None
            return result
        return "缺少選擇區域或語音指令"
```

## 時間同步機制

### 時間戳對齊

不同模態的輸入速度不同，需要時間同步視窗：

```python
class TemporalAlignment:
    def __init__(self, window_ms: int = 300):
        self.window_ms = window_ms
        self.events = []

    def add_event(self, modality: str, timestamp_ms: int, data: Any):
        self.events.append((modality, timestamp_ms, data))

    def align(self) -> List[List]:
        self.events.sort(key=lambda x: x[1])
        groups = []
        current = [self.events[0]]
        for i in range(1, len(self.events)):
            if self.events[i][1] - current[-1][1] <= self.window_ms:
                current.append(self.events[i])
            else:
                groups.append(current)
                current = [self.events[i]]
        if current:
            groups.append(current)
        return groups
```

## 結語

多模態輸入的關鍵不在於單一通道的精準度，而在於**多通道的互補與融合**。當語音吵雜時用手勢，當手勢模糊時用視線，當所有通道都不可靠時退回文字——這就是真正的多模態設計哲學。

---

**延伸閱讀**

- [多模態人機互動研究](https://www.google.com/search?q=multimodal+human+computer+interaction+2026)
- [語音與手勢融合演算法](https://www.google.com/search?q=speech+gesture+fusion+algorithm)
- [視線追蹤互動設計](https://www.google.com/search?q=gaze+tracking+interaction+design)
