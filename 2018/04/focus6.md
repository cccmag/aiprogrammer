# scikit-learn 入門：Python 機器學習庫的使用

## 前言

scikit-learn 是 Python 生態系統中最受歡迎的機器學習庫之一。它提供了從資料预处理到模型訓練、評估的完整工具鏈，且 API 設計優雅，深受開發者喜愛。

## scikit-learn 簡介

### 特色

- **簡潔一致的 API**：所有模型都遵循相同的 API 設計
- **完整的工具鏈**：從資料预处理到模型評估
- **豐富的演算法**：涵蓋監督式、非監督式學習
- **開源免費**：BSD 許可

### 安裝

```bash
pip install scikit-learn
```

或使用 conda：
```bash
conda install scikit-learn
```

## Estimator API

scikit-learn 的核心是 Estimator API，主要包含三個方法：

```python
# 1. 建立模型
model = SomeModel hyperparameters)

# 2. 訓練模型
model.fit(X_train, y_train)

# 3. 預測
y_pred = model.predict(X_test)

# 額外：獲取預測機率（分類器）
y_prob = model.predict_proba(X_test)
```

## 常見機器學習流程

### 載入資料

```python
from sklearn.datasets import load_iris

# 載入內建資料集
iris = load_iris()
X, y = iris.data, iris.target

print(f'特徵: {iris.feature_names}')
print(f'類別: {iris.target_names}')
print(f'資料形狀: {X.shape}')
```

### 分割資料

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
```

### 特徵標準化

```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)  # 注意：只用 training set 的統計量
```

### 訓練模型

```python
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

# 邏輯斯迴歸
log_reg = LogisticRegression(max_iter=200)
log_reg.fit(X_train_scaled, y_train)

# 決策樹
dt_clf = DecisionTreeClassifier(max_depth=5)
dt_clf.fit(X_train_scaled, y_train)

# 隨機森林
rf_clf = RandomForestClassifier(n_estimators=100)
rf_clf.fit(X_train_scaled, y_train)

# SVM
svm_clf = SVC(kernel='rbf', probability=True)
svm_clf.fit(X_train_scaled, y_train)
```

### 評估模型

```python
from sklearn.metrics import accuracy_score, classification_report

models = {
    'Logistic Regression': log_reg,
    'Decision Tree': dt_clf,
    'Random Forest': rf_clf,
    'SVM': svm_clf
}

for name, model in models.items():
    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    print(f'{name}: {accuracy:.4f}')
```

### 完整範例

```python
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report

# 載入資料
data = load_breast_cancer()
X, y = data.data, data.target

# 分割資料
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 建立 Pipeline：標準化 + 邏輯斯迴歸
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', LogisticRegression(max_iter=500))
])

# 交叉驗證
cv_scores = cross_val_score(pipeline, X_train, y_train, cv=5)
print(f'交叉驗證分數: {cv_scores}')
print(f'平均分數: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}')

# 訓練最終模型
pipeline.fit(X_train, y_train)

# 預測和評估
y_pred = pipeline.predict(X_test)
print(classification_report(y_test, y_pred,
                           target_names=data.target_names))
```

## Pipeline

Pipeline 將多個步驟串聯在一起，確保資料處理的一致性：

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression

pipeline = Pipeline([
    ('scaler', StandardScaler()),      # 步驟 1: 標準化
    ('pca', PCA(n_components=10)),      # 步驟 2: PCA 降維
    ('classifier', LogisticRegression()) # 步驟 3: 分類
])

# 一次呼叫 fit，Pipeline 會自動執行所有步驟
pipeline.fit(X_train, y_train)
y_pred = pipeline.predict(X_test)
```

## 特徵工程

### 特徵選擇

```python
from sklearn.feature_selection import SelectKBest, f_classif

# 選擇最重要的 K 個特徵
selector = SelectKBest(f_classif, k=5)
X_train_selected = selector.fit_transform(X_train, y_train)
X_test_selected = selector.transform(X_test)

# 查看每個特徵的分數
feature_scores = selector.scores_
for name, score in zip(feature_names, feature_scores):
    print(f'{name}: {score:.4f}')
```

### 處理類別特徵

```python
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer

# 假設有 categorical 和 numerical 兩種特徵
preprocessor = ColumnTransformer([
    ('num', StandardScaler(), numeric_features),
    ('cat', OneHotEncoder(), categorical_features)
])

X_processed = preprocessor.fit_transform(X)
```

## 超參數搜索

```python
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC

param_grid = {
    'C': [0.1, 1, 10],
    'kernel': ['linear', 'rbf'],
    'gamma': [0.1, 1, 10]
}

grid_search = GridSearchCV(
    SVC(), param_grid, cv=5, scoring='accuracy', n_jobs=-1
)
grid_search.fit(X_train, y_train)

print(f'最佳參數: {grid_search.best_params_}')
print(f'最佳分數: {grid_search.best_score_:.4f}')

# 使用最佳模型預測
best_model = grid_search.best_estimator_
y_pred = best_model.predict(X_test)
```

## 模型持久化

```python
from sklearn.externals import joblib

# 儲存模型
joblib.dump(model, 'model.pkl')

# 載入模型
loaded_model = joblib.load('model.pkl')
y_pred = loaded_model.predict(X_test)
```

或者使用 pickle（不推薦用於生產環境）：

```python
import pickle

with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('model.pkl', 'rb') as f:
    model = pickle.load(f)
```

## scikit-learn 速查表

```
┌─────────────────────────────────────────────────────┐
│              scikit-learn 速查表                     │
├─────────────────────────────────────────────────────┤
│                                                     │
│  分類                                                │
│  ├─ LogisticRegression  邏輯斯迴歸                  │
│  ├─ DecisionTreeClassifier  決策樹                   │
│  ├─ RandomForestClassifier  隨機森林                 │
│  ├─ SVM  支援向量機                                  │
│  ├─ KNeighborsClassifier  K-近鄰                     │
│  └─ GaussianNB  高斯樸素貝葉斯                       │
│                                                     │
│  迴歸                                                │
│  ├─ LinearRegression  線性迴歸                      │
│  ├─ Ridge  Ridge 迴歸                               │
│  ├─ Lasso  Lasso 迴歸                               │
│  └─ RandomForestRegressor  隨機森林迴歸              │
│                                                     │
│  分群                                                │
│  ├─ KMeans  K-平均                                   │
│  ├─ DBSCAN  密度分群                                 │
│  └─ AgglomerativeClustering  階層分群               │
│                                                     │
│  降維                                                │
│  ├─ PCA  主成分分析                                  │
│  └─ t-SNE  t-分佈隨機鄰近嵌入                        │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## 結語

scikit-learn 為 Python 機器學習提供了統一、簡潔的 API。本文介紹了從資料載入、预处理、模型訓練到評估的完整流程。熟練掌握 scikit-learn 是進入機器學習領域的重要一步。

下一篇文章將介紹機器學習專案的完整流程，從問題定義到模型部署。

---

## 延伸閱讀

- [scikit-learn 官方網站](https://www.google.com/search?q=scikit-learn+official+site)
- [scikit-learn 教程](https://www.google.com/search?q=scikit-learn+tutorial+beginner)
- [scikit-learn API 參考](https://www.google.com/search?q=scikit-learn+API+documentation)

---

*本篇文章為「AI 程式人雜誌 2018 年 4 月號」機器學習基礎系列之一。*