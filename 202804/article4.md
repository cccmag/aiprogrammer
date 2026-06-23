# Great Expectations 資料品質監控

## 前言

資料品質是 AI 系統的基石。髒資料進、髒模型出。Great Expectations（GE）是開源社群最受歡迎的資料品質框架，提供宣告式的方式定義、驗證和監控資料品質期望。

## 核心概念

GE 圍繞三個核心抽象：

- **Expectation**：對資料的斷言（如「欄位不為空」）
- **Suite**：一組 Expectation 的集合
- **Checkpoint**：執行驗證並產生文件的配置

```python
import great_expectations as ge
import pandas as pd

# 從 DataFrame 建立 GE 物件
df = pd.DataFrame({
    "user_id": [1, 2, 3, 4, 5],
    "age": [25, 30, None, 22, 35],
    "email": ["a@x.com", "b@x.com", "c@x.com", "d@x.com", "invalid"],
    "signup_date": ["2024-01-01", "2024-01-02", "2024-01-03", "bad-date", "2024-01-05"],
})

ge_df = ge.from_pandas(df)

# 定義期望
ge_df.expect_column_values_to_not_be_null("user_id")
ge_df.expect_column_values_to_be_between("age", min_value=0, max_value=120)
ge_df.expect_column_values_to_match_regex("email", r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]+$")
ge_df.expect_column_values_to_match_strftime_format("signup_date", "%Y-%m-%d")

# 驗證並取得結果
results = ge_df.validate()
print(f"通過: {results['statistics']['successful_expectations']}")
print(f"失敗: {results['statistics']['unsuccessful_expectations']}")
```

## 自動化驗證管線

將 GE 整合進資料管線，每批次自動驗證：

```python
from great_expectations.data_context import DataContext
from great_expectations.checkpoint import SimpleCheckpoint
import json

context = DataContext()

# 建立 Expectation Suite
context.create_expectation_suite("user_data_quality")

# 設定 Datasource
datasource_config = {
    "name": "my_datasource",
    "class_name": "Datasource",
    "execution_engine": {"class_name": "PandasExecutionEngine"},
    "data_connectors": {
        "default_runtime": {
            "class_name": "RuntimeDataConnector",
            "batch_identifiers": ["batch_id"],
        }
    },
}
context.add_datasource(**datasource_config)

# 建立 Checkpoint
checkpoint = SimpleCheckpoint(
    name="daily_validation",
    data_context=context,
    batches=[{
        "batch_kwargs": {
            "datasource": "my_datasource",
            "data_connector": "default_runtime",
            "data_asset_name": "users",
        },
        "expectation_suite_names": ["user_data_quality"],
    }],
)

# 執行驗證
result = checkpoint.run()
if not result["success"]:
    print("資料品質檢查失敗！")
    with open("quality_report.json", "w") as f:
        json.dump(result, f, indent=2)
```

## Data Docs 自動報表

GE 能自動產生 HTML 報表，直觀展示資料品質狀態：

```python
# 建立 Data Docs
context.build_data_docs()

# 報表會輸出到 great_expectations/uncommitted/data_docs/
# 包含每個 Expectation 的通過率、樣本數據和視覺化圖表
```

## 結語

Great Expectations 將「資料品質」從口號變為可自動驗證的工程實踐。搭配 CI/CD 管線，可以在資料進入模型訓練之前就發現問題，避免「垃圾進、垃圾出」的悲劇。

---

**延伸閱讀**

- [Great Expectations 官方文件](https://www.google.com/search?q=Great+Expectations+documentation)
- [資料品質監控最佳實踐](https://www.google.com/search?q=data+quality+monitoring+best+practices)
- [GE 與 Airflow 整合](https://www.google.com/search?q=Great+Expectations+Airflow+integration)
