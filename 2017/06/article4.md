# 文章 4：時間序列資料處理

## 前言

時間序列資料廣泛存在於金融、氣象、感測器等領域。本章節介紹如何處理時間序列資料。

## datetime 模組

```python
from datetime import datetime, timedelta

# 創建日期時間
dt = datetime(2023, 5, 15, 10, 30, 0)
print(dt)  # 2023-05-15 10:30:00

# 格式化
print(dt.strftime("%Y-%m-%d %H:%M:%S"))  # 2023-05-15 10:30:00
print(dt.strftime("%B %d, %Y"))  # May 15, 2023

# 解析
dt2 = datetime.strptime("2023-05-15", "%Y-%m-%d")
print(dt2)  # 2023-05-15 00:00:00
```

## 時間運算

```python
from datetime import datetime, timedelta

dt1 = datetime(2023, 5, 15)
dt2 = datetime(2023, 5, 20)

# 日期差
diff = dt2 - dt1
print(diff.days)  # 5

# 時間增減
new_dt = dt1 + timedelta(days=10, hours=5)
print(new_dt)  # 2023-05-25 05:00:00
```

## pandas 時間序列

```python
import pandas as pd

# 創建時間索引
dates = pd.date_range('2023-01-01', periods=10, freq='D')
print(dates)

# 創建時間序列 DataFrame
df = pd.DataFrame({
    'date': dates,
    'value': [10, 20, 15, 25, 30, 35, 28, 32, 38, 40]
})
print(df)

# 轉換日期列
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)
print(df)
```

## 時間序列切片

```python
import pandas as pd

df = pd.DataFrame({
    'date': pd.date_range('2023-01-01', periods=100),
    'value': range(100)
})
df.set_index('date', inplace=True)

# 按月選擇
print(df['2023-03'])

# 按範圍選擇
print(df['2023-01-10':'2023-01-20'])

# 重採樣
monthly = df.resample('M').mean()
print(monthly)
```

## 滑動視窗

```python
import pandas as pd

df = pd.DataFrame({
    'value': range(10)
})

# 移動平均
df['ma_3'] = df['value'].rolling(window=3).mean()
df['ma_5'] = df['value'].rolling(window=5).mean()

print(df)
```

## 時區處理

```python
import pandas as pd

# 創建帶時區的時間序列
dates = pd.date_range('2023-01-01', periods=10, freq='D', tz='UTC')
print(dates)

# 轉換時區
dates_taipei = dates.tz_convert('Asia/Taipei')
print(dates_taipei)
```

## 總結

時間序列處理需要特別注意時間的表示與運算。pandas 提供了強大的時間序列功能，是處理這類資料的首選工具。

## 延伸閱讀

- https://www.google.com/search?q=pandas+time+series+tutorial
- https://www.google.com/search?q=Python+datetime+timedelta