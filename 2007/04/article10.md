# 推薦系統的進化：協同過濾到矩陣分解

## 前言

2007 年，Netflix 舉辦的推薦系統大賽（Netflix Prize）成為推薦系統研究的轉捩點。這場競賽推動了矩陣分解技術在推薦系統中的應用。

## 傳統的協同過濾

### 基於記憶體的方法

```python
# 使用者-項目評分矩陣
#         電影 A  電影 B  電影 C  電影 D
# 用戶 1   5      4       ?       3
# 用戶 2   4      ?       5       2
# 用戶 3   ?      3       4       ?

# 相似用戶
def find_similar_users(user_id, ratings, k=5):
    user_ratings = ratings[user_id]
    similarities = []

    for other_id in ratings:
        if other_id != user_id:
            # 計算皮爾森相關係數
            common = [i for i in user_ratings if i in ratings[other_id]]
            if len(common) > 0:
                corr = pearson_correlation(user_ratings, ratings[other_id], common)
                similarities.append((other_id, corr))

    return sorted(similarities, key=lambda x: -x[1])[:k]
```

### 基於項目的協同過濾

```python
# 項目相似度
def item_similarity(ratings, item_id):
    item_ratings = [r[item_id] for r in ratings]
    similarities = []

    for other_item in range(len(ratings[0])):
        if other_item != item_id:
            other_ratings = [r[other_item] for r in ratings]
            # 計算餘弦相似度
            sim = cosine_similarity(item_ratings, other_ratings)
            similarities.append((other_item, sim))

    return similarities
```

## Netflix Prize 競賽

### 競賽背景

2006 年，Netflix 宣布舉辦推薦系統競賽，獎金 100 萬美元：

```
Netflix Prize 目標：
─────────────────────
任務：預測使用者對電影的評分
評估指標：RMSE（均方根誤差）
基準：Netflix 現有系統的 RMSE = 0.9514
目標：RMSE < 0.8572
獎金：100 萬美元
```

### BellKor 團隊的突破

2007-2009 年，BellKor 團隊最終獲勝，他們的方法結合了多項技術：

```python
# 矩陣分解（SVD）
class SVD:
    def __init__(self, n_factors=100):
        self.n_factors = n_factors

    def fit(self, ratings):
        # 使用奇異值分解
        # R ≈ U × Σ × V^T
        # 其中 U 和 V 是用戶和項目隱向量
        pass

    def predict(self, user_id, item_id):
        # 預測評分 = user_vector[user_id] · item_vector[item_id]
        return numpy.dot(self.U[user_id], self.V[item_id])
```

## 矩陣分解技術

### SVD 的優點

```python
# 矩陣分解 vs 傳統 CF
# 矩陣分解可以：
# 1. 處理稀疏資料（電影評分矩陣通常 99% 為空）
# 2. 學習潛在因子（動作片、浪漫片、熱門度等）
# 3. 泛化能力強（可以預測未見過的 user-item 組合）
```

### 加入偏置項

```python
# 帶偏置的矩陣分解
def predict_with_bias(user_id, item_id, U, V, bu, bi, global_mean):
    # 預測 = 全域平均 + 用戶偏置 + 項目偏置 + 交互
    return global_mean + bu[user_id] + bi[item_id] + numpy.dot(U[user_id], V[item_id])
```

## 結語

Netflix Prize 的故事說明：**公開競賽可以推動整個領域的進步**。矩陣分解技術在 2007 年後成為推薦系統的主流，影響了電子商務、社交網路等多個領域。

---

## 延伸閱讀

- [Netflix+Prize+2007](https://www.google.com/search?q=Netflix+Prize+2007)
- [Matrix+factorization+recommendation+systems](https://www.google.com/search?q=Matrix+factorization+recommendation+systems)

---