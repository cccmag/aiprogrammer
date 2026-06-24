# 線性迴歸實作

## 問題設定

我們用一個實際問題來示範線性迴歸：根據廣告支出預測銷售金額。

假設我們有一家公司的歷史資料，包含電視廣告支出和對應的銷售額。我們想建立一個模型，預測在不同廣告預算下可以達到的銷售額。

## 資料準備

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# 模擬廣告支出與銷售額資料
np.random.seed(42)
tv_ad = np.random.uniform(10, 100, size=50)
sales = 3.5 * tv_ad + 25 + np.random.normal(0, 15, size=50)

X = tv_ad.reshape(-1, 1)
y = sales
```

## 訓練與預測

```python
# 建立和訓練模型
model = LinearRegression()
model.fit(X, y)

# 預測
y_pred = model.predict(X)

print(f"權重 (w): {model.coef_[0]:.3f}")
print(f"截距 (b): {model.intercept_:.3f}")
print(f"R² 分數: {r2_score(y, y_pred):.3f}")
```

## 解讀結果

輸出範例：
```
權重 (w): 3.487
截距 (b): 24.356
R² 分數: 0.862
```

這意味著：廣告支出每增加 1 單位，銷售額平均增加 3.487 單位。截距 24.356 是在沒有廣告時的基本銷售額。R² 為 0.862 表示模型解釋了 86.2% 的銷售額變異。

## 預測新資料

```python
# 預測廣告支出為 80 時的銷售額
new_ad = np.array([[80]])
pred_sales = model.predict(new_ad)
print(f"廣告支出 80 → 預測銷售額: {pred_sales[0]:.2f}")
```

## 多變量線性迴歸

現實中，銷售可能受多個因素影響：

```python
# 多變量：電視廣告、廣播廣告、報紙廣告
np.random.seed(42)
n = 100
tv = np.random.uniform(10, 100, n)
radio = np.random.uniform(5, 50, n)
newspaper = np.random.uniform(1, 30, n)

sales = 3.2 * tv + 1.8 * radio + 0.5 * newspaper + 20 + np.random.normal(0, 10, n)

X_multi = np.column_stack([tv, radio, newspaper])

model_multi = LinearRegression()
model_multi.fit(X_multi, sales)

for name, coef in zip(["電視", "廣播", "報紙"], model_multi.coef_):
    print(f"{name} 權重: {coef:.3f}")

print(f"R² 分數: {r2_score(sales, model_multi.predict(X_multi)):.3f}")
```

## 注意事項

### 1. 特徵尺度

不同特徵的尺度差異可能影響模型的穩定性。使用 `StandardScaler` 可以改善：

```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_multi)
```

### 2. 異常值

線性迴歸對異常值敏感，因為最小平方法會放大離群點的影響。使用 `RANSACRegressor` 可以增強魯棒性。

### 3. 多重共線性

當特徵之間高度相關時，模型權重估計會不穩定。可以使用相關矩陣檢測，或用 Ridge 迴歸（L2 正則化）緩解。

```python
from sklearn.linear_model import Ridge

ridge = Ridge(alpha=1.0)
ridge.fit(X_multi, sales)
```

## 完整範例

完整的線性迴歸實作可參考 `_code/ml_intro.py` 中的第一部分，該範例使用 `make_regression` 生成人造資料並展示完整的訓練與評估流程。

---

## 延伸閱讀

- [scikit-learn 線性迴歸](https://www.google.com/search?q=scikit-learn+linear+regression)
- [多變量迴歸分析](https://www.google.com/search?q=multiple+linear+regression)
- [Ridge 與 Lasso 迴歸](https://www.google.com/search?q=ridge+lasso+regression)
