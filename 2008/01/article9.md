# 資料探勘技術

## 前言

資料探勘（Data Mining）是從大量資料中發現隱藏模式和新知識的過程。2008 年是大數據時代的開端，資料探勘技術變得越來越重要。

## 資料探勘的定義

### 什麼是資料探勘？

```python
# 資料探勘的定義
data_mining_definition = {
    "本質": "從大型資料庫中提取隱藏的、先前未知的、但有效的資訊",
    "目的": "支援商業決策、預測未來趨勢",
    "方法": "統計分析、機器學習、資料庫技術",
    "結果": "模式、規則、知識"
}
```

### KDD 流程

```
┌────────────────────────────────────────────┐
│           知識發現流程 (KDD)                │
├────────────────────────────────────────────┤
│                                            │
│  1. 資料收集 ──→ 2. 資料清洗 ──→ 3. 轉換   │
│                                            │
│  4. 資料探勘 ──→ 5. 模式評估 ──→ 6. 知識表達│
│                                            │
└────────────────────────────────────────────┘
```

## 主要技術

### 分類（Classification）

```python
# 分類是什麼？
# 根據已知類別的資料，預測新資料的類別

# 常見分類演算法
classification_algorithms = {
    "決策樹": "易於解釋，視覺化直觀",
    "類神經網路": "準確度高，適用複雜模式",
    "支援向量機": "處理高維度資料能力強",
    "樸素貝葉斯": "快速，適用於即時分類",
    "K-近鄰": "簡單，無需訓練階段"
}

# 應用範例：垃圾郵件分類
email_classification = {
    "輸入": "電子郵件內容",
    "輸出": "垃圾郵件 / 正常郵件",
    "訓練資料": "已標記的郵件樣本"
}
```

### 集群（Clustering）

```python
# 集群是什麼？
# 將相似的資料分組，事前不知道類別

# K-Means 集群演算法
def kmeans(data, k, max_iterations=100):
    # 1. 隨機選擇 k 個初始中心點
    centroids = random_select_centroids(data, k)

    for _ in range(max_iterations):
        # 2. 計算每個資料點到中心的距離
        clusters = assign_to_clusters(data, centroids)

        # 3. 重新計算中心點
        new_centroids = compute_means(data, clusters)

        # 4. 檢查收斂
        if converged(centroids, new_centroids):
            break

        centroids = new_centroids

    return clusters, centroids
```

### 關聯規則（Association Rules）

```python
# 關聯規則：發現項目之間的關聯性
# 經典案例：購物籃分析

# Apriori 演算法概念
shopping_analysis = {
    "交易資料": [
        ["麵包", "牛奶", "雞蛋"],
        ["麵包", "奶油"],
        ["牛奶", "雞蛋", "優格"],
        ["麵包", "牛奶", "雞蛋"]
    ],

    "發現的規則": [
        {"規則": "麵包 → 牛奶", "支持度": 0.75, "信心度": 1.0},
        {"規則": "雞蛋 → 牛奶", "支持度": 0.5, "信心度": 0.67}
    ]
}
```

### 回歸（Regression）

```python
# 回歸：預測連續數值

# 線性回歸
def linear_regression(X, y):
    # 最小平方法求解
    # y = w0 + w1*x1 + w2*x2 + ...

    # 閉式解
    X_b = add_bias_term(X)
    weights = inv(X_b.T @ X_b) @ X_b.T @ y

    return weights

# 應用：房價預測
housing_prediction = {
    "輸入特徵": ["坪數", "房間數", "屋齡", "地段"],
    "輸出": "房價預測值",
    "評估指標": "MAE, RMSE, R²"
}
```

## 推薦系統

### 协同过滤

2008 年，推​​荐系統開始普及：

```python
# 協同過濾推薦系統

collaborative_filtering = {
    "原理": "相似用戶有相似偏好",
    "輸入": "用戶-項目評分矩陣",
    "輸出": "對未評分項目的預測評分",
    "挑戰": "稀疏性、冷啟動問題"
}

# 矩陣分解
user_item_matrix = [
    # 項目A  項目B  項目C
    [5, 3, 0],  # 用戶1
    [4, 0, 2],  # 用戶2
    [1, 1, 0],  # 用戶3
    [0, 0, 4],  # 用戶4
]

# 預測：用戶3對項目A的評分
# 根據相似用戶推斷
```

