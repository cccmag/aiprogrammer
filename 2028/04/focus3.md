# 特徵儲存設計與實作（2019-2028）

## 什麼是特徵儲存？

特徵儲存（Feature Store）集中管理 ML 特徵，解決「特徵重複計算」和「訓練/推論不一致」兩大痛點。

在 2019 年以前，各 ML 團隊各自管理特徵，導致：
- 相同特徵被不同團隊重複計算
- 訓練與推論使用不同的特徵邏輯（訓練/推論偏差）
- 特徵缺乏版本管理，難以追溯

## 特徵儲存的核心功能

```
┌─────────────────────────────────────────┐
│           Feature Store                 │
├─────────────────────────────────────────┤
│  Online API          Offline Store      │
│  (低延遲推論)        (大批量訓練)       │
│  ┌──────────┐       ┌──────────┐       │
│  │ Redis /   │       │ S3 /     │       │
│  │ DynamoDB  │       │ Parquet  │       │
│  └──────────┘       └──────────┘       │
├─────────────────────────────────────────┤
│  點時間查詢（Point-in-Time Lookup）    │
│  特徵血緣追溯                           │
│  特徵版本管理                           │
└─────────────────────────────────────────┘
```

**點時間查詢**是最關鍵的設計：訓練資料需要「某個時間點」的特徵值，而非「當前」值，才能避免資料洩漏。

## Feast：開源特徵儲存

Feast 是 2019 年由 Google 與 Gojek 聯合開源的專案，是最廣泛使用的開源特徵儲存：

```python
from feast import FeatureStore, Entity, FeatureView, Field

store = FeatureStore(repo_path=".")
user = Entity(name="user_id", value_type=Int64)
user_features = FeatureView(
    name="user_transaction_features",
    entities=[user],
    schema=[Field(name="avg_amount", dtype=Float32)],
)
features = store.get_online_features(
    features=["user_transaction_features:avg_amount"],
    entity_rows=[{"user_id": 1001}],
).to_dict()
```

## 特徵儲存的演進

| 年份 | 專案 | 貢獻 |
|------|------|------|
| 2019 | Feast | 第一個開源特徵儲存 |
| 2020 | Tecton | 商業化特徵平台 |
| 2021 | Hopsworks | ML 平台內建特徵儲存 |
| 2022 | ByteDance | 大規模特徵工程 |
| 2024 | OpenFeature | 規範標準化 |

2022 年後，特徵儲存逐漸整合進更大的 ML 平台。2025 年趨勢是**特徵即服務**。

## 自製簡易特徵儲存

```python
class FeatureStore:
    def __init__(self):
        self._store, self._history = {}, {}

    def set_feature(self, key: str, value: float, ts: float):
        self._store[key] = value
        self._history.setdefault(key, []).append((ts, value))

    def get_online(self, key: str) -> float:
        return self._store.get(key, 0.0)

    def get_point_in_time(self, key: str, at: float) -> float:
        for ts, val in reversed(self._history.get(key, [])):
            if ts <= at:
                return val
        return 0.0
```

## 延伸閱讀

- [Feast Feature Store](https://www.google.com/search?q=Feast+feature+store+open+source)
- [Tecton Feature Platform](https://www.google.com/search?q=Tecton+feature+platform+ML)
- [Point-in-Time Correctness](https://www.google.com/search?q=point+in+time+correctness+feature+store)

---

*本篇文章為「AI 程式人雜誌 2028 年 4 月號」資料工程系列之三。*
