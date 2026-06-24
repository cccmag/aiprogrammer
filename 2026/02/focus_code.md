# 機器學習入門程式實作

## 前言

本篇文章將完整展示如何使用 Python 與 scikit-learn 實作機器學習入門範例，包含線性迴歸、決策樹、訓練/測試集分割以及模型評估等核心技術。

---

## 原始碼

完整的 Python 實作請參考：[_code/ml_intro.py](_code/ml_intro.py)

```python
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, confusion_matrix, classification_report
from sklearn.datasets import make_regression, make_classification

def demo():
    print("=" * 60)
    print("AI 程式人雜誌 - 機器學習入門範例")
    print("=" * 60)

    # 1. 線性迴歸
    print("\n[1] 線性迴歸")
    X, y = make_regression(n_samples=100, n_features=1, noise=10, random_state=42)
    model = LinearRegression()
    model.fit(X, y)
    y_pred = model.predict(X)
    print(f"係數: {model.coef_[0]:.2f}")
    print(f"截距: {model.intercept_:.2f}")
    print(f"R² 分數: {r2_score(y, y_pred):.3f}")

    # 2. 訓練/測試集分割 + 決策樹迴歸
    print("\n[2] 決策樹迴歸")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    dt = DecisionTreeRegressor(max_depth=3, random_state=42)
    dt.fit(X_train, y_train)
    y_pred_dt = dt.predict(X_test)
    print(f"測試集 MSE: {mean_squared_error(y_test, y_pred_dt):.2f}")
    print(f"測試集 R²: {r2_score(y_test, y_pred_dt):.3f}")

    # 3. 決策樹分類
    print("\n[3] 決策樹分類")
    X_cls, y_cls = make_classification(n_samples=150, n_features=4, n_informative=3, n_redundant=1, random_state=42)
    Xc_train, Xc_test, yc_train, yc_test = train_test_split(X_cls, y_cls, test_size=0.3, random_state=42)
    clf = DecisionTreeClassifier(max_depth=4, random_state=42)
    clf.fit(Xc_train, yc_train)
    yc_pred = clf.predict(Xc_test)
    acc = accuracy_score(yc_test, yc_pred)
    print(f"準確率: {acc:.3f}")
    print(f"混淆矩陣:\n{confusion_matrix(yc_test, yc_pred)}")
    print(f"分類報告:\n{classification_report(yc_test, yc_pred, target_names=['類別0', '類別1'])}")

if __name__ == "__main__":
    demo()
```

---

## 執行結果

```
============================================================
AI 程式人雜誌 - 機器學習入門範例
============================================================

[1] 線性迴歸
  係數: 44.44
  截距: 1.17
  R² 分數: 0.954

[2] 決策樹迴歸 (訓練/測試集分割)
  測試集 MSE: 186.43
  測試集 R²: 0.888

[3] 決策樹分類
  準確率: 0.800
  混淆矩陣:
[[21  0]
 [ 9 15]]
  分類報告:
              precision    recall  f1-score   support

         類別0       0.70      1.00      0.82        21
         類別1       1.00      0.62      0.77        24

    accuracy                           0.80        45
   macro avg       0.85      0.81      0.80        45
weighted avg       0.86      0.80      0.79        45
```

---

## 程式說明

### 1. 線性迴歸

使用 `make_regression` 生成 100 筆人造資料，包含一個特徵和連續的目標值。`LinearRegression` 使用最小平方法擬合直線，`coef_` 是斜率，`intercept_` 是截距。R² 分數越接近 1 表示模型解釋力越強。

### 2. 決策樹迴歸

`train_test_split` 將資料分成 80% 訓練集和 20% 測試集。`DecisionTreeRegressor` 學習資料中的非線性模式，`max_depth=3` 限制樹的深度以防止過擬合。

### 3. 決策樹分類

生成 150 筆分類資料，包含 4 個特徵。`DecisionTreeClassifier` 根據特徵值建立樹狀分類規則。混淆矩陣顯示正確分類與錯誤分類的分布，`classification_report` 提供精確率、召回率和 F1 分數。

---

## 延伸閱讀

- [scikit-learn 官方文檔](https://www.google.com/search?q=scikit-learn+documentation)
- [機器學習入門指南](https://www.google.com/search?q=machine+learning+tutorial+python)
- [scikit-learn 中文教學](https://www.google.com/search?q=scikit-learn+教學+Python)

---

*本篇文章為「AI 程式人雜誌 2026 年 2 月號」機器學習入門系列補充文章。*
