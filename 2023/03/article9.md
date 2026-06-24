# 雜湊碰撞處理

## 為什麼會有碰撞？

雜湊函數將無限的輸入空間映射到有限的輸出空間。根據鴿籠原理（Pigeonhole Principle），當輸入數量超過輸出範圍時，必定會發生碰撞。即使輸入數量小於輸出範圍，不良的雜湊函數也可能導致碰撞。良好的碰撞處理機制是雜湊表格效能的關鍵因素。

## 鏈結法（Chaining）

每個雜湊表位置維護一個鏈結串列或動態陣列，發生碰撞時新元素直接加入該位置的串列。

**優點**：
- 實作非常簡單，直觀易懂。
- 刪除操作容易，直接從串列中移除即可。
- 負載因子可以大於 1，效能會下降但不會崩潰。
- 不要求陣列大小為質數。

**缺點**：
- 需要額外的指標/引用儲存空間。
- 快取不友好：節點分散在記憶體各處，無法充分利用 CPU 快取。
- 當串列長度變長時，查詢效率退化為 O(n)。

## 開放定址法（Open Addressing）

所有資料都儲存在陣列本身，不需要額外的鏈結結構。當位置被佔用時，按照規則尋找下一個空位。

**線性探測（Linear Probing）**：逐一檢查 i+1, i+2, i+3... 實作最簡單，但容易產生主聚集（Primary Clustering）。

**二次探測（Quadratic Probing）**：檢查 i + 1², i + 2², i + 3²... 可減少聚集，但可能無法遍歷所有位置。

**雙重雜湊（Double Hashing）**：使用 h₂(key) 決定步長，探測序列為 i + h₂(key), i + 2·h₂(key)... 最均勻的開放定址法。

## 再雜湊（Rehashing）

當負載因子超過門檻值（通常 0.70~0.75）時，建立更大的陣列（通常為原來兩倍），重新計算所有元素的位置。雖然一次 rehashing 需要 O(n) 時間，但發生頻率不高（約 log n 次），平均攤銷後仍接近 O(1)。

## Python 的 dict 實作

Python 3.6+ 的字典使用隨機化雜湊與改良的開放定址法。3.7+ 保證插入順序。底層使用緊湊陣列結構，大幅減少記憶體使用，是 Python 最常用的資料結構之一。

## 延伸閱讀

- https://www.google.com/search?q=hash+collision+chaining+vs+open+addressing+比較+優缺點+效能
- https://www.google.com/search?q=linear+probing+quadratic+probing+double+hashing+差異+優劣
- https://www.google.com/search?q=雜湊碰撞+鏈結法+開放定址法+再雜湊+Python+dict+實作
