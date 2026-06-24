# 算術編碼

## 超越 Huffman 的限制

Huffman 編碼的每個符號都對應一個整數位元的碼字，這導致當某個符號的機率不是 $1/2^k$ 時，Huffman 編碼無法達到熵極限。算術編碼（Arithmetic Coding）則沒有這個限制：它將整個訊息編碼為一個 $[0,1)$ 區間內的實數，可以任意接近熵極限。

## 核心原理

算術編碼的核心概念是將整個輸入序列映射到 $[0,1)$ 之間的一個子區間：

1. 初始區間為 $[0, 1)$
2. 對每個符號，根據其機率比例將當前區間分割
3. 選擇符號對應的子區間作為新的當前區間
4. 重複直到所有符號處理完畢
5. 在最終區間內選擇一個數值來代表整個序列

## 簡單範例

以符號 A (0.6)、B (0.3)、C (0.1) 編碼 "AB"：

```
初始區間: [0, 1)

處理 A (機率 0.6):
  A: [0, 0.6), B: [0.6, 0.9), C: [0.9, 1)
  → 選擇 A: [0, 0.6)

處理 B (機率 0.3):
  在 [0, 0.6) 內分割:
  A: [0, 0.36), B: [0.36, 0.54), C: [0.54, 0.6)
  → 選擇 B: [0.36, 0.54)

最終選擇 e.g. 0.4 代表 "AB"
```

## Python 實作

```python
def arithmetic_encode(symbols, probs, seq):
    low, high = 0.0, 1.0
    for s in seq:
        span = high - low
        cum = 0.0
        for sym, p in zip(symbols, probs):
            if sym == s:
                high = low + span * (cum + p)
                break
            cum += p
            low = low + span * cum
    return (low + high) / 2

def arithmetic_decode(symbols, probs, code, length):
    result = []
    low, high = 0.0, 1.0
    for _ in range(length):
        span = high - low
        cum = 0.0
        for sym, p in zip(symbols, probs):
            if low + span * cum <= code < low + span * (cum + p):
                result.append(sym)
                high = low + span * (cum + p)
                low = low + span * cum
                break
            cum += p
    return "".join(result)
```

## 實務考量

算術編碼雖然壓縮率優於 Huffman，但有兩個實務缺點：
1. **運算複雜度**：需要高精度浮點數或整數運算來處理區間
2. **專利問題**：算術編碼在很長一段時間內受到專利保護，限制了其應用

現代的資料壓縮標準（如 JPEG 2000、H.264）仍然使用算術編碼的變體，如 CABAC（Context-Adaptive Binary Arithmetic Coding）。

## 參考資源

- https://www.google.com/search?q=arithmetic+coding+principle+interval+subdivision+compression+example
- https://www.google.com/search?q=arithmetic+coding+Python+implementation+encode+decode+tutorial
- https://www.google.com/search?q=CABAC+H.264+HEVC+context+adaptive+binary+arithmetic+coding+standard
