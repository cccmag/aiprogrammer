# 決策樹與隨機森林

## 決策樹概念

決策樹是一種監督式學習演算法，用於分類與迴歸問題。它透過學習簡單的規則構建出一棵樹狀模型。

## 決策樹構建

```python
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.2, random_state=42
)

clf = DecisionTreeClassifier(max_depth=3, random_state=42)
clf.fit(X_train, y_train)

plt.figure(figsize=(15, 10))
plot_tree(clf, feature_names=iris.feature_names,
          class_names=iris.target_names, filled=True)
plt.title('Decision Tree')
plt.show()

print(f"訓練集分數: {clf.score(X_train, y_train):.2%}")
print(f"測試集分數: {clf.score(X_test, y_test):.2%}")
```

## 決策樹切割準則

### Gini 不純度

```python
clf_gini = DecisionTreeClassifier(criterion='gini', max_depth=3)
clf_gini.fit(X_train, y_train)
print(f"Gini - 訓練分數: {clf_gini.score(X_train, y_train):.2%}")
print(f"Gini - 測試分數: {clf_gini.score(X_test, y_test):.2%}")
```

### 資訊熵（Entropy）

```python
clf_entropy = DecisionTreeClassifier(criterion='entropy', max_depth=3)
clf_entropy.fit(X_train, y_train)
print(f"Entropy - 訓練分數: {clf_entropy.score(X_train, y_train):.2%}")
print(f"Entropy - 測試分數: {clf_entropy.score(X_test, y_test):.2%}")
```

## 特徵重要性

```python
importances = clf.feature_importances_
for name, importance in zip(iris.feature_names, importances):
    print(f"{name}: {importance:.3f}")

plt.figure(figsize=(10, 6))
plt.barh(iris.feature_names, importances)
plt.xlabel('Importance')
plt.title('Feature Importance - Decision Tree')
plt.show()
```

## 隨機森林概念

隨機森林是多棵決策樹的集成，透過多數投票決定最終預測結果。

## 隨機森林實作

```python
from sklearn.ensemble import RandomForestClassifier

rf_clf = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
rf_clf.fit(X_train, y_train)

print(f"隨機森林 - 訓練分數: {rf_clf.score(X_train, y_train):.2%}")
print(f"隨機森林 - 測試分數: {rf_clf.score(X_test, y_test):.2%}")
```

## n_estimators 影響

```python
estimators = [10, 50, 100, 200, 500]
for n in estimators:
    rf = RandomForestClassifier(n_estimators=n, max_depth=5, random_state=42)
    rf.fit(X_train, y_train)
    print(f"n_estimators={n}: 測試分數={rf.score(X_test, y_test):.2%}")
```

## 超參數調優

```python
rf = RandomForestClassifier(
    n_estimators=100,
    max_depth=None,
    min_samples_split=2,
    min_samples_leaf=1,
    max_features='sqrt',
    bootstrap=True,
    random_state=42
)
rf.fit(X_train, y_train)
print(f"最佳參數 - 測試分數: {rf.score(X_test, y_test):.2%}")
```

## 特徵重要性（隨機森林）

```python
rf_importances = rf.feature_importances_
plt.figure(figsize=(10, 6))
plt.barh(iris.feature_names, rf_importances)
plt.xlabel('Importance')
plt.title('Feature Importance - Random Forest')
plt.show()

print("\n隨機森林特徵重要性:")
for name, importance in zip(iris.feature_names, rf_importances):
    print(f"  {name}: {importance:.3f}")
```

## Extra Trees

Extra Trees（Extremely Randomized Trees）比隨機森林更隨機，隨機選擇切割點。

```python
from sklearn.ensemble import ExtraTreesClassifier

et_clf = ExtraTreesClassifier(n_estimators=100, max_depth=5, random_state=42)
et_clf.fit(X_train, y_train)
print(f"Extra Trees - 測試分數: {et_clf.score(X_test, y_test):.2%}")
```

## 比較決策樹與隨機森林

```python
from sklearn.datasets import make_classification

X, y = make_classification(n_samples=1000, n_features=20, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

dt = DecisionTreeClassifier(max_depth=10, random_state=42)
rf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)

dt.fit(X_train, y_train)
rf.fit(X_train, y_train)

print(f"決策樹 - 訓練分數: {dt.score(X_train, y_train):.2%}, 測試分數: {dt.score(X_test, y_test):.2%}")
print(f"隨機森林 - 訓練分數: {rf.score(X_train, y_train):.2%}, 測試分數: {rf.score(X_test, y_test):.2%}")
```

## 參考資源

- https://www.google.com/search?q=decision+tree+Python+scikit-learn+tutorial+2019
- https://www.google.com/search?q=random+forest+ensemble+Python+scikit-learn+2019
- https://www.google.com/search?q=feature+importance+decision+tree+random+forest+Python+2019