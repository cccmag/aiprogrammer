# 頂點覆蓋問題

## 問題定義

頂點覆蓋問題（Vertex Cover Problem）是圖論中的經典問題，也是最著名的 NP-Complete 問題之一。

**給定**：一個無向圖 G = (V, E) 和一個整數 k

**問**：是否存在一個大小 ≤ k 的頂點集合 C ⊆ V，使得每一條邊 e ∈ E 至少有一個端點在 C 中？

直觀上，頂點覆蓋就是一個「監控」所有邊的頂點集合——無論你沿著哪條邊走，至少有一個端點被選中。

## 範例

```
圖：
  1 ── 2
  │    │
  3 ── 4

頂點覆蓋 {2, 3}：
  - 邊 (1,2)：被頂點 2 覆蓋 ✓
  - 邊 (1,3)：被頂點 3 覆蓋 ✓
  - 邊 (2,4)：被頂點 2 覆蓋 ✓
  - 邊 (3,4)：被頂點 3 覆蓋 ✓

頂點覆蓋 {1, 2, 3} 也是有效的，但大小為 3，不是最小覆蓋。
最小頂點覆蓋大小為 2。
```

## NP-Complete 證明

### 在 NP 中

給定一個頂點集合 C，驗證器可以在多項式時間內檢查：

1. C 的大小 ≤ k
2. 對每一條邊 (u, v)，u ∈ C 或 v ∈ C

### NP-Hard 歸約（從 3-SAT）

從 3-SAT 到頂點覆蓋的歸約是經典的 NP-Complete 證明：

**變數元件**：對每個變數 x，建立頂點 x 和 ¬x，並用邊連接。

```
   x ──── ¬x
```

選擇 x 或 ¬x 進入覆蓋對應於將該變數設為 True 或 False。

**子句元件**：對每個子句 C = (l₁ ∨ l₂ ∨ l₃)，建立一個三角形：

```
   l₁ ─── l₂
     \    /
      \  /
       l₃
```

每個子句需要至少選擇 2 個頂點來覆蓋三角形的 3 條邊。

**連接**：將子句中的文字頂點與對應的變數頂點連接。

**參數**：k = 變數數量 + 2 × 子句數量

## 演算法

### 精確演算法（指數時間）

```python
def vertex_cover_bruteforce(graph, k):
    vertices = list(graph.keys())
    from itertools import combinations
    for size in range(1, k + 1):
        for combo in combinations(vertices, size):
            if is_vertex_cover(graph, set(combo)):
                return set(combo)
    return None

def is_vertex_cover(graph, cover):
    for v in graph:
        for u in graph[v]:
            if v not in cover and u not in cover:
                return False
    return True
```

### 近似演算法

頂點覆蓋有一個非常簡單的 2-近似演算法：

```python
def approx_vertex_cover(graph):
    cover = set()
    edges = set()
    for v in graph:
        for u in graph[v]:
            if v < u: edges.add((v, u))
    while edges:
        v, u = edges.pop()
        cover.add(v); cover.add(u)
        edges = {(a, b) for (a, b) in edges
                 if a not in cover and b not in cover}
    return cover
```

這個演算法保證找到的頂點覆蓋大小不超過最小頂點覆蓋的 2 倍。

### 參數化演算法

使用 bounded search tree 技術，可以在 O(2^k × n) 時間內解決：

```python
def vertex_cover_param(graph, k):
    if not graph: return set()
    if k < 0: return None
    # 挑選一條邊 (u, v)
    u, v = None, None
    for node in graph:
        if graph[node]:
            u, v = node, graph[node][0]
            break
    if u is None: return set()
    # 嘗試包含 u
    g1 = remove_vertex(graph, u)
    res1 = vertex_cover_param(g1, k - 1)
    if res1 is not None: return {u} | res1
    # 嘗試包含 v
    g2 = remove_vertex(graph, v)
    res2 = vertex_cover_param(g2, k - 1)
    if res2 is not None: return {v} | res2
    return None
```

## 應用場景

頂點覆蓋在現實中有許多應用：

- **網路安全**：在網路中選擇最少數量的監控節點來覆蓋所有通訊鏈路
- **生物資訊學**：DNA 序列比對
- **排程問題**：資源分配與衝突解決
- **社群網路**：影響力最大化與意見監控

## 延伸閱讀

- [Vertex Cover 演算法](https://www.google.com/search?q=vertex+cover+algorithm+approximation)
- [Vertex Cover NP-Complete 證明](https://www.google.com/search?q=vertex+cover+NP+complete+reduction+SAT)
- [Parameterized Vertex Cover](https://www.google.com/search?q=parameterized+vertex+cover+algorithm)
