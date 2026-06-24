# 7. 實戰：分類器實作

## 專案概述

本章整合所学知識，從頭建立一個完整的分類器實作。我們使用鳶尾花（Iris）資料集，比較多種分類器的效能。

## 完整實作流程

```python
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import numpy as np

iris = load_iris()
print(f"資料集形狀: {iris.data.shape}")
print(f"類別: {iris.target_names}")

X = iris.data
y = iris.target

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
```

## 定義多個分類器

```python
classifiers = {
    'Logistic Regression': Pipeline([
        ('scaler', StandardScaler()),
        ('clf', LogisticRegression(max_iter=200, random_state=42))
    ]),
    'Decision Tree': DecisionTreeClassifier(max_depth=5, random_state=42),
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
    'SVM (RBF)': Pipeline([
        ('scaler', StandardScaler()),
        ('clf', SVC(kernel='rbf', probability=True, random_state=42))
    ]),
    'KNN': Pipeline([
        ('scaler', StandardScaler()),
        ('clf', KNeighborsClassifier(n_neighbors=5))
    ])
}
```

## 比較分類器效能

```python
results = {}
for name, clf in classifiers.items():
    clf.fit(X_train, y_train)
    train_score = clf.score(X_train, y_train)
    test_score = clf.score(X_test, y_test)
    cv_scores = cross_val_score(clf, X, y, cv=5)

    results[name] = {
        'train': train_score,
        'test': test_score,
        'cv_mean': cv_scores.mean(),
        'cv_std': cv_scores.std()
    }

    print(f"\n{name}:")
    print(f"  訓練集準確率: {train_score:.2%}")
    print(f"  測試集準確率: {test_score:.2%}")
    print(f"  交叉驗證: {cv_scores.mean():.2%} (+/- {cv_scores.std()*2:.2%})")
```

## 視覺化比較

```python
names = list(results.keys())
test_scores = [results[n]['test'] for n in names]

plt.figure(figsize=(10, 6))
bars = plt.barh(names, test_scores, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'])
plt.xlabel('Accuracy')
plt.title('Classifier Comparison - Test Set Performance')
plt.xlim(0.8, 1.0)

for bar, score in zip(bars, test_scores):
    plt.text(score + 0.005, bar.get_y() + bar.get_height()/2,
             f'{score:.2%}', va='center')

plt.tight_layout()
plt.show()
```

## 詳細評估最佳模型

```python
best_clf_name = max(results, key=lambda k: results[k]['test'])
best_clf = classifiers[best_clf_name]

y_pred = best_clf.predict(X_test)

print(f"\n最佳分類器: {best_clf_name}")
print(f"\n分類報告:")
print(classification_report(y_test, y_pred, target_names=iris.target_names))

print(f"\n混淆矩陣:")
cm = confusion_matrix(y_test, y_pred)
print(cm)

plt.figure(figsize=(8, 6))
plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
plt.title(f'Confusion Matrix - {best_clf_name}')
plt.colorbar()
tick_marks = np.arange(len(iris.target_names))
plt.xticks(tick_marks, iris.target_names)
plt.yticks(tick_marks, iris.target_names)

for i in range(len(cm)):
    for j in range(len(cm)):
        plt.text(j, i, format(cm[i, j], 'd'),
                ha="center", va="center",
                color="white" if cm[i, j] > cm.max()/2 else "black")

plt.ylabel('True Label')
plt.xlabel('Predicted Label')
plt.tight_layout()
plt.show()
```

## 特徵重要性分析

```python
rf_clf = classifiers['Random Forest']
rf_clf.fit(X_train, y_train)
feature_importance = rf_clf.feature_importances_

plt.figure(figsize=(10, 6))
plt.barh(iris.feature_names, feature_importance)
plt.xlabel('Importance')
plt.title('Random Forest - Feature Importance')
plt.tight_layout()
plt.show()

print("\n特徵重要性:")
for name, importance in zip(iris.feature_names, feature_importance):
    print(f"  {name}: {importance:.3f}")
```

## 模型預測新樣本

```python
new_samples = np.array([
    [5.1, 3.5, 1.4, 0.2],
    [6.2, 3.4, 5.4, 2.3],
    [7.0, 3.2, 4.7, 1.4]
])

predictions = best_clf.predict(new_samples)
probabilities = best_clf.predict_proba(new_samples)

print("\n新樣本預測:")
for i, (sample, pred, prob) in enumerate(zip(new_samples, predictions, probabilities)):
    print(f"  樣本 {i+1}: 預測為 {iris.target_names[pred]}, 機率 {prob.max():.2%}")
```

## 結論

本章展示了完整的機器學習工作流程：從資料載入、预处理、模型訓練到評估與預測。不同分類器有各自的優勢，選擇時需根據準確率、模型複雜度與可解釋性綜合考量。

## 參考資源

- https://www.google.com/search?q=iris+dataset+classification+Python+scikit-learn+2019
- https://www.google.com/search?q=classifier+comparison+random+forest+svm+knn+Python+2019
- https://www.google.com/search?q=machine+learning+project+workflow+Python+tutorial+2019