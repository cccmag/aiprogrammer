# 集成學習簡介

## 集成學習概念

集成學習透過組合多個基礎模型来提升整體預測效能，是機器學習中最重要的技術之一。

## 集成學習三大策略

1. **Bagging**：平行訓練，最終投票平均
2. **Boosting**：序列訓練，逐步修正錯誤
3. **Stacking**：堆疊多層模型

## Bagging 與 Bootstrap

Bagging（Bootstrap Aggregating）使用自助採樣（bootstrap sampling）生成多個訓練集，分別訓練模型後投票。

```python
from sklearn.ensemble import BaggingClassifier, RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

X, y = make_classification(n_samples=500, n_features=20, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

bagging = BaggingClassifier(
    estimator=DecisionTreeClassifier(max_depth=5),
    n_estimators=10,
    random_state=42
)
bagging.fit(X_train, y_train)
print(f"Bagging 測試分數: {bagging.score(X_test, y_test):.2%}")
```

## 隨機森林（屬於 Bagging）

```python
rf = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
rf.fit(X_train, y_train)
print(f"隨機森林測試分數: {rf.score(X_test, y_test):.2%}")
```

## Boosting 概念

Boosting 序列訓練模型，每個模型專注於修正前一個模型的錯誤。

### AdaBoost

```python
from sklearn.ensemble import AdaBoostClassifier

adaboost = AdaBoostClassifier(n_estimators=50, random_state=42)
adaboost.fit(X_train, y_train)
print(f"AdaBoost 測試分數: {adaboost.score(X_test, y_test):.2%}")
```

### Gradient Boosting

```python
from sklearn.ensemble import GradientBoostingClassifier

gb = GradientBoostingClassifier(n_estimators=100, max_depth=3, random_state=42)
gb.fit(X_train, y_train)
print(f"Gradient Boosting 測試分數: {gb.score(X_test, y_test):.2%}")
```

### XGBoost

```python
try:
    from xgboost import XGBClassifier

    xgb = XGBClassifier(n_estimators=100, max_depth=3, random_state=42)
    xgb.fit(X_train, y_train)
    print(f"XGBoost 測試分數: {xgb.score(X_test, y_test):.2%}")
except ImportError:
    print("XGBoost 未安裝")
```

### LightGBM

```python
try:
    from lightgbm import LGBMClassifier

    lgbm = LGBMClassifier(n_estimators=100, max_depth=3, random_state=42)
    lgbm.fit(X_train, y_train)
    print(f"LightGBM 測試分數: {lgbm.score(X_test, y_test):.2%}")
except ImportError:
    print("LightGBM 未安裝")
```

## Stacking

Stacking 使用多個基礎模型的預測作為輸入，訓練一個元分類器。

```python
from sklearn.ensemble import StackingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

estimators = [
    ('rf', RandomForestClassifier(n_estimators=50, max_depth=5, random_state=42)),
    ('svm', SVC(kernel='rbf', probability=True, random_state=42)),
    ('knn', KNeighborsClassifier(n_neighbors=5))
]

stacking = StackingClassifier(
    estimators=estimators,
    final_estimator=LogisticRegression(),
    cv=5
)
stacking.fit(X_train, y_train)
print(f"Stacking 測試分數: {stacking.score(X_test, y_test):.2%}")
```

## Voting Classifier

### 硬投票（Hard Voting）

```python
from sklearn.ensemble import VotingClassifier

voting_hard = VotingClassifier(
    estimators=[
        ('rf', RandomForestClassifier(n_estimators=50, random_state=42)),
        ('gb', GradientBoostingClassifier(n_estimators=50, random_state=42)),
        ('lr', LogisticRegression(max_iter=200, random_state=42))
    ],
    voting='hard'
)
voting_hard.fit(X_train, y_train)
print(f"Hard Voting 測試分數: {voting_hard.score(X_test, y_test):.2%}")
```

### 軟投票（Soft Voting）

```python
voting_soft = VotingClassifier(
    estimators=[
        ('rf', RandomForestClassifier(n_estimators=50, random_state=42)),
        ('gb', GradientBoostingClassifier(n_estimators=50, random_state=42)),
        ('lr', LogisticRegression(max_iter=200, random_state=42))
    ],
    voting='soft'
)
voting_soft.fit(X_train, y_train)
print(f"Soft Voting 測試分數: {voting_soft.score(X_test, y_test):.2%}")
```

## 集成方法比較

```python
models = {
    'Decision Tree': DecisionTreeClassifier(max_depth=5, random_state=42),
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
    'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
    'AdaBoost': AdaBoostClassifier(n_estimators=100, random_state=42)
}

results = {}
for name, model in models.items():
    model.fit(X_train, y_train)
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    results[name] = {'train': train_score, 'test': test_score}
    print(f"{name}: 訓練={train_score:.2%}, 測試={test_score:.2%}")
```

## 集成學習的優點

1. 提升預測準確率
2. 減少過擬合風險
3. 提高模型穩定性

## 參考資源

- https://www.google.com/search?q=ensemble+learning+bagging+boosting+stacking+Python+2019
- https://www.google.com/search?q=Random+Forest+Gradient+Boosting+XGBoost+Python+2019
- https://www.google.com/search?q=Voting+Classifier+sklearn+ensemble+Python+2019