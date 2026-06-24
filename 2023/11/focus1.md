# 1. 資訊的度量：熵與自資訊

## 資訊的直觀理解

什麼是「資訊」？當你聽到「明天太陽從東邊升起」，這句話幾乎不帶資訊量，因為你早已確定這件事會發生。相反地，當你聽到「明天會有地震」，這句話攜帶了大量資訊，因為地震是一個低機率事件。

Shannon 的精確之處在於：**資訊量與事件的不確定性成正比，與事件的發生機率成反比。**

## 自資訊

對於一個發生機率為 $p$ 的事件，其自資訊（Self-Information）定義為：

$$I(p) = -\log_2 p \text{ (bits)}$$

使用以 2 為底的對數，單位是「位元」（bits）。這意味著：
- 一個機率為 0.5 的事件攜帶 1 bit 的資訊
- 一個機率為 0.125 的事件攜帶 3 bits 的資訊
- 一個機率為 1 的事件攜帶 0 bits 的資訊

## 熵

熵（Entropy）是資訊理論中最核心的概念，它衡量一個隨機變數的**平均不確定性**。對於一個離散隨機變數 $X$ 取值於 $\{x_1, ..., x_n\}$ 且機率分布為 $p(x_i)$，其熵為：

$$H(X) = -\sum_{i=1}^{n} p(x_i) \log_2 p(x_i)$$

熵也可以視為自資訊的期望值：$H(X) = E[I(p(X))]$。

## 範例：擲硬幣 vs 骰子

一個公平的硬幣有兩種結果，各 0.5 機率：$H = -0.5 \log_2 0.5 - 0.5 \log_2 0.5 = 1$ bit。

一個公平的六面骰子有六種結果，各 $1/6$ 機率：$H = -6 \times (1/6) \log_2 (1/6) = \log_2 6 \approx 2.585$ bits。

骰子的熵較大，因為其結果的不確定性更高。當機率分布越均勻，熵就越大；當分布越集中（某個事件的機率接近 1），熵就越小。

## Python 實作

```python
import math

def entropy(probs):
    return -sum(p * math.log2(p) for p in probs if p > 0)

def self_info(p):
    return -math.log2(p)
```

## 參考資源

- https://www.google.com/search?q=Shannon+entropy+self+information+definition+bits+formula
- https://www.google.com/search?q=information+theory+entropy+examples+coin+dice+probability
