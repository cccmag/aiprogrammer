"""
合成資料生成器 — 文字、表格、程式碼合成
"""
import random
import string
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class SyntheticRecord:
    id: str
    text: str
    label: Optional[str] = None
    metadata: dict = field(default_factory=dict)

TEMPLATES = [
    "The {adj} {noun} {verb} the {obj}.",
    "A {adj} {noun} is {state} for {purpose}.",
    "When {noun} {verb}, the {obj} becomes {adj}.",
]

ADJ = ["quick", "smart", "fast", "efficient", "reliable", "advanced"]
NOUN = ["algorithm", "model", "system", "agent", "framework", "pipeline"]
VERB = ["processes", "analyzes", "generates", "optimizes", "validates", "trains"]
OBJ = ["data", "output", "input", "result", "feature", "prediction"]
STATE = ["useful", "essential", "critical", "optional", "standard"]
PURPOSE = ["training", "inference", "evaluation", "deployment", "testing"]

class SyntheticDataGenerator:
    def generate_text(self, n: int = 10) -> list[SyntheticRecord]:
        records = []
        for i in range(n):
            text = random.choice(TEMPLATES).format(
                adj=random.choice(ADJ), noun=random.choice(NOUN),
                verb=random.choice(VERB), obj=random.choice(OBJ),
                state=random.choice(STATE), purpose=random.choice(PURPOSE))
            records.append(SyntheticRecord(f"syn_{i}", text, random.choice(["pos", "neg"])))
        return records

    def generate_table(self, n: int = 10) -> list[dict]:
        return [{"id": i, "feature_a": random.gauss(0, 1), "feature_b": random.gauss(5, 2),
                 "category": random.choice(["A", "B", "C"]), "target": random.randint(0, 1)} for i in range(n)]

    def generate_code(self, pattern: str = "function") -> str:
        funcs = {
            "function": "def process(data):\n    result = [x * 2 for x in data]\n    return result",
            "class": "class Model:\n    def __init__(self, lr=0.01):\n        self.lr = lr\n    def train(self, X, y):\n        pass",
            "test": "def test_model():\n    assert True\n    print('All tests passed')"
        }
        return funcs.get(pattern, funcs["function"])

def demo():
    print("=== Synthetic Data Generator ===\n")
    gen = SyntheticDataGenerator()
    records = gen.generate_text(5)
    print("1. Text Data:")
    for r in records:
        print(f"  [{r.label}] {r.text}")
    print("\n2. Table Data:")
    for row in gen.generate_table(3):
        print(f"  {row}")
    print("\n3. Code Data:")
    print(f"  {gen.generate_code('class')}")
    print("\n=== Demo Complete ===")

if __name__ == "__main__":
    demo()
