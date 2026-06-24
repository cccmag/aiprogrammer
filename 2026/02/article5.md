# 決策樹可視化

## 為什麼可視化重要？

決策樹最大的優勢之一就是可解釋性——我們可以直接看到模型學到了什麼規則。可視化讓我們能理解模型的決策過程，發現潛在問題，並向非技術背景的人解釋模型行為。

## 訓練一棵決策樹

使用經典的鳶尾花資料集：

```python
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier

iris = load_iris()
X, y = iris.data, iris.target

clf = DecisionTreeClassifier(max_depth=3, random_state=42)
clf.fit(X, y)
```

`max_depth=3` 限制樹的深度，讓可視化更清晰。

## 文字化輸出

`export_text` 以文字形式輸出樹結構：

```python
from sklearn.tree import export_text

text_representation = export_text(
    clf,
    feature_names=iris.feature_names,
    class_names=iris.target_names,
    max_depth=3
)
print(text_representation)
```

輸出類似：
```
|--- petal length (cm) <= 2.45
|   |--- class: setosa
|--- petal length (cm) > 2.45
|   |--- petal width (cm) <= 1.75
|   |   |--- petal length (cm) <= 4.95
|   |   |   |--- class: versicolor
|   |   |--- petal length (cm) > 4.95
|   |   |   |--- class: virginica
|   |--- petal width (cm) > 1.75
|   |   |--- class: virginica
```

這相當於一組 if-else 規則，非常直觀。

## 圖形化輸出

`plot_tree` 產生圖形化的樹狀圖：

```python
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree

plt.figure(figsize=(12, 8))
plot_tree(
    clf,
    feature_names=iris.feature_names,
    class_names=iris.target_names,
    filled=True,
    rounded=True,
    fontsize=10,
    proportion=True
)
plt.title("決策樹可視化 - 鳶尾花分類")
plt.show()
```

參數說明：
- `filled=True`：根據類別上色
- `rounded=True`：圓角節點
- `proportion=True`：顯示樣本比例

## 匯出 Graphviz 格式

如果需要更精美的可視化，可以匯出 DOT 格式：

```python
from sklearn.tree import export_graphviz

export_graphviz(
    clf,
    out_file="iris_tree.dot",
    feature_names=iris.feature_names,
    class_names=iris.target_names,
    filled=True,
    rounded=True,
    special_characters=True
)
```

然後用 Graphviz 轉換為 PNG 或 PDF：

```bash
dot -Tpng iris_tree.dot -o iris_tree.png
```

## 理解節點資訊

每個節點顯示的資訊：

```
petal length (cm) <= 2.45
├── gini = 0.0           ← 基尼不純度（0 表示純淨）
├── samples = 50         ← 該節點的樣本數
├── value = [50, 0, 0]  ← 各類別樣本數
└── class = setosa       ← 多數類別
```

葉節點只有 `gini`、`samples`、`value`、`class`。

## 特徵重要性

決策樹可以計算每個特徵的重要性：

```python
importances = clf.feature_importances_
for name, imp in zip(iris.feature_names, importances):
    print(f"{name}: {imp:.3f}")

# 繪製長條圖
plt.figure(figsize=(8, 4))
plt.barh(iris.feature_names, importances)
plt.xlabel("特徵重要性")
plt.title("決策樹特徵重要性")
plt.show()
```

特徵重要性基於該特徵在所有節點中減少不純度的總和。

## 可視化隨機森林

隨機森林由多棵決策樹組成，可以選擇其中一棵來可視化：

```python
from sklearn.ensemble import RandomForestClassifier

rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X, y)

# 可視化第一棵樹
plot_tree(rf.estimators_[0], feature_names=iris.feature_names,
          class_names=iris.target_names, filled=True)
```

## 實作建議

- **設定 max_depth**：深度在 3-5 時可讀性最佳
- **特徵數量**：特徵名稱簡短易讀
- **類別名稱**：使用有意義的名稱而非數字
- **僅用於探索**：可視化是理解模型的好工具，但複雜模型的可視化意義不大

決策樹的可視化能力使其成為機器學習入門的最佳模型之一——你能親眼看到模型學到了什麼。

---

## 延伸閱讀

- [scikit-learn 樹模型可視化](https://www.google.com/search?q=sklearn+decision+tree+visualization)
- [Graphviz 安裝教學](https://www.google.com/search?q=graphviz+installation)
- [決策樹可解釋性](https://www.google.com/search?q=decision+tree+interpretability)
