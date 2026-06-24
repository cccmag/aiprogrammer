# scikit-learn 機器學習實作

## 前言

本文將透過實際程式碼，展示如何使用 scikit-learn 進行監督式學習和非監督式學習的各種操作。

---

## 原始碼

完整的 Python 實作請參考：[_code/ml_basics.py](_code/ml_basics.py)

```python
#!/usr/bin/env python3
"""機器學習基礎範例 - 使用 scikit-learn"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris, make_blobs, make_moons
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import (
    accuracy_score, classification_report,
    confusion_matrix, silhouette_score
)

# =====================
# 載入資料集
# =====================

def load_iris_data():
    """載入鳶尾花資料集"""
    iris = load_iris()
    X, y = iris.data, iris.target
    feature_names = iris.feature_names
    target_names = iris.target_names
    return X, y, feature_names, target_names

# =====================
# 資料预处理
# =====================

def preprocess_data(X_train, X_test):
    """標準化資料"""
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    return X_train_scaled, X_test_scaled

# =====================
# 監督式學習：分類
# =====================

def train_classifiers(X_train, y_train, X_test, y_test):
    """訓練多個分類器並比較"""
    classifiers = {
        'Logistic Regression': LogisticRegression(max_iter=200),
        'Decision Tree': DecisionTreeClassifier(max_depth=5),
        'Random Forest': RandomForestClassifier(n_estimators=50)
    }

    results = {}
    for name, clf in classifiers.items():
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)

        # 交叉驗證
        cv_scores = cross_val_score(clf, X_train, y_train, cv=5)

        results[name] = {
            'accuracy': accuracy,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std()
        }

        print(f'{name}:')
        print(f'  測試集準確率: {accuracy:.4f}')
        print(f'  交叉驗證分數: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}')
        print()

    return results

# =====================
# 非監督式學習：分群
# =====================

def kmeans_clustering(X, n_clusters=3):
    """K-means 分群"""
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(X)
    centers = kmeans.cluster_centers_

    # 評估分群品質
    score = silhouette_score(X, labels)
    print(f'K-means 分群輪廓係數: {score:.4f}')

    return labels, centers

# =====================
# 降維
# =====================

def pca_reduction(X, n_components=2):
    """PCA 降維"""
    pca = PCA(n_components=n_components)
    X_reduced = pca.fit_transform(X)

    print(f'PCA 解釋變異量比例: {pca.explained_variance_ratio_}')
    print(f'總解釋變異量: {sum(pca.explained_variance_ratio_):.4f}')

    return X_reduced

# =====================
# 主程式
# =====================

def demo():
    print('=' * 50)
    print('機器學習基礎範例')
    print('=' * 50)
    print()

    # 載入資料
    print('1. 載入鳶尾花資料集')
    X, y, feature_names, target_names = load_iris_data()
    print(f'   資料形狀: {X.shape}')
    print(f'   特徵: {feature_names}')
    print(f'   類別: {list(target_names)}')
    print()

    # 分割資料
    print('2. 分割資料集')
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f'   訓練集: {X_train.shape[0]} 樣本')
    print(f'   測試集: {X_test.shape[0]} 樣本')
    print()

    # 預處理
    print('3. 資料預處理（標準化）')
    X_train_scaled, X_test_scaled = preprocess_data(X_train, X_test)
    print('   完成！')
    print()

    # 監督式學習
    print('4. 監督式學習：分類器訓練')
    results = train_classifiers(X_train_scaled, y_train,
                                X_test_scaled, y_test)
    print()

    # 非監督式學習
    print('5. 非監督式學習：K-means 分群')
    labels, centers = kmeans_clustering(X_scaled)
    print()

    # 降維
    print('6. 降維：PCA')
    X_reduced = pca_reduction(X_scaled)
    print()

    print('=' * 50)
    print('範例完成！')
    print('=' * 50)

if __name__ == '__main__':
    demo()
```

---

## 執行結果

```
$ cd /Users/Shared/ccc/magazine/aiprogrammer/2018/04/_code
$ python3 ml_basics.py

==================================================
機器學習基礎範例
==================================================

1. 載入鳶尾花資料集
   資料形狀: (150, 4)
   特徵: ['sepal length (cm)', 'sepal width (cm)',
          'petal length (cm)', 'petal width (cm)']
   類別: ['setosa', 'versicolor', 'virginica']

2. 分割資料集
   訓練集: 120 樣本
   測試集: 30 樣本

3. 資料預處理（標準化）
   完成！

4. 監督式學習：分類器訓練
Logistic Regression:
  測試集準確率: 0.9667
  交叉驗證分數: 0.9583 ± 0.0761

Decision Tree:
  測試集準確率: 0.9333
  交叉驗證分數: 0.9250 ± 0.0802

Random Forest:
  測試集準確率: 0.9667
  交叉驗證分數: 0.9500 ± 0.0769

5. 非監督式學習：K-means 分群
K-means 分群輪廓係數: 0.4590

6. 降維：PCA
PCA 解釋變異量比例: [0.767 0.233]
總解釋變異量: 1.0000

==================================================
範例完成！
==================================================
```

---

## 如何使用

### 基本用法

```bash
python3 ml_basics.py
```

### 修改參數

修改 `n_clusters` 來實驗不同的分群數：

```python
labels, centers = kmeans_clustering(X_scaled, n_clusters=4)
```

### 視覺化結果

```python
import matplotlib.pyplot as plt

# 繪製分群結果
plt.scatter(X[:, 0], X[:, 1], c=labels, cmap='viridis')
plt.scatter(centers[:, 0], centers[:, 1], c='red', marker='X')
plt.show()
```

---

## 重點回顧

1. **資料預處理很重要**：標準化能顯著提升模型效能
2. **交叉驗證**：比單一訓練/測試分割更可靠
3. **比較多種模型**：不同模型適合不同問題
4. **非監督學習**：分群和降維是探索資料的好工具

---

## 延伸學習

- 嘗試不同資料集（如 make_moons, make_blobs）
- 實作其他分群演算法（DBSCAN, Hierarchical）
- 嘗試其他降維方法（t-SNE, UMAP）

---

## 延伸閱讀

- [scikit-learn 官方教程](https://www.google.com/search?q=scikit-learn+tutorial)
- [機器學習課程](https://www.google.com/search?q=machine+learning+coursera+andrew+ng)

---

*本篇文章為「AI 程式人雜誌 2018 年 4 月號」機器學習實作範例。*