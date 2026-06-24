# 統計分析與假設檢定

## 從資料到決策

統計告訴我們如何從樣本推論總體。在資料科學中，假設檢定是評估實驗結果是否具有統計顯著性的標準方法。

## 描述性統計

在進行檢定之前，先了解資料的基本特徵：

```python
import numpy as np
from scipy import stats

data = np.random.normal(loc=100, scale=15, size=100)

print(f"Mean:    {data.mean():.2f}")
print(f"Std:     {data.std():.2f}")
print(f"Median:  {np.median(data):.2f}")
print(f"Skew:    {stats.skew(data):.3f}")
print(f"Kurtosis:{stats.kurtosis(data):.3f}")
```

## 常態性檢定

許多統計檢定假設資料符合常態分佈：

```python
# Shapiro-Wilk 檢定
stat, p_value = stats.shapiro(data)
print(f"Shapiro: W={stat:.3f}, p={p_value:.4f}")
# p > 0.05：無法拒絕常態分佈的虛無假設

# Kolmogorov-Smirnov 檢定
stat, p_value = stats.kstest(data, "norm", args=(data.mean(), data.std()))
```

## t 檢定：比較兩組平均數

### 單一樣本 t 檢定

```python
# 檢定樣本平均是否顯著不同於 100
t_stat, p_value = stats.ttest_1samp(data, 100)
print(f"t = {t_stat:.3f}, p = {p_value:.4f}")
```

### 獨立樣本 t 檢定

```python
group_a = np.random.normal(100, 15, 50)
group_b = np.random.normal(110, 15, 50)

t_stat, p_value = stats.ttest_ind(group_a, group_b)
print(f"t = {t_stat:.3f}, p = {p_value:.4f}")
```

### 成對樣本 t 檢定

```python
before = np.random.normal(100, 15, 30)
after = before + np.random.normal(-5, 5, 30)

t_stat, p_value = stats.ttest_rel(before, after)
print(f"t = {t_stat:.3f}, p = {p_value:.4f}")
```

## ANOVA：比較多組平均數

```python
groups = [np.random.normal(100, 15, 30) for _ in range(3)]
f_stat, p_value = stats.f_oneway(*groups)
print(f"F = {f_stat:.3f}, p = {p_value:.4f}")
```

## 卡方檢定：類別變數關聯

```python
observed = np.array([[25, 15], [10, 30]])
chi2, p_value, dof, expected = stats.chi2_contingency(observed)
print(f"χ² = {chi2:.3f}, p = {p_value:.4f}")
```

## 相關性分析

```python
x = np.random.normal(0, 1, 100)
y = x + np.random.normal(0, 0.5, 100)

r, p_value = stats.pearsonr(x, y)
print(f"Pearson r = {r:.3f}, p = {p_value:.4f}")

rho, p_value = stats.spearmanr(x, y)
print(f"Spearman ρ = {rho:.3f}, p = {p_value:.4f}")
```

## 解讀 p 值的常見陷阱

1. **p 值不是效果大小**：大樣本下微小的差異也能產生顯著的 p 值
2. **多重比較**：同時進行多個檢定會增加型一錯誤
3. **p-hacking**：反覆檢定直到得到顯著結果是不道德的

```python
# Bonferroni 校正
p_values = [0.01, 0.04, 0.20, 0.50]
alpha = 0.05
adjusted = [min(p * len(p_values), 1.0) for p in p_values]
print(f"Adjusted p: {adjusted}")
```

## 延伸閱讀

- [SciPy 統計模組](https://www.google.com/search?q=SciPy+stats+tutorial)
- [假設檢定入門](https://www.google.com/search?q=hypothesis+testing+introduction)
- [p 值陷阱](https://www.google.com/search?q=p-value+pitfalls)