### Netflix Prize 的影響

2006-2009 年的 Netflix Prize 競賽推動了推薦系統的發展：

```python
netflix_prize = {
    "獎金": "$1,000,000",
    "目標": "比現有系統提升 10% 準確率",
    "資料規模": "1億個評分",
    "時間範圍": "2006-2009",
    "獲獎團隊": "BellKor",
    "技術創新": "矩陣分解、集成方法"
}
```

## 大規模資料處理

### MapReduce 的角色

```python
# MapReduce 適合的資料探勘任務

mapreduce_suitable_tasks = [
    "Word counting (文字探勘)",
    "PageRank (網頁排名)",
    "Log analysis (日誌分析)",
    "Graph processing (圖處理)",
    "Inverted index (倒排索引)"
]

# 分散式集群分析示意
distributed_clustering = {
    "問題": "百萬筆資料無法放進單一機器",
    "解決方案": "分散式 K-Means",
    "流程": [
        "1. Map: 每個資料點計算所屬集群",
        "2. Reduce: 聚合每個集群的資料",
        "3. 迭代直到收斂"
    ],
    "框架": "Hadoop, Spark"
}
```

## 文字探勘

### 2008 年的文字探勘

```python
# 文字探勘基本流程

text_mining_pipeline = {
    "文字收集": "網頁爬蟲、API、日誌",
    "文字前處理": [
        "斷詞 (Tokenization)",
        "移除停用詞 (Stopword removal)",
        "詞形還原 (Lemmatization)",
        "大小寫統一"
    ],
    "特徵提取": [
        "Bag of Words",
        "TF-IDF",
        "N-grams"
    ],
    "分析應用": [
        "情緒分析",
        "文字分類",
        "主題模型"
    ]
}
```

### 情緒分析（Sentiment Analysis）

```python
# 2008 年的情緒分析技術

sentiment_analysis = {
    "方法": {
        "基於詞典": "使用情感詞典（正面/負面詞）",
        "基於機器學習": "分類器（NB, SVM, MaxEnt）",
        "混合方法": "結合詞典和學習"
    },
    "挑戰": {
        "諷刺偵測": "「這個產品太棒了，壞透了」",
        "上下文依賴": "不同領域情感詞不同",
        "多語言": "需要針對每種語言建立資源"
    }
}
```

## 視覺化

### 資料視覺化的重要性

```python
# 資料視覺化在探勘中的作用

visualization_role = {
    "探索階段": "發現資料中的異常和模式",
    "驗證階段": "確認發現的模式的合理性",
    "呈現階段": "向非技術人員解釋結果",
    "工具": ["Excel", "Tableau", "Gnuplot", "R"]
}
```

### 常見視覺化圖形

```python
# 適合不同分析目的的圖形

charts_for_analysis = {
    "分佈": ["直方圖", "盒形圖", "密度圖"],
    "關係": ["散佈圖", "熱圖", "泡泡圖"],
    "趨勢": ["線圖", "面積圖"],
    "比較": ["長條圖", "雷達圖"],
    "集群": ["樹狀圖", " MDS 圖"]
}
```

## 挑戰與限制

### 2008 年的資料探勘挑戰

```python
# 當時面臨的問題

challenges_2008 = {
    "維度災難": "高維度資料難以處理",
    "記憶體限制": "大型資料集超出單機容量",
    "即時性": "需要即時或近即時分析",
    "資料品質": "雜訊、缺失值、異常值",
    "隱私問題": "個人資料保護法規"
}
```

## 未來展望

### 預測（2008-2012）

```python
# 資料探勘的未來趨勢

future_trends = {
    "2008-2010": [
        "Hadoop 生態系統成熟",
        "即時分析需求浮現",
        "NoSQL 資料庫普及"
    ],
    "2010-2012": [
        "Spark 成為主流",
        "串流處理興起",
        "深度學習應用於文字/圖片"
    ],
    "2012+": [
        "深度學習主導",
        "自動機器學習 (AutoML)",
        "邊緣運算與聯盟學習"
    ]
}
```

---

**延伸閱讀**

- [Data mining techniques](https://www.google.com/search?q=data+mining+techniques+2008)
- [MapReduce+data+mining](https://www.google.com/search?q=MapReduce+data+mining)
- [Recommendation+system+2008](https://www.google.com/search?q=recommendation+system+2008)