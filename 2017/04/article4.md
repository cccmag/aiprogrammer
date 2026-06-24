# 文章 4：機率與統計基礎

## 前言

機率與統計是機器學習的理論基礎。本章節介紹機器學習中常用的機率與統計概念。

## 基本機率

### 機率公理

1. P(A) ≥ 0
2. P(Ω) = 1
3. 若 A 與 B 互斥，P(A∪B) = P(A) + P(B)

### 條件機率

```
P(A|B) = P(A∩B) / P(B)
```

### 貝氏定理

```
P(A|B) = P(B|A) × P(A) / P(B)
```

## 機率分佈

### 均勻分佈

```python
import numpy as np

samples = np.random.uniform(0, 1, 1000)
```

### 常態分佈

```python
samples = np.random.normal(0, 1, 1000)  # 均值 0，標準差 1
```

### 伯努利分佈

```python
p = 0.3
samples = np.random.binomial(1, p, 1000)
```

## 統計量

### 均值（Mean）

```python
x = np.array([1, 2, 3, 4, 5])
mean = np.mean(x)  # 3.0
```

### 變異數（Variance）

```python
variance = np.var(x)  # 預設為母體變異數
sample_variance = np.var(x, ddof=1)  # 樣本變異數
```

### 標準差（Standard Deviation）

```python
std = np.std(x)  # 1.414
```

### 共變異數（Covariance）

```python
cov = np.cov(x, y)  # 2x2 共變異數矩陣
```

## 最大似然估計（MLE）

給定數據 D 與參數 θ，似然函數：

```
L(θ|D) = P(D|θ)
```

最大化似然函數得到參數估計：

```python
# 對常態分佈的均值與標準差進行 MLE
mean_mle = np.mean(data)
std_mle = np.std(data, ddof=0)
```

## 交叉熵（Cross Entropy）

兩個機率分佈 p 與 q 的差異：

```
H(p, q) = -Σ p(x) log(q(x))
```

```python
def cross_entropy(p, q):
    return -np.sum(p * np.log(q + 1e-8))
```

## 機器學習中的應用

1. **分類**：Softmax 輸出視為類別機率
2. **損失函數**：交叉熵損失
3. **正規化**：貝氏方法
4. **機率模型**：生成對抗網路、變分自動編碼器

## 總結

機率統計提供了分析數據與模型的數學框架。理解這些概念有助於選擇適當的演算法與評估模型性能。

## 延伸閱讀

- https://www.google.com/search?q=probability+statistics+machine+learning+basics
- https://www.google.com/search?q=cross+entropy+loss+explained