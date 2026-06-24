# Feast 特徵儲存實戰

## 前言

特徵儲存（Feature Store）是 AI 基礎設施的核心元件，解決了訓練和推論之間特徵不一致的問題。Feast 是開源領域最受歡迎的特徵儲存框架，由 Tecton 團隊維護，支援離線和線上特徵服務。

## 為什麼需要特徵儲存？

在傳統 ML 工作流中，資料科學家常重複撰寫相同的特徵計算邏輯，導致訓練和推論時的特徵值不一致。特徵儲存作為統一的中介層，一次定義、隨處使用。

## Feast 核心概念

Feast 有三個核心抽象的實體：

- **Feature View**：定義特徵來源和轉換邏輯
- **Entity**：特徵的索引鍵
- **Feature Service**：提供統一的特徵查詢介面

```python
from datetime import datetime, timedelta
from feast import Entity, FeatureView, FeatureService, Field
from feast.types import Float32, Int64
from feast.infra.offline_stores.file_source import FileSource

# 定義實體
user = Entity(name="user_id", description="用戶 ID")

# 定義資料來源
user_stats_source = FileSource(
    path="/data/user_stats.parquet",
    timestamp_field="event_timestamp",
)

# 定義特徵視圖
user_stats_fv = FeatureView(
    name="user_statistics",
    entities=[user],
    ttl=timedelta(days=1),
    schema=[
        Field(name="total_orders", dtype=Int64),
        Field(name="avg_order_value", dtype=Float32),
        Field(name="lifetime_value", dtype=Float32),
    ],
    source=user_stats_source,
)

# 定義特徵服務
feature_service = FeatureService(
    name="user_features",
    features=[user_stats_fv]
)
```

## 離線與線上推論

Feast 支援離線批次推論和即時線上推論：

```python
# 離線擷取（用於訓練）
import feast

store = feast.FeatureStore(repo_path="./feature_repo")
training_df = store.get_historical_features(
    entity_df="SELECT user_id, event_timestamp FROM my_entity_table",
    features=feature_service,
).to_df()

print(training_df.head())
```

```python
# 線上擷取（用於即時推論）
feature_vector = store.get_online_features(
    features=feature_service,
    entity_rows=[{"user_id": 123}]
).to_dict()

print(feature_vector)
```

## Redis 作為線上儲存

Feast 支援 Redis、DynamoDB 等多種線上儲存後端：

```python
# feature_store.yaml
project: my_project
provider: gcp
online_store:
  type: redis
  connection_string: "redis://localhost:6379"
offline_store:
  type: file
```

## 結語

Feast 讓特徵工程從混亂的筆記本腳本進化為可複用、可發現的基礎設施。無論是中小團隊還是大型企業，導入特徵儲存都能顯著提升 ML 開發效率與模型可靠性。

---

**延伸閱讀**

- [Feast 官方文件](https://www.google.com/search?q=Feast+feature+store+documentation)
- [特徵儲存設計模式](https://www.google.com/search?q=feature+store+design+pattern+ML)
- [Tecton 特徵平台介紹](https://www.google.com/search?q=Tecton+feature+platform)
