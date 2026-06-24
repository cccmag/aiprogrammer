# Huffman 編碼

## 什麼是 Huffman 編碼？

Huffman 編碼是一種無失真資料壓縮演算法，由 David A. Huffman 在 1952 年提出。這是貪婪演算法的經典案例，同時也是資訊理論中的重要基礎。

核心思想：**為頻繁出現的字元分配較短的編碼，為罕見的字元分配較長的編碼**。

## 前綴碼的性質

Huffman 編碼產生的是一種**前綴碼**（Prefix Code）——沒有任何字元的編碼是其他字元編碼的前綴。這保證了解碼的無歧義性。

例如：如果 A 的編碼是 0，則沒有任何其他字元的編碼以 0 開頭。這樣我們在解碼時就不需要分隔符號。

## Huffman 演算法詳解

### 步驟

1. 統計每個字元出現的頻率
2. 將每個字元視為一個節點，權重為其頻率
3. 重複以下步驟直到只剩一棵樹：
   a. 選取權重最小的兩個節點
   b. 合併它們為一個新節點（權重為兩者之和）
   c. 將新節點放回集合中
4. 從樹根到葉子的路徑即為編碼（左 0 右 1）

### Python 實作

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
    root = heap[0]
    codes = {}
    def dfs(node, code):
        if node.char is not None:
            codes[node.char] = code
            return
        if node.left:
            dfs(node.left, code + '0')
        if node.right:
            dfs(node.right, code + '1')
    dfs(root, '')
    encoded = ''.join(codes[c] for c in text)
    return encoded, codes
```

### 範例

字串："A SIMPLE STRING TO BE ENCODED"

統計頻率後建構 Huffman 樹，得到編碼表：
- 空格（最常見）→ 最短編碼 "00"
- E、N、O、T → 中等長度編碼
- B、C、D、G → 較長編碼

## 壓縮率分析

### 理論基礎

Huffman 編碼的最優性基於以下事實：對於給定的頻率分佈，它產生的編碼長度最接近資訊熵。

**資訊熵**：H = -Σ pᵢ × log₂(pᵢ)

其中 pᵢ 是字元 i 出現的機率。熵代表編碼每個字元所需的最小平均位元數。

### 範例計算

對於 "A SIMPLE STRING TO BE ENCODED"：
- 原始：26 字元 × 8 位元 = 208 位元（不含空格，實際 29 字元 × 8 = 232 位元）
- Huffman：僅 110 位元
- 壓縮比：約 52.6%

### 與其他壓縮演算法的比較

| 演算法 | 類型 | 壓縮率 | 速度 | 特點 |
|-------|------|-------|------|------|
| Huffman | 無失真 | 中等 | 快 | 最優前綴碼 |
| LZW | 無失真 | 高 | 中 | 字典壓縮 |
| LZ77 | 無失真 | 高 | 中 | 滑動視窗 |
| JPEG | 有失真 | 很高 | 中 | 針對圖片 |
| MP3 | 有失真 | 很高 | 中 | 針對音訊 |

## 應用場景

- **ZIP 壓縮**：與 LZ77 結合使用（DEFLATE 演算法）
- **JPEG**：在 DCT 轉換後對係數進行 Huffman 編碼
- **MP3**：對量化後的頻譜資料進行編碼
- **通訊協定**：在頻寬有限的通道中傳輸資料
- **硬體壓縮**：因為簡單，常被實作在硬體中

## 貪婪正確性證明

### 貪婪選擇性質

**引理**：在最優編碼樹中，頻率最低的兩個字元一定在最深層，且可以互換位置。

**證明**：假設最優樹 T 中，x 和 y 是頻率最低的兩個字元。如果 x 不在最深層，設深度最大的字元為 z。交換 x 和 z 不會增加總編碼長度。因此存在一棵最優樹，x 和 y 都在最深層。

### 最優子結構

**引理**：如果將頻率最低的兩個字元 x 和 y 合併為一個節點 z（freq(z) = freq(x) + freq(y)），則原問題的最優解包含子問題的最優解。

## 總結

Huffman 編碼展示了貪婪演算法如何在最優化問題中產生精確解。雖然壓縮領域已有更先進的演算法（如算術編碼），但 Huffman 編碼因其簡單性和最優性仍然是廣泛使用的基礎技術。

## 延伸閱讀

- [Huffman Coding Explained](https://www.google.com/search?q=huffman+coding+explained)
- [Information Theory Basics](https://www.google.com/search?q=information+theory+entropy)
- [DEFLATE Algorithm](https://www.google.com/search?q=DEFLATE+compression+algorithm)
