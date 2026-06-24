# 機器學習開源框架：scikit-learn 誕生

## 前言

scikit-learn 是 Python 生態系統中最重要的機器學習庫。它的前身是 scikits.learn，於 2007 年開始開發，2009 年已經成為活跃的开源專案。

## scikit-learn 的設計

### 統一介面

```python
# scikit-learn 的統一 API

from sklearn import svm, datasets
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# 載入資料
iris = datasets.load_iris()
X, y = iris.data, iris.target

# 分割資料
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3
)

# 訓練模型
clf = svm.SVC()
clf.fit(X_train, y_train)

# 預測
y_pred = clf.predict(X_test)

# 評估
accuracy = accuracy_score(y_test, y_pred)
print(f"準確率: {accuracy}")
```

### 經典機器學習演算法

```python
# 監督式學習
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

# 非監督式學習
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

# 降維
from sklearn.manifold import TSNE
```

## 2009 年的功能

### 主要模組

```markdown
scikit-learn 模組（2009年）：

1. 監督式學習
   - 線性模型
   - 決策樹
   - SVM
   - 集成方法

2. 非監督式學習
   - 聚類（K-means, DBSCAN）
   - 降維（PCA, ICA）

3. 資料预处理
   - 標準化
   - 缺失值處理

4. 模型選擇
   - 交叉驗證
   - 網格搜索
```

## 結語

scikit-learn 的出現，讓 Python 成為機器學習的主流語言之一。

## 延伸閱讀

- [scikit-learn 官方網站](https://www.google.com/search?q=scikit-learn+official+website)
- [scikit-learn 教程](https://www.google.com/search?q=scikit-learn+tutorial+2009)
- [Python 機器學習](https://www.google.com/search?q=Python+machine+learning+2009)

---

*本篇文章為「AI 程式人雜誌 2009 年 8 月號」文章系列之一。*