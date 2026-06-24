# 機器學習基礎概念

## 簡介

機器學習（Machine Learning）是人工智慧的一個分支，透過演算法讓電腦能從資料中學習並做出預測。本篇介紹機器學習的基礎概念與分類。

## 什麼是機器學習

機器學習是一种讓電腦透過資料學習模式、無須明確編寫規則的科技。傳統程式需要人類定義所有規則，而機器學習從資料中自動發現規則。

### 機器學習 vs 傳統程式

```
傳統程式:
輸入資料 → 規則 → 輸出結果

機器學習:
輸入資料 + 輸出結果 → 學習 → 模型 → 新輸入 → 預測結果
```

## 機器學習分類

### 監督式學習（Supervised Learning）

有標籤的資料，學習輸入到輸出的映射。

```python
# 範例：房價預測
# 輸入：房屋大小、房間數、位置
# 輸出：房價

# 訓練資料
X_train = [[1400, 3, "台北"], [1800, 4, "新北"], [1200, 2, "桃園"]]
y_train = [500, 650, 400]  # 房價（單位：萬）

# 訓練模型
from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(X_train, y_train)

# 預測
X_new = [[1600, 3, "新竹"]]
y_pred = model.predict(X_new)
print(f"預測房價: {y_pred[0]} 萬")
```

### 非監督式學習（Unsupervised Learning）

無標籤資料，發現資料內部結構。

```python
# 範例：客戶分群
from sklearn.cluster import KMeans
import numpy as np

# 客戶消費資料
X = np.array([[100, 30], [150, 40], [30, 10], [200, 60]])

# 分成 2 群
kmeans = KMeans(n_clusters=2)
kmeans.fit(X)

print(kmeans.labels_)  # [0, 0, 1, 0] 各客戶所屬群組
```

### 強化學習（Reinforcement Learning）

透過環境回饋學習最佳策略。

```python
# 概念示意（實際應用更複雜）
# 代理（Agent）在環境（Environment）中採取行動（Action）
# 根據獎勵（Reward）學習最佳策略（Policy）

class SimpleAgent:
    def __init__(self):
        self.epsilon = 0.1  # 探索機率

    def choose_action(self, state):
        if self.epsilon > random.random():
            return random.choice(["left", "right"])
        return self.q_table.get(state, "left")
```

## 常見演算法

### 監督式學習

| 演算法 | 用途 | 類型 |
|--------|------|------|
| 線性回歸 | 數值預測 | 回歸 |
| 邏輯回歸 | 分類 | 分類 |
| 決策樹 | 分類/回歸 | 通用 |
| 隨機森林 | 分類/回歸 | 集成 |
| SVM | 分類 | 分類 |
| KNN | 分類 | 分類 |

### 非監督式學習

| 演算法 | 用途 |
|--------|------|
| K-Means | 分群 |
| DBSCAN | 分群 |
| PCA | 降維 |
| 關聯規則 | 關聯分析 |

## 機器學習流程

### 1. 資料收集

```python
# 從檔案載入
import pandas as pd
df = pd.read_csv("data.csv")

# 從 API 取得
import requests
response = requests.get("https://api.example.com/data")
data = response.json()
```

### 2. 資料前處理

```python
# 處理缺失值
df.fillna(df.mean(), inplace=True)

# 特徵縮放
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 編碼類別變數
from sklearn.preprocessing import LabelEncoder
encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)
```

### 3. 分割資料

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
```

### 4. 訓練模型

```python
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
```

### 5. 評估模型

```python
from sklearn.metrics import accuracy_score, classification_report

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"準確率: {accuracy:.2f}")

print(classification_report(y_test, y_pred))
```

### 6. 模型調參

```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    "n_estimators": [50, 100, 200],
    "max_depth": [None, 10, 20]
}

grid_search = GridSearchCV(
    RandomForestClassifier(),
    param_grid,
    cv=5
)
grid_search.fit(X_train, y_train)
print(f"最佳參數: {grid_search.best_params_}")
```

## 機器學習的挑戰

1. **資料品質** - 雜訊、缺失值、偏差
2. **過擬合** - 模型過度擬合訓練資料
3. **維度災難** - 特徵過多導致效能下降
4. **可解釋性** - 模型決策難以解釋

## 建議學習路徑

1. Python 基礎
2. NumPy、Pandas 資料處理
3. Scikit-learn 基本操作
4. 統計與線性代數基礎
5. 特定領域深度學習