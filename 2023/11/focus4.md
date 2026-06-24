# 4. 通道容量與通道編碼

## 通道模型

一個通訊通道由輸入 $X$、輸出 $Y$ 與轉移機率 $p(y|x)$ 定義。通道可以是：
- **二元對稱通道（BSC）**：每個位元以機率 $p$ 翻轉
- **二元抹除通道（BEC）**：每個位元以機率 $\epsilon$ 被抹除
- **高斯通道（AWGN）**：輸出是輸入加上高斯雜訊

## 通道容量

通道容量（Channel Capacity）定義為輸入與輸出之間的最大互資訊：

$$C = \max_{p(x)} I(X; Y)$$

Shannon 的第二個編碼定理（通道編碼定理）指出：只要傳輸速率 $R < C$，就存在一種編碼方式使得錯誤率可以任意小。反之，若 $R > C$，則不可能實現可靠的通訊。

## BSC 通道容量

對於二元對稱通道（BSC），容量為：

$$C_{\text{BSC}} = 1 - H_b(p) = 1 + p \log_2 p + (1-p) \log_2 (1-p)$$

其中 $H_b(p)$ 是二元熵。當 $p = 0$ 時容量為 1（完美通道），$p = 0.5$ 時容量為 0（隨機通道）。

## 通道編碼的挑戰

通道編碼的目標是找到能逼近通道容量的實用碼。好的通道編碼需要具備：
- 高編碼率（接近容量）
- 低錯誤率（在容量內能正確解碼）
- 有效率的編解碼演算法（線性時間或接近線性時間）

從漢明碼（1950）到 LDPC（1960，1990 年代被重新發現）再到渦輪碼（1993），通道編碼的發展就是一部不斷逼近 Shannon 極限的歷史。

## Python 實作

```python
import math

def bsc_capacity(p):
    if p == 0 or p == 1: return 1.0
    h = -p * math.log2(p) - (1-p) * math.log2(1-p)
    return 1.0 - h
```

當 p=0.1 時容量約 0.531。這意味著傳送 1000 個位元最多只能攜帶 531 個位元的有效資訊。

## 參考資源

- https://www.google.com/search?q=channel+capacity+Shannon+channel+coding+theorem+BSC+BEC+AWGN
- https://www.google.com/search?q=binary+symmetric+channel+capacity+formula+entropy+derivation
- https://www.google.com/search?q=channel+coding+history+Hamming+LDPC+Turbo+Shannon+limit
