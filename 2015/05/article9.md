# scikit-learn 機器學習基礎

## scikit-learn 簡介

scikit-learn 是 Python 中最流行的機器學習庫，提供了從資料預處理到模型訓練、評估的完整工具鏈。

## 機器學習工作流程

```
1. 載入資料
   ↓
2. 预处理（標準化、編碼等）
   ↓
3. 分割資料（訓練集、測試集）
   ↓
4. 選擇模型
   ↓
5. 訓練模型
   ↓
6. 評估模型
   ↓
7. 預測新資料
```

## 載入資料

```python
from sklearn.datasets import load_iris

# 載入經典的鳶尾花資料集
iris = load_iris()
X = iris.data  # 特徵
y = iris.target  # 標籤

print(f"資料形狀：{X.shape}")
print(f"類別：{iris.target_names}")  # ['setosa', 'versicolor', 'virginica']
```

## 資料預處理

```python
from sklearn.preprocessing import StandardScaler

# 標準化（均值為0，標準差為1）
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
```

## 分割資料

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)
```

## 訓練模型

### 監督式學習

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

# 隨機森林
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# 邏輯回歸
clf = LogisticRegression(max_iter=1000)
clf.fit(X_train, y_train)

# SVM
clf = SVC(kernel='rbf')
clf.fit(X_train, y_train)
```

### 非監督式學習

```python
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

# K-Means 聚類
kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(X)

# PCA 降維
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)
```

## 評估模型

```python
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# 預測
y_pred = clf.predict(X_test)

# 準確率
print(f"準確率：{accuracy_score(y_test, y_pred):.2f}")

# 詳細報告
print(classification_report(y_test, y_pred, target_names=iris.target_names))

# 混淆矩陣
print(confusion_matrix(y_test, y_pred))
```

## 交叉驗證

```python
from sklearn.model_selection import cross_val_score

scores = cross_val_score(clf, X_scaled, y, cv=5)
print(f"交叉驗證分數：{scores}")
print(f"平均分數：{scores.mean():.3f} (+/- {scores.std() * 2:.3f})")
```

## 超參數調優

```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [None, 10, 20]
}

grid_search = GridSearchCV(
    RandomForestClassifier(random_state=42),
    param_grid,
    cv=5,
    scoring='accuracy'
)
grid_search.fit(X_train, y_train)

print(f"最佳參數：{grid_search.best_params_}")
print(f"最佳分數：{grid_search.best_score_:.3f}")
```

## 結論

scikit-learn 提供了統一的介面，讓機器學習變得簡單易懂。掌握這些基礎工具，可以幫助你快速入門機器學習領域。