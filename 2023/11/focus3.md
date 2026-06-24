# 3. 來源編碼定理與 Huffman

## 來源編碼定理

Shannon 的第一個編碼定理（來源編碼定理，Source Coding Theorem）回答了這個問題：在無失真壓縮下，一個符號平均需要多少位元？

定理指出，對於一個熵為 $H(X)$ 的離散無記憶來源，任何唯一可解碼的編碼方案的平均編碼長度 $\bar{L}$ 滿足：

$$\bar{L} \geq H(X)$$

而且存在一種編碼方案使得 $\bar{L}$ 可以任意接近 $H(X)$。換句話說，**熵是無失真壓縮的理論極限**。

## 前綴碼

為了讓編碼唯一可解，我們使用前綴碼（Prefix Code）：沒有任何碼字是其他碼字的前綴。這樣一來，編碼後的位元串可以被唯一地解碼。Huffman 演算法就是建構最佳前綴碼的經典方法。

## Huffman 編碼演算法

Huffman 編碼由 David A. Huffman 在 1952 年提出，透過以下步驟建構最佳前綴碼：

1. 計算每個符號的出現頻率
2. 將每個符號視為葉節點，權重為其頻率
3. 重複合併兩個權重最小的節點，新節點的權重為兩者之和
4. 合併時，左分支標記為 0，右分支標記為 1
5. 從根到葉的路徑上的標記即為該符號的編碼

## 範例

符號 A、B、C、D 的機率分別為 0.5、0.25、0.125、0.125。

```
熵 H = 0.5×1 + 0.25×2 + 0.125×3 + 0.125×3 = 1.75 bits
Huffman 平均長度 = 0.5×1 + 0.25×2 + 0.125×3 + 0.125×3 = 1.75 bits
```

在這個範例中，Huffman 編碼達到了熵極限。

## Python 實作

```python
from heapq import heapify, heappush, heappop

def huffman(symbols_with_probs):
    heap = [[w, [sym, ""]] for sym, w in symbols_with_probs]
    heapify(heap)
    while len(heap) > 1:
        lo = heappop(heap)
        hi = heappop(heap)
        for pair in lo[1:]: pair[1] = "0" + pair[1]
        for pair in hi[1:]: pair[1] = "1" + pair[1]
        heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    return sorted(heappop(heap)[1:], key=lambda p: len(p[1]))
```

## 參考資源

- https://www.google.com/search?q=Shannon+source+coding+theorem+entropy+optimal+compression+limit
- https://www.google.com/search?q=Huffman+coding+algorithm+prefix+code+optimal+lossless+compression
- https://www.google.com/search?q=Huffman+tree+construction+example+step+by+step+tutorial
