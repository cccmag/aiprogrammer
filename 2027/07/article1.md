# MLflow 深度實戰：從實驗追蹤到模型註冊

## 前言

在 MLOps 的工具生態系中，MLflow 無疑是最廣泛採用的開源方案之一。由 Databricks 在 2018 年開源、2020 年發布 1.0 版本，MLflow 提供了一個輕量但完整的 ML 生命週期管理平台。隨著 2027 年 4.0 版本的發布，MLflow 已從傳統 ML 工具擴展為支援 LLM 評估、提示詞追蹤與 RAG 管線的全方位平台。

本文將深入 MLflow 的核心元件——實驗追蹤（Tracking）、模型註冊（Model Registry）、評估（Evaluation）與部署（Serving），並展示如何在生產環境中有效使用這些功能。

## MLflow 的四個核心元件

MLflow 的設計哲學是「模組化」——每個元件可以獨立使用，也可以整合成完整管線：

- **Tracking**：記錄實驗參數、指標、程式碼版本與模型產出
- **Projects**：將 ML 程式碼封裝為可重複執行的套件
- **Models**：統一模型格式，支援多種部署目標
- **Model Registry**：管理模型版本、階段（Staging/Production）與註釋

### 實驗追蹤深入

實驗追蹤是 MLflow 最基礎也最實用的功能。除了記錄基本參數，進階用法包括自動記錄（Autologging）與自定義 artifacts：

```python
import mlflow
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

# 啟用自動記錄（支援 sklearn、PyTorch、TensorFlow 等）
mlflow.sklearn.autolog()

with mlflow.start_run(run_name="rf_experiment_v2"):
    # 記錄參數
    mlflow.log_param("n_estimators", 100)
    mlflow.log_param("max_depth", 10)
    mlflow.log_param("class_weight", "balanced")

    # 訓練模型
    X, y = make_classification(n_samples=1000, n_features=20, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    model = RandomForestClassifier(n_estimators=100, max_depth=10)
    model.fit(X_train, y_train)

    # 記錄自定義指標
    accuracy = model.score(X_test, y_test)
    mlflow.log_metric("accuracy", accuracy)

    # 記錄額外檔案（artifacts）
    with open("feature_importance.txt", "w") as f:
        f.write(str(model.feature_importances_))
    mlflow.log_artifact("feature_importance.txt")
    mlflow.log_artifact("training_data_profile.csv")
```

### 模型註冊與版本管理

Model Registry 解決了「哪個模型正在生產環境中運行？」這個關鍵問題。它提供了模型版本控制與階段轉換（Stage Transition）的機制：

```python
# 註冊模型到 Registry
mlflow.register_model(
    model_uri=f"runs:/{run_id}/model",
    name="CustomerChurnPredictor"
)

# 轉換模型階段
from mlflow.tracking.client import MlflowClient

client = MlflowClient()

# 將 v2 提升到 Staging 進行測試
client.transition_model_version_stage(
    name="CustomerChurnPredictor",
    version=2,
    stage="Staging"
)

# 測試通過後提升到 Production
client.transition_model_version_stage(
    name="CustomerChurnPredictor",
    version=2,
    stage="Production"
)

# 查詢目前 Production 的模型版本
production_models = client.get_latest_versions(
    name="CustomerChurnPredictor",
    stages=["Production"]
)
print(f"Production model version: {production_models[0].version}")
```

## LLM 支援：MLflow 4.0 的新功能

2027 年的 MLflow 4.0 加入了三個關鍵的 LLM 功能：

### 提示詞追蹤

```python
# MLflow 4.0 的提示詞記錄
with mlflow.start_run():
    # 記錄提示詞模板
    mlflow.log_prompt(
        template="請用三句話總結以下文章：\n\n{article}\n\n重點：",
        params=["article"],
        version="1.2.0"
    )

    # 記錄 LLM 回應
    response = llm_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "..."}]
    )
    mlflow.log_llm_response(
        prompt_id="summary_prompt",
        response=response.choices[0].message.content,
        latency_ms=342,
        token_usage={"prompt": 120, "completion": 85}
    )
```

### LLM 評估

```python
# MLflow 4.0 的 LLM 評估 API
import mlflow

def evaluate_llm_responses():
    with mlflow.start_run():
        # 建立評估資料
        eval_data = [
            {"question": "什麼是 MLOps？", "answer": "...", "reference": "..."},
            {"question": "如何監控模型漂移？", "answer": "...", "reference": "..."},
        ]

        # 使用內建評估器
        results = mlflow.evaluate_llm(
            data=eval_data,
            model_type="question-answering",
            evaluators=["bleu", "rouge", "llm_judge"],
            judge_config={"model": "gpt-4o", "rubric": "quality_rubric"}
        )

        print(f"BLEU: {results['bleu']:.3f}")
        print(f"ROUGE-L: {results['rouge_l']:.3f}")
        print(f"LLM Judge: {results['llm_judge_avg']:.2f}")
```

## 部署整合

MLflow 支援將模型部署到多種目標平台：

```python
# 將模型部署到 Docker 容器
import mlflow.sklearn

# 儲存模型
mlflow.sklearn.save_model(model, "my_model")

# 建立 Docker 映像檔
mlflow.models.build_docker(
    model_uri="models:/CustomerChurnPredictor/Production",
    image_name="churn-predictor:latest"
)

# 部署到 Kubernetes
mlflow deployments run -t kubernetes \
    --name churn-predictor \
    --model-uri "models:/CustomerChurnPredictor/Production" \
    --config replicas=3 gpu_type=A100
```

## 實戰建議

1. **命名規範**：使用統一的實驗命名規則，例如 `{專案}_{模型}_{日期}`，方便搜尋
2. **資料版本**：使用 `mlflow.log_input()` 記錄資料集版本（Delta Table 或 DVC 的 URI）
3. **自動註冊**：在訓練管線中設定自動註冊條件（accuracy > 0.9 時自動註冊到 Staging）
4. **清理策略**：定期清理舊的實驗版本，保留最近 30 天的執行記錄
5. **標籤系統**：使用 Tags 標註每個 Run 的用途（例如 `purpose: ab_test_control`, `team: ml_infra`）

## 參考資源

- [MLflow Documentation](https://www.google.com/search?q=MLflow+documentation+4.0)
- [MLflow LLM Evaluation Guide](https://www.google.com/search?q=MLflow+LLM+evaluation)
- [MLflow Model Registry Best Practices](https://www.google.com/search?q=MLflow+Model+Registry+best+practices)
- [MLflow + Kubernetes 部署](https://www.google.com/search?q=MLflow+Kubernetes+deployment)
