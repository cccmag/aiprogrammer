# CI/CD for ML：自動化管線實戰

## 前言

傳統軟體的 CI/CD 管線處理的是原始碼到可執行檔的轉換。ML 的 CI/CD 則需要處理一個更複雜的流程：資料 → 特徵 → 模型 → 評估 → 部署。每一步都有獨特的挑戰——資料版本、模型可重複性、評估指標的主觀性、以及部署後效能的持續監控。

2027 年的 ML CI/CD 已經發展出成熟的模式：將資料驗證、模型訓練、提示詞測試和部署策略整合為統一的自動化管線。本文將從實戰角度展示如何建構這樣的管線。

## ML CI/CD 管線的架構

```python
# ML CI/CD 管線的核心調度器
from datetime import datetime
from typing import Callable
import json

class MLPipeline:
    def __init__(self, name: str):
        self.name = name
        self.stages: list[dict] = []
        self.results: dict = {}
        self.start_time: datetime | None = None
        self.end_time: datetime | None = None

    def add_stage(self, name: str, func: Callable,
                  depends_on: list[str] = None,
                  timeout_seconds: int = 3600):
        """加入管線階段"""
        self.stages.append({
            "name": name,
            "func": func,
            "depends_on": depends_on or [],
            "timeout": timeout_seconds,
            "status": "pending",
            "start": None,
            "end": None,
            "output": None,
            "error": None,
        })

    def run(self, context: dict = None) -> dict:
        """執行管線"""
        self.start_time = datetime.now()
        context = context or {}

        while True:
            pending = [s for s in self.stages if s["status"] == "pending"]
            if not pending:
                break

            # 找到所有可執行的階段（依賴已完成的階段）
            executed = False
            for stage in pending:
                deps_met = all(
                    any(
                        s["name"] == dep and s["status"] == "completed"
                        for s in self.stages
                    )
                    for dep in stage["depends_on"]
                )
                if deps_met:
                    self._execute_stage(stage, context)
                    executed = True

            if not executed:
                # 有 pending 但無法執行 -> 依賴循環
                pending_names = [s["name"] for s in pending]
                for s in pending:
                    s["status"] = "failed"
                    s["error"] = f"Circular dependency: {pending_names}"
                break

        self.end_time = datetime.now()
        return self._report()

    def _execute_stage(self, stage: dict, context: dict):
        stage["start"] = datetime.now()
        stage["status"] = "running"
        print(f"[{self.name}] 執行階段: {stage['name']}")

        try:
            result = stage["func"](context)
            stage["output"] = result
            stage["status"] = "completed"
            context[stage["name"]] = result
            print(f"[{self.name}] ✓ {stage['name']} 完成")
        except Exception as e:
            stage["status"] = "failed"
            stage["error"] = str(e)
            print(f"[{self.name}] ✗ {stage['name']} 失敗: {e}")
        finally:
            stage["end"] = datetime.now()

    def _report(self) -> dict:
        stages_report = {}
        for s in self.stages:
            stages_report[s["name"]] = {
                "status": s["status"],
                "duration_seconds": (
                    (s["end"] - s["start"]).total_seconds()
                    if s["end"] and s["start"] else None
                ),
                "error": s["error"],
            }

        total_duration = (
            (self.end_time - self.start_time).total_seconds()
            if self.end_time and self.start_time else None
        )

        return {
            "pipeline": self.name,
            "total_duration_seconds": total_duration,
            "overall_status": (
                "passed"
                if all(s["status"] == "completed" for s in self.stages)
                else "failed"
            ),
            "stages": stages_report,
        }
```

## 階段 1：資料驗證

資料驗證是 ML 管線的第一道關卡：

```python
def data_validation_stage(context: dict) -> dict:
    """資料驗證階段"""
    import pandas as pd

    data_path = context.get("data_path", "data/train.parquet")
    df = pd.read_parquet(data_path)

    validation_results = {
        "rows": len(df),
        "columns": len(df.columns),
        "missing_values": df.isnull().sum().to_dict(),
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
    }

    # 檢查缺失值
    missing_cols = [k for k, v in validation_results["missing_values"].items() if v > 0]
    if missing_cols:
        validation_results["warnings"] = f"缺失值列: {missing_cols}"

    # 檢查類別分布
    context["data_profile"] = validation_results
    return validation_results
```

## 階段 2：特徵與模型訓練

