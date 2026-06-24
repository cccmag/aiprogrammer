"""
即時推論系統 — 串流處理、低延遲推論、模型快取
"""

import time
import random
import threading
from dataclasses import dataclass, field
from collections import deque
from typing import Optional


# --- 1. 串流推論引擎 ---

@dataclass
class StreamEvent:
    id: str
    data: dict
    timestamp: float = field(default_factory=time.time)


class StreamInferenceEngine:
    """Process streaming data with sliding window inference"""

    def __init__(self, window_size: int = 5):
        self.window: deque[StreamEvent] = deque(maxlen=window_size)

    def process(self, event: StreamEvent) -> Optional[dict]:
        self.window.append(event)
        if len(self.window) >= self.window.maxlen:
            return self._infer(list(self.window))
        return None

    def _infer(self, events: list[StreamEvent]) -> dict:
        values = [e.data.get("value", 0) for e in events]
        avg = sum(values) / len(values)
        trend = "up" if values[-1] > values[0] else "down"
        return {"avg": round(avg, 2), "trend": trend, "count": len(events)}


# --- 2. 模型快取層 ---

class ModelCache:
    """LRU cache for inference results"""

    def __init__(self, capacity: int = 100):
        self.capacity = capacity
        self.cache: dict = {}
        self.order: list = []

    def get(self, key: str) -> Optional[dict]:
        if key in self.cache:
            self.order.remove(key)
            self.order.append(key)
            return self.cache[key]
        return None

    def set(self, key: str, value: dict):
        if key in self.cache:
            self.order.remove(key)
        elif len(self.cache) >= self.capacity:
            oldest = self.order.pop(0)
            del self.cache[oldest]
        self.cache[key] = value
        self.order.append(key)


# --- 3. 批次推論 ---

class BatchInference:
    """Batch multiple requests for efficient inference"""

    def __init__(self, max_batch_size: int = 8, max_wait_ms: float = 50):
        self.max_batch_size = max_batch_size
        self.max_wait_ms = max_wait_ms
        self.queue: list[dict] = []
        self.lock = threading.Lock()

    def predict(self, data: dict) -> float:
        with self.lock:
            self.queue.append(data)
            if len(self.queue) >= self.max_batch_size:
                return self._flush()
        time.sleep(self.max_wait_ms / 1000)
        with self.lock:
            if data in self.queue:
                self.queue.remove(data)
        return random.random()

    def _flush(self) -> float:
        batch = self.queue[:self.max_batch_size]
        self.queue = self.queue[self.max_batch_size:]
        results = [sum(d.values()) / len(d) for d in batch if d]
        return sum(results) / len(results) if results else 0.0


# --- 4. 模型量化模擬 ---

class QuantizedModel:
    """Simulate quantized model (FP32 -> INT8)"""

    def __init__(self, scale: float = 0.01):
        self.scale = scale

    def quantize(self, value: float) -> int:
        return int(value / self.scale)

    def dequantize(self, value: int) -> float:
        return value * self.scale

    def predict_quantized(self, features: list[float]) -> int:
        q_features = [self.quantize(f) for f in features]
        result = sum(q_features) // len(q_features)
        return result


# --- Demo ---

def demo():
    print("=== Real-Time Inference System ===\n")

    # 1. Stream Inference
    print("1. Stream Inference (sliding window):")
    engine = StreamInferenceEngine(window_size=3)
    for i in range(10):
        event = StreamEvent(f"e{i}", {"value": random.uniform(0, 100)})
        result = engine.process(event)
        if result:
            print(f"  Event {i}: avg={result['avg']}, trend={result['trend']}")

    # 2. Model Cache
    print("\n2. Model Cache (LRU):")
    cache = ModelCache(capacity=3)
    for i in range(5):
        key = f"input_{i}"
        result = {"prediction": i * 10}
        cache.set(key, result)
        print(f"  Cached: {key}")
    print(f"  Cache hit for 'input_0': {cache.get('input_0') is not None}")
    print(f"  Cache hit for 'input_3': {cache.get('input_3') is not None}")

    # 3. Quantization
    print("\n3. Quantization (FP32 -> INT8):")
    model = QuantizedModel(scale=0.1)
    features = [1.23, 4.56, 7.89]
    q_result = model.predict_quantized(features)
    dq_result = model.dequantize(q_result)
    print(f"  Original: {features}")
    print(f"  Quantized: {q_result}, Dequantized: {dq_result:.2f}")

    # 4. Latency measurement
    print("\n4. Inference Latency:")
    for _ in range(3):
        start = time.perf_counter()
        time.sleep(random.uniform(0.001, 0.005))
        elapsed = (time.perf_counter() - start) * 1000
        print(f"  Inference time: {elapsed:.2f}ms")

    print("\n=== Demo Complete ===")


if __name__ == "__main__":
    demo()
