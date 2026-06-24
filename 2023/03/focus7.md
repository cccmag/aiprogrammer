# 雜湊與完美雜湊

## 什麼是雜湊？

雜湊（Hashing）是一種將任意大小的輸入映射到固定大小輸出的技術。雜湊函數（Hash Function）將鍵（Key）轉換為陣列索引，讓我們能在 O(1) 的平均時間內完成插入、刪除與搜尋操作。雜湊表是實現字典（Dictionary）ADT 最常見的方式，也是許多高效能系統如快取、資料庫、編譯器的核心元件。

## 雜湊表的結構

雜湊表使用陣列儲存鍵值對。插入時先計算鍵的雜湊值，透過取模運算得到陣列索引，再將鍵值對存入該位置。搜尋時計算同樣的雜湊值，直接存取目標位置。

一個好的雜湊函數需具備：確定性（同樣輸入產生同樣輸出）、均勻性（輸出均勻分布在範圍內）、高效性（計算快速）。常見的雜湊函數有 DJB2、MurmurHash、CityHash 與 SipHash 等。

## 碰撞處理

根據鴿籠原理，當鍵的數量超過陣列大小時，碰撞（Collision）是不可避免的。常見的處理方式：

1. **鏈結法（Chaining）**：每個陣列位置維護一個鏈結串列或動態陣列，碰撞元素串在同一個位置。實作簡單，動態成長。

2. **開放定址法（Open Addressing）**：當位置被佔用時，尋找下一個空位。包含線性探測（逐一檢查）、二次探測（間隔遞增）、雙重雜湊（第二雜湊函數決定步長）。

## 完美雜湊

完美雜湊（Perfect Hashing）能完全避免碰撞。對於靜態鍵集合，可以設計雜湊函數使每個鍵映射到不同位置。最小完美雜湊函數（Minimal Perfect Hash Function）不僅無碰撞，且映射範圍恰好等於鍵的數量，完全沒有空間浪費，特別適合字典中的關鍵字雜湊。

## 負載因子與動態擴容

負載因子 = 元素數量 / 陣列大小。超過門檻值（通常 0.75）時進行 rehashing。雖然耗時 O(n)，但平均攤銷後仍接近 O(1)。

## 延伸閱讀

- https://www.google.com/search?q=hash+table+load+factor+rehashing+dynamic+resizing+策略+門檻值
- https://www.google.com/search?q=perfect+hashing+minimal+perfect+hash+function+靜態+字典+應用
- https://www.google.com/search?q=雜湊表+碰撞處理+鏈結法+開放定址法+效能+比較+優缺點
