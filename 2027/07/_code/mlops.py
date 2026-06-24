"""
Mini MLOps Platform — model monitoring, drift detection, prompt management, A/B testing
"""

import json
import math
import random
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional

# ---------------------------------------------------------------------------
# 1. Prompt Version Management
# ---------------------------------------------------------------------------

@dataclass
class PromptTemplate:
    name: str
    version: str
    template: str
    params: list[str]
    created_at: str = ""

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()

    def render(self, **kwargs) -> str:
        return self.template.format(**kwargs)


class PromptRegistry:
    """Version-controlled prompt registry"""

    def __init__(self):
        self.prompts: dict[str, list[PromptTemplate]] = {}

    def register(self, prompt: PromptTemplate):
        if prompt.name not in self.prompts:
            self.prompts[prompt.name] = []
        self.prompts[prompt.name].append(prompt)

    def get_latest(self, name: str) -> Optional[PromptTemplate]:
        versions = self.prompts.get(name, [])
        return versions[-1] if versions else None

    def get_version(self, name: str, version: str) -> Optional[PromptTemplate]:
        for p in self.prompts.get(name, []):
            if p.version == version:
                return p
        return None

    def list_versions(self, name: str) -> list[str]:
        return [p.version for p in self.prompts.get(name, [])]

    def rollback(self, name: str, version: str) -> Optional[PromptTemplate]:
        """Rollback to a specific version (creates a new version pointing to old template)"""
        old = self.get_version(name, version)
        if old is None:
            return None
        new_version = f"{version}-rollback-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        rollback = PromptTemplate(name, new_version, old.template, old.params)
        self.register(rollback)
        return rollback


# ---------------------------------------------------------------------------
# 2. A/B Testing
# ---------------------------------------------------------------------------

@dataclass
class ABTest:
    name: str
    variants: dict[str, str]  # variant_name -> prompt_version
    traffic_split: dict[str, float]  # variant_name -> proportion
    metrics: dict[str, list[float]] = field(default_factory=dict)

    def __post_init__(self):
        for v in self.variants:
            if v not in self.metrics:
                self.metrics[v] = []

    def select_variant(self) -> str:
        r = random.random()
        cumulative = 0.0
        for variant, split in self.traffic_split.items():
            cumulative += split
            if r < cumulative:
                return variant
        return list(self.variants.keys())[-1]

    def record_metric(self, variant: str, value: float):
        if variant in self.metrics:
            self.metrics[variant].append(value)

    def report(self) -> dict:
        result = {}
        for variant, values in self.metrics.items():
            if values:
                result[variant] = {
                    "count": len(values),
                    "mean": sum(values) / len(values),
                    "min": min(values),
                    "max": max(values),
                }
            else:
                result[variant] = {"count": 0, "mean": 0, "min": 0, "max": 0}

        # Statistical significance (simplified t-test equivalent)
        variants_list = list(result.keys())
        if len(variants_list) == 2 and all(result[v]["count"] > 1 for v in variants_list):
            a = self.metrics[variants_list[0]]
            b = self.metrics[variants_list[1]]
            from statistics import mean, stdev
            if len(a) > 1 and len(b) > 1:
                try:
                    n1, n2 = len(a), len(b)
                    s1, s2 = stdev(a), stdev(b)
                    se = math.sqrt(s1**2/n1 + s2**2/n2)
                    t_stat = (mean(a) - mean(b)) / se if se > 0 else 0
                    result["t_statistic"] = round(t_stat, 4)
                    result["significant"] = abs(t_stat) > 1.96  # 95% confidence
                except:
                    pass

        return result


# ---------------------------------------------------------------------------
# 3. Drift Detection
# ---------------------------------------------------------------------------

def psi_score(reference: list[float], current: list[float], bins: int = 10) -> float:
    """Population Stability Index — measures distribution shift"""
    if not reference or not current:
        return 0.0
    combined = reference + current
    min_val, max_val = min(combined), max(combined)
    if max_val == min_val:
        return 0.0
    bin_width = (max_val - min_val) / bins
    ref_counts = [0] * bins
    cur_counts = [0] * bins
    for v in reference:
        idx = min(bins - 1, int((v - min_val) / bin_width))
        ref_counts[idx] += 1
    for v in current:
        idx = min(bins - 1, int((v - min_val) / bin_width))
        cur_counts[idx] += 1
    psi = 0.0
    for i in range(bins):
        p_i = (ref_counts[i] + 1) / (len(reference) + bins)  # Laplace smoothing
        q_i = (cur_counts[i] + 1) / (len(current) + bins)
        psi += (p_i - q_i) * math.log(p_i / q_i)
    return psi


@dataclass
class DriftMonitor:
    """Monitor model predictions for drift"""
    feature_name: str
    reference_distribution: list[float] = field(default_factory=list)
    threshold: float = 0.2
    alerts: list[dict] = field(default_factory=list)

    def add_reference(self, values: list[float]):
        self.reference_distribution.extend(values)

    def check_drift(self, current_values: list[float]) -> dict:
        psi = psi_score(self.reference_distribution, current_values)
        drifted = psi > self.threshold
        result = {
            "feature": self.feature_name,
            "psi": round(psi, 4),
            "threshold": self.threshold,
            "drifted": drifted,
            "timestamp": datetime.now().isoformat(),
        }
        if drifted:
            self.alerts.append(result)
        return result


# ---------------------------------------------------------------------------
# 4. Performance Monitor
# ---------------------------------------------------------------------------

