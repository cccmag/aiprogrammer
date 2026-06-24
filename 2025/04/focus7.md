# 從資料到洞察

## 資料分析的工作流程

資料分析不是一個單一動作，而是一個循環迭代的過程。理解完整的工作流程，有助於更有效地從資料中提取價值。

### 1. 定義問題

在開始分析之前，先問自己：我想從資料中了解什麼？清晰的問題定義能引導後續的分析方向。

### 2. 資料取得

從資料庫、API、CSV 檔案或網頁爬蟲取得資料。Pandas 提供了多種讀取函式：

```python
import pandas as pd
df = pd.read_csv("data.csv")
```

### 3. 資料清理

處理缺失值、移除重複、修正格式錯誤。這個階段通常最耗時，但也最重要。

### 4. 探索性資料分析（EDA）

EDA 是資料分析的核心環節。目標是透過統計摘要和視覺化來理解資料的結構、分佈和關聯性。

```python
# EDA 常用操作
print(df.head())           # 查看前幾筆
print(df.info())           # 資料型別與缺失
print(df.describe())       # 統計摘要
print(df["類別"].value_counts())  # 類別計數
```

### 5. 視覺化探索

```python
import matplotlib.pyplot as plt

fig, axes = plt.subplots(2, 2, figsize=(12, 8))
df.hist(ax=axes[0, 0])
df.boxplot(ax=axes[0, 1])
axes[1, 0].scatter(df["x"], df["y"])
df.corr().plot(ax=axes[1, 1], kind="heat")
```

## 敘述性統計

敘述性統計幫助我們用數字來描述資料的特徵：

```python
# 集中趨勢
mean = df["數值"].mean()
median = df["數值"].median()
mode = df["數值"].mode()

# 離散程度
std = df["數值"].std()
var = df["數值"].var()
iqr = df["數值"].quantile(0.75) - df["數值"].quantile(0.25)

# 分佈形狀
skew = df["數值"].skew()    # 偏度
kurt = df["數值"].kurtosis() # 峰度
```

## 相關性分析

```python
# 相關係數矩陣
corr = df.corr(method="pearson")

# 視覺化相關性
import seaborn as sns
sns.heatmap(corr, annot=True, cmap="coolwarm")
```

## 視覺化說故事

好的視覺化不只呈現數字，更要傳達故事。以下是幾個原則：

**選擇正確的圖表**：趨勢用折線圖，比較用長條圖，分佈用直方圖，關聯用散佈圖。

**簡潔為上**：移除不必要的裝飾，讓資料自己說話。

**注釋引導**：在關鍵處加上標註，引導讀者的注意力。

```python
plt.figure(figsize=(10, 5))
plt.plot(dates, values, marker="o")
plt.axvline(x=關鍵日期, color="red", linestyle="--", label="事件")
plt.annotate("重大變化", xy=(關鍵日期, 對應值),
             xytext=(關鍵日期, 對應值 + 10),
             arrowprops=dict(arrowstyle="->"))
```

## 結論

從資料到洞察的過程，是技術與思考的結合。熟練使用 NumPy、Pandas 和 Matplotlib 等工具是基礎，但真正的價值來自於提出正確的問題、選擇合適的分析方法、以及用清晰的方式傳達發現。

---

**延伸閱讀**
- [探索性資料分析指南](https://www.google.com/search?q=exploratory+data+analysis+guide+Python)
- [資料視覺化最佳實踐](https://www.google.com/search?q=data+visualization+best+practices)
