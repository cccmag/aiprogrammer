#!/usr/bin/env python3
"""機器學習基礎範例 - 使用 scikit-learn"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris, make_blobs, make_moons
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import (
    accuracy_score, classification_report,
    confusion_matrix, silhouette_score
)

# =====================
# 載入資料集
# =====================

def load_iris_data():
    """載入鳶尾花資料集"""
    iris = load_iris()
    X, y = iris.data, iris.target
    feature_names = iris.feature_names
    target_names = iris.target_names
    return X, y, feature_names, target_names

# =====================
# 資料预处理
# =====================

def preprocess_data(X_train, X_test):
    """標準化資料"""
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    return X_train_scaled, X_test_scaled

# =====================
# 監督式學習：分類
# =====================

def train_classifiers(X_train, y_train, X_test, y_test):
    """訓練多個分類器並比較"""
    classifiers = {
        'Logistic Regression': LogisticRegression(max_iter=200),
        'Decision Tree': DecisionTreeClassifier(max_depth=5),
        'Random Forest': RandomForestClassifier(n_estimators=50)
    }

    results = {}
    for name, clf in classifiers.items():
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)

        cv_scores = cross_val_score(clf, X_train, y_train, cv=5)

        results[name] = {
            'accuracy': accuracy,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std()
        }

        print(f'{name}:')
        print(f'  測試集準確率: {accuracy:.4f}')
        print(f'  交叉驗證分數: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}')
        print()

    return results

# =====================
# 非監督式學習：分群
# =====================

def kmeans_clustering(X, n_clusters=3):
    """K-means 分群"""
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(X)
    centers = kmeans.cluster_centers_

    score = silhouette_score(X, labels)
    print(f'K-means 分群輪廓係數: {score:.4f}')

    return labels, centers

# =====================
# 降維
# =====================

def pca_reduction(X, n_components=2):
    """PCA 降維"""
    pca = PCA(n_components=n_components)
    X_reduced = pca.fit_transform(X)

    print(f'PCA 解釋變異量比例: {pca.explained_variance_ratio_}')
    print(f'總解釋變異量: {sum(pca.explained_variance_ratio_):.4f}')

    return X_reduced

# =====================
# 主程式
# =====================

def demo():
    print('=' * 50)
    print('機器學習基礎範例')
    print('=' * 50)
    print()

    print('1. 載入鳶尾花資料集')
    X, y, feature_names, target_names = load_iris_data()
    print(f'   資料形狀: {X.shape}')
    print(f'   特徵: {feature_names}')
    print(f'   類別: {list(target_names)}')
    print()

    print('2. 分割資料集')
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f'   訓練集: {X_train.shape[0]} 樣本')
    print(f'   測試集: {X_test.shape[0]} 樣本')
    print()

    print('3. 資料預處理（標準化）')
    X_train_scaled, X_test_scaled = preprocess_data(X_train, X_test)
    print('   完成！')
    print()

    print('4. 監督式學習：分類器訓練')
    results = train_classifiers(X_train_scaled, y_train,
                                X_test_scaled, y_test)
    print()

    print('5. 非監督式學習：K-means 分群')
    labels, centers = kmeans_clustering(X_scaled)
    print()

    print('6. 降維：PCA')
    X_reduced = pca_reduction(X_scaled)
    print()

    print('=' * 50)
    print('範例完成！')
    print('=' * 50)

if __name__ == '__main__':
    demo()