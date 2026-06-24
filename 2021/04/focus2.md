# Focus 2：Pandas 1.2/1.3 新特性與效能改進

## Pandas 的統治地位

Pandas 是處理結構化資料的事實標準。DataFrame 以二維表格為核心，Series 處理一維資料，Index 提供標籤索引。三者構成 pandas 的核心抽象，支援豐富的資料操作：篩選、聚合、合併、透視、重塑。2021 年的 pandas 1.2/1.3 版本帶來諸多實用改進。

## 1.2 版本的關鍵改進

Pandas 1.2（2020 年 12 月發布）在效能上有明顯進步。GroupBy 操作採用新的聚合引擎，多欄位聚合效能提升顯著。StringMethods 更加強大，正規表達式支援更完整。DatetimeTZDtype 改善時區處理，與 Python 標準庫更加一致。新的 `pandas.testing` 模組簡化測試撰寫。

## 1.3 版本的創新

Pandas 1.3（2021 年 7 月）帶來多項重要更新。新的字串處理 API 基於 pyarrow，處理大文字欄位效能提升數倍。nullable integer 和 string 型態更加穩定，處理缺失值的方式更加優雅。DataFrame.groupby 的 transform 效能進一步優化。Apache Arrow 整合成為核心功能。

## 效能優化技巧

使用 `df.apply()` 時，優先使用軸專門化的函數。`df.sum(axis=1)` 比行級迴圈快得多。避免在 apply 中使用 Python 內建函數，改用向量化替代方案。對於大型 DataFrame，考慮使用 `df.itertuples()` 而非 `df.iterrows()`。適時使用 `df.select_dtypes()` 限制處理的欄位。

## 經典操作模式

```python
import pandas as pd

df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
df.groupby('a').agg({'b': ['sum', 'mean']})  # 多欄位聚合
df.query('a > 1')  # 字串查詢
df.pipe(清洗函數)  # 鏈式處理
```

## 參考資源

- Pandas 官方文件：https://www.google.com/search?q=Pandas+documentation
- Pandas 1.3 Release Notes：https://www.google.com/search?q=Pandas+1.3+release+notes+2021