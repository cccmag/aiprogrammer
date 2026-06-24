"""
模型推論最佳化工具 — 量化、剪枝、蒸餾、KV Cache
"""

import math
import random
from dataclasses import dataclass, field
from typing import Optional


# --- 1. 模型量化 (FP32 -> INT8) ---

def quantize_weights(weights: list[float], bits: int = 8) -> tuple[list[int], float, float]:
    """Quantize floating-point weights to integer"""
    min_w = min(weights)
    max_w = max(weights)
    scale = (max_w - min_w) / (2**bits - 1) if max_w != min_w else 1.0
    zero_point = -min_w / scale if scale != 0 else 0.0
    q_weights = [int((w - min_w) / scale) if scale != 0 else 0 for w in weights]
    q_weights = [max(0, min(2**bits - 1, w)) for w in q_weights]
    return q_weights, scale, min_w


def dequantize_weights(q_weights: list[int], scale: float, min_w: float) -> list[float]:
    return [w * scale + min_w for w in q_weights]


def quantization_error(original: list[float], quantized: list[float]) -> float:
    return math.sqrt(sum((a - b)**2 for a, b in zip(original, quantized))) / len(original)


# --- 2. 模型剪枝 ---

def magnitude_prune(weights: list[float], threshold: float = 0.1) -> list[float]:
    """Prune weights below threshold"""
    max_abs = max(abs(w) for w in weights) if weights else 1.0
    return [w if abs(w) / max_abs >= threshold else 0.0 for w in weights]


def sparsity(weights: list[float]) -> float:
    return sum(1 for w in weights if w == 0.0) / len(weights) if weights else 0.0


# --- 3. 知識蒸餾模擬 ---

class TeacherModel:
    """Large teacher model (simulated)"""

    def predict(self, x: list[float]) -> list[float]:
        return [math.sin(v) + random.gauss(0, 0.01) for v in x]


class StudentModel:
    """Small student model"""

    def __init__(self, params: Optional[list[float]] = None):
        self.params = params or [random.gauss(0, 0.1) for _ in range(4)]

    def predict(self, x: list[float]) -> list[float]:
        return [(p + sum(x) / len(x)) / 2 for p in self.params[:len(x)]]

    def distill(self, teacher: TeacherModel, data: list[list[float]], epochs: int = 10):
        for epoch in range(epochs):
            total_loss = 0.0
            for x in data:
                teacher_out = teacher.predict(x)
                student_out = self.predict(x)
                loss = sum((t - s)**2 for t, s in zip(teacher_out, student_out))
                total_loss += loss
                # Simple gradient step
                for i in range(min(len(self.params), len(x))):
                    self.params[i] -= 0.01 * 2 * (self.params[i] - teacher_out[i]) / len(teacher_out)


# --- 4. KV Cache 模擬 ---

class KVCache:
    """Simple KV cache for transformer inference"""

    def __init__(self):
        self.cache: dict[int, tuple[list[float], list[float]]] = {}

    def store(self, position: int, key: list[float], value: list[float]):
        self.cache[position] = (key, value)

    def retrieve(self) -> tuple[list[list[float]], list[list[float]]]:
        keys = [k for k, _ in sorted(self.cache.items())]
        return (
            [self.cache[k][0] for k in keys],
            [self.cache[v][1] for v in keys]
        )

    def size(self) -> int:
        return sum(len(k) + len(v) for k, v in self.cache.values())


# --- Demo ---

def demo():
    print("=== Inference Optimization Toolkit ===\n")

    # 1. Quantization
    print("1. Weight Quantization (FP32->INT8):")
    original = [random.gauss(0, 1) for _ in range(100)]
    q_weights, scale, min_w = quantize_weights(original, bits=8)
    deq_weights = dequantize_weights(q_weights, scale, min_w)
    error = quantization_error(original, deq_weights)
    print(f"  Original: {len(original)} FP32 = {len(original)*4} bytes")
    print(f"  Quantized: {len(q_weights)} INT8 = {len(q_weights)} bytes")
    print(f"  Compression: 4x, Error: {error:.6f}")

    # 2. Pruning
    print("\n2. Magnitude Pruning:")
    weights = [random.gauss(0, 1) for _ in range(50)]
    pruned = magnitude_prune(weights, threshold=0.2)
    print(f"  Original density: 100%")
    print(f"  After pruning: {sparsity(pruned)*100:.0f}% zero")

    # 3. Knowledge Distillation
    print("\n3. Knowledge Distillation:")
    teacher = TeacherModel()
    student = StudentModel()
    data = [[random.gauss(0, 1) for _ in range(4)] for _ in range(50)]
    x_test = [random.gauss(0, 1) for _ in range(4)]
    before = sum((t - s)**2 for t, s in zip(teacher.predict(x_test), student.predict(x_test)))
    student.distill(teacher, data, epochs=20)
    after = sum((t - s)**2 for t, s in zip(teacher.predict(x_test), student.predict(x_test)))
    print(f"  Teacher-student loss before: {before:.4f}")
    print(f"  Teacher-student loss after:  {after:.4f}")

    # 4. KV Cache
    print("\n4. KV Cache:")
    cache = KVCache()
    for pos in range(5):
        cache.store(pos, [random.random() for _ in range(64)],
                    [random.random() for _ in range(64)])
    keys, values = cache.retrieve()
    print(f"  Stored: {cache.size()} floats")
    print(f"  Cached positions: {len(keys)}")

    print("\n=== Demo Complete ===")


if __name__ == "__main__":
    demo()