@dataclass
class ModelPerformanceMonitor:
    """Track model serving metrics"""
    latency_ms: list[float] = field(default_factory=list)
    throughput_rps: list[float] = field(default_factory=list)
    error_count: int = 0
    total_requests: int = 0

    def record_request(self, latency_ms: float, success: bool):
        self.latency_ms.append(latency_ms)
        self.total_requests += 1
        if not success:
            self.error_count += 1

    def record_throughput(self, requests_per_second: float):
        self.throughput_rps.append(requests_per_second)

    def report(self) -> dict:
        if not self.latency_ms:
            return {"status": "no data"}
        p50 = sorted(self.latency_ms)[len(self.latency_ms) // 2]
        p99 = sorted(self.latency_ms)[int(len(self.latency_ms) * 0.99)]
        return {
            "total_requests": self.total_requests,
            "error_rate": round(self.error_count / max(self.total_requests, 1), 4),
            "latency_ms_p50": round(p50, 2),
            "latency_ms_p99": round(p99, 2),
            "avg_throughput_rps": round(sum(self.throughput_rps) / max(len(self.throughput_rps), 1), 2)
            if self.throughput_rps else 0,
        }


# ---------------------------------------------------------------------------
# 5. Evaluation
# ---------------------------------------------------------------------------

def llm_as_judge_score(response: str, rubric: dict) -> float:
    """Simulate LLM-as-Judge evaluation (simplified)"""
    score = 0.0
    if rubric.get("min_length", 0) > 0 and len(response) > rubric["min_length"]:
        score += 0.3
    if rubric.get("has_code", False) and ("def " in response or "class " in response or "```" in response):
        score += 0.3
    if rubric.get("has_explanation", False) and any(w in response for w in ["因為", "所以", "因此", "原因"]):
        score += 0.2
    if rubric.get("has_example", False) and any(w in response for w in ["例如", "比如", "舉例"]):
        score += 0.2
    return min(score, 1.0)


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def demo():
    print("=== Mini MLOps Platform Demo ===\n")

    # 1. Prompt Registry
    print("--- 1. Prompt Version Management ---")
    registry = PromptRegistry()
    registry.register(PromptTemplate(
        "summarize", "1.0",
        "請摘要以下內容：{text}",
        ["text"]
    ))
    registry.register(PromptTemplate(
        "summarize", "1.1",
        "用三句話摘要以下內容：{text}\n重點：{focus}",
        ["text", "focus"]
    ))
    latest = registry.get_latest("summarize")
    print(f"Latest summarize prompt (v{latest.version}):")
    print(f"  {latest.render(text='MLOps is important', focus='維運')}")
    print(f"All versions: {registry.list_versions('summarize')}")
    print()

    # 2. A/B Testing
    print("--- 2. A/B Testing ---")
    ab = ABTest(
        name="summarize-v1-vs-v2",
        variants={"v1": "1.0", "v2": "1.1"},
        traffic_split={"v1": 0.5, "v2": 0.5},
    )
    for _ in range(100):
        variant = ab.select_variant()
        # Simulate user rating (0-1)
        score = 0.5 + random.gauss(0, 0.2)
        if variant == "v2":
            score += 0.1  # v2 is slightly better
        score = max(0, min(1, score))
        ab.record_metric(variant, score)

    report = ab.report()
    print("A/B Test Results:")
    for variant, stats in report.items():
        if variant not in ("t_statistic", "significant"):
            print(f"  {variant}: mean={stats['mean']:.3f}, n={stats['count']}")
    if "significant" in report:
        print(f"  Statistically significant: {report['significant']}")
    print()

    # 3. Drift Detection
    print("--- 3. Drift Detection ---")
    monitor = DriftMonitor("prediction_score", threshold=0.2)
    # Reference distribution (training data)
    monitor.add_reference([random.gauss(0.7, 0.1) for _ in range(1000)])
    # Current distribution (production — shifted)
    current = [random.gauss(0.5, 0.15) for _ in range(100)]
    drift_result = monitor.check_drift(current)
    print(f"Feature: {drift_result['feature']}")
    print(f"PSI: {drift_result['psi']} (threshold: {drift_result['threshold']})")
    print(f"Drift detected: {drift_result['drifted']}")
    print()

    # 4. Performance Monitoring
    print("--- 4. Model Performance ---")
    perf_monitor = ModelPerformanceMonitor()
    for _ in range(200):
        perf_monitor.record_request(
            latency_ms=random.gauss(150, 50),
            success=random.random() > 0.02  # 2% error rate
        )
    perf_monitor.record_throughput(45.2)
    perf_monitor.record_throughput(52.1)
    perf_report = perf_monitor.report()
    print(f"Total requests: {perf_report['total_requests']}")
    print(f"Error rate: {perf_report['error_rate']:.2%}")
    print(f"Latency P50: {perf_report['latency_ms_p50']}ms")
    print(f"Latency P99: {perf_report['latency_ms_p99']}ms")
    print()

    # 5. LLM Evaluation
    print("--- 5. LLM Evaluation ---")
    rubric = {"min_length": 20, "has_explanation": True, "has_example": True}
    responses = [
        "因為資料漂移是常見問題，所以需要持續監控。例如使用 PSI 指標。",
        "是的。",
        "好的，我來解釋。原因在於模型在生產環境中會遇到訓練時未見過的資料分布。"
        "舉例來說，如果訓練資料是 2025 年的，而 2026 年的資料分布改變了。",
    ]
    for i, resp in enumerate(responses):
        score = llm_as_judge_score(resp, rubric)
        print(f"  Response {i+1}: score={score:.2f} | {resp[:40]}...")
    print()

    print("=== Demo Complete ===")


if __name__ == "__main__":
    demo()
