# Article 3：Pandas GroupBy 效能優化

## GroupBy 工作原理

pandas 的 groupby 操作分三階段：分割（split）、應用（apply）、合併（combine）。分割將 DataFrame 按鍵分組，應用對每組執行聚合/轉換操作，合併將結果重新組裝。效能瓶頸通常在應用階段，特別是使用自定義函數時。

## 優化策略

首先選擇適當的鍵類型。字串鍵比數值鍵慢；類別型別（category）比 object 型別快。其次使用內建聚合函數而非 apply。`df.groupby('a')['b'].sum()` 比 `df.groupby('a')['b'].apply(np.sum)` 快得多。對於多欄位聚合，一次完成比多次 groupby 更高效。

## 多程序加速

pandas 的 groupby 支援使用多核心。通過設定 `pandas.set_option('use_threads', True)` 或使用 modin、dask.dataframe 可實現並行處理。但並行化有額外協調成本，只有處理大型資料集時才有淨收益。

## 升級到新版本

pandas 1.3 的 groupby 效能較之前版本有明顯提升。特別是 transform 操作和带有多層索引的 groupby。如果效能是問題，優先考慮升級 pandas 版本。

## 參考資源

- pandas GroupBy Documentation：https://www.google.com/search?q=pandas+groupby+performance
- pandas 1.3 Release Notes：https://www.google.com/search?q=pandas+1.3+groupby+improvements