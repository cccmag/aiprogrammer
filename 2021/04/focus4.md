# Focus 4：Dask — 大規模資料處理

## 為什麼需要 Dask？

當資料量超過單機記憶體時，需要分散式處理能力。傳統方案如 Spark 功能強大但部署複雜。Dask 提供輕量級替代方案：用純 Python 實現，與 numpy/pandas API 高度相容，讓小幅調整現有程式碼就能處理超大型資料。

## 核心概念

Dask 由三部分組成：延遲評估的任務圖、多執行緒/多程序排程器、以及豐富的集合類別（dask.array、dask.dataframe、dask.delayed）。任務圖描述計算依賴關係，排程器負責將任務分配到可用資源，集合類別提供高層 API。關鍵洞察是：將大型問題分解為可在單機處理的小塊，然後協調這些小塊的執行。

## Dask Array 對應 NumPy

dask.array 是 NumPy 的替代品，支援大多數 NumPy API。用 `dask.array.from_array()` 將 numpy 陣列轉換為 dask 陣列，或用 `da.ones()`、`da.random.random()` 直接創建。計算時調用 `.compute()` 取得結果。對於大型影像、氣候資料等科學計算，dask.array 是理想選擇。

## Dask DataFrame 對應 Pandas

dask.dataframe 提供類似 pandas 的 API。`dd.read_csv()` 可處理無法放入記憶體的 CSV 檔案。groupby、join、揉作等操作自動分割執行。某些操作如 sort 需要資料重分區，會有額外開銷。理解分區概念很重要——過度細碎的分區帶來協調成本，過於粗獷的分區則限制平行度。

## 分散式叢集

dask.distributed 提供真正的分散式能力。可在叢集上部署 Dask worker，客戶端提交任務並收集結果。支援即時監控、資源管理和容錯恢復。對於需要處理 TB 級資料的場景，Dask 叢集是值得考慮的架構。

## 參考資源

- Dask 官方網站：https://www.google.com/search?q=Dask+Python+distributed+computing
- Dask Documentation：https://www.google.com/search?q=Dask+documentation+DataFrame