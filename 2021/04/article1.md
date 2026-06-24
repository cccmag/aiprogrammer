# Article 1：從 pandas 轉換到 Polars 的實務經驗

## 為何要遷移？

pandas 是資料處理的首選工具，但單執行緒的設計使其在處理大型資料集時力不從心。Polars 以 Rust 實現，支援多執行緒並行處理，在許多基準測試中效能提升顯著。對於需要處理百萬級以上列的場景，Polars 是值得考慮的替代方案。

## 遷移策略

建議採用漸進式遷移。首先在非關鍵路徑試用 Polars，驗證功能正確性。然後逐步將效能瓶頸模組替換為 Polars。最後評估全面遷移的效益與成本。過程中保持 pandas 作為備份，確保有問題時可快速回退。

## 語法對照

很多操作有直接對應關係。`df.filter()` 對應 pandas 的 `df[]`。`df.select()` 對應 `df[]`。`df.with_columns()` 對應 `df.assign()`。但也有不一致之處，如 groupby 的語法略有不同。建議查閱官方文檔中的對照表。

## 效能比較

在我們的測試中，Polars 在以下場景有顯著優勢：大型 DataFrame 的篩選和聚合、多欄位連接操作、重複訪問同一資料集。對於小型資料集或需要丰富 pandas 生態的場景，pandas 仍是更好的選擇。

## 參考資源

- Polars Migration Guide：https://www.google.com/search?q=Polars+pandas+migration+guide
- Polars vs Pandas Benchmark：https://www.google.com/search?q=Polars+vs+Pandas+performance+benchmark