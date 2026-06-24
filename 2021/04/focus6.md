# Focus 6：Vaex — 記憶體映射的奇蹟

## Vaex 的核心創新

Vaex 採用記憶體映射技術，實現真正意義上的「核外計算」——資料無需載入 RAM，即可進行高效能篩選、聚合、視覺化等操作。這對於處理數十 GB 到數 TB 的資料集極為重要，因為這類資料可能遠超可用記憶體。

## 技術原理

Vaex 使用 HDF5 或 Apache Arrow 作為底層格式，檔案包含完整描述資料結構的中繼資料。讀取操作只載入需要的部分，而非整個檔案。延遲評估和向量化查詢引擎確保即使操作複雜資料，也能保持高效。預先計算的索引和統計數據加速常見查詢。

## 特色功能

表達式系統允許在磁片上進行計算，無需實現原始資料。虛擬欄位在查詢時動態計算，節省儲存空間。高效的繪圖功能可直接對大型資料集生成直方圖、密度圖。時間序列處理有專門優化，支援重採樣和移動窗口計算。

## 與 Pandas 的比較

Vaex 的 API 設計參考了 pandas，對於 pandas 使用者而言學習曲線平緩。然而，並非所有 pandas 功能都有對應；某些操作可能需要不一樣的寫法。Vaex 擅長的操作包括：過濾、選擇、聚合、分組計算。不擅長的操作包括：需要訪問多列的復雜計算、某些複雜的資料改編。

## 使用範例

```python
import vaex as vx

df = vx.open('large_dataset.hdf5')
df_filtered = df[df.amount > 100]
result = df_filtered.groupby('category', agg='count')
```

## 參考資源

- Vaex 官方網站：https://www.google.com/search?q=Vaex+Python+memory+mapped
- Vaex GitHub：https://www.google.com/search?q=Vaex+GitHub+large+data