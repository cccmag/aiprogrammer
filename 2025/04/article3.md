# Pandas 讀取 CSV/Excel

## 前言

資料分析的第一步是載入資料。Pandas 提供了豐富的 I/O 功能，從 CSV、Excel、SQL 資料庫到 JSON 和 Parquet，幾乎支援所有常見的資料格式。本文將重點介紹 CSV 和 Excel 的讀取技巧。

## 讀取 CSV 檔案

CSV（Comma-Separated Values）是最常見的資料交換格式：

```python
import pandas as pd

# 基本讀取
df = pd.read_csv("data.csv")

# 指定分隔符
df = pd.read_csv("data.tsv", sep="\t")

# 指定編碼
df = pd.read_csv("data.csv", encoding="utf-8")

# 跳過行數
df = pd.read_csv("data.csv", skiprows=2)
```

### 常用參數

```python
# 只讀取特定欄位
df = pd.read_csv("data.csv", usecols=["name", "age", "city"])

# 指定資料型別
df = pd.read_csv("data.csv", dtype={"age": int, "price": float})

# 將特定欄位設為索引
df = pd.read_csv("data.csv", index_col="id")

# 處理缺失值標記
df = pd.read_csv("data.csv", na_values=["NA", "NULL", "-"])
```

### 大檔案處理

```python
# 分塊讀取 (回傳迭代器)
chunks = pd.read_csv("large.csv", chunksize=10000)
for chunk in chunks:
    process(chunk)

# 只讀取前 n 行
df = pd.read_csv("large.csv", nrows=100)
```

## 讀取 Excel 檔案

```python
# 基本讀取
df = pd.read_excel("data.xlsx")

# 指定工作表
df = pd.read_excel("data.xlsx", sheet_name="Sheet1")
df = pd.read_excel("data.xlsx", sheet_name=0)  # 第一個工作表

# 讀取多個工作表
sheets = pd.read_excel("data.xlsx", sheet_name=None)
print(sheets.keys())  # 所有工作表名稱
```

### Excel 進階參數

```python
# 指定資料範圍
df = pd.read_excel("data.xlsx", sheet_name=0, skiprows=3, nrows=100)

# 合併儲存格處理
df = pd.read_excel("data.xlsx", header=[0, 1])  # 多層表頭

# 指定解析引擎
df = pd.read_excel("data.xlsx", engine="openpyxl")  # .xlsx
df = pd.read_excel("data.xls", engine="xlrd")        # .xls
```

## 寫入檔案

```python
# 寫入 CSV
df.to_csv("output.csv", index=False, encoding="utf-8-sig")

# 寫入 Excel
df.to_excel("output.xlsx", sheet_name="Results", index=False)

# 寫入多個工作表到同一個 Excel
with pd.ExcelWriter("report.xlsx") as writer:
    df_summary.to_excel(writer, sheet_name="Summary")
    df_detail.to_excel(writer, sheet_name="Detail")
```

## 實戰範例

### 從網路讀取 CSV

```python
url = "https://raw.githubusercontent.com/datasets/covid-19/main/data/countries-aggregated.csv"
df = pd.read_csv(url)
print(df.head())
```

### 讀取與處理

```python
df = pd.read_csv("sales.csv", parse_dates=["date"])
df["year"] = df["date"].dt.year
monthly = df.groupby("year")["amount"].sum()
print(monthly)
```

## 常見問題

### 編碼問題

遇到亂碼時，嘗試不同編碼：

```python
encodings = ["utf-8", "cp950", "big5", "latin1"]
for enc in encodings:
    try:
        df = pd.read_csv("data.csv", encoding=enc)
        print(f"Success with {enc}")
        break
    except UnicodeDecodeError:
        continue
```

---

**延伸閱讀**
- [Pandas I/O 官方文件](https://www.google.com/search?q=Pandas+IO+tools+documentation)
- [Pandas read_csv 參數說明](https://www.google.com/search?q=Pandas+read_csv+parameters)
