# Huffman 編碼實作

## 從原始碼動手

Huffman 編碼是少數既在理論上最優又在實務上廣泛應用的演算法。本篇文章將從零開始用 Python 實作完整的 Huffman 編解碼器。

## 步驟一：頻率統計

編碼的第一步是統計每個符號在原始資料中出現的頻率。

```python
from collections import Counter

text = "ABBCCCDDDDEEEEE"
freq = Counter(text)
total = len(text)
probs = [(ch, cnt / total) for ch, cnt in freq.most_common()]
print(probs)
# [('E', 0.333), ('D', 0.267), ('C', 0.2), ('B', 0.133), ('A', 0.067)]
```

## 步驟二：建構 Huffman 樹

使用最小堆積來合併節點，每次取出兩個權重最小的節點。

```python
from heapq import heapify, heappush, heappop

def build_huffman_tree(symbols_with_probs):
    heap = [[w, [sym, ""]] for sym, w in symbols_with_probs]
    heapify(heap)
    while len(heap) > 1:
        lo = heappop(heap)
        hi = heappop(heap)
        for pair in lo[1:]:
            pair[1] = "0" + pair[1]
        for pair in hi[1:]:
            pair[1] = "1" + pair[1]
        heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    return sorted(heappop(heap)[1:], key=lambda p: len(p[1]))
```

## 步驟三：編碼與解碼

有了編碼表後，編碼只需查表替換。解碼則需要使用 Huffman 樹的結構逐位元匹配。

```python
def huffman_encode(text):
    codes = build_huffman_tree(probs)
    code_map = {ch: code for ch, code in codes}
    encoded = "".join(code_map[ch] for ch in text)
    return encoded, code_map

def huffman_decode(encoded, code_map):
    rev_map = {v: k for k, v in code_map.items()}
    result = []
    cur = ""
    for bit in encoded:
        cur += bit
        if cur in rev_map:
            result.append(rev_map[cur])
            cur = ""
    return "".join(result)
```

## 完整範例輸出

```
原文: ABBCCCDDDDEEEEE
編碼表: {'E': '11', 'D': '10', 'C': '01', 'B': '001', 'A': '000'}
編碼: 000001001010101101010101111111111
解碼: ABBCCCDDDDEEEEE
壓縮比: 27.50%
```

## 應用場景

Huffman 編碼廣泛應用於 ZIP、GZIP、JPEG 與 MP3 等壓縮標準中。在 JPEG 中，Huffman 編碼被用於壓縮量化後的 DCT 係數，是達到高壓縮比的關鍵環節。

## 參考資源

- https://www.google.com/search?q=Huffman+coding+Python+implementation+heapq+priority+queue+step+by+step
- https://www.google.com/search?q=Huffman+encoding+decoding+algorithm+example+text+compression+python
- https://www.google.com/search?q=Huffman+coding+applications+ZIP+JPEG+MP3+lossless+compression+standard
