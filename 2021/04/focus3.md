# Focus 3：Polars — Rust 實現的高速 DataFrame

## Polars 的崛起

Polars 是用 Rust 編寫的 DataFrame 庫，2021 年獲得廣泛關注。基於 Apache Arrow 的記憶體模型，支援無拷貝的列式儲存和多執行緒查詢引擎。效能基準測試顯示，Polars 在多數場景下顯著超越 pandas，特別是涉及大量聚合和連接操作時。

## 核心設計理念

Polars 的設計有三個核心原則：高效、明確、傾聽社群。高效來自 Rust 的記憶體安全和零成本抽象，以及多執行緒並行處理。明確意味著反對隱性行為，所有操作都有清晰定義。社群驅動開發使得各種實務需求能得到快速回應。

## Lazy API 的威力

Polars 提供兩種 API：Eager 和 Lazy。Eager API 類似 pandas，立即執行操作。Lazy API 則構建查詢計劃並進行優化後再執行。Lazy 模式允許 Polars 分析整個查詢圖，進行謂詞下推、投影裁剪、選擇合適的 join 順序等優化。這種設計與傳統 SQL 查詢優化器異曲同工。

## 與 pandas 的相容性

Polars 提供與 pandas 的良好轉換介面。可以從 pandas DataFrame 建立 Polars DataFrame，反之亦然。這讓遷移更加平滑——可以先在關鍵路徑使用 Polars，其他部分保持 pandas。Python API 的設計也盡量與 pandas 相容，降低學習曲線。

## 基礎範例

```python
import polars as pl

df = pl.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
result = (df.lazy()
          .filter(pl.col('a') > 1)
          .groupby('a')
          .agg(pl.col('b').sum())
          .collect())
```

## 參考資源

- Polars 官方網站：https://www.google.com/search?q=Polars+DataFrame+Rust
- Polars GitHub：https://www.google.com/search?q=Polars+GitHub+repository