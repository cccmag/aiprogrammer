# Pandas 資料處理入門

## Pandas 簡介

Pandas 是 Python 中最強大的資料處理和分析庫，提供了 DataFrame 和 Series 兩種主要資料結構。

## Series

Series 是一個帶標籤的一維陣列：

```python
import pandas as pd

# 從列表創建
s = pd.Series([10, 20, 30, 40], index=['a', 'b', 'c', 'd'])
print(s)
print(s['a'])       # 10
print(s.values)     # [10, 20, 30, 40]
print(s.index)      # Index(['a', 'b', 'c', 'd'])
```

## DataFrame

DataFrame 是一個二維表格資料結構，類似於電子表格或 SQL 資料表：

```python
import pandas as pd

# 從字典創建
data = {
    'name': ['張小明', '李小華', '王小美'],
    'age': [28, 35, 24],
    'salary': [50000, 75000, 45000]
}
df = pd.DataFrame(data)
print(df)

# 基本屬性
print(df.shape)     # (3, 3)
print(df.columns)   # ['name', 'age', 'salary']
print(df.dtypes)    # 欄位類型
```

## 選擇資料

```python
# 選擇欄位
print(df['name'])           # 單欄
print(df[['name', 'age']])  # 多欄

# 選擇列
print(df.iloc[0])           # 第一列（位置）
print(df.loc[0])            # 第一列（標籤）

# 條件過濾
print(df[df['age'] > 25])
print(df[(df['age'] > 25) & (df['salary'] > 50000)])
```

## 資料操作

```python
# 新增欄位
df['bonus'] = df['salary'] * 0.1

# 刪除欄位
df = df.drop('bonus', axis=1)

# 重命名欄位
df = df.rename(columns={'name': '姓名', 'age': '年齡'})

# 排序
df = df.sort_values('salary', ascending=False)
```

## 處理缺失值

```python
# 模擬缺失值
df.loc[1, 'salary'] = None

# 檢測缺失值
print(df.isnull())
print(df.isnull().sum())

# 處理缺失值
df['salary'].fillna(df['salary'].mean(), inplace=True)  # 用平均數填補
df = df.dropna()  # 刪除有缺失值的列
```

## 群組運算

```python
# 分組聚合
grouped = df.groupby('city')
print(grouped['salary'].mean())

# 多重聚合
df.groupby('city').agg({
    'salary': ['mean', 'max', 'min'],
    'age': 'mean'
})
```

## 合併資料

```python
# 串接
pd.concat([df1, df2])

# 合併（類似 SQL JOIN）
pd.merge(df1, df2, on='common_column', how='inner')
```

## 結論

Pandas 是處理表格資料的利器。掌握好 DataFrame 的操作，能讓資料處理工作變得輕鬆高效。