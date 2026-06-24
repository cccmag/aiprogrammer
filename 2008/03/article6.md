# 機器學習基礎

## 前言

機器學習是人工智慧的核心，讓電腦能夠從資料中學習並做出預測。2008 年時，機器學習已廣泛應用於各種領域。

## 什麼是機器學習？

### 定義

```python
machine_learning_definition = {
    "Arthur Samuel (1959)": "讓電腦有能力學習而不需要明確程式設計",
    "Tom Mitchell (1998)": "經驗 E 學習，任務 T，效能 P，若 P 隨著 E 而提升，則 E 是經驗",
    "核心": "從資料中發現模式和規律"
}
```

### 與傳統程式設計的對比

```python
# 傳統程式設計
traditional_programming = {
    "輸入": "資料 + 規則",
    "處理": "套用規則",
    "輸出": "答案"
}

# 機器學習
machine_learning = {
    "輸入": "資料 + 答案（訓練資料）",
    "處理": "學習規則",
    "輸出": "學習到的規則"
}
```

## 機器學習的類型

### 監督式學習

```python
supervised_learning = {
    "定義": "從標註過的訓練資料學習",
    "輸入": "特徵 + 標籤",
    "目標": "學習輸入到輸出的映射",
    "類型": ["分類", "迴歸"]
}

# 分類範例：垃圾郵件偵測
# 輸入：郵件內容（特徵）
# 輸出：垃圾郵件 / 正常郵件（標籤）

# 迴歸範例：房價預測
# 輸入：坪數、房間數、地點（特徵）
# 輸出：價格（連續值）
```

### 無監督式學習

```python
unsupervised_learning = {
    "定義": "從未標註的資料學習",
    "輸入": "只有特徵，無標籤",
    "目標": "發現資料中的結構",
    "類型": ["集群", "降維", "關聯規則"]
}

# 集群範例：客戶分群
# 輸入：客戶的購買行為
# 輸出：客戶群組（未知的分組）

# 降維範例：視覺化
# 輸入：高維度特徵
# 輸出：2D 或 3D 表示
```

### 增強式學習

```python
reinforcement_learning = {
    "定義": "透過環境回饋學習",
    "學習者": "代理人（Agent）",
    "反饋": "獎勵或懲罰",
    "目標": "最大化長期獎勵"
}
```

## 機器學習流程

### 基本流程

```python
ml_pipeline = {
    "1. 收集資料": "從各種來源收集資料",
    "2. 資料預處理": "清理、轉換、標準化",
    "3. 訓練模型": "使用訓練資料擬合模型",
    "4. 評估模型": "在測試資料上評估效能",
    "5. 調整參數": "根據評估結果調整",
    "6. 部署模型": "上線預測新資料"
}
```

### 資料预处理

```python
data_preprocessing = {
    "清理缺失值": "填補或刪除",
    "處理異常值": "檢測和處理",
    "標準化": "將資料縮放到相同範圍",
    "編碼": "將類別資料轉為數值",
    "特徵工程": "從原始資料創造新特徵"
}
```

## 常見演算法

### 監督式學習演算法

```python
supervised_algorithms = {
    "線性迴歸": "連續值預測",
    "邏輯斯迴歸": "二元分類",
    "決策樹": "可解釋的分類",
    "隨機森林": "集成學習，強大的分類",
    "SVM": "支持向量機，強大的分類",
    "類神經網路": "可學習複雜模式"
}
```

### 無監督式學習演算法

```python
unsupervised_algorithms = {
    "K-Means": "集群",
    "階層式集群": "嵌套的集群",
    "PCA": "主成分分析，降維",
    "LDA": "線性判別分析",
    "關聯規則": "發現頻繁模式"
}
```

## 模型評估

### 常用指標

```python
classification_metrics = {
    "準確率 (Accuracy)": "正確預測 / 總數",
    "精確率 (Precision)": "TP / (TP + FP)",
    "召回率 (Recall)": "TP / (TP + FN)",
    "F1 分數": "2 × Precision × Recall / (Precision + Recall)"
}

# 混淆矩陣
#              預測
#           正   負
# 實際 正  TP  FN
#      負  FP  TN
```

### 交叉驗證

```python
cross_validation = {
    "概念": "將資料分成 k 份，輪流作為測試集",
    "目的": "減少過擬合的風險",
    "優點": "更可靠的性能估計"
}

# 5-fold 交叉驗證：
# 將資料分成 5 份
# 每次用 4 份訓練，1 份測試
# 報告平均性能
```

## 過擬合和欠擬合

### 過擬合（Overfitting）

```python
overfitting = {
    "定義": "模型對訓練資料擬合過度，泛化能力差",
    "原因": "模型太複雜，或訓練資料不足",
    "解決": [
        "更多訓練資料",
        "正則化",
        "減少模型複雜度",
        "交叉驗證"
    ]
}
```

### 欠擬合（Underfitting）

```python
underfitting = {
    "定義": "模型太簡單，無法捕捉資料規律",
    "原因": "模型太簡單或特徵不足",
    "解決": [
        "更複雜的模型",
        "更多特徵",
        "減少正則化"
    ]
}
```

## Scikit-learn

### Python 機器學習庫

```python
# scikit-learn 是 Python 機器學習的主要工具

from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# 載入資料
X, y = datasets.load_boston(return_X_y=True)

# 分割資料
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# 訓練模型
model = LinearRegression()
model.fit(X_train, y_train)

# 預測
predictions = model.predict(X_test)

# 評估
mse = mean_squared_error(y_test, predictions)
```

## 應用領域

```python
ml_applications = {
    "影像辨識": "臉部偵測、物體辨識",
    "自然語言處理": "情感分析、機器翻譯",
    "推薦系統": "電影推薦、商品推薦",
    "醫療診斷": "疾病預測、影像診斷",
    "金融": "信用評分、欺詐偵測",
    "語音辨識": "語音轉文字、語音助理"
}
```

## 未來展望

### 2008 年後的發展

```python
future_ml = {
    "2008-2012": "傳統機器學習成熟，開始被廣泛採用",
    "2012-2015": "深度學習興起，超越傳統方法",
    "2015+": "深度學習主導，特別是影像和語言"
}
```

---

**延伸閱讀**

- [Machine+learning+tutorial](https://www.google.com/search?q=machine+learning+tutorial)
- [Supervised+vs+unsupervised+learning](https://www.google.com/search?q=supervised+vs+unsupervised+learning)
- [Scikit-learn+tutorial](https://www.google.com/search?q=scikit-learn+tutorial)