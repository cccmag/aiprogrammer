# 二元對稱通道 BSC

## 最簡單的雜訊通道

二元對稱通道（Binary Symmetric Channel, BSC）是最基本也是最經典的通道模型。輸入與輸出都是二進位值 {0, 1}，每個位元以機率 $p$ 被翻轉（0→1 或 1→0），以機率 $1-p$ 保持不變。

BSC 是理解通道編碼定理的理想起點，因為它簡單到可以手動計算，又能展示所有重要的通道編碼概念。

## 通道容量計算

對於 BSC，通道容量公式為：

$$C = 1 - H_b(p) = 1 + p \log_2 p + (1-p) \log_2 (1-p)$$

| 錯誤率 p | 通道容量 C | 意義 |
|----------|-----------|------|
| 0.0 | 1.000 | 完美通道 |
| 0.1 | 0.531 | 一半容量 |
| 0.25 | 0.189 | 接近無用 |
| 0.5 | 0.000 | 隨機通道 |

當 p=0.5 時，輸出與輸入完全獨立，通道無法傳遞任何資訊。

## 重複碼：最簡單的通道編碼

最直接的錯誤修正方法是重複碼：將每個位元重複 $n$ 次，解碼時以多數決決定。

```python
def repeat_encode(bits, n=3):
    return [b for b in bits for _ in range(n)]

def repeat_decode(bits, n=3):
    result = []
    for i in range(0, len(bits), n):
        chunk = bits[i:i+n]
        result.append(1 if sum(chunk) > n/2 else 0)
    return result
```

重複碼的代價是編碼率 $R = 1/n$。當 p=0.1 時，使用三重複碼可以將錯誤率降低到約 $3p^2 \approx 0.03$，但編碼率只有 $1/3$，遠低於通道容量的 0.531。

## 通道編碼定理的啟示

Shannon 的通道編碼定理告訴我們：使用更精巧的編碼，可以在不犧牲太多編碼率的情況下達到任意低的錯誤率。這就是為什麼 LDPC 和渦輪碼可以在編碼率 0.9 以上達到極低的錯誤率，這對重複碼來說是不可能的。

## Python 實作

```python
import math

def bsc_capacity(p):
    if p == 0 or p == 1: return 1.0
    h = -p * math.log2(p) - (1-p) * math.log2(1-p)
    return 1.0 - h

for p in [0.0, 0.1, 0.25, 0.5]:
    print(f"p={p:.2f}, C={bsc_capacity(p):.4f}")
```

## 參考資源

- https://www.google.com/search?q=binary+symmetric+channel+BSC+channel+capacity+formula+derivation+Shannon
- https://www.google.com/search?q=repetition+code+error+correction+majority+vote+BER+channel+coding+example
- https://www.google.com/search?q=Shannon+channel+coding+theorem+implication+capacity+achieving+codes
