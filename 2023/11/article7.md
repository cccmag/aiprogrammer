# 漢明碼除錯

## 當位元出錯時

在實際的通訊系統中，位元錯誤是不可避免的。漢明碼（Hamming Code）可以在編碼開銷很小的情況下修正單一位元錯誤。本篇文章深入探討漢明碼的除錯機制，並以 Python 實作完整的偵錯與糾錯流程。

## 伴隨式計算

漢明碼 (7,4) 的 7 個位元中，有 3 個是同位檢查位元。解碼時，我們使用這 3 個同位位元來計算伴隨式（Syndrome）：

```python
def hamming_syndrome(bits7):
    s1 = bits7[0] ^ bits7[2] ^ bits7[4] ^ bits7[6]
    s2 = bits7[1] ^ bits7[2] ^ bits7[5] ^ bits7[6]
    s3 = bits7[3] ^ bits7[4] ^ bits7[5] ^ bits7[6]
    return s1, s2, s3
```

伴隨式 $(s_1, s_2, s_3)$ 是一個 3 位元的二進位數，其值正好對應錯誤位元的位置（1-indexed）。

## 錯誤定位表

| 伴隨式 (s1,s2,s3) | 錯誤位置 |
|------------------|---------|
| 000 | 無錯誤 |
| 001 | 位元 1 |
| 010 | 位元 2 |
| 011 | 位元 3 |
| 100 | 位元 4 |
| 101 | 位元 5 |
| 110 | 位元 6 |
| 111 | 位元 7 |

## 完整的編解碼器

```python
def hamming_encode(bits4):
    d = list(bits4)
    p1 = d[0] ^ d[1] ^ d[3]
    p2 = d[0] ^ d[2] ^ d[3]
    p3 = d[1] ^ d[2] ^ d[3]
    return [p1, p2, d[0], p3, d[1], d[2], d[3]]

def hamming_decode(bits7):
    s1 = bits7[0] ^ bits7[2] ^ bits7[4] ^ bits7[6]
    s2 = bits7[1] ^ bits7[2] ^ bits7[5] ^ bits7[6]
    s3 = bits7[3] ^ bits7[4] ^ bits7[5] ^ bits7[6]
    err_pos = s1 * 1 + s2 * 2 + s3 * 4
    fixed = list(bits7)
    if 1 <= err_pos <= 7:
        fixed[err_pos - 1] ^= 1
    return [fixed[2], fixed[4], fixed[5], fixed[6]]
```

## 除錯流程圖

```
接收位元 r[0..6]
    ↓
計算伴隨式 s = H × r^T
    ↓
s = 0? ──是──→ 無錯誤，輸出資料位元
    ↓否
找出錯誤位置 pos = s (二進位值)
    ↓
反轉 r[pos-1] 修正錯誤
    ↓
輸出修正後的資料位元
```

## 範例：模擬一個錯誤

```python
# 原始資料: 1011
original = [1, 0, 1, 1]
encoded = hamming_encode(original)
# [0, 1, 1, 0, 0, 1, 1]

# 在第 4 個位元注入錯誤
received = encoded[:]
received[3] ^= 1
# [0, 1, 1, 1, 0, 1, 1]

# 解碼偵錯
decoded = hamming_decode(received)
# [1, 0, 1, 1] ← 正確還原
```

## 限制

漢明碼 (7,4) 只能修正單一位元錯誤。當兩個位元同時錯誤時，漢明碼會誤判為另一個位置的單一錯誤（或無法正確修正）。這是實務上需要使用更強大的編碼（如 BCH、LDPC）的原因。

## 參考資源

- https://www.google.com/search?q=Hamming+code+syndrome+calculation+error+position+table+parity+check+matrix
- https://www.google.com/search?q=Hamming+code+7+4+encode+decode+Python+implementation+error+correction
- https://www.google.com/search?q=Hamming+code+limitation+single+error+correction+double+error+detection+SECDED
