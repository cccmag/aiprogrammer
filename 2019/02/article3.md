# Pandas 資料分析

## Pandas 簡介

Pandas 是 Python 資料處理的關鍵工具，提供 DataFrame 結構與豐富的資料處理功能。

## Series 與 DataFrame

```python
import pandas as pd
import numpy as np

s = pd.Series([1, 3, 5, np.nan, 6, 8])
print(s)

dates = pd.date_range('20190101', periods=6)
df = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=['A', 'B', 'C', 'D'])
print(df)
print(df.dtypes)
```

## 讀取資料

```python
df = pd.read_csv('data.csv')
df = pd.read_excel('data.xlsx')
df = pd.read_json('data.json')

df = pd.read_csv('data.csv', nrows=100)
df = pd.read_csv('data.csv', usecols=['name', 'age', 'score'])
```

## 基本操作

```python
print(df.head())
print(df.tail(3))
print(df.describe())
print(df.info())
print(df.shape)
print(df.columns)
print(df.index)
```

## 選擇資料

```python
print(df['name'])
print(df[['name', 'age']])
print(df[0:3])
print(df.loc['row_name'])
print(df.iloc[0])
print(df.iloc[0:3, 1:3])
print(df[df['age'] > 20])
```

## 布林索引

```python
print(df[df['age'] > 20])
print(df[(df['age'] > 20) & (df['score'] > 80)])
print(df[df['name'].str.contains('John')])
```

## 缺失值處理

```python
print(df.isnull().sum())
df_cleaned = df.dropna()
df_filled = df.fillna(0)
df_interpolated = df.interpolate()
```

## 排序

```python
df_sorted = df.sort_values(by='age')
df_sorted_desc = df.sort_values(by='age', ascending=False)
df_sorted_multi = df.sort_values(by=['age', 'score'])
```

## 分組聚合

```python
grouped = df.groupby('category')
print(grouped.mean())
print(grouped.sum())
print(grouped.agg(['mean', 'sum', 'count']))

grouped_specific = df.groupby('category')['score'].mean()
print(grouped_specific)
```

## 合併資料

```python
df1 = pd.DataFrame({'key': ['a', 'b', 'c'], 'value': [1, 2, 3]})
df2 = pd.DataFrame({'key': ['a', 'b', 'd'], 'value': [4, 5, 6]})

merged = pd.merge(df1, df2, on='key', how='inner')
concatenated = pd.concat([df1, df2], ignore_index=True)
```

## 應用函數

```python
df['age_double'] = df['age'].apply(lambda x: x * 2)
df['category'] = df['name'].apply(lambda x: '成人' if x > 18 else '兒童')

def categorize(score):
    if score >= 90:
        return 'A'
    elif score >= 80:
        return 'B'
    return 'C'

df['grade'] = df['score'].apply(categorize)
```

## 時間序列

```python
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)
print(df.resample('M').sum())
print(df.resample('W').mean())
```

## 資料透視表

```python
pivot = pd.pivot_table(df, values='score', index='category',
                       columns='gender', aggfunc='mean')
print(pivot)
```

## 輸出資料

```python
df.to_csv('output.csv', index=False)
df.to_excel('output.xlsx', index=False)
df.to_json('output.json', orient='records')
```

## 參考資源

- https://www.google.com/search?q=Pandas+tutorial+DataFrame+Python+data+analysis+2019
- https://www.google.com/search?q=Pandas+groupby+merge+filter+Python+2019
- https://www.google.com/search?q=Pandas+time+series+resample+Python+tutorial+2019