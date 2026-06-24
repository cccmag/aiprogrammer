# 熵的計算與意義

## 熵的直觀理解

熵（Entropy）是資訊理論中最重要也最容易被誤解的概念。直觀上，熵衡量一個系統的「混亂程度」或「不確定性」。在資訊理論中，它衡量的是從一個隨機來源中觀察到一個結果時，平均獲得的資訊量。

## 從硬幣開始

考慮一個公平的硬幣：正面與反面的機率各為 0.5。擲一次硬幣的熵為：

$$H = -0.5 \log_2 0.5 - 0.5 \log_2 0.5 = 1 \text{ bit}$$

這意味著每次擲硬幣的結果平均攜帶 1 bit 的資訊。而一個不公平的硬幣（正面機率 0.9，反面機率 0.1）的熵為：

$$H = -0.9 \log_2 0.9 - 0.1 \log_2 0.1 \approx 0.469 \text{ bits}$$

因為大多數時候都會出現正面，不確定性較低，所以資訊量也較少。

## 文字的熵

英文文字的熵約為 1.0–1.5 bits/letter，低於 26 個字母均勻分布的熵（$\log_2 26 \approx 4.7$ bits）。這是因為英文存在大量的結構性冗餘：
- 字母 e 遠比 z 常見
- q 幾乎總是跟著 u
- 語法規則限制了字母組合

這種冗餘其實是好的：它讓英文在有雜訊的環境下仍然可被理解。

## 最大熵原理

當我們對一個分布所知有限時，應該選擇滿足約束條件下熵最大的分布。這個「最大熵原理」由 E. T. Jaynes 提出，它是邏輯上最保守的選擇——不做任何額外假設。

例如，如果只知道一個六面骰子的平均值為 3.5，最大熵原理會告訴我們選擇均勻分布（每面 1/6），因為任何其他分布都隱含了我們不知道的額外資訊。

## Python 實作

```python
import math

def entropy(probs):
    return -sum(p * math.log2(p) for p in probs if p > 0)

# 公平硬幣
print(entropy([0.5, 0.5]))        # 1.0
# 不公平硬幣
print(entropy([0.9, 0.1]))        # 0.469
# 公平骰子
print(entropy([1/6] * 6))         # 2.585
```

## 參考資源

- https://www.google.com/search?q=information+theory+entropy+examples+coin+flip+English+text+max+entropy
- https://www.google.com/search?q=entropy+of+English+language+redundancy+Shannon+estimate+bits+per+letter
- https://www.google.com/search?q=maximum+entropy+principle+Jaynes+constrained+optimization+probability+distribution
