# 時間序列資料處理

## 時間資料的獨特性

時間序列資料在金融、物聯網、監控等領域無處不在。不同於靜態資料，時間序列的觀察值之間存在時間依賴性——今天的股價和昨天的股價有關。

## Pandas 時間序列工具

Pandas 提供了一套完整的時間序列處理功能：

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 建立時間序列
dates = pd.date_range("2022-01-01", periods=100, freq="D")
ts = pd.Series(np.cumsum(np.random.randn(100)) + 100, index=dates)
```

## 日期範圍與頻率

```python
# 各種頻率
pd.date_range("2022-01", periods=12, freq="M")   # 月底
pd.date_range("2022-01", periods=12, freq="MS")   # 月初
pd.date_range("2022-01", periods=52, freq="W")    # 每週
pd.date_range("2022-01", periods=24, freq="h")    # 每小時

# 自訂頻率
pd.date_range("2022-01", periods=10, freq="2D")  # 每兩天
```

## 索引與切片

```python
# 字串索引
ts["2022-01"]
ts["2022-01-15":"2022-02-15"]

# 日期屬性
ts.index.year
ts.index.month
ts.index.weekday
```

## 重採樣（Resampling）

將時間序列從高頻轉為低頻（降採樣）或反之（升採樣）：

```python
# 降採樣：日資料 → 月平均
monthly = ts.resample("M").mean()

# 自訂聚合
weekly = ts.resample("W").agg(["mean", "std", "min", "max"])

# 升採樣：日資料 → 每小時（需要填充）
hourly = ts.resample("h").ffill()  # 向前填充
```

## 滾動視窗

```python
# 7 天滾動平均
ts_rolling = ts.rolling(window=7).mean()

# 滾動相關係數
returns = ts.pct_change().dropna()
rolling_corr = returns.rolling(20).corr(returns.shift(1))

# 指數加權移動平均
ewma = ts.ewm(span=7).mean()
```

## 時間序列分解

時間序列通常包含以下成分：

- **趨勢**：長期變化方向
- **季節性**：固定週期的波動
- **殘差**：隨機噪聲

```python
from statsmodels.tsa.seasonal import seasonal_decompose

# 季節性分解
result = seasonal_decompose(ts, model="additive", period=7)
trend = result.trend
seasonal = result.seasonal
residual = result.resid
```

## 時間差與位移

```python
# 計算前一天的變化
ts_diff = ts.diff()

# 計算百分比變化（收益率）
returns = ts.pct_change()

# 位移
ts_shifted = ts.shift(1)  # 前一天的值
ts_future = ts.shift(-1)  # 後一天的值
```

## 延伸閱讀

- [Pandas 時間序列教學](https://www.google.com/search?q=Pandas+time+series+tutorial)
- [時間序列分析基礎](https://www.google.com/search?q=time+series+analysis+basics)
- [statsmodels 時間序列](https://www.google.com/search?q=statsmodels+time+series)
