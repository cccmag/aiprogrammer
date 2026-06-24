# Pandas 資料處理

## Pandas 概述

Pandas 是 Python 資料分析的關鍵工具，提供了 DataFrame 這種表格化資料結構。

## Series 與 DataFrame

```python
import pandas as pd

# Series
s = pd.Series([1, 3, 5, 7, 9], index=['a', 'b', 'c', 'd', 'e'])
print(s['c'])  # 5

# DataFrame
df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Carol'],
    'age': [25, 30, 35],
    'score': [90, 85, 88]
})
print(df.head())
```

## 資料讀取

```python
# 讀取 CSV
df = pd.read_csv('data.csv')

# 讀取 Excel
df = pd.read_excel('data.xlsx', sheet_name='Sheet1')

# 讀取 JSON
df = pd.read_json('data.json')

# 顯示基本資訊
print(df.info())
print(df.describe())
```

## 選擇資料

```python
# 選擇列
print(df[df['age'] > 25])

# 選擇欄位
print(df[['name', 'score']])

# iloc[index] 和 loc[label]
print(df.iloc[0])      # 第一列
print(df.loc[0])       # 標籤為 0 的列
```

## 資料清洗

```python
# 處理缺失值
df.dropna()           # 刪除有缺失值的列
df.fillna(0)          # 用 0 填補缺失值
df['age'].fillna(df['age'].mean())

# 去除重複
df.drop_duplicates()

# 欄位重新命名
df.rename(columns={'name': 'username', 'age': 'years'})
```

## 資料轉換

```python
# 新增欄位
df['pass'] = df['score'] >= 60

#  apply 函數
df['name_upper'] = df['name'].apply(str.upper)

# Lambda
df['age_group'] = df['age'].apply(lambda x: 'young' if x < 30 else 'adult')
```

## 分組聚合

```python
# groupby
grouped = df.groupby('department')

for dept, group in grouped:
    print(f"{dept}: {len(group)} 人")

# 聚合函數
print(df.groupby('department')['salary'].mean())
print(df.groupby(['department', 'year'])['score'].agg(['mean', 'max']))
```

## 合併資料

```python
# concat
df1 = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
df2 = pd.DataFrame({'A': [5, 6], 'B': [7, 8]})
result = pd.concat([df1, df2])

# merge
df3 = pd.DataFrame({'name': ['Alice', 'Bob'], 'city': ['NY', 'LA']})
merged = df.merge(df3, on='name', how='left')
```

## 排序

```python
# 按欄位排序
df.sort_values('score', ascending=False)

# 多欄位排序
df.sort_values(['department', 'score'], ascending=[True, False])

# 排名
df['rank'] = df['score'].rank(ascending=False)
```

## 輸出

```python
# 寫入 CSV
df.to_csv('output.csv', index=False)

# 寫入 Excel
df.to_excel('output.xlsx', sheet_name='Sheet1', index=False)

# 轉為 JSON
df.to_json('output.json', orient='records', indent=2)
```

## 參考資源

- https://www.google.com/search?q=Pandas+tutorial+data+analysis+dataframe+2019
- https://www.google.com/search?q=Pandas+groupby+merge+reshape+data+manipulation+2019
- https://www.google.com/search?q=Pandas+performance+tips+large+dataset+2019