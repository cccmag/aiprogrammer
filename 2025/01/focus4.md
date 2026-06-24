# 函數定義與使用

## 為什麼需要函數？

函數（Function）是組織程式碼的基本單元。想像你要寫一個程式來計算圓形面積，如果沒有函數，你會在每個需要計算的地方重複寫同樣的公式：

```python
# 沒有函數 — 重複程式碼
r1 = 5
area1 = 3.14159 * r1 ** 2
print(f"圓形面積：{area1}")

r2 = 10
area2 = 3.14159 * r2 ** 2
print(f"圓形面積：{area2}")
```

有了函數後，你可以將重複的邏輯封裝起來：

```python
# 有函數 — 可重複使用
def circle_area(radius):
    return 3.14159 * radius ** 2

print(f"圓形面積：{circle_area(5)}")
print(f"圓形面積：{circle_area(10)}")
```

## 定義與呼叫函數

### 基本語法

```python
def greet(name):
    """向使用者打招呼的函數"""
    message = f"你好，{name}！"
    return message

# 呼叫函數
result = greet("小明")
print(result)  # 你好，小明！
```

### 函數的組成部分

1. **`def` 關鍵字**：宣告函數定義的開始
2. **函數名稱**：遵循變數命名規則
3. **參數列表**：括號內的輸入參數
4. **docstring**：函數的文件字串（可選）
5. **函數體**：縮排的程式碼區塊
6. **return 語句**：回傳結果（可選）

## 參數傳遞

### 位置參數

參數依照位置順序對應：

```python
def introduce(name, age, city):
    return f"我叫{name}，今年{age}歲，住在{city}"

print(introduce("Alice", 25, "台北"))
```

### 關鍵字參數

```python
print(introduce(city="高雄", name="Bob", age=30))
```

### 預設參數

```python
def power(base, exp=2):
    return base ** exp

print(power(5))     # 25 (5的平方)
print(power(2, 10)) # 1024 (2的10次方)
```

### 可變長度參數

```python
def sum_all(*args):
    """接收任意數量的參數"""
    total = 0
    for num in args:
        total += num
    return total

print(sum_all(1, 2, 3))      # 6
print(sum_all(1, 2, 3, 4, 5))  # 15
```

### 關鍵字可變參數

```python
def print_info(**kwargs):
    """接收任意數量的關鍵字參數"""
    for key, value in kwargs.items():
        print(f"{key}: {value}")

print_info(name="Alice", age=25, city="台北")
# name: Alice
# age: 25
# city: 台北
```

## 回傳值

### 單一回傳值

```python
def add(a, b):
    return a + b
```

### 多個回傳值

```python
def min_max(numbers):
    return min(numbers), max(numbers)

low, high = min_max([3, 7, 1, 9, 4])
print(f"最小值：{low}, 最大值：{high}")
```

### 無回傳值

```python
def show_menu():
    print("1. 新增")
    print("2. 刪除")
    print("3. 結束")

result = show_menu()
print(result)  # None
```

## 變數作用域

### 區域變數 vs 全域變數

```python
x = 10  # 全域變數

def my_func():
    y = 20  # 區域變數
    print(f"函數內部：x = {x}, y = {y}")

my_func()
# print(y)  # 錯誤！y 在函數外部不可見
```

### global 關鍵字

```python
counter = 0

def increment():
    global counter
    counter += 1

increment()
increment()
print(counter)  # 2
```

## 遞迴函數

函數可以呼叫自身，這就是遞迴：

```python
def factorial(n):
    """計算 n 的階乘"""
    if n <= 1:
        return 1
    return n * factorial(n - 1)

print(factorial(5))  # 120

def fibonacci(n):
    """計算費氏數列的第 n 項"""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

for i in range(10):
    print(fibonacci(i), end=" ")  # 0 1 1 2 3 5 8 13 21 34
```

## 小結

函數是程式設計中最重要的抽象工具。透過函數，我們可以將複雜的程式拆解為小型、可管理的單元，提高程式碼的可讀性、可維護性和可重用性。

---

**延伸閱讀**

- [Python 官方文件 — 函數](https://www.google.com/search?q=Python+functions+documentation)
- [Python 遞迴函數教學](https://www.google.com/search?q=Python+recursion+tutorial)
