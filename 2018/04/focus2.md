# 監督式學習：分類與迴歸的基礎理論

## 前言

監督式學習是機器學習中最常見的類型。在監督式學習中，我們有一組已經標註過的訓練資料，每筆資料包含輸入特征和正確的輸出標籤。演算法的任務是學習一個從輸入到輸出的映射函數，能夠對新的、未見過的資料做出準確預測。

## 監督式學習的兩大類型

### 1. 分類（Classification）

分類問題的輸出是離散的類別標籤。例如：
- 電子郵件分類：垃圾郵件 vs 正常郵件
- 圖像辨識：貓 vs 狗 vs 鳥
- 疾病診斷：有病 vs 無病
- 信用風險：高風險 vs 中風險 vs 低風險

### 2. 迴歸（Regression）

迴歸問題的輸出是連續的數值。例如：
- 房價預測：50 萬 ~ 500 萬
- 溫度預測：15°C ~ 35°C
- 銷售額預測：10 萬 ~ 1000 萬

```
┌─────────────────────────────────────────────────────┐
│                 分類 vs 迴歸                         │
├─────────────────────────────────────────────────────┤
│                                                     │
│   分類：輸出是類別                                    │
│   ┌─────┐    ┌─────┐    ┌─────┐                  │
│   │ 類別A │    │ 類別B │    │ 類別C │                  │
│   └─────┘    └─────┘    └─────┘                  │
│                                                     │
│   迴歸：輸出是連續數值                                │
│   ┌─────────────────────────────────┐             │
│   │  50    100   150   200   250    │             │
│   └─────────────────────────────────┘             │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## 線性迴歸（Linear Regression）

### 簡單線性迴歸

簡單線性迴歸模型：
```
y = wx + b
```

其中：
- y 是預測值（輸出）
- x 是輸入特征
- w 是權重（斜率）
- b 是偏置（截距）

目標：找到最佳的 w 和 b，使得預測值與真實值的誤差最小。

### 代價函數

使用均方誤差（Mean Squared Error, MSE）作為代價函數：
```
MSE = (1/n) * Σ(y_pred - y_true)²
```

### 梯度下降法

使用梯度下降（Gradient Descent）來優化：
```
w = w - α * ∂MSE/∂w
b = b - α * ∂MSE/∂b
```

其中 α 是學習率（Learning Rate）。

## 邏輯斯迴歸（Logistic Regression）

雖然名字叫「迴歸」，邏輯斯迴歸實際上是一個分類演算法！它用於二分類問題。

### sigmoid 函數

邏輯斯迴歸使用 sigmoid 函數將輸出轉換為 0~1 之間的機率：
```
σ(z) = 1 / (1 + e^(-z))
```

### 決策邊界

當 σ(z) > 0.5 時，預測為類別 1；否則為類別 0。

## 決策樹（Decision Tree）

決策樹通過一系列的是/否問題來進行預測。每個內部節點代表一個特征上的測試，每個葉節點代表一個類別或數值。

### 決策樹的建構

1. 選擇最佳的特征進行分割
2. 遞迴地對每個子集建構子树
3. 當滿足停止條件時建立葉節點

### 信息增益（Information Gain）

使用信息增益或 Gini 不純度來選擇分割特征：
- 信息增益 = 母節點的熵 - 子節點加權平均熵

### 決策樹的問題

- 容易過擬合（Overfitting）
- 對資料的小變化敏感

**解決方法**：隨機森林（Random Forest）—— 使用多棵樹進行投票。

## 隨機森林（Random Forest）

隨機森林是一種集成學習（Ensemble Learning）方法，它結合多棵決策樹的預測結果。

### 特點

- **Bagging**：對訓練資料進行有放回抽樣
- **特征子集**：每棵樹只使用部分特征
- **投票機制**：多棵樹投票決定最終輸出

### 優勢

- 不容易過擬合
- 能處理高維度資料
- 能處理缺失值

## 支援向量機（Support Vector Machine, SVM）

SVM 的目標是找到一個「最大間隔」的超平面來分隔不同類別的資料點。

### 核函數（Kernel Function）

SVM 可以使用核函數來處理非線性可分的資料：
- 線性核（Linear Kernel）
- 多項式核（Polynomial Kernel）
- 徑向基核函數（RBF Kernel）

```
┌─────────────────────────────────────────────────────┐
│                 SVM 的核函數                         │
├─────────────────────────────────────────────────────┤
│                                                     │
│   線性可分：使用線性核                                │
│   ┌─────────────────────────────────┐             │
│   │    A A A    B B B               │             │
│   │    A A A    B B B               │             │
│   └─────────────────────────────────┘             │
│                                                     │
│   非線性可分：使用 RBF 核                             │
│   ┌─────────────────────────────────┐             │
│   │      ╭───────╮                  │             │
│   │   ╭──┤ A A A ├──╮               │             │
│   │   │  ╰───────╯  │               │             │
│   │   │    B B B    │               │             │
│   └─────────────────────────────────┘             │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## 實作：使用 scikit-learn 進行分類

```python
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report

# 載入資料
iris = load_iris()
X, y = iris.data, iris.target

# 分割資料
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 特徵標準化
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 建立模型
models = {
    'Logistic Regression': LogisticRegression(max_iter=200),
    'Decision Tree': DecisionTreeClassifier(max_depth=5),
    'Random Forest': RandomForestClassifier(n_estimators=100),
    'SVM': SVC(kernel='rbf')
}

# 訓練和評估
for name, model in models.items():
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    print(f'{name}: {accuracy:.4f}')
```

## 結語

監督式學習是機器學習的核心，涵蓋了從簡單的線性迴歸到複雜的類神經網路等多種演算法。選擇合適的演算法需要考慮：
- 問題類型（分類還是迴歸）
- 資料量與特徵維度
- 計算資源
- 可解釋性需求

下一篇文章將介紹非監督式學習，包括分群和降維等重要技術。

---

## 延伸閱讀

- [scikit-learn 監督式學習文檔](https://www.google.com/search?q=scikit-learn+supervised+learning)
- [機器學習中的分類演算法](https://www.google.com/search?q=classification+algorithms+machine+learning)
- [邏輯斯迴歸詳解](https://www.google.com/search?q=logistic+regression+tutorial)

---

*本篇文章為「AI 程式人雜誌 2018 年 4 月號」機器學習基礎系列之一。*