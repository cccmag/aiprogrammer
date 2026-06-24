# 支援向量機的原理與應用

## SVM 概述

支援向量機（Support Vector Machine, SVM）是一種強大的監督式學習演算法，由 Vladimir Vapnik 在 1990 年代開發。

## 線性可分情況

### 超平面

在 n 維空間中，(n-1) 維的超平面分隔 n 維空間：

```
二維：直線分隔平面
三維：平面分隔空間
n維：超平面分隔n維空間
```

### 最大邊界分類器

SVM 的目標是找到一個超平面，使兩個類別之間的邊界最大化：

```python
# 最大化邊界
# min  ½ ||w||²
# s.t. yᵢ(w·xᵢ + b) ≥ 1
```

## 核函數

### 核技巧

當資料線性不可分時，SVM 使用核函數將資料映射到高維空間：

```python
# 線性核
K(x, z) = x·z

# 多項式核
K(x, z) = (γx·z + r)^d

# RBF（徑向基函數）核
K(x, z) = exp(-γ||x - z||²)
```

### 選擇核函數

| 核函數 | 適用場景 |
|--------|----------|
| 線性 | 特徵維度高，樣本多 |
| RBF | 特徵維度適中 |
| 多項式 | 需要特徵交互 |

## SVM 推導

### 優化問題

```python
from cvxopt import matrix, solvers

# 最大化 margin 轉換為二次規劃
# min ½ w²
# s.t. yᵢ(w·xᵢ + b) ≥ 1

# 對偶問題
# max Σαᵢ - ½Σαᵢαⱼyᵢyⱼ(xᵢ·xⱼ)
# s.t. Σαᵢyᵢ = 0, αᵢ ≥ 0
```

### 支援向量

只有支援向量（邊界上的點）影響分類器：

```python
# 識別支援向量
support_vectors = X[alphas > 0]
```

## SVM 實現

### scikit-learn

```python
from sklearn import svm

# 建立分類器
clf = svm.SVC(kernel='rbf', C=1.0, gamma='scale')

# 訓練
clf.fit(X_train, y_train)

# 預測
predictions = clf.predict(X_test)
```

### 參數調整

```python
# C：正規化參數（越大越容易過擬合）
clf = svm.SVC(C=10)

# gamma：RBF 核參數
clf = svm.SVC(gamma=0.01)
```

## SVM 的優缺點

### 優點

- 高維空間表現良好
- 記憶體效率高（只需支援向量）
- 多功能性（核函數）

### 缺點

- 對大規模資料訓練時間長
- 對噪聲敏感
- 結果依賴核函數選擇

## 應用場景

| 應用 | 說明 |
|------|------|
| 文字分類 | 垃圾郵件過濾 |
| 影像辨識 | 人臉辨識 |
| 生物資訊 | 蛋白質分類 |
| 異常檢測 | 欺詐偵測 |

## 與其他演算法的比較

| 演算法 | 適用維度 | 樣本數 | 核技巧 |
|--------|----------|--------|--------|
| SVM | 高/中 | 中等 | 必須 |
| 決策樹 | 低/中 | 任意 | 不需要 |
| 類神經網路 | 高 | 大量 | 隱含 |

## 結論

支援向量機是機器學習的重要工具。其最大邊界思想和核技巧使其在高維空間分類問題表現出色。

---

**延伸閱讀**

- [機器學習的數學基礎](article8.md)
- [SVM+tutorial](https://www.google.com/search?q=support+vector+machine+tutorial)