# Python 3.8 walrus 運算子

## 基礎語法

Walrus 運算子 `:=` 是 Python 3.8 引入的賦值運算式，可以在表達式中同時賦值與使用變數。這解決了傳統 Python 需要先賦值、再使用的冗長語法。

```python
# 傳統寫法
n = len(data)
if n > 10:
    print(f"資料筆數：{n}")

# 使用 walrus 運算子
if (n := len(data)) > 10:
    print(f"資料筆數：{n}")
```

## 實用場景

### 1. while 迴圈中的輸入處理

```python
# 傳統寫法：需要先讀取一次
line = input("請輸入：")
while line != "quit":
    print(f"您輸入了：{line}")
    line = input("請輸入：")

# Walrus 運算子
while (line := input("請輸入：")) != "quit":
    print(f"您輸入了：{line}")
```

### 2. 列表推到式中的複用計算

```python
# 假設有個昂貴的計算
data = [1, 2, 3, 4, 5]

# 傳統：需要迴圈或分開處理
squared = [x**2 for x in data]
filtered = [y for y in squared if y > 10]

# Walrus：用於條件判斷中
filtered = [y for x in data if (y := x**2) > 10]
print(filtered)  # [16, 25]
```

### 3. 正規表達式匹配

```python
import re

text = "價格是 1000 元"

# 傳統：需要先匹配，再檢查結果
match = re.search(r"(\d+)", text)
if match:
    price = match.group(1)
    print(f"價格：{price}")

# Walrus
if (match := re.search(r"(\d+)", text)):
    print(f"價格：{match.group(1)}")
```

### 4. f-string 診斷（Python 3.8+）

```python
x = 42

# 傳統
print(f"x={x}")

# Python 3.8+ f-string 診斷
print(f"{x=}")
# 輸出：x=42
```

## 使用限制

### 1. 不能用於匿名赋值

```python
# 錯誤
(x := 1) = 2  # SyntaxError

# 正確
x := 1  # 這會輸出 1（互動式環境中）
```

### 2. 需要括號包圍

```python
# 錯誤
y = x := 10  # SyntaxError

# 正確
y = (x := 10)
```

### 3. 可讀性考量

過度使用 walrus 可能降低程式碼可讀性。建議只在能顯著簡化邏輯時使用。

## 參考資源

- https://www.google.com/search?q=Python+3.8+walrus+operator+:=+tutorial+examples+2020
- https://www.google.com/search?q=Python+assignment+expression+walrus+operator+use+cases
- https://www.google.com/search?q=Python+3.8+new+features+walrus+operator+best+practices