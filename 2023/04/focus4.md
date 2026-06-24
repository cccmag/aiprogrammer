# 貪婪演算法

## 什麼是貪婪演算法？

貪婪演算法（Greedy Algorithm）是一種簡單而直覺的演算法設計策略：**在每一步選擇中都採取當前看來最好的選擇**，希望最終能得到全域最優解。

想像你去爬山：貪婪策略就是「每次都選擇眼前最陡峭的上坡路」。在有些地形中（如凸函數），這樣做確實會帶你到達山頂；但在某些地形中，你可能會被困在一個小山丘上（區域最優），而非真正的山頂（全域最優）。

## 貪婪演算法的兩個關鍵性質

### 1. 貪婪選擇性質（Greedy Choice Property）

一個問題具有貪婪選擇性質，意味著可以透過一系列局部最優選擇來建構全域最優解。這意味著我們不需要考慮未來——當下最好的選擇就是全域最好的選擇的一部分。

### 2. 最優子結構（Optimal Substructure）

與 DP 一樣，問題的整體最優解包含子問題的最優解。但在貪婪演算法中，我們只做一次選擇，然後遞迴地解決剩下的問題。

## 經典案例：Huffman 編碼

Huffman 編碼是無失真資料壓縮中最經典的演算法之一。

### 問題描述

給定一個字串，為每個字元分配一個二元編碼，使得總編碼長度最短。為了能夠無歧義地解碼，編碼必須是**前綴碼**——沒有任何字元的編碼是其他字元編碼的前綴。

### Huffman 演算法

```python
import heapq
from collections import Counter

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
    def __lt__(self, other):
        return self.freq < other.freq

def huffman_encoding(text):
    freq = Counter(text)
    heap = [HuffmanNode(c, f) for c, f in freq.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)
    # 建立編碼表...
```

### 為什麼它是貪婪的？

Huffman 演算法每一步都合併當前頻率最低的兩個節點，這就是「貪婪」所在。

### 為什麼它得到最優解？

可以證明：在最優編碼樹中，頻率最低的兩個字元一定在最深層，且可以互換位置而不影響最優性。因此每次合併最小頻率節點是安全的。

## 案例：最小生成樹

### Kruskal 演算法

從最小權重的邊開始，如果加入此邊不會形成環，就保留它。不斷重複直到所有頂點連通。

```python
def kruskal(edges, n):
    edges.sort(key=lambda x: x[2])
    parent = list(range(n))
    mst = []
    for u, v, w in edges:
        if find(u) != find(v):
            union(u, v)
            mst.append((u, v, w))
    return mst
```

### Prim 演算法

從一個頂點開始，每次都加入能夠連接到新頂點的最小權重邊。

## 案例：活動選擇問題

給定一堆活動（每個有開始和結束時間），選擇最多的不衝突活動。

貪婪策略：**每次選擇結束時間最早的活動**。

```python
def activity_selection(activities):
    activities.sort(key=lambda x: x[1])
    selected = [activities[0]]
    for act in activities[1:]:
        if act[0] >= selected[-1][1]:
            selected.append(act)
    return selected
```

## 貪婪 vs 動態規劃

| 面向 | 貪婪演算法 | 動態規劃 |
|------|-----------|---------|
| 決策方式 | 每一步做一個選擇 | 考慮所有可能性 |
| 子問題範圍 | 一個子問題 | 多個重疊子問題 |
| 證明難度 | 需要證明貪婪選擇正確性 | 需要定義正確的遞迴式 |
| 時間複雜度 | 通常較低 | 可能較高 |
| 適用範圍 | 少數問題有貪婪選擇性質 | 廣泛的最優化問題 |

## 貪婪演算法的侷限

並非所有最優化問題都適用貪婪策略。例如：
- 背包問題：0/1 背包不適用貪婪，分數背包適用
- 硬幣找零：某些幣值系統下貪婪會失敗

## 總結

貪婪演算法雖然簡單，但證明其正確性往往需要嚴謹的數學推理。當遇到一個問題時，先問問自己：局部最優選擇會不會導致全域最優解？

## 延伸閱讀

- [Greedy Algorithms](https://www.google.com/search?q=greedy+algorithm+tutorial)
- [Huffman Coding Explained](https://www.google.com/search?q=huffman+coding+explained)
- [Kruskal vs Prim](https://www.google.com/search?q=Kruskal+vs+Prim+algorithm)
