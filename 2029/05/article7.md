# 持續評估管線設計

## 為什麼需要持續評估？

模型迭代速度快，每次更新都可能改變行為。持續評估管線（Continuous Evaluation Pipeline）能自動化監控模型性能，及早發現回歸問題。

## 管線架構設計

```python
import json
from datetime import datetime
from pathlib import Path

class EvaluationPipeline:
    def __init__(self, config_path="pipeline_config.json"):
        with open(config_path) as f:
            self.config = json.load(f)
        self.results_dir = Path("evaluation_results")
        self.results_dir.mkdir(exist_ok=True)

    def run_evaluation(self, model, model_version):
        timestamp = datetime.now().isoformat()
        results = {"model_version": model_version,
                   "timestamp": timestamp, "benchmarks": {}}

        for benchmark in self.config["benchmarks"]:
            result = self.run_benchmark(model, benchmark)
            results["benchmarks"][benchmark["name"]] = result

        result_file = self.results_dir / f"{model_version}.json"
        with open(result_file, "w") as f:
            json.dump(results, f, indent=2)
        self.check_regression(results)
        return results

    def run_benchmark(self, model, benchmark_config):
        from lm_eval import simple_evaluate
        return simple_evaluate(
            model=model,
            tasks=[benchmark_config["task"]],
            num_fewshot=benchmark_config.get("fewshot", 0)
        )

    def check_regression(self, results):
        for name, result in results["benchmarks"].items():
            history = self.get_history(name)
            if history:
                prev = history[-1]["score"]
                curr = result.get("acc", 0)
                if curr < prev - 0.02:
                    print(f"[警報] {name} 回歸: {prev:.3f} -> {curr:.3f}")

    def get_history(self, benchmark_name):
        history = []
        for f in sorted(self.results_dir.glob("*.json")):
            data = json.load(open(f))
            if benchmark_name in data.get("benchmarks", {}):
                score = data["benchmarks"][benchmark_name].get("acc", 0)
                history.append({"version": data["model_version"],
                                "score": score})
        return history
```

## CI/CD 整合

```python
def ci_evaluation(model):
    pipeline = EvaluationPipeline()
    quick = ["hellaswag", "arc_easy"]
    config = {"benchmarks": [
        {"name": b, "task": b, "fewshot": 0} for b in quick
    ]}
    return pipeline.run_evaluation(model, "ci-latest")
```

## 結語

持續評估管線能將模型評估融入開發流程，確保每次變更都經過驗證。
