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

    ax = axes[0, 0]
    x = np.linspace(0, 2 * np.pi, 100)
    ax.plot(x, np.sin(x), label="sin(x)")
    ax.plot(x, np.cos(x), label="cos(x)")
    ax.set_title("Trig Functions")
    ax.legend()

    ax = axes[0, 1]
    data = np.random.randn(500)
    ax.hist(data, bins=30, alpha=0.7, color="steelblue")
    ax.set_title("Histogram")

    ax = axes[1, 0]
    categories = ["A", "B", "C", "D"]
    values = [23, 45, 12, 38]
    ax.bar(categories, values, color="coral")
    ax.set_title("Bar Chart")

    ax = axes[1, 1]
    np.random.seed(42)
    scatter_x = np.random.randn(50)
    scatter_y = scatter_x + np.random.randn(50) * 0.3
    ax.scatter(scatter_x, scatter_y, alpha=0.6, color="green")
    ax.set_title("Scatter Plot")

    plt.tight_layout()
    plt.savefig("plot.png", dpi=100)
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