```python
def feature_engineering_stage(context: dict) -> dict:
    """特徵工程階段"""
    import pandas as pd
    from sklearn.preprocessing import StandardScaler

    df = pd.read_parquet(context["data_path"])
    numerical_cols = df.select_dtypes(include=["int64", "float64"]).columns
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns

    features = {
        "numerical_features": list(numerical_cols),
        "categorical_features": list(categorical_cols),
        "total_features": len(numerical_cols) + len(categorical_cols),
    }

    # 記錄特徵統計
    for col in numerical_cols[:5]:
        features[f"{col}_stats"] = {
            "mean": float(df[col].mean()),
            "std": float(df[col].std()),
            "min": float(df[col].min()),
            "max": float(df[col].max()),
        }

    context["features"] = features
    return features

def training_stage(context: dict) -> dict:
    """模型訓練階段"""
    import pandas as pd
    from sklearn.ensemble import GradientBoostingClassifier
    from sklearn.model_selection import train_test_split
    import mlflow

    df = pd.read_parquet(context["data_path"])
    X = df.drop("target", axis=1)
    y = df["target"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    with mlflow.start_run() as run:
        model = GradientBoostingClassifier(
            n_estimators=200,
            learning_rate=0.1,
            max_depth=5,
            random_state=42
        )
        model.fit(X_train, y_train)

        train_acc = model.score(X_train, y_train)
        test_acc = model.score(X_test, y_test)

        mlflow.log_params({
            "n_estimators": 200,
            "learning_rate": 0.1,
            "max_depth": 5,
        })
        mlflow.log_metrics({
            "train_accuracy": train_acc,
            "test_accuracy": test_acc,
        })
        mlflow.sklearn.log_model(model, "model")

    result = {
        "run_id": run.info.run_id,
        "experiment_id": run.info.experiment_id,
        "train_accuracy": train_acc,
        "test_accuracy": test_acc,
        "model_uri": f"runs:/{run.info.run_id}/model",
    }

    context["training"] = result
    return result
```

## 階段 3：評估與品質閘道

```python
def evaluation_stage(context: dict) -> dict:
    """模型評估階段"""
    import mlflow
    import numpy as np
    from sklearn.metrics import (
        accuracy_score, precision_score, recall_score, f1_score,
        confusion_matrix, roc_auc_score
    )
    import pandas as pd

    # 載入模型與資料
    model_uri = context["training"]["model_uri"]
    model = mlflow.sklearn.load_model(model_uri)

    df = pd.read_parquet(context["data_path"])
    X = df.drop("target", axis=1)
    y = df["target"]

    y_pred = model.predict(X)
    y_proba = model.predict_proba(X)[:, 1]

    metrics = {
        "accuracy": float(accuracy_score(y, y_pred)),
        "precision": float(precision_score(y, y_pred, average="weighted")),
        "recall": float(recall_score(y, y_pred, average="weighted")),
        "f1": float(f1_score(y, y_pred, average="weighted")),
        "auc_roc": float(roc_auc_score(y, y_proba)),
    }

    # 額外：切片評估
    if "customer_segment" in df.columns:
        segments = df["customer_segment"].unique()
        segment_metrics = {}
        for seg in segments:
            mask = df["customer_segment"] == seg
            seg_y = y[mask]
            seg_pred = y_pred[mask]
            segment_metrics[str(seg)] = {
                "accuracy": float(accuracy_score(seg_y, seg_pred)),
                "count": int(mask.sum()),
            }
        metrics["by_segment"] = segment_metrics

    context["evaluation"] = metrics
    return metrics

def quality_gate_stage(context: dict) -> dict:
    """品質閘道：決定是否繼續部署"""
    metrics = context["evaluation"]
    thresholds = context.get("quality_thresholds", {
        "accuracy": 0.85,
        "f1": 0.80,
        "auc_roc": 0.85,
    })

    failures = []
    for metric, threshold in thresholds.items():
        if metric in metrics and metrics[metric] < threshold:
            failures.append(f"{metric}: {metrics[metric]:.3f} < {threshold}")

    # 比較與當前生產模型
    production_metrics = context.get("production_metrics", {})
    if production_metrics:
        for metric in ["accuracy", "f1"]:
            if metric in metrics and metric in production_metrics:
                improvement = metrics[metric] - production_metrics[metric]
                if improvement < -0.02:
                    failures.append(
                        f"{metric} 低於生產模型 {improvement:+.3f}"
                    )

    passed = len(failures) == 0
    result = {
        "passed": passed,
        "failures": failures,
        "metrics_summary": "; ".join(
            f"{k}={v:.3f}" for k, v in metrics.items()
            if isinstance(v, (int, float))
        ),
        "decision": "deploy" if passed else "reject",
    }

    context["quality_gate"] = result
    return result
```

## 階段 4：部署

```python
def deployment_stage(context: dict) -> dict:
    """模型部署階段"""
    import json

    model_uri = context["training"]["model_uri"]
    strategy = context.get("deployment_strategy", "blue_green")
    evaluatioin_metrics = context["evaluation"]

    deployment = {
        "model_uri": model_uri,
        "strategy": strategy,
        "target_environment": context.get("environment", "staging"),
        "timestamp": datetime.now().isoformat(),
        "model_version": context["training"]["test_accuracy"],
        "trigger": "auto",
    }

    if strategy == "blue_green":
        deployment["blue_green"] = {
            "blue": context.get("current_production_version", "v1"),
            "green": model_uri,
            "traffic_switch": "gradual",
        }
    elif strategy == "canary":
        deployment["canary"] = {
            "initial_percent": 5,
            "increment": 5,
            "monitoring_hours": 24,
            "rollback_on_failure": True,
        }

    context["deployment"] = deployment
    return deployment

def post_deployment_monitoring(context: dict) -> dict:
    """部署後監控設定"""
    import json

    monitor_config = {
        "model_uri": context["deployment"]["model_uri"],
        "monitoring_config": {
            "metrics": ["accuracy", "latency_p50", "latency_p99", "error_rate"],
            "drift_check": {
                "enabled": True,
                "interval_minutes": 60,
                "method": "psi",
                "threshold": 0.2,
            },
            "alerts": {
                "error_rate": "> 5% for 5 minutes",
                "latency_p99": "> 2000ms for 5 minutes",
                "drift": "PSI > 0.25",
            },
            "auto_rollback": {
                "enabled": True,
                "conditions": ["error_rate > 0.1", "drift_detected"],
            },
        },
        "dashboard_url": f"https://grafana.example.com/d/ml-monitor/{context.get('model_name', 'unknown')}",
    }

    context["monitoring"] = monitor_config
    return monitor_config
```

