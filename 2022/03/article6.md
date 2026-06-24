# 資料視覺化最佳實踐

## 好的圖表 vs 壞的圖表

一張好的圖表應該讓讀者在一秒鐘內理解核心資訊。壞的圖表則會誤導或混淆讀者。資料視覺化不僅是技術，更是溝通藝術。

## 選擇正確的圖表類型

```
資料類型          │ 建議圖表
─────────────────┼──────────────────
隨時間變化        │ 折線圖
類別比較          │ 長條圖
分佈              │ 直方圖、箱型圖
相關性            │ 散點圖
組成比例          │ 圓餅圖（謹慎使用）
地理資料          │ 地圖
多維資料          │ 刻面圖（facet）
```

### 常見錯誤

**圓餅圖濫用**：超過 5 個類別或比例相近時，圓餅圖難以閱讀。

```python
# ❌ 避免使用圓餅圖
plt.pie(values, labels=labels)

# ✅ 改用長條圖
plt.bar(labels, values)
```

**3D 圖表**：除非有真正的第三維，否則永遠不要使用 3D 圖表。

```python
# ❌ 避免 3D
ax = plt.axes(projection="3d")
ax.bar3d(...)

# ✅ 改用刻面或顏色編碼
sns.FacetGrid(...)
```

## 色彩選擇的重要性

```python
# 連續資料：漸層色
sns.color_palette("viridis", 10)
sns.color_palette("coolwarm", 10)

# 類別資料：離散色
sns.color_palette("Set2", 8)
sns.color_palette("colorblind", 10)

# 色盲友善
from palettable.colorbrewer.qualitative import Set2_8
```

## 圖表設計原則

### Tufte 原則

Edward Tufte 提出的資料-墨水比概念：

```
資料-墨水比 = 用於顯示資料的墨水 / 總墨水
```

目標是最大化這個比例——去除所有不必要的元素：

```python
# 去除邊框
sns.despine()

# 減少網格
plt.grid(True, alpha=0.3)

# 去除不必要的標籤
ax.tick_params(labelbottom=False)
```

### 字體與可讀性

```python
plt.rcParams.update({
    "font.size": 12,
    "axes.titlesize": 14,
    "axes.labelsize": 12,
    "figure.dpi": 150,
})
```

## 進階技巧

### 刻面（Faceting）

```python
sns.FacetGrid(df, col="category", hue="type").map(
    sns.scatterplot, "x", "y"
)
```

### 註釋

```python
# 在圖表上標註關鍵點
ax.annotate("Peak", xy=(x_peak, y_peak),
            xytext=(x_peak + 0.5, y_peak + 0.5),
            arrowprops=dict(facecolor="black", shrink=0.05))
```

### 多重圖層

```python
# 結合分佈和原始資料
sns.violinplot(data=df, x="group", y="value")
sns.stripplot(data=df, x="group", y="value",
              color="black", alpha=0.3)
```

## 延伸閱讀

- [Edward Tufte 視覺化原則](https://www.google.com/search?q=Edward+Tufte+data+visualization+principles)
- [Matplotlib 官方範例](https://www.google.com/search?q=Matplotlib+gallery)
- [Seaborn 圖表範例](https://www.google.com/search?q=Seaborn+example+gallery)
- [色盲友善調色盤](https://www.google.com/search?q=colorblind+friendly+palette)
