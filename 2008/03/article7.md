# 決策樹與隨機森林

## 前言

決策樹是機器學習中最直觀的演算法之一，隨機森林則是透過集成多棵決策樹來提升預測準確率。

## 決策樹基礎

### 什麼是決策樹？

```python
# 決策樹是一棵樹狀結構

decision_tree_concept = {
    "節點類型": [
        "根節點：整個資料集",
        "內部節點：特徵測試",
        "葉節點：預測結果"
    ],
    "分支": "測試結果的輸出路徑",
    "深度": "從根到葉的最長路徑長度"
}
```

### 決策樹範例

```
                    天氣？
                 /    |    \
              晴      陰     雨
             /        |      \
         外出      外出      室內
         /          \        |
      ✓          帶傘       ✗
```

## 資訊增益

### 選擇分割特徵

```python
# 如何決定在哪個特徵分割？

information_gain = {
    "概念": "分割前後資訊熵的減少量",
    "熵 (Entropy)": "衡量資料的不純度",
    "目標": "選擇讓熵減少最多的特徵"
}

# 計算
# Entropy(S) = -Σ p_i * log2(p_i)
# IG(S, feature) = Entropy(S) - Σ (|S_v|/|S|) * Entropy(S_v)
```

### 熵的計算

```python
import math

def entropy(labels):
    """計算資料集的熵"""
    n = len(labels)
    if n == 0:
        return 0

    counts = {}
    for label in labels:
        counts[label] = counts.get(label, 0) + 1

    ent = 0
    for count in counts.values():
        p = count / n
        if p > 0:
            ent -= p * math.log2(p)

    return ent

# 範例
labels = ['Yes', 'Yes', 'No', 'No', 'No']
print(entropy(labels))  # 0.97095...
```

## ID3 演算法

### 貪心建構

```python
id3_algorithm = {
    "輸入": "訓練資料和特徵集合",
    "過程": "貪心選擇資訊增益最大的特徵",
    "遞迴": "對每個分割递归建構子樹",
    "終止": "所有樣本為同一類，或無特徵可分"
}
```

### 決策樹建構

```python
def build_tree(data, features):
    # 取出所有標籤
    labels = [row[-1] for row in data]

    # 終止條件：全部為同一類
    if len(set(labels)) == 1:
        return labels[0]

    # 終止條件：無特徵可分割
    if len(features) == 0:
        return majority_label(labels)

    # 選擇最佳特徵
    best_feature = choose_best_feature(data, features)

    # 建立節點
    tree = {best_feature: {}}

    # 對每個特徵值递归建構子樹
    for value in get_unique_values(data, best_feature):
        subset = [row for row in data if row[best_feature] == value]
        subtree = build_tree(subset, features - {best_feature})
        tree[best_feature][value] = subtree

    return tree
```

## 決策樹的修剪

### 前修剪（Pre-pruning）

```python
pre_pruning = {
    "方法": "在建構時設定條件提前停止",
    "條件": [
        "最大深度",
        "最小樣本數",
        "最小增益閾值"
    ],
    "優點": "避免過擬合",
    "缺點": "可能提前停止，不够理想"
}
```

### 後修剪（Post-pruning）

```python
post_pruning = {
    "方法": "先完整建構，再刪除不重要的節點",
    "技術": "代價複雜度修剪",
    "公式": "最小化 (錯誤率 + α × 葉節點數)"
}
```

## 隨機森林

### 集成學習的概念

```python
ensemble_learning = {
    "核心思想": "三個臭皮匠，勝過諸葛亮",
    "方法": "訓練多個模型，結合它們的預測",
    "優點": "減少過擬合，提高穩定性"
}
```

### 隨機森林的建構

```python
random_forest = {
    "輸入": "訓練資料",
    "步驟": [
        "1. 從原始資料有放回抽樣（Bootstrap）",
        "2. 對每個樣本隨機選擇部分特徵",
        "3. 建構決策樹",
        "4. 重複 1-3 多次",
        "5. 多数投票決定最終預測"
    ],
    "特點": "兩層隨機性（樣本和特徵）"
}
```

### 實現

```python
def random_forest_train(X_train, y_train, n_trees=100):
    trees = []

    for _ in range(n_trees):
        # Bootstrap 抽樣
        indices = [random.randint(0, len(X_train) - 1)
                   for _ in range(len(X_train))]
        X_bootstrap = X_train[indices]
        y_bootstrap = y_train[indices]

        # 訓練決策樹（使用隨機特徵子集）
        tree = build_tree(X_bootstrap, y_bootstrap,
                         max_features='sqrt')
        trees.append(tree)

    return trees

def random_forest_predict(X, trees):
    # 多數投票
    predictions = [tree_predict(tree, X) for tree in trees]
    return majority_vote(predictions)
```

## 優點和缺點

### 決策樹優點

```python
decision_tree_advantages = {
    "可解釋性": "可以視覺化，直觀理解",
    "不需要標準化": "對特徵尺度不敏感",
    "處理類別特徵": "自然支援類別資料",
    "快速": "訓練和預測都快"
}
```

### 決策樹缺點

```python
decision_tree_disadvantages = {
    "過擬合": "容易對訓練資料擬合過度",
    "不穩定": "小的資料變化可能导致大树的变化",
    "偏向多值特徵": "傾向選擇有較多唯一值的特徵"
}
```

### 隨機森林優點

```python
random_forest_advantages = {
    "準確率": "通常比單一棵樹高",
    "抗過擬合": "集成減少變異數",
    "處理缺失值": "可以處理缺失資料",
    "並行化": "樹之間相互獨立"
}
```

## Scikit-learn 使用

### DecisionTreeClassifier

```python
from sklearn.tree import DecisionTreeClassifier

tree = DecisionTreeClassifier(
    max_depth=5,
    min_samples_split=10,
    min_samples_leaf=5
)
tree.fit(X_train, y_train)
predictions = tree.predict(X_test)
```

### RandomForestClassifier

```python
from sklearn.ensemble import RandomForestClassifier

forest = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    min_samples_split=5,
    n_jobs=-1  # 使用所有 CPU
)
forest.fit(X_train, y_train)
predictions = forest.predict(X_test)
```

## 應用場景

```python
applications = {
    "分類任務": "垃圾郵件偵測、風險評估",
    "迴歸任務": "房價預測、數值預測",
    "特徵選擇": "識別重要特徵",
    "異常偵測": "金融欺詐偵測"
}
```

---

**延伸閱讀**

- [Decision+tree+algorithm](https://www.google.com/search?q=decision+tree+algorithm)
- [Random+forest+python](https://www.google.com/search?q=random+forest+python)
- [Information+gain+decision+tree](https://www.google.com/search?q=information+gain+decision+tree)