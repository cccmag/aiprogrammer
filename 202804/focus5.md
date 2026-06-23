# 資料品質監控（2020-2028）

## 資料品質危機

2020 年，一篇來自 Google 的論文揭露了驚人數據：在某些 ML 系統中，**超過 80% 的模型效能衰退源自資料品質問題，而非模型問題**。資料品質從邊緣問題一躍成為核心關注。

### 常見的資料品質問題

| 問題類型 | 影響 | 發生頻率 |
|---------|------|---------|
| 缺失值 | 模型偏差、預測不準 | 非常高 |
| 重複資料 | 訓練集偏差、評估失真 | 高 |
| 離群值 | 模型不穩定 | 中 |
| 標籤錯誤 | 監督學習崩潰 | 中 |
| 資料偏移 | 模型過時、預測失準 | 持續發生 |

## Great Expectations

Great Expectations 是 2020 年開源的資料品質框架，將「單元測試」的概念引入資料世界：

```python
import great_expectations as gx

context = gx.get_context()
datasource = context.sources.add_pandas("my_data")
data_asset = datasource.add_dataframe_asset("my_asset")

batch = data_asset.get_batch(dataframe=df)

# 定義期望
expectation = batch.expect_column_values_to_not_be_null("user_id")
assert expectation["success"]

batch.expect_column_values_to_be_between("age", 0, 120)
batch.expect_column_values_to_be_unique("email")
batch.expect_column_mean_to_be_between("amount", 0, 10000)
```

Great Expectations 的關鍵設計：
- **Expectation Suite**：一組資料品質斷言，可重用、可版本控制
- **Data Docs**：自動生成 HTML 品質報告
- **Result**：每次檢驗都可記錄到中繼資料儲存

## 資料偏移檢測

資料偏移（Data Drift）是即時系統中最致命的品質問題。模型上線時表現良好，數週後卻大幅衰退——不是模型變了，是資料變了。

### 特徵偏移 vs. 概念偏移

```
特徵偏移（Feature Drift）：P(特徵) 改變
概念偏移（Concept Drift）：P(標籤|特徵) 改變

檢測方法：
  統計檢定：KS 檢定、JS 散度
  分布比較：訓練集 vs 線上推論資料
  監控指標：預測分布、信心分數
```

## 品質監控系統設計

```python
class DataQualityMonitor:
    def __init__(self):
        self.rules = []

    def add_rule(self, name: str, check_fn):
        self.rules.append((name, check_fn))

    def check(self, data: list[dict]) -> dict:
        results = {}
        for name, fn in self.rules:
            results[name] = fn(data)
        results["overall_score"] = (
            sum(v for v in results.values() if isinstance(v, float)) / len(self.rules)
        )
        return results

# 使用
monitor = DataQualityMonitor()
monitor.add_rule("no_nulls", lambda d: 1 - sum(1 for r in d if None in r.values()) / len(d))
```

## 實務建議

1. **定義 SLA**：每個資料集都應該有明確的品質 SLA
2. **自動化檢查**：管線中嵌入品質檢查，失敗時告警而非靜默跳過
3. **趨勢追蹤**：記錄每次檢查結果，觀察品質趨勢
4. **根本原因**：品質問題發生時，快速追溯來源

## 延伸閱讀

- [Great Expectations](https://www.google.com/search?q=Great+Expectations+data+quality+framwork)
- [Data Drift Detection](https://www.google.com/search?q=data+drift+detection+machine+learning)
- [ML Data Quality Monitoring](https://www.google.com/search?q=ML+data+quality+monitoring+best+practices)

---

*本篇文章為「AI 程式人雜誌 2028 年 4 月號」資料工程系列之五。*
