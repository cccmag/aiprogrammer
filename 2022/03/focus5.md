# Matplotlib 與 Seaborn 視覺化

## 資料視覺化的角色

在資料科學中，視覺化不僅是呈現結果的工具，更是探索資料的重要手段。一張好的圖表往往能揭示隱藏在數字背後的模式，遠比統計摘要更加直觀。Python 生態系中兩個最重要的視覺化函式庫是 Matplotlib 和 seaborn（通常寫作 Seaborn）。

## Matplotlib：底層繪圖引擎

Matplotlib 由 John Hunter 於 2003 年創建，靈感來自 MATLAB 的繪圖功能。它提供了對圖表元素的完全控制，從座標軸、刻度到圖例，每個細節都可以調整。

### 基本繪圖

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
y = np.sin(x)

plt.figure(figsize=(8, 4))
plt.plot(x, y, label="sin(x)", color="blue", linewidth=2)
plt.plot(x, np.cos(x), label="cos(x)", color="red", linestyle="--")
plt.xlabel("x")
plt.ylabel("y")
plt.title("Trigonometric Functions")
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
```

### 物件導向 API

Matplotlib 有兩層 API：`pyplot` 和物件導向介面。專業使用建議使用 OO API：

```python
fig, axes = plt.subplots(2, 2, figsize=(10, 8))
axes[0, 0].plot(x, y)
axes[0, 1].hist(data, bins=30)
axes[1, 0].scatter(x, y_noisy)
axes[1, 1].bar(categories, values)
plt.tight_layout()
```

### 常見圖表類型

| 類型 | 函數 | 用途 |
|------|------|------|
| 折線圖 | `plot()` | 時間序列、趨勢 |
| 散點圖 | `scatter()` | 相關性分析 |
| 直方圖 | `hist()` | 分佈分析 |
| 長條圖 | `bar()` | 類別比較 |
| 箱型圖 | `boxplot()` | 異常值檢測 |
| 熱力圖 | `imshow()` | 矩陣視覺化 |

## Seaborn：統計圖表利器

Seaborn 是建立在 Matplotlib 之上的高階統計視覺化函式庫，由 Michael Waskom 創建。它透過簡潔的 API 產生美觀的統計圖表。

```python
import seaborn as sns

# 載入內建資料集
iris = sns.load_dataset("iris")

# 成對散佈圖
sns.pairplot(iris, hue="species")

# 箱型圖
sns.boxplot(data=iris, x="species", y="petal_length")

# 熱力圖（相關矩陣）
sns.heatmap(iris.corr(), annot=True, cmap="coolwarm")
```

### Seaborn 的主題系統

```python
sns.set_theme(style="darkgrid", palette="muted", font_scale=1.2)
```

內建主題：`darkgrid`、`whitegrid`、`dark`、`white`、`ticks`

## 圖表設計原則

好的圖表遵循一些基本原則：

1. **簡潔**：去除不必要的裝飾，讓資料說話
2. **一致性**：同一報告中使用一致的色調和風格
3. **可讀性**：字體夠大、對比夠強、顏色考慮色盲友善
4. **誠實**：座標軸從零開始，不過度操縱視覺比例

```python
# 色盲友善的調色盤
sns.color_palette("colorblind")

# 避免 3D 圖表——除非真的需要
# 優先使用刻面（facet）來展示多維資料
```

## 延伸閱讀

- [Matplotlib 官方教學](https://www.google.com/search?q=Matplotlib+tutorial)
- [Seaborn 官方教學](https://www.google.com/search?q=Seaborn+tutorial)
- [資料視覺化最佳實踐](https://www.google.com/search?q=data+visualization+best+practices)

---

*本篇文章為「AI 程式人雜誌 2022 年 3 月號」歷史回顧系列之一。*
