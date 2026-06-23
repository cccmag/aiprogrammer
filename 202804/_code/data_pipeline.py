"""
資料工程管線 — 特徵儲存、資料版本控制、品質監控
"""

import hashlib
import json
import time
from dataclasses import dataclass, field
from typing import Optional
from collections import Counter


# --- 1. 特徵儲存 ---

@dataclass
class Feature:
    name: str
    value: float
    timestamp: float = field(default_factory=time.time)
    version: str = "v1"


class FeatureStore:
    """Simple feature store with point-in-time lookup"""

    def __init__(self):
        self.features: dict[str, list[Feature]] = {}

    def register(self, name: str):
        if name not in self.features:
            self.features[name] = []

    def set(self, name: str, value: float, version: str = "v1"):
        self.register(name)
        self.features[name].append(Feature(name, value, version=version))

    def get(self, name: str, at_time: Optional[float] = None) -> Optional[float]:
        if name not in self.features:
            return None
        if at_time is None:
            return self.features[name][-1].value if self.features[name] else None
        for f in reversed(self.features[name]):
            if f.timestamp <= at_time:
                return f.value
        return None

    def get_all(self) -> dict[str, float]:
        return {name: self.features[name][-1].value
                for name in self.features if self.features[name]}


# --- 2. 資料版本控制 ---

class DataVersionControl:
    """Simple data versioning with hash-based dedup"""

    def __init__(self):
        self.versions: dict[str, dict] = {}

    def hash_data(self, data: list[dict]) -> str:
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()[:12]

    def commit(self, data: list[dict], message: str = "") -> str:
        version_id = self.hash_data(data)
        self.versions[version_id] = {
            "data": data,
            "message": message,
            "timestamp": time.time(),
            "size": len(data)
        }
        return version_id

    def checkout(self, version_id: str) -> Optional[list[dict]]:
        if version_id in self.versions:
            return self.versions[version_id]["data"]
        return None

    def diff(self, v1: str, v2: str) -> dict:
        d1 = self.versions.get(v1, {}).get("data", [])
        d2 = self.versions.get(v2, {}).get("data", [])
        return {
            "added": len(d2) - len(d1),
            "v1_size": len(d1),
            "v2_size": len(d2)
        }


# --- 3. 資料品質監控 ---

@dataclass
class QualityReport:
    total_rows: int
    missing_values: dict[str, int]
    duplicates: int
    score: float


def quality_check(data: list[dict]) -> QualityReport:
    """Check data quality metrics"""
    if not data:
        return QualityReport(0, {}, 0, 0.0)

    total = len(data)
    missing = Counter()
    for row in data:
        for key, value in row.items():
            if value is None or (isinstance(value, str) and value.strip() == ""):
                missing[key] += 1

    hashes = [hashlib.md5(json.dumps(r, sort_keys=True).encode()).hexdigest()
              for r in data]
    duplicates = len(hashes) - len(set(hashes))

    # Score: 1.0 - penalties
    missing_penalty = sum(missing.values()) / (total * len(data[0])) if data[0] else 0
    dup_penalty = duplicates / total if total > 0 else 0
    score = max(0.0, 1.0 - missing_penalty - dup_penalty)

    return QualityReport(total, dict(missing), duplicates, round(score, 2))


# --- Demo ---

def demo():
    print("=== Data Engineering Pipeline ===\n")

    # 1. Feature Store
    print("1. Feature Store:")
    fs = FeatureStore()
    fs.set("temperature", 36.5)
    time.sleep(0.01)
    fs.set("temperature", 37.0)
    fs.set("heart_rate", 72.0)

    now = time.time()
    print(f"  Current temperature: {fs.get('temperature')}")
    print(f"  All features: {fs.get_all()}")

    # 2. Data Version Control
    print("\n2. Data Version Control:")
    dvc = DataVersionControl()
    data_v1 = [{"id": 1, "value": "a"}, {"id": 2, "value": "b"}]
    data_v2 = [{"id": 1, "value": "a"}, {"id": 2, "value": "b"}, {"id": 3, "value": "c"}]

    v1 = dvc.commit(data_v1, "Initial data")
    v2 = dvc.commit(data_v2, "Added row 3")
    print(f"  v1: {v1} ({len(data_v1)} rows)")
    print(f"  v2: {v2} ({len(data_v2)} rows)")

    diff = dvc.diff(v1, v2)
    print(f"  Diff: +{diff['added']} rows")

    # 3. Quality Check
    print("\n3. Data Quality Check:")
    sample = [
        {"name": "Alice", "age": 30, "email": "alice@example.com"},
        {"name": "Bob", "age": None, "email": "bob@example.com"},
        {"name": "Alice", "age": 30, "email": ""},
        {"name": "Charlie", "age": 25, "email": "charlie@example.com"},
        {"name": "Bob", "age": None, "email": "bob@example.com"},
    ]
    report = quality_check(sample)
    print(f"  Total rows: {report.total_rows}")
    print(f"  Missing values: {report.missing_values}")
    print(f"  Duplicates: {report.duplicates}")
    print(f"  Quality score: {report.score}")

    print("\n=== Demo Complete ===")


if __name__ == "__main__":
    demo()
