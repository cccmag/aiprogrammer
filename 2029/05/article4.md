# 程式碼生成評估 (SWE-bench)

## SWE-bench 簡介

SWE-bench 由普林斯頓大學推出，是評估 LLM 程式碼生成能力的標竿基準。它要求模型解決真實 GitHub 儲存庫中的 issue，包含理解程式碼庫、定位 bug、生成修補程式等完整流程。

## 評估流程

```python
import json
import subprocess
import tempfile
from pathlib import Path

class SWEBenchEvaluator:
    def __init__(self, dataset_path):
        with open(dataset_path) as f:
            self.instances = json.load(f)

    def evaluate_instance(self, instance, model):
        repo_dir = Path(tempfile.mkdtemp())
        subprocess.run(["git", "clone", instance["repo"], repo_dir])
        subprocess.run(["git", "checkout", instance["base_commit"]],
                       cwd=repo_dir)

        # 模型生成修補程式
        patch = model.generate_patch(
            instance["problem_statement"],
            repo_dir
        )

        # 儲存修補程式
        patch_file = repo_dir / "patch.diff"
        patch_file.write_text(patch)

        # 執行測試
        result = subprocess.run(
            ["git", "apply", "patch.diff"],
            cwd=repo_dir, capture_output=True, text=True
        )

        if result.returncode != 0:
            return {"success": False, "error": result.stderr}

        test_result = subprocess.run(
            instance["test_command"].split(),
            cwd=repo_dir, capture_output=True, text=True
        )
        return {
            "success": test_result.returncode == 0,
            "output": test_result.stdout
        }

evaluator = SWEBenchEvaluator("swe_bench.json")
# evaluator.evaluate_instance(evaluator.instances[0], model)
```

## 結果分析

```python
def analyze_results(results):
    total = len(results)
    resolved = sum(1 for r in results if r["success"])
    print(f"解決率: {resolved}/{total} ({resolved/total*100:.1f}%)")

    by_repo = {}
    for r in results:
        repo = r.get("repo", "unknown")
        if repo not in by_repo:
            by_repo[repo] = []
        by_repo[repo].append(r)

    for repo, repo_results in by_repo.items():
        rate = sum(1 for r in repo_results if r["success"]) / len(repo_results)
        print(f"{repo}: {rate*100:.1f}%")
```

## 主要挑戰

- **長期上下文**：需要理解整個程式碼庫結構
- **精確修改**：生成的 diff 必須完全正確
- **依賴管理**：需要處理複雜的建置環境

## 結語

Google 搜尋「SWE-bench Leaderboard」可查看最新排名。程式碼生成評估正在從簡單的函數生成進化到完整的軟體工程任務。
