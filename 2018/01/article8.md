# 機率與統計

## 簡介

機率與統計是資料科學與機器學習的核心數學基礎。本篇介紹基本概念及其 Python 實現。

## 基本統計量

### 平均數、中位數、眾數

```python
import numpy as np
from scipy import stats

data = [1, 2, 2, 3, 3, 3, 4, 5, 5, 5, 5]

# 平均數
mean = np.mean(data)
print(f"平均數: {mean}")  # 3.3636...

# 中位數
median = np.median(data)
print(f"中位數: {median}")  # 3.0

# 眾數
mode = stats.mode(data)
print(f"眾數: {mode.mode[0]}, 次數: {mode.count[0]}")  # 5, 4
```

### 變異數與標準差

```python
data = [1, 2, 3, 4, 5]

# 母體變異數（除以 N）
variance = np.var(data)
print(f"變異數（母體）: {variance}")  # 2.0

# 樣本變異數（除以 N-1）
sample_variance = np.var(data, ddof=1)
print(f"變異數（樣本）: {sample_variance}")  # 2.5

# 標準差
std = np.std(data)
print(f"標準差: {std}")  # 1.414...
```

### 百分位數

```python
data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# 計算百分位數
p25 = np.percentile(data, 25)   # 第25百分位
p50 = np.percentile(data, 50)   # 第50百分位（中位數）
p75 = np.percentile(data, 75)   # 第75百分位

print(f"P25: {p25}, P50: {p50}, P75: {p75}")
```

## 機率分布

### 離散分布

```python
import numpy as np
from scipy import stats

# 均勻分布（擲骰子）
uniform = stats.randint(1, 7)
print("擲骰子的機率分布:")
for i in range(1, 7):
    print(f"  P(X={i}) = {uniform.pmf(i):.4f}")

# 二項分布（10次試驗，成功率0.5）
n, p = 10, 0.5
binomial = stats.binom(n, p)
print(f"\n二項分布 B(10, 0.5):")
print(f"  P(X=5) = {binomial.pmf(5):.4f}")
print(f"  E[X] = {binomial.mean():.2f}")
print(f"  Var[X] = {binomial.var():.2f}")
```

### 連續分布

```python
from scipy import stats

# 常態分布
mu, sigma = 0, 1  # 平均數、標準差
normal = stats.norm(mu, sigma)

print("標準常態分布:")
print(f"  P(X=0) = {normal.pdf(0):.4f}")  # 機率密度
print(f"  P(X<0) = {normal.cdf(0):.4f}")  # 累積分布
print(f"  P(X>1.96) = {1 - normal.cdf(1.96):.4f}")

# 生成服從常態分布的亂數
samples = normal.rvs(size=1000)
print(f"\n生成 1000 個樣本，平均值: {np.mean(samples):.4f}")
```

## 機率運算

### 條件機率

```python
# P(A|B) = P(A and B) / P(B)

# 範例：抽撲克牌
# 計算 P(紅心 | 已抽到紅色牌)

# P(紅心) = 13/52 = 0.25
# P(紅色) = 26/52 = 0.5
# P(紅心且紅色) = 13/52 = 0.25

# P(紅心|紅色) = 0.25 / 0.5 = 0.5

p_red = 0.5
p_heart_and_red = 0.25
p_heart_given_red = p_heart_and_red / p_red
print(f"P(紅心|紅色) = {p_heart_given_red}")  # 0.5
```

### 貝葉斯定理

```python
# P(A|B) = P(B|A) * P(A) / P(B)

# 疾病檢測範例
# 疾病盛行率: P(Disease) = 0.01 (1%)
# 檢測準確率: P(Positive|Disease) = 0.99 (99%)
# 偽陽率: P(Positive|No Disease) = 0.05 (5%)

p_disease = 0.01
p_positive_given_disease = 0.99
p_positive_given_no_disease = 0.05

# P(Positive) = P(Positive|Disease)*P(Disease) + P(Positive|No Disease)*P(No Disease)
p_positive = (p_positive_given_disease * p_disease +
               p_positive_given_no_disease * (1 - p_disease))

# P(Disease|Positive) = P(Positive|Disease) * P(Disease) / P(Positive)
p_disease_given_positive = (p_positive_given_disease * p_disease) / p_positive

print(f"P(Disease|Positive) = {p_disease_given_positive:.4f}")
print(f"化驗為陽性時，實際有病的機率: {p_disease_given_positive*100:.2f}%")
```

## 假設檢定

### t 檢定

```python
from scipy import stats

# 兩組樣本
group1 = [80, 85, 78, 92, 88]
group2 = [75, 82, 79, 90, 85]

# 獨立樣本 t 檢定
t_stat, p_value = stats.ttest_ind(group1, group2)
print(f"t 統計量: {t_stat:.4f}")
print(f"p 值: {p_value:.4f}")

if p_value < 0.05:
    print("兩組有顯著差異 (p < 0.05)")
else:
    print("兩組無顯著差異")
```

### 卡方檢定

```python
from scipy import stats
import numpy as np

# 觀察值
observed = np.array([[30, 10], [20, 40]])

# 卡方檢定
chi2, p_value, dof, expected = stats.chi2_contingency(observed)

print(f"卡方統計量: {chi2:.4f}")
print(f"p 值: {p_value:.4f}")
print(f"自由度: {dof}")
print(f"期望值:\n{expected}")
```

## 亂數生成

```python
import numpy as np
from scipy import stats

np.random.seed(42)

# 隨機整數
random_int = np.random.randint(1, 100)
print(f"隨機整數 (1-99): {random_int}")

# 隨機浮點數
random_float = np.random.random()
print(f"隨機浮點數: {random_float}")

# 從分布生成
normal_samples = np.random.normal(0, 1, 100)
print(f"常態分布樣本平均值: {np.mean(normal_samples):.4f}")

# 隨機選擇
choices = ['A', 'B', 'C', 'D']
selected = np.random.choice(choices, size=3, replace=False)
print(f"隨機選擇: {selected}")
```

## 練習題

1. 計算資料 [2, 4, 4, 6, 8, 10] 的平均數、變異數、標準差
2. 某考試成績服從常態分布，平均70分，標準差10分，估計約有多少比例學生高於80分
3. 投擲兩個骰子，計算點數和大於7的機率
4. 比較兩組資料是否有顯著差異