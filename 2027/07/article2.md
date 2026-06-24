# Kubeflow 與 TFX：生產級 ML 管線平台

## 前言

當機器學習專案從 Jupyter Notebook 原型階段成長為需要團隊協作的生產系統時，第一個需要解決的問題是：如何標準化 ML 工作流程？Kubeflow 和 TFX（TensorFlow Extended）是這個領域最具影響力兩個開源專案，它們分別從不同的角度解決了 ML 管線的標準化問題。

## Kubeflow：Kubernetes 上的 ML 平台

Kubeflow 最初由 Google 在 2018 年的 KubeCon 上發布，目標是讓 ML 工作負載在 Kubernetes 上「像微服務一樣運行」。經過近十年的發展，Kubeflow 已從單純的 TensorFlow 部署工具演進為完整的 ML 平台。

### Kubeflow 核心元件

```python
# Kubeflow Pipeline 定義範例
import kfp
from kfp import dsl
from kfp.dsl import component

@component(base_image="python:3.10", packages_to_install=["pandas", "scikit-learn"])
def validate_data(dataset_path: str) -> dict:
    """資料驗證元件"""
    import pandas as pd
    df = pd.read_parquet(dataset_path)
    report = {
        "rows": len(df),
        "columns": list(df.columns),
        "missing_rates": df.isnull().mean().to_dict(),
        "passed": df.isnull().sum().sum() == 0
    }
    print(f"Data validation: {report}")
    return report

@component(base_image="python:3.10", packages_to_install=["scikit-learn", "mlflow"])
def train_model(training_data: str, params: dict) -> str:
    """模型訓練元件"""
    import pandas as pd
    from sklearn.ensemble import GradientBoostingClassifier
    import mlflow
    import json

    df = pd.read_parquet(training_data)
    X = df.drop("target", axis=1)
    y = df["target"]

    with mlflow.start_run():
        model = GradientBoostingClassifier(**params)
        model.fit(X, y)
        accuracy = model.score(X, y)
        mlflow.log_metric("accuracy", accuracy)
        mlflow.sklearn.log_model(model, "model")

    return json.dumps({"accuracy": accuracy, "run_id": mlflow.active_run().info.run_id})

@component(base_image="python:3.10", packages_to_install=["mlflow"])
def evaluate_and_deploy(accuracy: str, threshold: float = 0.85) -> str:
    """評估與部署元件"""
    import json
    import mlflow

    metrics = json.loads(accuracy)
    acc = metrics["accuracy"]
    run_id = metrics["run_id"]

    if acc >= threshold:
        # 自動註冊模型
        model_uri = f"runs:/{run_id}/model"
        mlflow.register_model(model_uri, "ProductionModel")
        return f"Deployed (accuracy={acc:.3f})"
    return f"Rejected (accuracy={acc:.3f} < {threshold})"

# 組裝管線
@dsl.pipeline(name="ml-training-pipeline")
def ml_pipeline(dataset_path: str = "data/train.parquet"):
    v_data = validate_data(dataset_path)
    v_model = train_model(
        training_data=dataset_path,
        params={"n_estimators": 100, "learning_rate": 0.1}
    ).after(v_data)
    v_deploy = evaluate_and_deploy(accuracy=v_model.output)
```

### Kubeflow 的優勢與限制

Kubeflow 的最大優勢是與 Kubernetes 生態的深度整合——如果你的組織已經使用 Kubernetes，導入 Kubeflow 的學習曲線相對平緩。它提供了 Notebook、Pipeline、Katib（超參數調優）、KFServing（模型服務）等完整工具鏈。

然而，Kubeflow 的複雜性也是它的主要缺點——完整部署需要管理多個微服務（認證、儲存、網路），維運成本不低。

## TFX：端到端的生產 ML 管線

TFX 是 Google 內部的 ML 平台開源版本，強調管線的可靠性和可重複性。與 Kubeflow 的「平台」定位不同，TFX 更像是一個「函式庫」——它提供了資料驗證、特徵工程、模型訓練、評估和部署的標準化元件。

### TFX 的核心元件

