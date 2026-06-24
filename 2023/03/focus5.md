# 圖論基礎

## 什麼是圖？

圖（Graph）由頂點（Vertex / Node）與邊（Edge）組成，記為 G = (V, E)。圖可以用來表示現實世界中各種關係，例如社交網路中的好友關係、交通路線圖中的城市與道路、網頁之間的超連結、電路中的元件連接等。圖論是電腦科學中最重要也最通用的抽象工具之一，廣泛應用於網路分析、路徑規劃、推薦系統等領域。

## 圖的分類

**有向圖 vs 無向圖**：有向圖的邊有方向，u→v 與 v→u 不同。無向圖的邊無方向，u—v 表示雙向連通。有向圖常用於表示依賴關係或流程方向，如課程先修條件與工作排程。

**加權圖 vs 無權圖**：加權圖的邊帶有權重（距離、成本、時間等），例如地圖上路段的長度。無權圖所有邊權重相同，或者不考慮權重值。

**連通圖 vs 不連通圖**：連通圖中任意兩頂點間都存在路徑。不連通圖由多個連通分量（Connected Component）組成。

## 圖的表示法

**鄰接矩陣（Adjacency Matrix）**：V×V 的二維陣列，matrix[i][j] 表示頂點 i 到 j 是否有邊。空間 O(V²)，適合稠密圖（邊數接近 V²）。檢查兩頂點是否相連只需 O(1)。

**鄰接串列（Adjacency List）**：為每個頂點維護一個串列，儲存相鄰頂點的編號。空間 O(V+E)，適合稀疏圖（邊數接近 V）。走訪所有鄰居的效率高。

## 圖的基本性質

**度（Degree）**：無向圖中頂點連接的邊數。有向圖分入度（indegree）與出度（outdegree）。總入度等於總出度等於邊數。

**路徑（Path）**：相鄰頂點間有邊相連的序列。簡單路徑不重複經過頂點。

**環（Cycle）**：起點與終點相同的路徑。無環有向圖稱為 DAG（Directed Acyclic Graph），在拓撲排序中非常重要。

**連通分量**：無向圖中最大的連通子圖。有向圖則分為強連通分量（SCC, Strongly Connected Component）。

## 延伸閱讀

- https://www.google.com/search?q=graph+data+structure+types+properties+directed+undirected+weighted+graph
- https://www.google.com/search?q=adjacency+matrix+vs+adjacency+list+空間+時間+複雜度+比較+選擇
- https://www.google.com/search?q=圖論+基礎+頂點+邊+度+環+連通分量+DAG+教學+範例
