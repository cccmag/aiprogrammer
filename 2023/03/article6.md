# 最小生成樹：Kruskal 與 Prim

## 什麼是最小生成樹？

最小生成樹（Minimum Spanning Tree, MST）是連通加權圖中，連接所有頂點且邊權重總和最小的樹（無環連通子圖）。MST 在網路設計、管線規劃、電路設計與運輸系統等領域有廣泛應用。例如，設計一個連接所有城市的公路網路使得總造價最低，就是一個典型的 MST 問題。

## Kruskal 演算法

Kruskal 演算法使用貪婪策略，每次選擇權重最小的邊，只要加入後不會形成環，就將該邊納入 MST。這個演算法由 Joseph Kruskal 在 1956 年發表。

**步驟**：
1. 將圖中所有邊按權重從小到大排序。
2. 初始化一個空的 MST（邊集合）。
3. 從最小權重的邊開始檢查：如果加入該邊不會在 MST 中形成環，則加入。
4. 重複直到 MST 包含 V-1 條邊或所有邊都已檢查完畢。

**環的檢查**：使用 Union-Find（並查集）資料結構來判斷兩個頂點是否已經連通。每個頂點初始屬於自己的集合，加入邊時將端點集合合併。若端點已在同一集合，則加入該邊會形成環。Union-Find 經過路徑壓縮與合併優化後，接近 O(1) 的攤銷時間。

**時間複雜度**：O(E log E)，主要來自排序步驟。

## Prim 演算法

Prim 演算法從一個起點開始，每次選擇連接「已在 MST 中的頂點集合」與「未在 MST 中的頂點集合」的最小權重邊。由 Vojtěch Jarník 在 1930 年提出，後被 Robert Prim 獨立發現。

**步驟**：
1. 選擇任意起點，加入 MST 集合。
2. 使用最小堆積儲存所有連接已選與未選頂點的邊。
3. 取出權重最小的邊，若目標頂點尚未加入則加入 MST。
4. 將新頂點的所有邊加入堆積。
5. 重複直到所有頂點都加入 MST。

**時間複雜度**：使用二元堆積為 O(E log V)，使用斐波那契堆積可達 O(E + V log V)。

## 比較總結

| 特性 | Kruskal | Prim |
|------|---------|------|
| 策略 | 以邊為中心，全域選邊 | 以頂點為中心，增量擴展 |
| 核心資料結構 | Union-Find（並查集） | 優先佇列（最小堆積） |
| 適合圖類型 | 稀疏圖（E ≈ V） | 稠密圖（E ≈ V²） |
| 時間複雜度 | O(E log E) | O(E log V) |

## 延伸閱讀

- https://www.google.com/search?q=Kruskal+algorithm+Union+Find+minimum+spanning+tree+MST+範例
- https://www.google.com/search?q=Prim+algorithm+priority+queue+minimum+spanning+tree+步驟
- https://www.google.com/search?q=最小生成樹+Kruskal+Prim+MST+差異+比較+圖解
