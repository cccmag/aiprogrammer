# 主成分分析

## 前言

主成分分析（Principal Component Analysis, PCA）是最常用的降維技術之一。它找到資料中方差最大的方向，將高維資料投射到低維空間。

## 為何需要降維？

### 維度災難

```python
# 維度增加帶來的問題

curse_of_dimensionality = {
    "計算成本": "高維度資料計算量大",
    "過擬合": "維度越高，模型越容易過擬合",
    "視覺化": "無法直接視覺化高維資料",
    "儲存": "需要更多儲存空間"
}
```

### 降維的好處

```python
dimensionality_reduction_benefits = {
    "加速訓練": "降低計算成本",
    "減少過擬合": "提高泛化能力",
    "視覺化": "降至 2D 或 3D 進行視覺化",
    "去噪聲": "可能移除雜訊"
}
```

## PCA 的概念

### 核心思想

```python
pca_concept = {
    "目標": "找到資料變異最大的方向",
    "第一主成分": "資料變異最大的方向",
    "第二主成分": "與第一主成分垂直，且變異次大",
    "以此類推": "找到所有主成分"
}

# 降維時：選擇前 k 個主成分
# 這些主成分保留了大部分的資訊
```

### 幾何解釋

```
原始資料（二維）：
    ●
  ●    ●
    ●
      ●
    ●

PCA 轉換後：
    ↑ 第一主成分
    │   ●
    │   ● ●
    │   ● ●
    └────────→ 第二主成分
```

## PCA 的數學

### 協方差矩陣

```python
import numpy as np

def compute_covariance_matrix(X):
    """計算協方差矩陣"""
    # 中心化資料
    X_centered = X - X.mean(axis=0)

    # 計算協方差
    n = len(X)
    cov = np.dot(X_centered.T, X_centered) / (n - 1)

    return cov
```

### 特徵值分解

```python
# 對協方差矩陣進行特徵值分解

# Cov = V × D × V^(-1)
# V: 特徵向量矩陣（主成分方向）
# D: 對角矩陣（特徵值，代表該方向的重要性）
```

### PCA 步驟

```python
def pca(X, n_components):
    """
    PCA 實現
    X: 原始資料 (n_samples, n_features)
    n_components: 目標維度
    """
    # 1. 中心化
    X_centered = X - X.mean(axis=0)

    # 2. 計算協方差矩陣
    cov = np.cov(X_centered.T)

    # 3. 特徵值分解
    eigenvalues, eigenvectors = np.linalg.eig(cov)

    # 4. 按特徵值排序（降序）
    idx = eigenvalues.argsort()[::-1]
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]

    # 5. 選擇前 n_components 個主成分
    principal_components = eigenvectors[:, :n_components]

    # 6. 轉換資料
    X_transformed = np.dot(X_centered, principal_components)

    return X_transformed, principal_components, eigenvalues
```

## 方差解釋

### 解釋的方差比例

```python
def explained_variance_ratio(eigenvalues):
    """計算每個主成分解釋的方差比例"""
    total = sum(eigenvalues)
    return [eig / total for eig in eigenvalues]


# 範例
eigenvalues = [10, 5, 2, 1]
ratios = explained_variance_ratio(eigenvalues)
# [0.556, 0.278, 0.111, 0.056]
# 第一主成分解釋了 55.6% 的變異
```

### 累積解釋方差

```python
def cumulative_variance(eigenvalues, threshold=0.95):
    """找出需要多少主成分才能達到閾值"""
    total = sum(eigenvalues)
    cumsum = 0
    n_components = 0

    for eig in eigenvalues:
        cumsum += eig
        n_components += 1
        if cumsum / total >= threshold:
            break

    return n_components
```

## 還原與重建

### 從低維重建

```python
def reconstruct_from_pca(X_original, X_transformed, principal_components, mean):
    """從降維後的資料重建"""
    # 轉換回原始維度
    X_reconstructed = np.dot(X_transformed, principal_components.T)

    # 加上中心化時減去的平均值
    X_reconstructed += mean

    return X_reconstructed

# 重建誤差
error = np.sqrt(np.sum((X_original - X_reconstructed) ** 2))
```

## 應用場景

### 視覺化

```python
# 將高維資料降至 2D 或 3D 進行視覺化

from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

pca = PCA(n_components=2)
X_2d = pca.fit_transform(X)

plt.scatter(X_2d[:, 0], X_2d[:, 1], c=y)
plt.xlabel('First Principal Component')
plt.ylabel('Second Principal Component')
plt.show()
```

### 特徵減少

```python
# 在分類或迴歸前先降維

from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression

# 降至 50 維
pca = PCA(n_components=50)
X_reduced = pca.fit_transform(X_train)

# 訓練模型
model = LogisticRegression()
model.fit(X_reduced, y_train)
```

### 雜訊過濾

```python
# 保留主要變異，可以過濾掉雜訊

# 假設雜訊主要在小的特徵值中
# 只保留解釋 99% 方差的主成分
pca = PCA(n_components=0.99)
X_denoised = pca.fit_transform(X)
X_reconstructed = pca.inverse_transform(X_denoised)
```

## Scikit-learn 使用

### PCA 類別

```python
from sklearn.decomposition import PCA

# 建立 PCA 物件
pca = PCA(n_components=2)

# 擬合和轉換
X_transformed = pca.fit_transform(X)

# 取得主成分
components = pca.components_  # (2, n_features)

# 解釋的方差比例
explained_variance = pca.explained_variance_ratio_
```

### 完整範例

```python
from sklearn.decomposition import PCA
from sklearn.datasets import load_iris

# 載入資料
iris = load_iris()
X, y = iris.data, iris.target

# PCA
pca = PCA(n_components=2)
X_2d = pca.fit_transform(X)

print(f"解釋的方差: {pca.explained_variance_ratio_}")
# [0.92461621, 0.05306657]
# 第一主成分解釋了 92.5% 的變異

# 可視化
import matplotlib.pyplot as plt
plt.scatter(X_2d[:, 0], X_2d[:, 1], c=y)
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.show()
```

## 注意事項

### 標準化

```python
# PCA 對尺度敏感，應先標準化

from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)
```

### 線性假設

```python
# PCA 假設數據的主要變異是線性的

limitations = {
    "線性假設": "只能捕捉線性關係",
    "資訊損失": "丟棄小的特徵值可能丟失資訊",
    "可解釋性": "主成分有時難以解釋"
}
```

---

**延伸閱讀**

- [Principal+Component+Analysis+tutorial](https://www.google.com/search?q=Principal+Component+Analysis+tutorial)
- [PCA+dimensionality+reduction](https://www.google.com/search?q=PCA+dimensionality+reduction)
- [PCA+python+sklearn](https://www.google.com/search?q=PCA+python+sklearn)