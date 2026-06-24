# 資訊理論入門

## 資訊理論基礎

資訊理論量化資訊量，解決「資訊有多少」的問題。

## 熵（Entropy）

熵是隨機變數不確定性的度量。

H(X) = -Σ P(x) log P(x)

```python
import numpy as np
from scipy.stats import entropy

# 公平硬幣
p = [0.5, 0.5]
h_coin = entropy(p, base=2)
print(f"硬幣熵: {h_coin:.2f} bits")  # 1 bit

# 不公平硬幣（90% 正面）
p = [0.9, 0.1]
h_biased = entropy(p, base=2)
print(f"偏向硬幣熵: {h_biased:.2f} bits")  # ~0.47 bits

# 擲骰子
p = [1/6] * 6
h_dice = entropy(p, base=2)
print(f"骰子熵: {h_dice:.2f} bits")  # ~2.58 bits
```

## 聯合熵

兩個隨機變數的聯合不確定性。

H(X, Y) = -ΣΣ P(x, y) log P(x, y)

```python
# 計算聯合熵
def joint_entropy(X, Y):
    from collections import Counter
    xy_counts = Counter(zip(X, Y))
    n = len(X)
    h = 0
    for count in xy_counts.values():
        p = count / n
        h -= p * np.log2(p)
    return h

X = [0, 0, 1, 1]
Y = [0, 1, 0, 1]
print(f"聯合熵: {joint_entropy(X, Y):.2f} bits")
```

## 條件熵

已知 Y 的情況下，X 的剩餘不確定性。

H(X|Y) = H(X, Y) - H(Y)

```python
def conditional_entropy(X, Y):
    from collections import Counter
    xy_counts = Counter(zip(X, Y))
    y_counts = Counter(Y)
    n = len(X)
    h = 0
    for (x, y), count in xy_counts.items():
        p_xy = count / n
        p_y = y_counts[y] / n
        p_x_given_y = p_xy / p_y
        if p_x_given_y > 0:
            h -= p_xy * np.log2(p_x_given_y)
    return h

X = [0, 0, 1, 1]
Y = [0, 1, 0, 1]
print(f"條件熵 H(X|Y): {conditional_entropy(X, Y):.2f} bits")
```

## 互資訊（Mutual Information）

兩個變數共享的資訊量。

I(X; Y) = H(X) - H(X|Y) = H(Y) - H(Y|X)

```python
def mutual_information(X, Y):
    return entropy([X.count(0)/len(X), X.count(1)/len(X)], base=2) - conditional_entropy(X, Y)

X = [0, 0, 1, 1]
Y = [0, 1, 0, 1]
print(f"互資訊 I(X;Y): {mutual_information(X, Y):.2f} bits")
```

## KL 散度（Kullback-Leibler Divergence）

兩個機率分佈的差異。

D_KL(P || Q) = Σ P(x) log(P(x) / Q(x))

```python
from scipy.stats import entropy

P = [0.5, 0.3, 0.2]
Q = [0.4, 0.4, 0.2]

# 使用 scipy 的 entropy 計算 KL 散度
# D_KL(P || Q) = entropy(P, Q) - entropy(P)
kl_div = entropy(P, Q) - entropy(P)
print(f"D_KL(P||Q): {kl_div:.4f}")
```

## 交叉熵

常用於機器學習的損失函數。

H(P, Q) = -Σ P(x) log Q(x) = H(P) + D_KL(P || Q)

```python
def cross_entropy(P, Q):
    return -sum(p * np.log2(q) if q > 0 else 0 for p, q in zip(P, Q))

P = [0.5, 0.3, 0.2]
Q = [0.4, 0.4, 0.2]
print(f"交叉熵 H(P,Q): {cross_entropy(P, Q):.4f}")
print(f"熵 H(P): {entropy(P, base=2):.4f}")
```

## 在機器學習中的應用

### 決策樹 - 使用資訊增益

```python
def information_gain(X_parent, Y_parent, X_left, Y_left, X_right, Y_right):
    n_parent = len(X_parent)
    n_left = len(X_left)
    n_right = len(X_right)

    h_parent = entropy([X_parent.count(0)/n_parent, X_parent.count(1)/n_parent], base=2)

    h_left = entropy([X_left.count(0)/n_left, X_left.count(1)/n_left], base=2) if n_left > 0 else 0
    h_right = entropy([X_right.count(0)/n_right, X_right.count(1)/n_right], base=2) if n_right > 0 else 0

    h_after = (n_left * h_left + n_right * h_right) / n_parent

    return h_parent - h_after

# 假裝的資料分割
X = [0, 0, 1, 1, 0, 1, 1, 0]
Y = [0, 1, 1, 0, 0, 1, 1, 0]

print(f"資訊增益: {information_gain(X, X, X[:4], X[:4], X[4:], X[4:]):.4f}")
```

## 總結

資訊理論提供量化資訊的數學框架：
- **熵**：衡量不確定性
- **互資訊**：衡量變數間共享資訊
- **KL 散度**：衡量分佈差異

這些概念廣泛應用於機器學習演算法設計與分析。