## 整合管線執行

```python
# 完整的 CI/CD for ML 管線
def run_full_pipeline(data_path: str, environment: str = "staging"):
    pipeline = MLPipeline("ml-cd-pipeline")

    pipeline.add_stage("data_validation", data_validation_stage)
    pipeline.add_stage("feature_engineering", feature_engineering_stage,
                       depends_on=["data_validation"])
    pipeline.add_stage("model_training", training_stage,
                       depends_on=["feature_engineering"])
    pipeline.add_stage("model_evaluation", evaluation_stage,
                       depends_on=["model_training"])
    pipeline.add_stage("quality_gate", quality_gate_stage,
                       depends_on=["model_evaluation"])

    # 只有品質閘道通過才執行部署
    def conditional_deploy(context):
        if context.get("quality_gate", {}).get("passed"):
            return deployment_stage(context)
        return {"skipped": True, "reason": "Quality gate failed"}

    pipeline.add_stage("deployment", conditional_deploy,
                       depends_on=["quality_gate"])
    pipeline.add_stage("monitoring_setup", post_deployment_monitoring,
                       depends_on=["deployment"])

    context = {
        "data_path": data_path,
        "environment": environment,
        "quality_thresholds": {
            "accuracy": 0.85,
            "f1": 0.80,
            "auc_roc": 0.85,
        },
        "deployment_strategy": "canary",
    }

    report = pipeline.run(context)

    print(json.dumps(report, indent=2, default=str))

    if report["overall_status"] == "passed":
        print(f"\n管線成功！模型已部署到 {environment}")
    else:
        print(f"\n管線失敗，請檢查各階段錯誤")

    return report
```

## 提示詞的 CD：更輕量的管線

LLM 時代的提示詞變更比模型更頻繁，需要專用的 CD 管線：

```python
def prompt_cd_pipeline(prompt_changes: list[dict]) -> dict:
    """提示詞持續部署管線"""
    pipeline = MLPipeline("prompt-cd")

    def validate_prompt(context):
        changes = context["prompt_changes"]
        results = []
        for change in changes:
            validation = {
                "name": change["name"],
                "version": change["version"],
                "template_valid": "{article}" in change.get("template", ""),
                "params_match": True,
                "test_count": len(change.get("tests", [])),
            }
            results.append(validation)
        return {"validated": all(r["template_valid"] for r in results), "details": results}

    def run_prompt_tests(context):
        # 執行提示詞測試（模擬）
        test_results = []
        for change in context["prompt_changes"]:
            for test in change.get("tests", []):
                test_results.append({
                    "prompt": change["name"],
                    "test": test["name"],
                    "passed": True,
                    "latency_ms": 150,
                })
        return {
            "total": len(test_results),
            "passed": sum(1 for t in test_results if t["passed"]),
            "failed": sum(1 for t in test_results if not t["passed"]),
        }

    pipeline.add_stage("validate", validate_prompt)
    pipeline.add_stage("test", run_prompt_tests, depends_on=["validate"])
    pipeline.add_stage("deploy", lambda ctx: {
        "deployed": True,
        "prompts": [c["name"] for c in ctx["prompt_changes"]],
        "strategy": "canary_5pct",
    }, depends_on=["test"])

    return pipeline.run({"prompt_changes": prompt_changes})
```

## 實戰建議

1. **分階段執行**：將資料驗證、模型訓練、評估分階段執行，便於定位問題
2. **品質閘道是護欄**：永遠在部署前設定品質閘道，拒絕不合格的模型或提示詞
3. **部署策略**：新模型先部署到 Staging 進行 24 小時驗證，再透過金絲雀發布進入 Production
4. **監控要跟上**：部署完成後自動設定監控與警報，確保能即時發現問題
5. **可重複性**：記錄每次管線執行的完整上下文（資料版本、程式碼版本、參數）

## 參考資源

- [CI/CD for Machine Learning Guide](https://www.google.com/search?q=CI+CD+for+machine+learning+best+practices)
- [ML Pipeline Design Patterns](https://www.google.com/search?q=ML+pipeline+design+patterns)
- [Canary Deployments for ML Models](https://www.google.com/search?q=canary+deployment+machine+learning+models)
- [GitHub Actions for ML](https://www.google.com/search?q=GitHub+Actions+machine+learning+pipeline)
