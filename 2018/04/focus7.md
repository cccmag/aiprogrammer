# 機器學習專案流程：從資料到模型的完整流程

## 前言

機器學習專案的成功不僅取決於模型的選擇，更取決於整個流程的每個環節。本文將介紹一個完整的機器學習專案流程，幫助讀者系統地掌握機器學習專案的每個步驟。

## 機器學習專案生命週期

```
┌─────────────────────────────────────────────────────┐
│             機器學習專案生命週期                      │
├─────────────────────────────────────────────────────┤
│                                                     │
│  1. 問題定義 ──► 2. 資料收集 ──► 3. 資料預處理      │
│        │                │                │          │
│        ▼                ▼                ▼          │
│  6. 模型部署 ◄── 5. 模型評估 ◄── 4. 模型訓練        │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## 步驟 1：問題定義

### 確定問題類型

- **監督式學習**：分類、迴歸
- **非監督式學習**：分群、降維
- **強化學習**：決策問題

### 定義商業目標

- 這個模型要解決什麼問題？
- 成功的標準是什麼？
- 模型上線後如何衡量效果？

### 設定基線

建立一個簡單的基線模型（Baseline），作為後續改進的參考點。

```python
# 基線模型：總是預測最常見的類別
from sklearn.dummy import DummyClassifier

baseline = DummyClassifier(strategy='most_frequent')
baseline.fit(X_train, y_train)
baseline_score = baseline.score(X_test, y_test)
print(f'基線準確率: {baseline_score:.4f}')
```

## 步驟 2：資料收集

### 資料來源

- 內部資料庫
- 公開資料集
- Web Scraper
- API

### 資料存儲

- CSV/Parquet 檔案
- SQL 資料庫
- NoSQL 資料庫
- Data Lake

### 資料倫理

- 確保有權使用資料
- 保護個人隱私（脫敏處理）
- 遵守法規（如 GDPR）

## 步驟 3：資料預處理

### 探索性資料分析（EDA）

```python
import pandas as pd
import matplotlib.pyplot as plt

# 載入資料
df = pd.read_csv('data.csv')

# 基本統計
print(df.describe())

# 檢查缺失值
print(df.isnull().sum())

# 視覺化分布
df.hist(figsize=(12, 8))
plt.tight_layout()
plt.show()
```

### 處理缺失值

```python
# 刪除有缺失值的行
df.dropna()

# 用均值填補數值型缺失值
df['age'].fillna(df['age'].mean())

# 用眾數填補類別型缺失值
df['city'].fillna(df['city'].mode()[0])

# 用前一個值填補（forward fill）
df['price'].fillna(method='ffill')
```

### 處理異常值

```python
# Z-score 方法
from scipy import stats
import numpy as np

z_scores = np.abs(stats.zscore(df['value']))
df_clean = df[z_scores < 3]

# IQR 方法
Q1 = df['value'].quantile(0.25)
Q3 = df['value'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
df_clean = df[(df['value'] >= lower_bound) &
              (df['value'] <= upper_bound)]
```

### 特徵工程

```python
# 創建新特徵
df['total_spent'] = df['quantity'] * df['unit_price']

# 類別編碼
from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()
df['city_encoded'] = le.fit_transform(df['city'])

# One-Hot 編碼
df = pd.get_dummies(df, columns=['category'])
```

### 訓練/測試分割

```python
from sklearn.model_selection import train_test_split

X = df.drop('target', axis=1)
y = df['target']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
```

## 步驟 4：模型訓練

### 選擇模型

根據問題類型和資料特性選擇模型：

| 問題類型 | 推薦模型 |
|----------|----------|
| 分類（簡單） | 邏輯斯迴歸、決策樹 |
| 分類（複雜） | 隨機森林、SVM、類神經網路 |
| 迴歸（簡單） | 線性迴歸、嶺迴歸 |
| 迴歸（複雜） | 隨機森林、梯度提升 |

### 訓練多個模型

```python
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC

models = {
    'Logistic Regression': LogisticRegression(max_iter=500),
    'Decision Tree': DecisionTreeClassifier(max_depth=10),
    'Random Forest': RandomForestClassifier(n_estimators=100),
    'Gradient Boosting': GradientBoostingClassifier(),
    'SVM': SVC(kernel='rbf')
}

results = {}
for name, model in models.items():
    model.fit(X_train, y_train)
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    results[name] = {
        'train': train_score,
        'test': test_score
    }
    print(f'{name}: Train={train_score:.4f}, Test={test_score:.4f}')
```

### 超參數調優

```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [5, 10, 15],
    'min_samples_split': [2, 5, 10]
}

