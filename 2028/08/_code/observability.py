"""
AI 可觀測性與監控系統 — 漂移檢測、追蹤、警報
"""

import math
import random
import time
from dataclasses import dataclass, field
from collections import deque
from typing import Optional


# --- 1. 資料漂移檢測 ---

@dataclass
class DriftReport:
    drifted: bool
    drift_score: float
    drifted_features: list[str]
    message: str


class DriftDetector:
    """Detect data drift using distribution comparison"""

    def __init__(self, threshold: float = 0.1):
        self.threshold = threshold
        self.baseline: dict[str, dict] = {}
        self.reference: dict[str, list[float]] = {}

    def set_baseline(self, name: str, mean: float, std: float):
        self.baseline[name] = {"mean": mean, "std": max(std, 1e-6)}

    def set_reference(self, name: str, values: list[float]):
        self.reference[name] = values

    def check(self, name: str, current_values: list[float]) -> DriftReport:
        if name not in self.baseline:
            return DriftReport(False, 0.0, [], "No baseline")

        base = self.baseline[name]
        if not current_values:
            return DriftReport(False, 0.0, [], "No current data")

        current_mean = sum(current_values) / len(current_values)
        # PSI-like score
        score = abs(current_mean - base["mean"]) / base["std"]
        drifted = score > self.threshold

        return DriftReport(drifted, round(score, 3), [name] if drifted else [],
                           f"Drift score: {score:.3f}")


# --- 2. 推論日誌與追蹤 ---

@dataclass
class TraceSpan:
    name: str
    start_time: float
    end_time: Optional[float] = None
    attributes: dict = field(default_factory=dict)
    children: list['TraceSpan'] = field(default_factory=list)


class Tracer:
    """Distributed tracing for inference requests"""

    def __init__(self):
        self.spans: list[TraceSpan] = []
        self.current_stack: list[TraceSpan] = []

    def start_span(self, name: str, **attrs) -> TraceSpan:
        span = TraceSpan(name, time.time(), attributes=attrs)
        self.spans.append(span)
        if self.current_stack:
            self.current_stack[-1].children.append(span)
        self.current_stack.append(span)
        return span

    def end_span(self):
        if self.current_stack:
            span = self.current_stack.pop()
            span.end_time = time.time()

    def get_trace(self) -> list[dict]:
        traces = []
        for span in self.spans:
            duration = (span.end_time - span.start_time) * 1000 if span.end_time else 0
            traces.append({
                "name": span.name,
                "duration_ms": round(duration, 2),
                "attributes": span.attributes,
                "children": len(span.children)
            })
        return traces


# --- 3. 警報系統 ---

@dataclass
class Alert:
    rule: str
    severity: str  # info / warning / critical
    message: str
    timestamp: float = field(default_factory=time.time)


class AlertManager:
    """Alert management with dedup and escalation"""

    def __init__(self):
        self.rules: dict[str, callable] = {}
        self.suppressed: set[str] = set()
        self.alert_history: list[Alert] = []

    def add_rule(self, name: str, condition: callable):
        self.rules[name] = condition

    def check_and_alert(self, rule_name: str, condition: bool,
                        severity: str = "warning", message: str = ""):
        if rule_name in self.suppressed:
            return
        if condition:
            alert = Alert(rule_name, severity, message)
            self.alert_history.append(alert)
            if severity == "critical":
                print(f"  🔴 [{severity.upper()}] {rule_name}: {message}")
            elif severity == "warning":
                print(f"  🟡 [{severity.upper()}] {rule_name}: {message}")
            else:
                print(f"  🔵 [{severity.upper()}] {rule_name}: {message}")

    def suppress(self, rule_name: str):
        self.suppressed.add(rule_name)

    def get_alerts(self, severity: Optional[str] = None) -> list[Alert]:
        if severity:
            return [a for a in self.alert_history if a.severity == severity]
        return self.alert_history


# --- 4. 健康檢查 ---

@dataclass
class HealthStatus:
    status: str  # healthy / degraded / down
    checks: dict[str, bool]
    message: str


class HealthChecker:
    """System health check framework"""

    def __init__(self):
        self.checks: dict[str, callable] = {}

    def register(self, name: str, check_fn: callable):
        self.checks[name] = check_fn

    def run_all(self) -> HealthStatus:
        results = {}
        for name, check_fn in self.checks.items():
            try:
                results[name] = check_fn()
            except Exception:
                results[name] = False

        failed = sum(1 for v in results.values() if not v)
        if failed == 0:
            status = "healthy"
        elif failed <= len(results) // 3:
            status = "degraded"
        else:
            status = "down"

        return HealthStatus(status, results, f"{failed} of {len(results)} checks failed")


# --- Demo ---

def demo():
    print("=== AI Observability & Monitoring ===\n")

    # 1. Drift Detection
    print("1. Data Drift Detection:")
    detector = DriftDetector(threshold=0.5)
    detector.set_baseline("accuracy", mean=0.95, std=0.02)

    for day in range(5):
        values = [random.gauss(0.95 - day * 0.02, 0.03) for _ in range(100)]
        report = detector.check("accuracy", values)
        status = "⚠️ DRIFT" if report.drifted else "✅ OK"
        print(f"  Day {day+1}: {status} (score={report.drift_score:.3f})")

    # 2. Tracing
    print("\n2. Distributed Tracing:")
    tracer = Tracer()
    tracer.start_span("request", method="POST", path="/predict")
    tracer.start_span("preprocess")
    time.sleep(0.001)
    tracer.end_span()
    tracer.start_span("inference", model="gpt-5")
    time.sleep(0.002)
    tracer.end_span()
    tracer.end_span()

    for t in tracer.get_trace():
        print(f"  {t['name']}: {t['duration_ms']:.2f}ms ({t['children']} children)")

    # 3. Alerting
    print("\n3. Alerts:")
    alert_mgr = AlertManager()
    for i in range(5):
        alert_mgr.check_and_alert(
            f"latency_p99",
            condition=random.random() < 0.3,
            severity="critical" if random.random() < 0.2 else "warning",
            message="Response time exceeded threshold"
        )

    # 4. Health Check
    print("\n4. Health Check:")
    hc = HealthChecker()
    hc.register("model_loaded", lambda: True)
    hc.register("database_up", lambda: True)
    hc.register("cache_warm", lambda: random.random() > 0.2)
    status = hc.run_all()
    print(f"  Status: {status.status}")
    for name, ok in status.checks.items():
        print(f"  {'✅' if ok else '❌'} {name}")

    print("\n=== Demo Complete ===")


if __name__ == "__main__":
    demo()
