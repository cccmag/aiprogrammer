"""
AI 公平性檢測工具 — 偏見測量、群體公平性、緩解策略
"""
import math
import random
from dataclasses import dataclass, field
from typing import Optional, Callable
from collections import Counter

@dataclass
class FairnessReport:
    demographic_parity: float
    equal_opportunity: float
    disparate_impact: float
    biases: list[str]
    score: float

class BiasDetector:
    def check_gender_bias(self, texts: list[str]) -> dict:
        male_words = {"he", "him", "his", "man", "men", "boy"}
        female_words = {"she", "her", "hers", "woman", "women", "girl"}
        male_count = sum(1 for t in texts for w in t.lower().split() if w in male_words)
        female_count = sum(1 for t in texts for w in t.lower().split() if w in female_words)
        total = male_count + female_count
        return {"male_pct": male_count / total if total else 0.5, "female_pct": female_count / total if total else 0.5,
                "biased": abs(male_count - female_count) > total * 0.3}

def compute_fairness(model_fn: Callable, groups: dict[str, list]) -> FairnessReport:
    results = {}
    for group, samples in groups.items():
        outcomes = [model_fn(s) for s in samples]
        results[group] = sum(outcomes) / len(outcomes) if outcomes else 0
    pos_rates = list(results.values())
    dp = max(pos_rates) - min(pos_rates) if pos_rates else 0
    eo = abs(results.get("privileged", 0) - results.get("unprivileged", 0)) if "privileged" in results else 0
    di = min(pos_rates) / max(pos_rates) if max(pos_rates) > 0 else 1
    biases = [f"{g}: {r:.2%}" for g, r in results.items()]
    score = max(0, 1 - dp - eo / 2)
    return FairnessReport(dp, eo, di, biases, score)

def mitigate_bias(predictions: list[float], sensitive_attr: list[str]) -> list[float]:
    groups = {g: [p for p, s in zip(predictions, sensitive_attr) if s == g] for g in set(sensitive_attr)}
    means = {g: sum(v) / len(v) if v else 0 for g, v in groups.items()}
    global_mean = sum(predictions) / len(predictions) if predictions else 0
    return [p + (global_mean - means[s]) for p, s in zip(predictions, sensitive_attr)]

def demo():
    print("=== AI Fairness Detection Tool ===\n")
    detector = BiasDetector()
    texts = ["he is a doctor", "she is a nurse", "his work is great", "her contribution matters"]
    report = detector.check_gender_bias(texts)
    print(f"  Gender bias: male={report['male_pct']:.0%}, female={report['female_pct']:.0%}, biased={report['biased']}")
    model = lambda x: 1 if hash(x) % 100 > 40 else 0
    groups = {"privileged": [f"p{i}" for i in range(100)], "unprivileged": [f"u{i}" for i in range(100)]}
    fair = compute_fairness(model, groups)
    print(f"  Demographic parity: {fair.demographic_parity:.3f}")
    print(f"  Disparate impact: {fair.disparate_impact:.3f}")
    print(f"  Fairness score: {fair.score:.2f}")
    print(f"  Biases detected: {fair.biases}")
    print("\n=== Demo Complete ===")

if __name__ == "__main__":
    demo()
