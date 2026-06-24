# 變數、型別與運算子

## 變數：程式的記憶單元

變數是程式中儲存資料的基本單位。你可以把變數想像成一個帶有標籤的盒子，裡面可以存放各種資料。

### 變數的命名規則

Python 的變數命名需要遵循以下規則：

```python
# 合法的變數名稱
name = "Alice"
age = 25
my_score = 100
student_name_1 = "Bob"

# 不合法的變數名稱
# 2nd_place = "error"    # 不能以數字開頭
# my-name = "error"      # 不能包含連字號
# class = "error"        # 不能使用保留字
```

### 動態型別特性

Python 是動態型別語言，變數不需要事先宣告型別：

```python
x = 10        # x 是整數
print(type(x))  # <class 'int'>

x = "hello"   # x 現在是字串
print(type(x))  # <class 'str'>

x = [1, 2, 3] # x 現在是列表
print(type(x))  # <class 'list'>
```

## 基本資料型別

Python 內建了多種資料型別，最常用的包括：

### 數值型別

```python
# 整數 (int)
a = 42
b = -7
c = 0

# 浮點數 (float)
x = 3.14
y = -0.001
z = 1.5e10  # 科學記號

# 複數 (complex)
c1 = 1 + 2j
c2 = complex(3, 4)
```

### 布林值

```python
is_valid = True
is_finished = False

# 布林值其實是整數的子類別
print(True + True)    # 2
print(False * 10)     # 0
```

### None 型別

```python
result = None  # 表示「沒有值」
```

## 運算子

### 算術運算子

```python
a, b = 10, 3

print(a + b)   # 13  加法
print(a - b)   # 7   減法
print(a * b)   # 30  乘法
print(a / b)   # 3.333...  除法 (結果為浮點數)
print(a // b)  # 3   整數除法
print(a % b)   # 1   取餘數
print(a ** b)  # 1000  次方
```

### 比較運算子

```python
x, y = 5, 10

print(x == y)   # False  等於
print(x != y)   # True   不等於
print(x < y)    # True   小於
print(x > y)    # False  大於
print(x <= y)   # True   小於等於
print(x >= y)   # False  大於等於
```

### 邏輯運算子

```python
a, b = True, False

print(a and b)  # False  且
print(a or b)   # True   或
print(not a)    # False  非

# 短路求值
print(False and print("不會執行"))  # False
print(True or print("不會執行"))    # True
```

### 賦值運算子

```python
x = 10
x += 5   # x = x + 5 → 15
x -= 3   # x = x - 3 → 12
x *= 2   # x = x * 2 → 24
x /= 4   # x = x / 4 → 6.0
x //= 2  # x = x // 2 → 3.0
```

## 型別轉換

Python 提供了內建函式來進行型別轉換：

```python
# 字串轉數字
age = "25"
age_num = int(age) + 1
print(age_num)  # 26

# 數字轉字串
score = 95
message = "你的分數是：" + str(score)

# 浮點數轉整數
pi = 3.14159
print(int(pi))     # 3 (無條件捨去)
print(round(pi))   # 3 (四捨五入)
```

## 小結

變數、型別與運算子是所有程式的基礎。理解這些概念後，你就可以開始編寫真正有意義的程式了。記住：Python 的動態型別讓開發更靈活，但也需要開發者更注意資料的一致性。

---

**延伸閱讀**

- [Python 官方文件 — 資料型別](https://www.google.com/search?q=Python+built-in+types+documentation)
- [Python 運算子優先級](https://www.google.com/search?q=Python+operator+precedence)
