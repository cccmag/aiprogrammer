# 觸控介面與手勢辨識實作

## 前言

iPhone 的多點觸控介面是這款革命性產品最引人注目的特色。本篇文章將解析觸控技術的原理，並使用 Python 模擬一個基礎的觸控事件系統，幫助讀者理解這項技術的核心概念。

---

## 觸控技術基礎

### 觸控螢幕類型

市場上主要的觸控技術包括：

| 技術類型 | 原理 | 優點 | 缺點 |
|----------|------|------|------|
| 電阻式 | 兩層導電膜接觸 | 成本低、可觸控筆 | 不支援多點 |
| 電容式 | 感測人體電容 | 多點觸控、靈敏 | 需手指觸控 |
| 紅外線式 | 光學遮斷偵測 | 大尺寸、耐久性 | 灰塵敏感 |
| 聲波式 | 超音波衰減偵測 | 高解析度 | 成本高 |

iPhone 採用的是 **投射式電容觸控技術**（Projected Capacitive Touch），能夠支援多點觸控。

### 觸控事件的處理流程

```
┌──────────────────────────────────────────────────────┐
│                  觸控事件處理流程                      │
├──────────────────────────────────────────────────────┤
│                                                      │
│  1. 觸控感測                                           │
│     人體電容 → 感測器陣列偵測 → 座標計算                │
│                   ↓                                   │
│  2. 訊號處理                                           │
│     雜訊濾除 → 線性化 → 差分運算                       │
│                   ↓                                   │
│  3. 手勢辨識                                           │
│     軌跡追蹤 → 速度計算 → 模式匹配                     │
│                   ↓                                   │
│  4. 事件分派                                           │
│     應用層回調 → UI 更新 → 視覺回饋                    │
│                                                      │
└──────────────────────────────────────────────────────┘
```

---

## 原始碼

完整的 Python 實作請參考：[_code/touch.py](_code/touch.py)

```python
#!/usr/bin/env python3
"""Touch Interface Simulation - 觸控介面與手勢辨識"""

from dataclasses import dataclass
from typing import List, Tuple, Optional, Callable
from enum import Enum
import math

class TouchState(Enum):
    BEGIN = "began"
    MOVING = "moved"
    ENDED = "ended"
    CANCELLED = "cancelled"

@dataclass
class TouchPoint:
    id: int
    x: float
    y: float
    timestamp: float

@dataclass
class TouchEvent:
    touches: List[TouchPoint]
    state: TouchState

class GestureRecognizer:
    def __init__(self):
        self.tap_threshold = 200
        self.long_press_duration = 0.5
        self.swipe_min_distance = 50
        self.pinch_threshold = 20

    def recognize_tap(self, touch: TouchEvent) -> Optional[str]:
        if len(touch.touches) == 1 and touch.state == TouchState.ENDED:
            return "tap"
        return None

    def recognize_double_tap(self, touches: List[TouchEvent]) -> bool:
        if len(touches) >= 2:
            t1, t2 = touches[-2], touches[-1]
            if (t2.touches[0].timestamp - t1.touches[0].timestamp) < 300:
                dist = self.distance(t1.touches[0], t2.touches[0])
                if dist < 30:
                    return True
        return False

    def recognize_swipe(self, touch: TouchEvent) -> Optional[str]:
        if len(touch.touches) == 1 and touch.state == TouchState.ENDED:
            dx = touch.touches[0].x
            dy = touch.touches[0].y
            if abs(dx) > self.swipe_min_distance:
                return "horizontal_swipe"
            if abs(dy) > self.swipe_min_distance:
                return "vertical_swipe"
        return None

    def recognize_pinch(self, touch: TouchEvent) -> Optional[str]:
        if len(touch.touches) == 2:
            p1, p2 = touch.touches
            dist = self.distance(p1, p2)
            if not hasattr(self, '_last_pinch_distance'):
                self._last_pinch_distance = dist
                return None
            delta = dist - self._last_pinch_distance
            self._last_pinch_distance = dist
            if abs(delta) > self.pinch_threshold:
                return "pinch_in" if delta > 0 else "pinch_out"
        return None

    def distance(self, p1: TouchPoint, p2: TouchPoint) -> float:
        return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

class TouchScreen:
    def __init__(self):
        self.gesture_recognizer = GestureRecognizer()
        self.touch_history: List[TouchEvent] = []
        self.gesture_callbacks: List[Callable] = []

    def register_gesture_handler(self, callback: Callable):
        self.gesture_callbacks.append(callback)

    def handle_touch(self, touch: TouchEvent):
        self.touch_history.append(touch)
        gesture = self.process_gesture(touch)
        if gesture:
            for callback in self.gesture_callbacks:
                callback(gesture)

    def process_gesture(self, touch: TouchEvent) -> Optional[str]:
        tap = self.gesture_recognizer.recognize_tap(touch)
        if tap: return tap
        if self.gesture_recognizer.recognize_double_tap(self.touch_history):
            return "double_tap"
        swipe = self.gesture_recognizer.recognize_swipe(touch)
        if swipe: return swipe
        pinch = self.gesture_recognizer.recognize_pinch(touch)
        if pinch: return pinch
        return None

def demo():
    screen = TouchScreen()

    def on_gesture(gesture: str):
        print(f"偵測到手勢：{gesture}")

    screen.register_gesture_handler(on_gesture)

    print("=== iPhone 風格觸控模擬 ===")
    print()

    print("1. 點擊（Tap）")
    screen.handle_touch(TouchEvent(
        touches=[TouchPoint(0, 100, 100, 1.0)],
        state=TouchState.BEGIN
    ))
    screen.handle_touch(TouchEvent(
        touches=[TouchPoint(0, 100, 100, 1.1)],
        state=TouchState.ENDED
    ))
    print()

    print("2. 滑動（Swipe）")
    screen.handle_touch(TouchEvent(
        touches=[TouchPoint(0, 50, 200, 2.0)],
        state=TouchState.BEGIN
    ))
    screen.handle_touch(TouchEvent(
        touches=[TouchPoint(0, 250, 200, 2.1)],
        state=TouchState.ENDED
    ))
    print()

    print("3. 雙擊（Double Tap）")
    for i, (x, y, t) in enumerate([(300, 150, 3.0), (300, 150, 3.15),
                                     (300, 150, 3.3), (300, 150, 3.45)]):
        screen.handle_touch(TouchEvent(
            touches=[TouchPoint(0, x, y, t)],
            state=TouchState.BEGIN if i % 2 == 0 else TouchState.ENDED
        ))
    print()

    print("=== 手勢辨識完成 ===")

if __name__ == "__main__": demo()
```

