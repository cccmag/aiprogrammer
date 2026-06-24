import numpy as np
from sklearn.datasets import load_iris, make_blobs
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import classification_report, silhouette_score


def demo():
    print("=" * 60)
    print("機器學習基礎展示")
    print("=" * 60)

    print("\n[1] 監督式學習 - 分類")
    demonstrate_classification()

    print("\n[2] 非監督式學習 - K-means 聚類")
    demonstrate_clustering()

    print("\n[3] 資料预处理 - StandardScaler")
    demonstrate_preprocessing()

    print("\n[4] Pipeline 展示")
    demonstrate_pipeline()

    print("\n" + "=" * 60)
    print("展示完成")
    print("=" * 60)


def demonstrate_classification():
    iris = load_iris()
    X = iris.data
    y = iris.target

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print(f"資料集大小: {len(iris.data)}")
    print(f"訓練集: {len(X_train)}, 測試集: {len(X_test)}")

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    clf = LogisticRegression(max_iter=200, random_state=42)
    clf.fit(X_train_scaled, y_train)

    y_pred = clf.predict(X_test_scaled)
    accuracy = clf.score(X_test_scaled, y_test)

    print(f"\n分類報告:")
    print(classification_report(y_test, y_pred, target_names=iris.target_names))
    print(f"測試集準確率: {accuracy:.2%}")


def demonstrate_clustering():
    X, _ = make_blobs(n_samples=300, centers=4, cluster_std=0.6, random_state=42)

    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X)

    silhouette = silhouette_score(X, labels)

    print(f"集群數量: {len(np.unique(labels))}")
    print(f"集群中心:\n{kmeans.cluster_centers_[:2]}")
    print(f"輪廓係數: {silhouette:.3f}")


def demonstrate_preprocessing():
    iris = load_iris()
    X = iris.data

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    print(f"標準化前均值: {X.mean(axis=0).round(2)}")
    print(f"標準化前標準差: {X.std(axis=0).round(2)}")
    print(f"標準化後均值: {X_scaled.mean(axis=0).round(6)}")
    print(f"標準化後標準差: {X_scaled.std(axis=0).round(2)}")


def demonstrate_pipeline():
    iris = load_iris()
    X = iris.data
    y = iris.target

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('clf', LogisticRegression(max_iter=200, random_state=42))
    ])

    pipeline.fit(X_train, y_train)

    train_score = pipeline.score(X_train, y_train)
    test_score = pipeline.score(X_test, y_test)

    cv_scores = cross_val_score(pipeline, X, y, cv=5)

    print(f"Pipeline 訓練集分數: {train_score:.2%}")
    print(f"Pipeline 測試集分數: {test_score:.2%}")
    print(f"交叉驗證分數: {cv_scores.mean():.2%} (+/- {cv_scores.std()*2:.2%})")


if __name__ == "__main__":
    demo()