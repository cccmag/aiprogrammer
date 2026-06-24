# 機率論基礎

## 基本概念

機率論是統計與機器學習的數學基礎。

### 機率空間

- **樣本空間 Ω**：所有可能結果的集合
- **事件**：樣本空間的子集
- **機率 P**：從事件到 [0,1] 的函數

```python
# 拋硬幣實驗
sample_space = {"H", "T"}  # 正面、反面
P_H = 0.5
P_T = 0.5
```

## 隨機變數

### 離散隨機變數

```python
import numpy as np
from scipy import stats

# 公平的硬幣
p = 0.5
coin_dist = stats.bernoulli(p)

# 期望值 E[X]
print(coin_dist.mean())  # 0.5

# 變異數 Var(X)
print(coin_dist.var())  # 0.25

# 機率質量函數 PMF
print(coin_dist.pmf(1))  # P(X=1) = 0.5
```

### 連續隨機變數

```python
# 常態分佈 N(0, 1)
normal_dist = stats.norm(0, 1)

# 機率密度函數 PDF
print(normal_dist.pdf(0))  # 0.3989...

# 累積分佈函數 CDF
print(normal_dist.cdf(1.96))  # 0.975
```

## 常見分佈

### 伯努力分佈

```python
# P(X=1) = p, P(X=0) = 1-p
p = 0.3
bernoulli = stats.bernoulli(p)
print(bernoulli.pmf(1))  # 0.3
```

### 二項分佈

N 次伯努力試驗的成功次數。

```python
# 10 次硬幣，5 次正面的機率
n, p = 10, 0.5
binom = stats.binom(n, p)
print(binom.pmf(5))  # 0.246
print(binom.cdf(5))   # P(X <= 5)
```

### 常態分佈

```python
# 平均值 100，標準差 15
mu, sigma = 100, 15
normal = stats.norm(mu, sigma)

# P(85 < X < 115)
prob = normal.cdf(115) - normal.cdf(85)
print(prob)  # ~0.6827
```

## 條件機率與貝氏定理

### 條件機率

P(A|B) = P(A∩B) / P(B)

```python
# P(A and B) = P(A|B) * P(B)
# = P(B|A) * P(A)

P_A = 0.01  # 疾病發生率
P_B_given_A = 0.99  # 有病時測試為陽性的機率
P_B_given_not_A = 0.05  # 沒病時測試為陽性的機率（偽陽性）

# P(B) = P(B|A)P(A) + P(B|not A)P(not A)
P_B = P_B_given_A * P_A + P_B_given_not_A * (1 - P_A)

# 貝氏定理：P(A|B) = P(B|A)P(A) / P(B)
P_A_given_B = P_B_given_A * P_A / P_B
print(f"P(A|B) = {P_A_given_B:.4f}")  # 0.1667
```

## 期望值與變異數

### 期望值 E[X]

```python
# 擲骰子的期望值
outcomes = [1, 2, 3, 4, 5, 6]
probabilities = [1/6] * 6
expected_value = sum(o * p for o, p in zip(outcomes, probabilities))
print(f"E[X] = {expected_value}")  # 3.5
```

### 變異數 Var(X)

```python
# Var(X) = E[(X - E[X])^2] = E[X^2] - E[X]^2

def variance(values, probabilities):
    mean = sum(v * p for v, p in zip(values, probabilities))
    mean_sq = sum(v**2 * p for v, p in zip(values, probabilities))
    return mean_sq - mean**2

print(f"Var(X) = {variance(outcomes, probabilities)}")  # 35/12 ≈ 2.917
```

## 大數定律與中央極限定理

### 大數定律

樣本數量足夠大時，樣本平均值趨近於期望值。

```python
import random

def demonstrate_lln(n_samples):
    samples = [random.randint(1, 6) for _ in range(n_samples)]
    return sum(samples) / n_samples

for n in [100, 1000, 10000, 100000]:
    avg = demonstrate_lln(n)
    print(f"n={n:6d}: average = {avg:.4f}")
```

### 中央極限定理

大量獨立隨機變數的和趨近於常態分佈。

```python
import matplotlib.pyplot as plt

def sample_means(num_samples, sample_size):
    return [sum(random.randint(1, 6) for _ in range(sample_size)) / sample_size
            for _ in range(num_samples)]

# 繪製樣本平均的分佈（會趨近常態）
means = sample_means(10000, 30)
# plt.hist(means, bins=50)
```

## 共變異數與相關係數

```python
import numpy as np

# 資料
X = [1, 2, 3, 4, 5]
Y = [2, 4, 5, 4, 5]

# 計算共變異數
cov_xy = np.cov(X, Y)[0][1]
print(f"Cov(X, Y) = {cov_xy:.2f}")

# 計算相關係數
corr_xy = np.corrcoef(X, Y)[0][1]
print(f"Corr(X, Y) = {corr_xy:.2f}")
```

## 總結

機率論是機器學習的核心數學基礎。需掌握機率分佈、條件機率、貝氏定理、期望值與變異數等概念。這些將幫助理解機器學習演算法的理論基礎。