grid_search = GridSearchCV(
    RandomForestClassifier(),
    param_grid,
    cv=5,
    scoring='accuracy',
    n_jobs=-1
)
grid_search.fit(X_train, y_train)

print(f'最佳參數: {grid_search.best_params_}')
print(f'最佳交叉驗證分數: {grid_search.best_score_:.4f}')
```

## 步驟 5：模型評估

### 評估指標

```python
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, classification_report, confusion_matrix,
    roc_auc_score, roc_curve
)

y_pred = best_model.predict(X_test)

# 基本指標
print(f'準確率: {accuracy_score(y_test, y_pred):.4f}')
print(f'精確率: {precision_score(y_test, y_pred):.4f}')
print(f'召回率: {recall_score(y_test, y_pred):.4f}')
print(f'F1 分數: {f1_score(y_test, y_pred):.4f}')

# 詳細報告
print(classification_report(y_test, y_pred))

# 混淆矩陣
print('混淆矩陣:')
print(confusion_matrix(y_test, y_pred))

# AUC
y_prob = best_model.predict_proba(X_test)[:, 1]
auc = roc_auc_score(y_test, y_prob)
print(f'AUC: {auc:.4f}')
```

### 學習曲線

```python
from sklearn.model_selection import learning_curve

train_sizes, train_scores, test_scores = learning_curve(
    RandomForestClassifier(n_estimators=100),
    X_train, y_train, cv=5, n_jobs=-1,
    train_sizes=np.linspace(0.1, 1.0, 10)
)

# 繪製學習曲線
```

### 模型解釋

```python
# 特徵重要性
feature_importance = pd.DataFrame({
    'feature': X.columns,
    'importance': best_model.feature_importances_
}).sort_values('importance', ascending=False)

print(feature_importance)
```

## 步驟 6：模型部署

### 模型序列化

```python
import joblib

# 儲存模型
joblib.dump(best_model, 'model.pkl')

# 載入模型
model = joblib.load('model.pkl')
```

### 建立預測服務

```python
# predict.py
import joblib
import numpy as np

model = joblib.load('model.pkl')

def predict(input_data):
    """
    輸入: numpy array 或 list
    輸出: 預測結果
    """
    return model.predict(input_data)

if __name__ == '__main__':
    # 測試
    test_input = np.array([[1.0, 2.0, 3.0, 4.0]])
    result = predict(test_input)
    print(f'預測結果: {result}')
```

### API 包裝

```python
# app.py
from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)
model = joblib.load('model.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    input_data = np.array(data['features'])
    prediction = model.predict(input_data)
    return jsonify({'prediction': prediction.tolist()})

if __name__ == '__main__':
    app.run(debug=True)
```

## 專案最佳實踐

1. **版本控制**：使用 Git 管理程式碼
2. **文件記錄**：清楚記錄資料來源、處理步驟、模型參數
3. **實驗追蹤**：使用工具如 MLflow 或 TensorBoard
4. **自動化測試**：確保模型在不同環境下有一致的行為
5. **監控模型**：部署後持續監控模型效能

## 結語

機器學習專案是一個迭代的過程。從問題定義到模型部署，每個步驟都需要仔細規劃和執行。希望本文能幫助讀者建立一個系統化的機器學習專案流程。

---

## 延伸閱讀

- [機器學習專案流程](https://www.google.com/search?q=machine+learning+project+workflow)
- [scikit-learn 機器學習流程](https://www.google.com/search?q=scikit-learn+pipeline+tutorial)
- [ML 專案最佳實踐](https://www.google.com/search?q=machine+learning+best+practices+2018)

---

*本篇文章為「AI 程式人雜誌 2018 年 4 月號」機器學習基礎系列之一。*