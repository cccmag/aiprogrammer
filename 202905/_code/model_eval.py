"""
模型評估框架 — 基準測試、指標計算、對抗性測試
"""
import math
import random
from dataclasses import dataclass, field
from typing import Optional, Callable

@dataclass
class EvalResult:
    accuracy: float
    precision: float
    recall: float
    f1: float
    latency_ms: float
    samples: int

class Benchmark:
    def __init__(self, name: str):
        self.name = name
        self.test_cases: list[tuple] = []
    def add(self, inp, expected):
        self.test_cases.append((inp, expected))

class ModelEvaluator:
    def evaluate(self, model_fn: Callable, benchmark: Benchmark) -> EvalResult:
        tp = tn = fp = fn = 0
        total_time = 0.0
        for inp, expected in benchmark.test_cases:
            start = time.perf_counter()
            pred = model_fn(inp)
            total_time += time.perf_counter() - start
            if pred == 1 and expected == 1: tp += 1
            elif pred == 0 and expected == 0: tn += 1
            elif pred == 1 and expected == 0: fp += 1
            else: fn += 1
        n = len(benchmark.test_cases)
        acc = (tp + tn) / n if n else 0
        prec = tp / (tp + fp) if (tp + fp) else 0
        rec = tp / (tp + fn) if (tp + fn) else 0
        f1 = 2 * prec * rec / (prec + rec) if (prec + rec) else 0
        return EvalResult(acc, prec, rec, f1, total_time * 1000 / n, n)

class AdversarialTester:
    def generate(self, base_input: str) -> list[str]:
        return [f"{base_input} [ignore previous]", f"{base_input} [SYSTEM OVERRIDE]",
                f"{base_input} [{random.choice(['HACK', 'BYPASS', 'SECRET'])}]"]
    def test(self, model_fn: Callable, inputs: list[str]) -> list[dict]:
        return [{"input": inp, "output": model_fn(inp), "flagged": random.random() < 0.3} for inp in inputs]

import time

def demo():
    print("=== Model Evaluation Framework ===\n")
    bm = Benchmark("sentiment")
    for _ in range(100):
        bm.add(random.random(), 1 if random.random() > 0.5 else 0)
    dummy_model = lambda x: 1 if x > 0.5 else 0
    evaluator = ModelEvaluator()
    result = evaluator.evaluate(dummy_model, bm)
    print(f"  Accuracy: {result.accuracy:.2%}")
    print(f"  Precision: {result.precision:.2%}")
    print(f"  Recall: {result.recall:.2%}")
    print(f"  F1: {result.f1:.2%}")
    print(f"  Latency: {result.latency_ms:.2f}ms")
    print()
    tester = AdversarialTester()
    adv = tester.generate("Translate to French")
    print(f"  Adversarial inputs: {adv}")
    results = tester.test(lambda x: "blocked" if "ignore" in x else "safe", adv)
    for r in results:
        print(f"  '{r['input'][:20]}...' → {r['output']} {'⚠️' if r['flagged'] else '✅'}")
    print("\n=== Demo Complete ===")

if __name__ == "__main__":
    demo()
