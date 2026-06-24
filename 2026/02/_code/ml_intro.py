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

    print("\n[1] 線性迴歸")
    X, y = make_regression(n_samples=100, n_features=1, noise=10, random_state=42)
    model = LinearRegression()
    model.fit(X, y)
    y_pred = model.predict(X)
    print(f"  係數: {model.coef_[0]:.2f}")
    print(f"  截距: {model.intercept_:.2f}")
    print(f"  R² 分數: {r2_score(y, y_pred):.3f}")

    print("\n[2] 決策樹迴歸 (訓練/測試集分割)")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    dt = DecisionTreeRegressor(max_depth=3, random_state=42)
    dt.fit(X_train, y_train)
    y_pred_dt = dt.predict(X_test)
    print(f"  測試集 MSE: {mean_squared_error(y_test, y_pred_dt):.2f}")
    print(f"  測試集 R²: {r2_score(y_test, y_pred_dt):.3f}")

    print("\n[3] 決策樹分類")
    X_cls, y_cls = make_classification(n_samples=150, n_features=4, n_informative=3, n_redundant=1, random_state=42)
    Xc_train, Xc_test, yc_train, yc_test = train_test_split(X_cls, y_cls, test_size=0.3, random_state=42)
    clf = DecisionTreeClassifier(max_depth=4, random_state=42)
    clf.fit(Xc_train, yc_train)
    yc_pred = clf.predict(Xc_test)
    acc = accuracy_score(yc_test, yc_pred)
    print(f"  準確率: {acc:.3f}")
    print(f"  混淆矩陣:\n{confusion_matrix(yc_test, yc_pred)}")
    print(f"  分類報告:\n{classification_report(yc_test, yc_pred, target_names=['類別0', '類別1'])}")

if __name__ == "__main__":
    demo()
