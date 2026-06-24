# 圖著色問題

## 問題定義

圖著色問題（Graph Coloring Problem）是圖論和計算理論中的經典問題。

**給定**：一個無向圖 G = (V, E) 和一個整數 k

**問**：是否存在一個 k-著色方案，為每個頂點分配一種顏色（從 1 到 k），使得相鄰頂點顏色不同？

如果存在這樣的著色方案，我們說 G 是 k-可著色的。

## 特殊情況

- **1-著色**：只有在沒有邊的圖上才有可能
- **2-著色**：圖必須是二分圖（bipartite graph），可以用 BFS 在 O(V+E) 時間內判斷
- **3-著色**：NP-Complete

## 從地圖到圖

圖著色問題起源於地圖著色：給定一張地圖，相鄰的區域必須塗上不同顏色。這個問題可以自然地轉換為圖著色問題——每個區域對應一個頂點，相鄰的區域之間有邊連接。

著名的**四色定理**（Four Color Theorem）聲明：任何平面圖都可以用 4 種顏色著色。這個定理在 1976 年被 Kenneth Appel 和 Wolfgang Haken 用電腦輔助證明，是第一個依賴電腦的數學證明。

## 3-著色是 NP-Complete

### 在 NP 中

給定一個著色方案，驗證器可以在多項式時間內檢查每條邊的兩個端點顏色是否不同。

### NP-Hard 歸約（從 3-SAT）

從 3-SAT 歸約到 3-著色：

**調色盤元件**：三個特殊頂點 T（True）、F（False）、R（Reference），互相連接：

```
  T ─── R
   \   /
    \ /
     F
```

**變數元件**：對每個變數 x，建立頂點 x 和 ¬x，並設定：

```
  x ─── T ─── ¬x
```

x 和 ¬x 不能著色為 T，但可以著色為 F 或 R。這保證了 x 和 ¬x 取值相反。

**子句元件**：對每個 3-子句 (a ∨ b ∨ c)，使用一個 5-頂點的 OR-gadget 來模擬邏輯或。

```
     a ─── o₁
          /  \
         R ── o₂
          \  /
     b ─── o₃
          /  \
         R ── o₄
          \  /
     c ─── o₅
```

如果 a、b、c 都是 F，則無法完成著色；否則可以。

## 著色問題的演算法

### 貪婪著色

```python
def greedy_coloring(graph, order):
    colors = {}
    for v in order:
        used = set()
        for u in graph[v]:
            if u in colors:
                used.add(colors[u])
        for c in range(len(graph)):
            if c not in used:
                colors[v] = c
                break
    return colors
```

貪婪著色在最壞情況下可能需要 n 種顏色，但對於某些圖和適合的頂點順序可以接近最優。

### 精確演算法

```python
def is_k_colorable(graph, k, assign=None, idx=0):
    if assign is None:
        assign = {}
        vertices = list(graph.keys())
    else:
        vertices = list(graph.keys())
    if idx == len(vertices):
        return assign
    v = vertices[idx]
    used = {assign[u] for u in graph[v] if u in assign}
    for c in range(k):
        if c not in used:
            assign[v] = c
            res = is_k_colorable(graph, k, assign, idx + 1)
            if res: return res
            del assign[v]
    return None
```

這個演算法的時間複雜度是 O(k^n)，僅在 n 很小時實用。

## 圖著色的應用

- **排課系統**：將課程安排到時段，衝突的課程必須在不同時段
- **暫存器分配**：編譯器中將變數分配到暫存器
- **頻率分配**：無線通訊中分配不互相干擾的頻率
- **時間表編排**：考試時間表、會議排程
- **Sudoku**：數獨本質上是一個部分著色問題

## 延伸閱讀

- [Graph Coloring Algorithm](https://www.google.com/search?q=graph+coloring+algorithm+approximation)
- [3-Coloring NP-Completeness](https://www.google.com/search?q=3+coloring+NP+complete+reduction)
- [Four Color Theorem](https://www.google.com/search?q=four+color+theorem+proof+history)