```python
# TFX 管線定義範例
import tfx
from tfx.components import (
    CsvExampleGen, StatisticsGen, SchemaGen,
    ExampleValidator, Transform, Trainer, Tuner,
    Evaluator, Pusher
)
from tfx.orchestration import pipeline as tfx_pipeline

# 定義 TFX 管線
def create_pipeline(pipeline_name: str, pipeline_root: str, data_path: str):
    example_gen = CsvExampleGen(input_base=data_path)

    # 資料統計與驗證
    statistics_gen = StatisticsGen(examples=example_gen.outputs["examples"])
    schema_gen = SchemaGen(statistics=statistics_gen.outputs["statistics"])
    example_validator = ExampleValidator(
        statistics=statistics_gen.outputs["statistics"],
        schema=schema_gen.outputs["schema"]
    )

    # 特徵轉換
    transform = Transform(
        examples=example_gen.outputs["examples"],
        schema=schema_gen.outputs["schema"],
        module_file="transform.py"  # 自定義轉換邏輯
    )

    # 模型訓練
    trainer = Trainer(
        module_file="trainer.py",
        examples=transform.outputs["transformed_examples"],
        schema=schema_gen.outputs["schema"],
        transform_graph=transform.outputs["transform_graph"],
        hyperparameters={
            "epochs": 10,
            "batch_size": 32,
            "learning_rate": 0.001
        }
    )

    # 模型評估
    evaluator = Evaluator(
        examples=example_gen.outputs["examples"],
        model=trainer.outputs["model"],
        eval_config={
            "metrics": [
                {"metric_class": "Accuracy", "config": {"name": "accuracy"}},
                {"metric_class": "AUC", "config": {"name": "auc"}},
            ],
            "slicing_specs": [{"feature_keys": ["customer_segment"]}]
        }
    )

    # 部署閘道
    pusher = Pusher(
        model=trainer.outputs["model"],
        model_blessing=evaluator.outputs["blessing"],
        push_destination={
            "filesystem": {"base_directory": "serving_model"}
        }
    )

    return tfx_pipeline.Pipeline(
        pipeline_name=pipeline_name,
        pipeline_root=pipeline_root,
        components=[
            example_gen, statistics_gen, schema_gen,
            example_validator, transform, trainer,
            evaluator, pusher
        ]
    )
```

### TFX 的資料驗證機制

TFX 的一大特色是內建的資料驗證（TFDV - TensorFlow Data Validation）。它能自動檢測訓練資料與生產資料之間的分布差異：

```python
# 使用 TFDV 進行資料驗證
import tensorflow_data_validation as tfdv

# 計算訓練資料統計
train_stats = tfdv.generate_statistics_from_csv(
    data_location="train.csv",
    delimiter=","
)

# 推導 schema
schema = tfdv.infer_schema(statistics=train_stats)

# 計算生產資料統計
prod_stats = tfdv.generate_statistics_from_csv(
    data_location="production_data.csv",
    delimiter=","
)

# 檢測漂移
anomalies = tfdv.validate_statistics(
    statistics=prod_stats,
    schema=schema,
    serving_statistics=train_stats
)

# 輸出異常檢測結果
for feature_name, feature_anomalies in anomalies.anomaly_info.items():
    for anomaly in feature_anomalies:
        print(f"Feature '{feature_name}': {anomaly.description}")
        print(f"  Severity: {anomaly.severity}")
```

## Kubeflow vs TFX：如何選擇？

| 面向 | Kubeflow | TFX |
|------|----------|-----|
| 基礎設施 | Kubernetes 原生 | 可運行在 Airflow、Kubeflow、本地 |
| 學習曲線 | 中（需要 K8s 知識） | 高（需要 TF 生態知識） |
| 元件豐富度 | 廣泛（Notebook、Katib、KFServing） | 深度（資料驗證、轉換內建） |
| 框架相依性 | 框架無關 | TensorFlow 生態最佳 |
| 維運複雜度 | 高 | 中 |

實務上，許多團隊採用混合策略：使用 Kubeflow 作為管線調度平台，在管線內部使用 TFX 元件進行資料驗證與模型評估。

## 參考資源

- [Kubeflow 官方文件](https://www.google.com/search?q=Kubeflow+documentation)
- [TFX 使用者指南](https://www.google.com/search?q=TFX+user+guide)
- [Kubeflow vs MLflow 比較](https://www.google.com/search?q=Kubeflow+vs+MLflow+comparison)
- [TFDV 資料驗證教學](https://www.google.com/search?q=TensorFlow+Data+Validation+tutorial)
