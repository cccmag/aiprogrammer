# 1. 機器學習概述

## 什麼是機器學習？

機器學習是人工智慧的一個分支，專注於讓電腦系統從資料中自動學習並改進，而無需明確程式設計。Arthur Samuel 在 1959 年提出這個概念，現在已成為現代科技的基礎。

## 機器學習的三大類型

### 監督式學習（Supervised Learning）

監督式學習使用已標記的訓練資料。每筆資料包含輸入特徵與正確輸出，系統學習輸入與輸出之間的對應關係。

```python
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.2
)

clf = LogisticRegression()
clf.fit(X_train, y_train)
accuracy = clf.score(X_test, y_test)
print(f"準確率: {accuracy:.2%}")
```

### 非監督式學習（Unsupervised Learning）

非監督式學習使用未標記的資料，目標是發現資料的內在結構。

```python
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs

X, _ = make_blobs(n_samples=300, centers=4, random_state=42)

kmeans = KMeans(n_clusters=4)
labels = kmeans.fit_predict(X)
print(f"聚類結果: {labels[:10]}")
```

### 增強式學習（Reinforcement Learning）

增強式學習透過與環境互動，根據獎勵信號學習最佳策略。

## 機器學習工作流程

1. **資料收集**：取得相關資料集
2. **資料预处理**：清理、轉換、標準化
3. **特徵工程**：選擇與提取有意義的特徵
4. **模型訓練**：選擇演算法並訓練模型
5. **模型評估**：使用測試資料評估效能
6. **模型優化**：調整超參數改善效能
7. **部署預測**：將模型用於新資料預測

## 機器學習 vs 傳統程式設計

傳統程式設計由人定義規則，而機器學習由資料自動學習規則：

```
傳統程式設計：規則 + 資料 → 答案
機器學習：答案 + 資料 → 規則
```

## 常見術語

- **特徵（Feature）**：輸入變數
- **標籤（Label）**：輸出目標
- **訓練集（Training Set）**：用於訓練模型的資料
- **測試集（Test Set）**：用於評估模型的資料
- **模型（Model）**：學習到的規律表示

## 參考資源

- https://www.google.com/search?q=machine+learning+introduction+supervised+unsupervised+reinforcement+2019
- https://www.google.com/search?q=machine+learning+workflow+data+preprocessing+feature+engineering+2019
- https://www.google.com/search?q=machine+learning+vs+traditional+programming+difference+2019