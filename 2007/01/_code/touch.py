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