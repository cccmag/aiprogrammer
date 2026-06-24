# 貝氏分類器

## 前言

貝氏分類器基於貝氏斯定理，是一個簡單但強大的分類演算法。特別是樸素貝氏分類器，雖然假設特徵之間獨立，但在大多數實際應用中表現良好。

## 貝氏斯定理

### 基本公式

```python
# 貝氏斯定理

bayes_theorem = {
    "公式": "P(A|B) = P(B|A) × P(A) / P(B)",
    "P(A|B)": "後驗機率（Posterior）",
    "P(B|A)": "似然（Likelihood）",
    "P(A)": "先驗機率（Prior）",
    "P(B)": "證據（Evidence）"
}

# 在分類問題中：
# P(y|X) = P(X|y) × P(y) / P(X)

# 其中：
# y 是類別
# X 是特徵向量
```

### 機率詮釋

```
貝氏斯詮釋：

先驗 P(y) ───────→ 我們對類別的初始信念
                    │
                    ▼
訓練資料 ───────→ 更新信念 ───→ 後驗 P(y|X)
                   (似然)
```

## 樸素貝氏分類器

### 「樸素」的假設

```python
# 假設特徵之間條件獨立

naive_assumption = {
    "定義": "在類別已知的條件下，所有特徵之間相互獨立",
    "數學": "P(X1, X2, ..., Xn | y) = P(X1|y) × P(X2|y) × ... × P(Xn|y)",
    "影響": "簡化計算，代價是可能不符合現實"
}
```

### 為何稱為「樸素」

```python
# 現實中特徵往往不完全獨立
# 但這個假設在很多情況下仍然有效

why_naive = {
    "1": "分類任務中，我們只需要知道哪個類別機率更高，不需要準確的機率值",
    "2": "即使有偏差，排序可能還是正確的",
    "3": "類別之間的依賴可能相互抵消"
}
```

## 演算法

### 分類過程

```python
def naive_bayes_classify(X, y, x_new):
    """
    對新資料點 x_new 分類
    X: 特徵矩陣
    y: 標籤向量
    x_new: 新資料點
    """
    classes = set(y)
    best_class = None
    best_prob = -1

    for c in classes:
        # 計算 P(y=c) - 先驗
        prior = sum(1 for label in y if label == c) / len(y)

        # 計算 P(x_new|y=c) - 似然
        # 假設特徵獨立，乘積
        likelihood = 1
        for i, feature_value in enumerate(x_new):
            prob = calculate_feature_prob(X, y, i, feature_value, c)
            likelihood *= prob

        # 計算後驗（未標準化）
        posterior = prior * likelihood

        if posterior > best_prob:
            best_prob = posterior
            best_class = c

    return best_class
```

## 高斯樸素貝氏

### 假設特徵常態分佈

```python
from math import sqrt, exp, pi

def gaussian_probability(x, mean, std):
    """計算 x 在 N(mean, std) 中的機率密度"""
    exponent = exp(-((x - mean) ** 2) / (2 * std ** 2))
    return (1 / (sqrt(2 * pi) * std)) * exponent


class GaussianNB:
    def fit(self, X, y):
        self.classes = set(y)
        self.class_stats = {}

        for c in self.classes:
            X_c = [x for x, label in zip(X, y) if label == c]
            self.class_stats[c] = {
                'mean': [sum(feature) / len(feature) for feature in zip(*X_c)],
                'std': [calculate_std(feature) for feature in zip(*X_c)]
            }

    def predict(self, X):
        predictions = []
        for x in X:
            probs = {}
            for c, stats in self.class_stats.items():
                prob = 1
                for i, (mean, std) in enumerate(zip(stats['mean'], stats['std'])):
                    prob *= gaussian_probability(x[i], mean, std)
                probs[c] = prob * (sum(1 for label in y if label == c) / len(y))
            predictions.append(max(probs, key=probs.get))
        return predictions
```

## 多項式樸素貝氏

### 適合文字分類

```python
class MultinomialNB:
    def fit(self, X, y):
        self.classes = set(y)
        self.class_counts = {}
        self.feature_counts = {}

        for c in self.classes:
            X_c = [x for x, label in zip(X, y) if label == c]
            self.class_counts[c] = len(X_c)

            # 計算每個特徵在類別 c 中的總和
            feature_sums = [0] * len(X[0])
            for x in X_c:
                for i, val in enumerate(x):
                    feature_sums[i] += val
            self.feature_counts[c] = feature_sums

    def predict(self, X):
        predictions = []
        for x in X:
            probs = {}
            for c in self.classes:
                prob = self.class_counts[c] / sum(self.class_counts.values())
                for i, val in enumerate(x):
                    prob *= (self.feature_counts[c][i] + 1) / (sum(self.feature_counts[c]) + len(x))
            probs[c] = prob
            predictions.append(max(probs, key=probs.get))
        return predictions
```

## 拉普拉斯平滑

### 處理零機率

```python
# 問題：如果某個特徵值在某個類別中從未出現，機率為 0

laplacian_smoothing = {
    "問題": "P(feature|class) = 0 導致整體機率為 0",
    "解決": "拉普拉斯平滑（加一平滑）",
    "公式": "P(x|c) = (count(x,c) + 1) / (count(c) + |V|)",
    "V": "所有可能的特徵值數量"
}
```

## 文字分類應用

### 垃圾郵件偵測

```python
# 將文字轉換為詞頻向量
from collections import Counter

def text_to_vector(text, vocabulary):
    """將文字轉換為詞頻向量"""
    words = text.lower().split()
    word_counts = Counter(words)
    vector = [word_counts.get(word, 0) for word in vocabulary]
    return vector

# 訓練
spam_emails = [...]  # 垃圾郵件列表
ham_emails = [...]    # 正常郵件列表

# 計算每個詞在垃圾郵件和正常郵件中的頻率
# ...

# 分類新郵件
def classify_email(email):
    vector = text_to_vector(email, vocabulary)
    prob_spam = calculate_spam_probability(vector)
    return "Spam" if prob_spam > 0.5 else "Not Spam"
```

## 優點和缺點

### 優點

```python
naive_bayes_advantages = {
    "簡單快速": "幾乎不需要訓練時間",
    "可處理多類別": "自然擴展",
    "對缺失資料": "不敏感",
    "對特徵尺度": "不敏感"
}
```

### 缺點

```python
naive_bayes_disadvantages = {
    "獨立假設": "很多情況不符合現實",
    "機率估計": "機率估計可能不準確",
    "零機率": "需要平滑處理"
}
```

## Scikit-learn 使用

### 高斯樸素貝氏

```python
from sklearn.naive_bayes import GaussianNB

gnb = GaussianNB()
gnb.fit(X_train, y_train)
predictions = gnb.predict(X_test)
```

### 多項式樸素貝氏

```python
from sklearn.naive_bayes import MultinomialNB

mnb = MultinomialNB()
mnb.fit(X_train, y_train)
predictions = mnb.predict(X_test)
```

## 應用場景

```python
applications = {
    "文字分類": "垃圾郵件偵測、文件分類、情感分析",
    "即時分類": "需要快速判斷的場景",
    "基線模型": "作為更復雜模型的基準",
    "多類別分類": "類別數量很多時"
}
```

---

**延伸閱讀**

- [Naive+Bayes+classifier+tutorial](https://www.google.com/search?q=Naive+Bayes+classifier+tutorial)
- [Bayes+theorem+machine+learning](https://www.google.com/search?q=Bayes+theorem+machine+learning)
- [Spam+filtering+Naive+Bayes](https://www.google.com/search?q=Spam+filtering+Naive+Bayes)