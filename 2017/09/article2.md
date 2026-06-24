# 亂數與機率模組

## random 模組

```python
import random

# 基本函數
random.random()        # [0, 1) 均勻分布
random.randint(1, 10)  # [1, 10] 整數
random.uniform(1, 10) # [1, 10) 均勻分布
random.choice([1, 2, 3])  # 隨機選擇
random.shuffle([1, 2, 3, 4])  # 洗牌
```

## 抽樣

```python
# 不重複抽樣
random.sample([1, 2, 3, 4, 5], k=3)

# 加權抽樣
choices = ['a', 'b', 'c']
weights = [0.5, 0.3, 0.2]
random.choices(choices, weights=weights, k=10)
```

## 機率分布

```python
import random

# 常態分布
random.gauss(0, 1)  # 均值 0, 標準差 1
random.normalvariate(0, 1)

# 指數分布
random.expovariate(1/5)

# 卜瓦松分布
random.poisson(3)

# Gamma 分布
random.gammavariate(2, 2)
```

## scipy.stats

```python
from scipy import stats
import numpy as np

# 常態分布
norm = stats.norm(loc=0, scale=1)
print(norm.pdf(0))  # PDF
print(norm.cdf(1.96))  # CDF
print(norm.ppf(0.975))  # 逆 CDF

# 抽樣
samples = norm.rvs(size=100)

# 統計
print(np.mean(samples))
print(np.std(samples))
```

## 統計基礎

```python
import numpy as np
from collections import Counter

data = [1, 2, 2, 3, 3, 3, 4, 4, 5]

# 平均值
mean = sum(data) / len(data)
print(f"Mean: {mean}")

# 中位數
sorted_data = sorted(data)
n = len(sorted_data)
median = sorted_data[n // 2] if n % 2 == 1 else (sorted_data[n//2-1] + sorted_data[n//2]) / 2
print(f"Median: {median}")

# 眾數
counter = Counter(data)
mode = counter.most_common(1)[0][0]
print(f"Mode: {mode}")

# 變異數
variance = sum((x - mean) ** 2 for x in data) / len(data)
print(f"Variance: {variance}")

# 標準差
std_dev = variance ** 0.5
print(f"Std: {std_dev}")
```

## 亂數種子

```python
import random

# 設定種子（可重現結果）
random.seed(42)
print(random.random())
print(random.random())

random.seed(42)
print(random.random())  # 與上面相同
```

## 密碼學安全隨機數

```python
import secrets

# 安全隨機
secrets.randbelow(10)  # [0, 10)
secrets.token_bytes(16)  # 16 位元組隨機
secrets.token_hex(32)  # 32 字元十六進制

# 安全密碼
password = secrets.token_urlsafe(32)
```

## 總結

Python 提供完整的亂數與機率工具：
- random 模組：基礎隨機功能
- scipy.stats：高階統計分布
- secrets：密碼學安全隨機

選擇適當的工具取決於應用場景。