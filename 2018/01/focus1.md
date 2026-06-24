# Python 3.6 新特性解析

## 簡介

Python 3.6 於 2016 年 12 月 23 日發布，代號「軾」 (Flag of the Pearls, Bilbies)。這個版本帶來了多項重要的新特性，其中 f-string、async/await 語法完善、以及型別提示增強最為重要。

## 主要新特性

### 1. f-string 格式化（PEP 498）

f-string 是 Python 3.6 最重要的新特性，提供了直觀的字串格式化方式：

```python
name = "Alice"
age = 30

# 舊式格式化
print("Name: {}, Age: {}".format(name, age))

# f-string 格式化
print(f"Name: {name}, Age: {age}")

# 支援表達式
print(f"Age in 5 years: {age + 5}")

# 格式化選項
pi = 3.14159
print(f"Pi: {pi:.2f}")  # Pi: 3.14
```

### 2. 型別提示增強（PEP 526）

Python 3.6 允許在變數宣告時直接指定型別：

```python
name: str = "Alice"
age: int = 30
scores: list = [90, 85, 88]
info: dict = {"name": "Bob", "age": 25}
```

### 3. 數字底線（PEP 515）

使大數字更易讀：

```python
million = 1_000_000
hex_val = 0x_FF_FF
binary = 0b_1010_1010
```

### 4. async/await 語法完善

```python
async def fetch_data():
    await asyncio.sleep(1)
    return "data"

async def main():
    result = await fetch_data()
    print(result)
```

### 5. 更新版 dict（PEP 468）

保持字典插入順序（Python 3.7+ 正式保證，但 3.6 已在實現中支援）。

### 6. 新聞的字面表達式（Unpacking generalizations）

```python
{*range(4), 4, *(5, 6)}  # {0, 1, 2, 3, 4, 5, 6}
```

## 效能提升

Python 3.6 在以下方面有顯著效能提升：

- dict 的記憶體使用量減少約 20%
- 字串格式化速度提升約 20%
- locals() 訪問速度提升約 25%

## 向下相容性

Python 3.6 與 Python 3.5 高度相容，大部分程式無需修改即可執行。少數已棄用功能在 3.6 中顯示警告。

## 結論

Python 3.6 是一個重要的里程碑，f-string 和型別提示的引入大幅提升了程式碼的可讀性與可維護性。建議所有 Python 開發者盡快遷移到 3.6 或更新版本。