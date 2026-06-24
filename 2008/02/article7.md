# 支援向量機

## 前言

支援向量機（Support Vector Machine, SVM）是 1990 年代到 2000 年代最重要的機器學習演算法之一。在深度學習興起之前，SVM 是許多領域的首選方法。

## SVM 的基本概念

### 最大邊界分類器

```python
# SVM 的核心思想：找到能夠最大化類別間距的分類邊界

svm_concept = {
    "目標": "找到一個超平面，能夠完美分開兩類資料",
    "約束": "最大化兩個類別到超平面的最小距離",
    "幾何意義": "找到最寬的「街道」分開兩類"
}
```

### 線性可分的情況

```
       Support Vector Machine

    類別 A ● ●    ┃    ● ● 類別 B
              ● ● ┃ ● ●
                  ┃ ← 最大邊界
              ● ● ┃ ● ●
    類別 A ● ●    ┃    ● ● 類別 B

    ┃ = 分類超平面
    ● = 支援向量（決定超平面位置的點）
```

## 核心數學

### 超平面

```python
# n 維空間的超平面定義

hyperplane_equation = {
    "表示": "w·x + b = 0",
    "w": "權重向量（垂直於超平面）",
    "x": "輸入向量",
    "b": "偏置項"
}

# 分類決策：
# 如果 w·x + b > 0 → 類別 1
# 如果 w·x + b < 0 → 類別 -1
```

### 優化問題

```python
# SVM 的最佳化問題

optimization_problem = {
    "目標函數": "最小化 ||w||²（最大化邊界）",
    "約束": "對所有訓練樣本：yi(w·xi + b) ≥ 1",
    "yi": "類別標籤（+1 或 -1）"
}

# 這是一個凸二次規劃問題，有全域最佳解
```

## 核心函數（Kernel Trick）

### 為何需要核心函數？

```python
# 現實世界的資料往往不是線性可分的

non_linear_problem = {
    "問題": "線性分類器無法處理複雜邊界",
    "解決方案": "將資料映射到高維空間",
    "核心函數": "在原空間計算高維空間的內積"
}
```

### 常見核心函數

```python
kernel_functions = {
    "線性核心": "K(x, y) = x·y",
    "多項式核心": "K(x, y) = (x·y + c)^d",
    "徑向基函數 (RBF)": "K(x, y) = exp(-γ||x-y||²)",
    "Sigmoid": "K(x, y) = tanh(αx·y + c)"
}
```

### 核心函數範例

```
低維空間 → 高維空間映射：

二維資料：無法用直線分開（XOR 問題）

映射到三維：
(x1, x2) → (x1², x2², √2·x1·x2)

在三維空間中可用平面分開！
```

## 支援向量

### 支援向量的意義

```python
# 支援向量是離分類邊界最近的點

support_vectors = {
    "定義": "落在邊界上的訓練樣本",
    "數量": "通常只是訓練集的一小部分",
    "重要性": "只有支援向量決定分類器，其他點無關"
}

# 好處：模型稀疏，預測時只需要少數支援向量
```

### 稀疏性

```python
# SVM 的稀疏性優點

sparsity_benefits = {
    "記憶體": "只需要儲存支援向量",
    "預測速度": "預測時只計算支援向量",
    "泛化能力": "減少過擬合的風險"
}
```

## 軟間隔與正規化

### 允許錯誤分類

```python
# 軟間隔 SVM 允許一些錯誤分類

soft_margin = {
    "引數": "C（正規化參數）",
    "C 小": "較大邊界，較多錯誤（欠擬合）",
    "C 大": "較小邊界，較少錯誤（過擬合）",
    "目標": "在模型複雜度和錯誤之間取得平衡"
}
```

### 正規化公式

```python
soft_margin_formula = {
    "目標": "最小化 ||w||² + C·Σξi",
    "ξi": "鬆弛變數（允許的錯誤）",
    "約束": "yi(w·xi + b) ≥ 1 - ξi"
}
```

## SVM 的應用

### 文字分類

```python
# SVM 在文字分類的應用

text_classification = {
    "方法": "TF-IDF 向量化 + SVM",
    "優點": "高維度下表現良好",
    "應用": "垃圾郵件偵測、情緒分析",
    "範例": "Reuters-21578 新聞分類"
}
```

### 影像分類

```python
# 2008 年 SVM 用於影像分類

image_classification = {
    "方法": "SIFT/HOG 特徵 + SVM",
    "流程": "提取特徵 → 向量量化 → SVM 分類",
    "優點": "比簡單神經網路好",
    "缺點": "特徵工程需要專業知識"
}
```

## 實作

### 使用 LIBSVM

```python
# LIBSVM 是最流行的 SVM 函式庫

libsvm_usage = {
    "語言": "C++, Java, Python",
    "功能": "分類、回歸、分布估計",
    "參數": "C, gamma (RBF), kernel"
}

# Python 使用範例（概念）
def svm_classify(train_data, test_data):
    # 訓練
    model = svm_train(train_labels, train_data, '-c 1.0 -g 0.01')

    # 預測
    predictions = svm_predict(test_labels, test_data, model)

    return predictions
```

## 與其他方法的比較

### SVM vs 類神經網路

```python
svm_vs_nn = {
    "SVM": {
        "優點": "理論基礎強、全域最佳解、稀疏性",
        "缺點": "對大規模資料計算量大、核函數選擇困難"
    },
    "類神經網路": {
        "優點": "可處理複雜模式、自动特徵學習",
        "缺點": "容易陷入局部最小、訓練不穩定"
    }
}
```

### SVM vs 其他方法

```python
svm_vs_others = {
    "vs 決策樹": "SVM 通常更準確，但較難解釋",
    "vs 樸素貝葉斯": "SVM 更準確，但需要更多訓練時間",
    "vs KNN": "SVM 預測更快，儲存需求更少"
}
```

## 極限與挑戰

### SVM 的限制

```python
svm_limitations = {
    "計算複雜度": "訓練時間 O(n²) 到 O(n³)",
    "記憶體需求": "需要儲存核矩陣",
    "參數選擇": "C 和 gamma 的選擇不直觀",
    "不適合大規模訓練": "百萬樣本難以處理"
}
```

### 替代方案

```python
alternatives_for_large_scale = {
    "線性 SVM": "使用 SGD 訓練，適用於高維資料",
    "核心近似": "Random Fourier Features",
    "Gradient Descent": "邏輯回歸等方法"
}
```

## 未來展望

### 2008 年後的發展

```python
future_developments = {
    "深度學習興起": "SVM 熱度下降",
    "整合方法": "SVM 與其他方法結合",
    "理論工作": "理解深度學習與核方法的關係",
    "實際應用": "在某些領域仍是首選"
}
```

---

**延伸閱讀**

- [Support Vector Machine tutorial](https://www.google.com/search?q=Support+Vector+Machine+tutorial)
- [SVM+kernel+trick](https://www.google.com/search?q=SVM+kernel+trick)
- [LIBSVM+documentation](https://www.google.com/search?q=LIBSVM+documentation)