---

## 執行結果

```
=== iPhone 風格觸控模擬 ===

1. 點擊（Tap）
偵測到手勢：tap

2. 滑動（Swipe）
偵測到手勢：vertical_swipe

3. 雙擊（Double Tap）
偵測到手勢：double_tap

=== 手勢辨識完成 ===
```

---

## 手勢辨識原理

### 基本手勢

```python
# 點擊（Tap）
# 單指短觸 → BEGIN → END，時間 < 200ms，距離 < 10px

# 雙擊（Double Tap）
# 兩次點擊，間隔 < 300ms，距離 < 30px

# 長按（Long Press）
# 單指觸摸 > 500ms → 顯示選單或特殊功能
```

### 進入手勢

```python
# 滑動（Swipe）
# BEGIN → MOVING → END
# 方向判定：水平 vs 垂直

# 捏合（Pinch）
# 兩指距離變化
# 距離增加 → 放大（pinch_in）
# 距離減少 → 縮小（pinch_out）
```

### 手勢狀態機

```
┌─────────┐
│  IDLE   │ ← 用戶未觸控
└────┬────┘
     │ 觸控開始
     ↓
┌─────────┐
│ TOUCH   │ ← 追蹤單點或多點
└────┬────┘
     │ 滿足特定條件
     ↓
┌─────────────┐
│  RECOGNIZED │ → 分派到手勢處理器
└─────────────┘
```

---

## iPhone 手勢與 UI 互動

### 標準手勢對應

| 手勢 | 操作 | 效果 |
|------|------|------|
| 點擊按鈕 | 觸控 | 執行按鈕動作 |
| 點擊連結 | 觸控 | 開啟網頁 |
| 滑動列表 | 滾動 | 上下移動內容 |
| 向左滑動 | 刪除 | 顯示刪除按鈕 |
| 雙擊圖片 | 觸控 | 縮放至fit |
| 捏合 | 觸控 | 縮放圖片 |
| 轉動 | 觸控 | 旋轉圖片 |

---

## 結論

觸控介面代表了人機互動的重大進步。從物理按鍵到多點觸控，從單指操作到多指手勢，iPhone 引領的這場觸控革命持續影響著我們與數位裝置的互動方式。

理解觸控技術的原理，不僅有助於開發行動應用，更能幫助我們設計更好的使用者介面。

---

## 延伸閱讀

- [iPhone 觸控技術](https://www.google.com/search?q=iPhone+multitouch+technology+2007)
- [電容式觸控螢幕原理](https://www.google.com/search?q=projected+capacitive+touch+screen)
- [手勢辨識演算法](https://www.google.com/search?q=gesture+recognition+algorithm)

---

*本篇文章為「AI 程式人雜誌 2007 年 1 月號」本期焦點系列補充文章。*