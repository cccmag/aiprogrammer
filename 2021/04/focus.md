# Python 資料科學工具鏈 2021 — 主題介紹

## 為什麼關注 Python 資料工具？

Python 在資料科學領域的主導地位已無需質疑。然而，工具鏈的快速演進意味著工程師需要持續學習。2021 年是個關鍵節點：傳統的 pandas 正面臨新興對手的挑戰，記憶體映射技術讓超大型資料處理成為常態，而分散式運算的門檻也在持續降低。

## 工具生態全景

現代 Python 資料工具可分為幾個層次。核心陣列庫 NumPy 支撐一切，其向量化思維影響深遠。pandas 是處理結構化資料的默認選擇，1.3 版帶來諸多改進。Polars 以 Rust 實現，效能表現亮眼。Vaex 擅長記憶體映射，適合超大型資料。Dask 提供分散式平行處理能力。Modin 嘗試用分散式引擎加速 pandas。PyArrow 是跨語言資料交換的樞紐。

## 效能與易用性的權衡

選擇工具時需考量多重因素。pandas 的豐富生態和社群無可匹敵，但單執行緒限制使其在大型資料上力不從心。Polars 效能出色但生態尚在成熟。Vaex 無需將資料載入記憶體，但自訂分析靈活性受限。Dask 強大但部署複雜度較高。理解每種工具的設計哲學，才能做出正確選擇。

## 本期導覽

[focus1](focus1.md) 回顧 NumPy 的核心概念與 2021 年更新。[focus2](focus2.md) 深入探討 pandas 1.2/1.3 的新特性。[focus3](focus3.md) 介紹新興的 Polars。[focus4](focus4.md) 展示 Dask 的分散式處理能力。[focus5](focus5.md) 討論資料流水線的架構設計。[focus6](focus6.md) 探索 Vaex 的記憶體映射奇蹟。[focus7](focus7.md) 宏觀審視 Python 資料科學生態的演進。十篇 [article](articles.md) 提供實務經驗與深入分析。

## 參考資源

- Pandas 官方文件：https://www.google.com/search?q=Pandas+documentation+2021
- Polars 官方網站：https://www.google.com/search?q=Polars+Rust+DataFrame+homepage
- Dask 官方文件：https://www.google.com/search?q=Dask+Python+distributed+computing