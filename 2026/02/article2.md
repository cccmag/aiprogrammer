# scikit-learn 入門

## 什麼是 scikit-learn？

scikit-learn 是 Python 生態系中最流行的機器學習套件。它提供了統一的 API 和豐富的演算法實作，涵蓋分類、迴歸、聚類、降維、模型選擇和預處理等任務。

### 安裝

```bash
pip install scikit-learn
```

### 統一 API

scikit-learn 的核心設計哲學是統一的 Estimator API：

1. **所有模型都繼承 `BaseEstimator`**
2. **訓練用 `fit(X, y)`**
3. **預測用 `predict(X)`**
4. **評估用 `score(X, y)`**

這種一致性讓開發者可以輕鬆切換不同演算法。

## 快速開始

以下示範一個完整的 scikit-learn 工作流程：

```python
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report

# 1. 載入資料
iris = load_iris()
X, y = iris.data, iris.target

# 2. 分割資料
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 3. 特徵標準化
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 4. 訓練模型
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X_train_scaled, y_train)

# 5. 評估模型
y_pred = knn.predict(X_test_scaled)
print(classification_report(y_test, y_pred, target_names=iris.target_names))
```

## 核心模組

### 資料集

```python
from sklearn.datasets import (
    load_iris,       # 鳶尾花資料集（分類）
    load_diabetes,   # 糖尿病資料集（迴歸）
    make_classification,  # 人造分類資料
    make_regression       # 人造迴歸資料
)
```

### 預處理

```python
from sklearn.preprocessing import (
    StandardScaler,   # 標準化（Z-score）
    MinMaxScaler,     # 歸一化到 [0, 1]
    LabelEncoder,     # 標籤編碼
    OneHotEncoder     # 獨熱編碼
)
```

### 模型選擇

```python
from sklearn.model_selection import (
    train_test_split,  # 資料分割
    cross_val_score,   # 交叉驗證
    GridSearchCV,      # 網格搜尋參數
    learning_curve     # 學習曲線
)
```

### 常用模型

```python
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
```

### 評估指標

```python
from sklearn.metrics import (
    accuracy_score,     # 準確率
    precision_score,    # 精確率
    recall_score,       # 召回率
    f1_score,           # F1 分數
    confusion_matrix,   # 混淆矩陣
    mean_squared_error, # 均方誤差
    r2_score            # 決定係數
)
```

## Pipeline：串接工作流程

Pipeline 將預處理和模型訓練串接成一個單一元件：

```python
from sklearn.pipeline import Pipeline

pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("classifier", RandomForestClassifier())
])

# 一次訓練整個流程
pipeline.fit(X_train, y_train)
y_pred = pipeline.predict(X_test)
```

## 為什麼選擇 scikit-learn？

- **成熟穩定**：2007 年發布至今，社群龐大
- **文件齊全**：官方文件和範例極其豐富
- **與 NumPy/SciPy 整合**：底層資料結構互通
- **商業友好**：BSD 授權

scikit-learn 是進入機器學習世界的最佳起點。掌握它之後，要學習 PyTorch、TensorFlow 等深度學習框架也會更容易。

---

## 延伸閱讀

- [scikit-learn 官方教學](https://www.google.com/search?q=scikit-learn+tutorial)
- [scikit-learn API 參考](https://www.google.com/search?q=scikit-learn+api+reference)
- [scikit-learn 範例集](https://www.google.com/search?q=scikit-learn+examples)
