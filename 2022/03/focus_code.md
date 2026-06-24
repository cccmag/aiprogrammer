# 資料科學完整實作

## 前言

本期焦點程式碼以 Python 實作了一個完整的資料科學範例，涵蓋 NumPy 陣列運算、Pandas 資料操作、scikit-learn 機器學習管線、以及 Matplotlib 與 Seaborn 視覺化。程式碼位於 `_code/data_science.py`。

## 原始碼

完整的 Python 實作請參考：[_code/data_science.py](_code/data_science.py)

```python
#!/usr/bin/env python3
"""Python Data Science Demo: NumPy, Pandas, scikit-learn, Matplotlib"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.metrics import classification_report
import warnings
warnings.filterwarnings("ignore")


def demo():
    print("=" * 60)
    print("Python Data Science Demo")
    print("=" * 60)

    # --- NumPy ---
    print("\n1. NumPy Operations")
    a = np.array([[1, 2], [3, 4]])
    b = np.array([[5, 6], [7, 8]])
    print(f"a =\n{a}")
    print(f"b =\n{b}")
    print(f"a + b =\n{a + b}")
    print(f"a @ b =\n{a @ b}")
    print(f"Broadcasting: {np.array([1, 2, 3]) + np.array([[0], [10], [20]])}")

    # --- Pandas ---
    print("\n2. Pandas DataFrame Operations")
    df = pd.DataFrame({
        "name": ["Alice", "Bob", "Charlie", "Diana", "Eve"],
        "age": [25, 32, 37, 28, 41],
        "salary": [50000, 62000, 78000, 54000, 92000],
        "dept": ["IT", "HR", "IT", "HR", "IT"]
    })
    print(f"DataFrame:\n{df}")
    print(f"\nMean age by dept:\n{df.groupby('dept')['age'].mean()}")
    print(f"\nHigh earners:\n{df[df['salary'] > 60000]}")

    # --- scikit-learn Pipeline ---
    print("\n3. Scikit-learn Pipeline with Grid Search")
    X, y = make_classification(n_samples=200, n_features=5, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("svm", SVC()),
    ])
    param_grid = {"svm__C": [0.1, 1, 10], "svm__gamma": [0.01, 0.1]}
    grid = GridSearchCV(pipeline, param_grid, cv=5)
    grid.fit(X_train, y_train)
    print(f"Best params: {grid.best_params_}")
    print(f"Best CV score: {grid.best_score_:.3f}")

    y_pred = grid.predict(X_test)
    print(f"Test score: {grid.score(X_test, y_test):.3f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, zero_division=0))

    # --- Matplotlib ---
    print("\n4. Matplotlib Visualization")
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    axes[0, 0].plot(x := np.linspace(0, 2 * np.pi, 100), np.sin(x))
    axes[0, 0].plot(x, np.cos(x))
    axes[0, 1].hist(np.random.randn(500), bins=30)
    axes[1, 0].bar(["A", "B", "C", "D"], [23, 45, 12, 38])
    axes[1, 1].scatter(*np.random.randn(2, 50))
    plt.tight_layout()
    plt.savefig("plot.png")
    print("Plot saved to plot.png")

    # --- Seaborn ---
    print("\n5. Seaborn Statistical Plot")
    iris = sns.load_dataset("iris")
    sns_plot = sns.pairplot(iris, hue="species")
    sns_plot.savefig("pairplot.png")
    print("Pairplot saved to pairplot.png")

    print("\n" + "=" * 60)
    print("Demo completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    demo()
```

## 執行結果

```
$ python3 data_science.py
============================================================
Python Data Science Demo
============================================================

1. NumPy Operations
a =
[[1 2]
 [3 4]]
b =
[[5 6]
 [7 8]]
a + b =
[[ 6  8]
 [10 12]]
a @ b =
[[19 22]
 [43 50]]
...

3. Scikit-learn Pipeline with Grid Search
Best params: {'svm__C': 0.1, 'svm__gamma': 0.1}
Best CV score: 0.863
Test score: 0.825

Classification Report:
              precision    recall  f1-score   support
           0       0.92      0.67      0.77        18
           1       0.78      0.95      0.86        22
    accuracy                           0.82        40
   macro avg       0.85      0.81      0.82        40

4. Matplotlib Visualization
Plot saved to plot.png

5. Seaborn Statistical Plot
Pairplot saved to pairplot.png

============================================================
Demo completed successfully!
============================================================
```

## 重點解析

### NumPy 陣列運算

- 展示基本的陣列加法和矩陣乘法
- 展示廣播機制（不同形狀陣列的運算）

### Pandas DataFrame 操作

- 從字典建立 DataFrame
- 使用 groupby 進行分組聚合
- 使用布林索引進行資料篩選

### scikit-learn 管線

- 使用 Pipeline 串接標準化和 SVC
- 使用 GridSearchCV 進行超參數搜尋
- 輸出分類報告

### Matplotlib 與 Seaborn

- 使用 Matplotlib 繪製多子圖
- 使用 Seaborn 繪製 Iris 資料集配對圖

## 延伸閱讀

- [NumPy 快速入門](https://www.google.com/search?q=NumPy+quickstart)
- [Pandas 教學](https://www.google.com/search?q=Pandas+tutorial)
- [scikit-learn 管線](https://www.google.com/search?q=scikit-learn+pipeline)
- [Matplotlib 教學](https://www.google.com/search?q=Matplotlib+tutorial)

---

*本篇文章為「AI 程式人雜誌 2022 年 3 月號」主題補充文章。*
