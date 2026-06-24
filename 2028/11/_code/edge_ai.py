"""
邊緣 AI 推論引擎 — TinyML, TFLite 模擬, ONNX Runtime, 邊緣-雲端協同
"""

import math
import random
import time
from dataclasses import dataclass, field
from typing import Optional


# --- 1. TinyML 模型 (微型神經網路) ---

class TinyMLModel:
    """Minimal neural network for MCU inference"""

    def __init__(self):
        self.weights = [random.uniform(-0.5, 0.5) for _ in range(4)]
        self.bias = random.uniform(-0.5, 0.5)

    def predict(self, x: list[float]) -> float:
        result = self.bias
        for w, xi in zip(self.weights, x):
            result += w * xi
        # Quantize to simulate 8-bit MCU
        result = max(-128, min(127, int(result * 100)))
        return result / 100

    def model_size(self) -> int:
        """Estimate model size in bytes (INT8 quantized)"""
        return len(self.weights) + 1  # weights + bias


# --- 2. TFLite 模擬 ---

class SimulatedTFLite:
    """Simulate TFLite delegate inference"""

    def __init__(self, model_path: str = "model.tflite"):
        self.model_path = model_path
        self.delegates = {
            "cpu": lambda: time.sleep(0.005),
            "gpu": lambda: time.sleep(0.002),
            "npu": lambda: time.sleep(0.001),
            "hexagon": lambda: time.sleep(0.0015),
        }

    def infer(self, input_data: list[float],
              delegate: str = "cpu") -> list[float]:
        if delegate in self.delegates:
            self.delegates[delegate]()  # Simulated latency
        return [v * random.uniform(0.9, 1.1) for v in input_data]


# --- 3. ONNX Runtime 模擬 ---

class SimulatedONNX:
    """Simulate ONNX Runtime inference"""

    def __init__(self):
        self.optimization_levels = {
            "none": 1.0,
            "basic": 0.8,
            "extended": 0.6,
            "all": 0.4,
        }

    def optimize(self, model_ops: list[str], level: str = "basic"):
        factor = self.optimization_levels.get(level, 1.0)
        return f"Optimized {len(model_ops)} ops at {level} level ({factor}x speedup)"

    def infer(self, input_data: list[float], opt_level: str = "basic") -> list[float]:
        time.sleep(0.003 * self.optimization_levels.get(opt_level, 1.0))
        return [v * random.uniform(0.95, 1.05) for v in input_data]


# --- 4. 邊緣-雲端協同 ---

@dataclass
class EdgeCloudResult:
    edge_result: Optional[float]
    cloud_result: Optional[float]
    edge_latency: float
    cloud_latency: float
    edge_confidence: float
    used_edge: bool


class EdgeCloudOrchestrator:
    """Route requests to edge or cloud based on confidence"""

    def __init__(self, confidence_threshold: float = 0.8):
        self.threshold = confidence_threshold
        self.edge_model = TinyMLModel()
        self.edge_latency_ms = 5
        self.cloud_latency_ms = 200

    def infer(self, x: list[float]) -> EdgeCloudResult:
        # Edge inference
        edge_start = time.perf_counter()
        edge_result = self.edge_model.predict(x)
        edge_elapsed = (time.perf_counter() - edge_start) * 1000

        # Simulate confidence
        edge_confidence = min(1.0, max(0.0, 0.7 + random.gauss(0, 0.1)))

        cloud_result = None
        cloud_elapsed = 0

        if edge_confidence < self.threshold:
            # Fall back to cloud
            cloud_start = time.perf_counter()
            time.sleep(self.cloud_latency_ms / 1000)
            cloud_result = sum(x) / len(x) if x else 0
            cloud_elapsed = (time.perf_counter() - cloud_start) * 1000

        return EdgeCloudResult(
            edge_result=edge_result if edge_confidence >= self.threshold else None,
            cloud_result=cloud_result,
            edge_latency=edge_elapsed,
            cloud_latency=cloud_elapsed,
            edge_confidence=edge_confidence,
            used_edge=edge_confidence >= self.threshold
        )


# --- Demo ---

def demo():
    print("=== Edge AI Inference Engine ===\n")

    # 1. TinyML Model
    print("1. TinyML on Microcontroller:")
    tiny = TinyMLModel()
    x = [0.5, -0.3, 0.8, 0.1]
    result = tiny.predict(x)
    print(f"  Input: {x}")
    print(f"  Output: {result:.3f}")
    print(f"  Model size: {tiny.model_size()} bytes")
    print()

    # 2. Delegate Comparison
    print("2. TFLite Delegate Comparison:")
    tflite = SimulatedTFLite()
    for delegate in ["cpu", "gpu", "npu"]:
        start = time.perf_counter()
        result = tflite.infer(x, delegate=delegate)
        elapsed = (time.perf_counter() - start) * 1000
        print(f"  {delegate}: {elapsed:.2f}ms")
    print()

    # 3. ONNX Optimization
    print("3. ONNX Runtime Optimization:")
    onnx = SimulatedONNX()
    ops = ["Conv", "Relu", "Pool", "FC", "Softmax"]
    for level in ["none", "basic", "all"]:
        print(f"  {onnx.optimize(ops, level)}")
    print()

    # 4. Edge-Cloud Orchestration
    print("4. Edge-Cloud Orchestration:")
    orchestrator = EdgeCloudOrchestrator(confidence_threshold=0.75)
    for i in range(5):
        x = [random.uniform(-1, 1) for _ in range(4)]
        result = orchestrator.infer(x)
        location = "EDGE" if result.used_edge else "CLOUD"
        conf = result.edge_confidence
        print(f"  Sample {i+1}: {location} (confidence={conf:.2f}, "
              f"edge={result.edge_latency:.1f}ms, cloud={result.cloud_latency:.1f}ms)")

    print("\n=== Demo Complete ===")


if __name__ == "__main__":
    demo()
