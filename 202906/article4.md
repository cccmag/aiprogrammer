# 多模態輸入處理

## 前言

多模態輸入讓使用者能透過語音、文字、手勢、視線等多種管道與 AI 互動。本文探討多模態輸入的同步、融合與衝突解決策略。

## 輸入通道抽象

```python
from abc import ABC, abstractmethod

class InputChannel(ABC):
    @abstractmethod
    def read(self) -> dict:
        pass

    @abstractmethod
    def confidence(self) -> float:
        pass

class TextInput(InputChannel):
    def __init__(self):
        self.modality = "text"

    def read(self):
        return {"type": "text", "content": input("請輸入文字：")}

    def confidence(self):
        return 0.95

class VoiceInput(InputChannel):
    def __init__(self):
        self.modality = "voice"

    def read(self):
        import random
        # 模擬語音辨識
        texts = ["開啟檔案", "儲存文件", "關閉視窗"]
        return {"type": "voice", "content": random.choice(texts)}

    def confidence(self):
        import random
        return random.uniform(0.6, 0.95)

class GestureInput(InputChannel):
    def __init__(self):
        self.modality = "gesture"

    def read(self):
        import random
        gestures = ["swipe_left", "swipe_right", "tap", "pinch"]
        return {"type": "gesture", "content": random.choice(gestures)}

    def confidence(self):
        import random
        return random.uniform(0.7, 0.98)
```

## 多模態融合器

```python
class MultimodalFusion:
    def __init__(self):
        self.channels = []

    def add_channel(self, channel):
        self.channels.append(channel)

    def fuse(self, timeout=5):
        import time
        results = []
        start = time.time()
        while time.time() - start < timeout:
            for ch in self.channels:
                if ch.confidence() > 0.7:
                    data = ch.read()
                    results.append(data)
            if results:
                break
            time.sleep(0.5)
        return self.resolve_conflicts(results)

    def resolve_conflicts(self, results):
        if len(results) <= 1:
            return results
        text_results = [r for r in results if r["type"] == "text"]
        if text_results:
            return text_results
        # 依信心度排序
        results.sort(key=lambda r: r.get("confidence", 0), reverse=True)
        return [results[0]]

    def interpret_gesture(self, gesture):
        mapping = {
            "swipe_left": "undo",
            "swipe_right": "redo",
            "tap": "select",
            "pinch": "zoom",
        }
        return mapping.get(gesture, "unknown")

fusion = MultimodalFusion()
fusion.add_channel(VoiceInput())
fusion.add_channel(GestureInput())
result = fusion.fuse(timeout=2)
print("融合結果:", result)
```

## 語音轉文字輔助

```python
class SpeechAssistant:
    def __init__(self):
        self.commands = {
            "開啟": "open",
            "儲存": "save",
            "關閉": "close",
            "刪除": "delete",
        }

    def process_voice(self, voice_text):
        for zh, en in self.commands.items():
            if zh in voice_text:
                return en
        return "unknown_command"

    def multimodal_fallback(self, text, gesture):
        # 文字與手勢互補
        command = self.process_voice(text)
        if command == "unknown_command" and gesture:
            gesture_cmd = {
                "swipe_left": "navigate_back",
                "swipe_right": "navigate_forward",
            }
            return gesture_cmd.get(gesture, "unknown")
        return command

    def execute(self, text, gesture=None):
        cmd = self.multimodal_fallback(text, gesture)
        print(f"執行指令：{cmd}")

assistant = SpeechAssistant()
assistant.execute("開啟檔案")
assistant.execute("我不確定", "swipe_left")
```

---

**延伸閱讀**

- [Multimodal Interaction Design](https://www.google.com/search?q=multimodal+interaction+design+patterns)
- [Sensor Fusion Techniques](https://www.google.com/search?q=sensor+fusion+multimodal+input)
- [Voice and Gesture Integration](https://www.google.com/search?q=voice+gesture+multimodal+integration)
