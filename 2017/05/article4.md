# 文章 4：機率論基礎

## 前言

機率論是機器學習的理論基礎。本章節介紹機器學習中常用的機率概念。

## 隨機變數

隨機變數是將隨機實驗結果映射為數值的函數：

### 離散隨機變數

```python
import numpy as np
from collections import Counter

# 骰子擲硬幣實驗
outcomes = np.random.choice([1, 2, 3, 4, 5, 6], size=1000)
counts = Counter(outcomes)
probs = {k: v/1000 for k, v in counts.items()}
```

### 連續隨機變數

```python
# 常態分佈
samples = np.random.normal(0, 1, 1000)
```

## 機率分佈

### 常態分佈（高斯分佈）

```python
import matplotlib.pyplot as plt

x = np.linspace(-4, 4, 100)
y = (1 / np.sqrt(2 * np.pi)) * np.exp(-x**2 / 2)

plt.plot(x, y)
plt.title('Standard Normal Distribution')
plt.show()
```

### 均匀分佈

```python
samples = np.random.uniform(0, 1, 1000)
```

## 期望值與變異數

```python
# 期望值
mean = np.mean(samples)

# 變異數
variance = np.var(samples)

# 標準差
std = np.std(samples)
```

## 條件機率

```python
# P(A|B) = P(A,B) / P(B)
def conditional_prob(joint_prob, marginal_b):
    return joint_prob / marginal_b
```

## 貝氏定理

```
P(A|B) = P(B|A) × P(A) / P(B)
```

```python
def bayes theorem(prior_a, likelihood_b_given_a, evidence_b):
    posterior = (likelihood_b_given_a * prior_a) / evidence_b
    return posterior
```

## 最大似然估計（MLE）

給定數據 D 與參數 θ，似然函數：

```python
# 對常態分佈參數的 MLE
mean_mle = np.mean(data)
std_mle = np.std(data, ddof=0)
```

## 機器學習中的機率

- **分類**：Softmax 輸出視為類別機率
- **損失函數**：交叉熵、對數損失
- **正規化**：貝氏方法
- **生成模型**：VAE、GAN

## 總結

機率論提供了解釋與分析機器學習模型的數學框架。掌握這些基礎概念對理解機器學習至關重要。

## 延伸閱讀

- https://www.google.com/search?q=probability+theory+machine+learning+basics
- https://www.google.com/search?q=maximum+likelihood+estimation+explained