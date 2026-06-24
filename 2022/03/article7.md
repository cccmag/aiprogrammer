# Scikit-learn 模型選擇

## 沒有免費的午餐

機器學習領域有一句名言：沒有免費的午餐定理（No Free Lunch Theorem）。沒有任何一種模型在所有資料集上都表現最好。因此，模型選擇是資料科學家最重要的技能之一。

## 模型選擇的考量因素

| 因素 | 考量 |
|------|------|
| 資料大小 | 小樣本 → 簡單模型；大樣本 → 複雜模型 |
| 特徵數量 | 高維 → 正則化/特徵選擇 |
| 噪音程度 | 高噪音 → 簡單模型防過擬合 |
| 可解釋性 | 醫療/金融 → 線性模型/決策樹 |
| 預測效能 | 不在乎解釋 → 集成/深度學習 |

## 分類模型比較

```python
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier

X, y = make_classification(n_samples=500, n_features=10, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

models = {
    "Logistic Regression": LogisticRegression(),
    "Decision Tree": DecisionTreeClassifier(max_depth=5),
    "Random Forest": RandomForestClassifier(n_estimators=100),
    "Gradient Boosting": GradientBoostingClassifier(),
    "SVM (RBF)": SVC(kernel="rbf"),
    "KNN": KNeighborsClassifier(n_neighbors=5),
}

for name, model in models.items():
    scores = cross_val_score(model, X_train, y_train, cv=5)
    model.fit(X_train, y_train)
    test_score = model.score(X_test, y_test)
    print(f"{name:20} CV={scores.mean():.3f} Test={test_score:.3f}")
```

## 模型複雜度與偏差-方差權衡

```
高偏差（欠擬合）    ←  →    高方差（過擬合）
       │                       │
       └── 複雜度適中 ────────┘
         偏差和方差平衡

模型複雜度增加 → 訓練誤差↓、測試誤差先↓後↑
```

- **高偏差**：模型太簡單，無法捕捉資料模式
- **高方差**：模型太複雜，記住了噪音
- **最佳點**：偏差和方差之間的平衡

## 學習曲線

```python
from sklearn.model_selection import learning_curve

train_sizes, train_scores, test_scores = learning_curve(
    model, X, y, cv=5, train_sizes=np.linspace(0.1, 1.0, 10)
)
```

學習曲線可以幫助診斷：
- 訓練和測試分數之間差距大 → 過擬合
- 兩者都低 → 欠擬合
- 增加更多資料後測試分數上升 → 資料不足

## 驗證曲線

```python
from sklearn.model_selection import validation_curve

param_range = [1, 3, 5, 7, 10, 15, 20]
train_scores, test_scores = validation_curve(
    DecisionTreeClassifier(), X, y, param_name="max_depth",
    param_range=param_range, cv=5
)
```

## 集成方法：多數決的智慧

```python
from sklearn.ensemble import VotingClassifier

ensemble = VotingClassifier([
    ("lr", LogisticRegression()),
    ("rf", RandomForestClassifier()),
    ("svm", SVC(probability=True)),
], voting="soft")

ensemble.fit(X_train, y_train)
```

## 延伸閱讀

- [scikit-learn 模型選擇](https://www.google.com/search?q=scikit-learn+model+selection)
- [偏差-方差權衡](https://www.google.com/search?q=bias+variance+tradeoff)
- [集成學習介紹](https://www.google.com/search?q=ensemble+learning+tutorial)
