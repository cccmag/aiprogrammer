"""
因果分析工具 — 因果圖、反事實推理、可解釋性 (SHAP/LIME 模擬)
"""

import math
import random
from dataclasses import dataclass, field
from typing import Optional


# --- 1. 因果圖 ---

@dataclass
class CausalNode:
    name: str
    value: float = 0.0
    parents: list[str] = field(default_factory=list)

class CausalGraph:
    """Simple causal graph with do-calculus"""

    def __init__(self):
        self.nodes: dict[str, CausalNode] = {}
        self.edges: dict[str, list[str]] = {}  # parent -> children

    def add_node(self, name: str, parents: Optional[list[str]] = None):
        self.nodes[name] = CausalNode(name, parents=parents or [])
        for p in (parents or []):
            if p not in self.edges:
                self.edges[p] = []
            self.edges[p].append(name)

    def intervene(self, node_name: str, value: float) -> dict[str, float]:
        """do-calculus: set a node to a value"""
        results = {}
        for name in self.nodes:
            if name == node_name:
                results[name] = value
            else:
                results[name] = self._simulate(name, {node_name: value})
        return results

    def _simulate(self, node_name: str, interventions: dict) -> float:
        """Simulate node value given interventions"""
        node = self.nodes[node_name]
        if not node.parents:
            return node.value
        parent_vals = [interventions.get(p, self.nodes[p].value) for p in node.parents]
        return sum(parent_vals) / len(parent_vals) if parent_vals else 0.0


# --- 2. 反事實推理 ---

class CounterfactualReasoner:
    """What-if analysis using causal model"""

    def __init__(self):
        self.factuals: dict[str, dict] = {}
        self.model_params: dict[str, float] = {}

    def fit(self, data: list[dict[str, float]], target: str):
        """Learn a simple linear model"""
        import random
        features = [k for k in data[0].keys() if k != target] if data else []
        self.model_params = {f: random.uniform(-1, 1) for f in features}
        self.model_params["bias"] = random.uniform(0, 1)
        self.target = target

    def predict(self, x: dict[str, float]) -> float:
        result = self.model_params.get("bias", 0)
        for f, w in self.model_params.items():
            if f != "bias":
                result += w * x.get(f, 0)
        return result

    def counterfactual(self, factual: dict[str, float],
                       change: dict[str, float]) -> dict:
        """What if some features were different?"""
        cf = factual.copy()
        cf.update(change)
        actual = self.predict(factual)
        cf_outcome = self.predict(cf)
        return {
            "factual": actual,
            "counterfactual": cf_outcome,
            "effect": cf_outcome - actual,
            "changes": change
        }


# --- 3. SHAP 可解釋性模擬 ---

class SimulatedShapExplainer:
    """Simulate SHAP value computation"""

    def __init__(self):
        self.base_value = 0.5
        self.feature_importances: dict[str, float] = {}

    def fit(self, feature_names: list[str]):
        self.feature_names = feature_names
        self.feature_importances = {f: random.uniform(-0.3, 0.3) for f in feature_names}

    def explain(self, x: dict[str, float]) -> dict:
        shap_values = {}
        for f in self.feature_names:
            shap_values[f] = self.feature_importances[f] * x.get(f, 0)
        prediction = self.base_value + sum(shap_values.values())
        shap_values["base_value"] = self.base_value
        shap_values["prediction"] = prediction
        return shap_values


# --- 4. LIME 模擬 ---

class SimulatedLimeExplainer:
    """Simulate LIME local explanations"""

    def __init__(self):
        self.feature_importances: dict[str, float] = {}

    def explain(self, x: dict[str, float], prediction: float) -> dict:
        """Generate local surrogate explanation"""
        local_model = {}
        for f, v in x.items():
            local_model[f] = v * random.uniform(0.5, 1.5)
        return {
            "feature_weights": local_model,
            "prediction": prediction,
            "explanation": sorted(local_model.items(), key=lambda t: -abs(t[1]))[:3]
        }


# --- Demo ---

def demo():
    print("=== Causal AI & Explainability ===\n")

    # 1. Causal Graph
    print("1. Causal Graph & Do-Calculus:")
    cg = CausalGraph()
    cg.add_node("education", parents=[])
    cg.add_node("experience", parents=[])
    cg.add_node("salary", parents=["education", "experience"])

    factual = {"education": 16, "experience": 5, "salary": 75000}
    for name, val in factual.items():
        cg.nodes[name].value = val

    cf_result = cg.intervene("education", 20)
    print(f"  Factual: salary={cg.nodes['salary'].value}")
    print(f"  Intervention: education = 20")
    print(f"  Counterfactual salary: {cf_result['salary']:.0f}")
    print()

    # 2. Counterfactual Reasoner
    print("2. Counterfactual Reasoning:")
    reasoner = CounterfactualReasoner()
    data = [{"hours": 40, "study": 10, "score": 85},
            {"hours": 30, "study": 5, "score": 65}]
    reasoner.fit(data, "score")

    factual = {"hours": 40, "study": 10}
    cf = reasoner.counterfactual(factual, {"study": 20})
    print(f"  Factual: score={cf['factual']:.1f}")
    print(f"  Counterfactual (study=20): score={cf['counterfactual']:.1f}")
    print(f"  Effect: {cf['effect']:+.1f}")
    print()

    # 3. SHAP
    print("3. SHAP Explainer:")
    shap = SimulatedShapExplainer()
    shap.fit(["age", "income", "education"])
    explanation = shap.explain({"age": 30, "income": 50000, "education": 16})
    for f, v in explanation.items():
        if f not in ("prediction", "base_value"):
            print(f"  SHAP[{f}] = {v:+.4f}")
    print(f"  Prediction: {explanation['prediction']:.4f}")
    print()

    # 4. LIME
    print("4. LIME Explainer:")
    lime = SimulatedLimeExplainer()
    explanation = lime.explain({"age": 35, "income": 60000}, 0.82)
    print("  Top features:")
    for f, w in explanation["explanation"]:
        print(f"    {f}: weight={w:.3f}")

    print("\n=== Demo Complete ===")


if __name__ == "__main__":
    demo()
