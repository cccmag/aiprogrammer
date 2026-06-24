# 運算子與表達式

## 簡介

運算子是指定如何處理資料的符號，而表達式是由值、變數和運算子組成的語句。

## 算術運算子

```python
a, b = 10, 3

print(f"{a} + {b} = {a + b}")   # 加法：13
print(f"{a} - {b} = {a - b}")   # 減法：7
print(f"{a} * {b} = {a * b}")   # 乘法：30
print(f"{a} / {b} = {a / b}")   # 除法：3.333...
print(f"{a} // {b} = {a // b}") # 整數除法：3
print(f"{a} % {b} = {a % b}")   # 餘數：1
print(f"{a} ** {b} = {a ** b}") # 次方：1000
```

### 運算子優先順序

```python
# 優先順序（從高到低）
# 1. ()     - 括號
# 2. **     - 次方
# 3. * / // % - 乘除取餘
# 4. + -    - 加減

result = 2 + 3 * 4      # 14 (不是 20)
result = (2 + 3) * 4    # 20
result = 2 ** 3 ** 2    # 512 (右到左)
```

## 比較運算子

```python
a, b = 5, 10

print(f"{a} == {b}: {a == b}")   # 等於：False
print(f"{a} != {b}: {a != b}")   # 不等於：True
print(f"{a} > {b}: {a > b}")    # 大於：False
print(f"{a} < {b}: {a < b}")    # 小於：True
print(f"{a} >= {b}: {a >= b}")  # 大於等於：False
print(f"{a} <= {b}: {a <= b}")  # 小於等於：True
```

### 鏈式比較

```python
x = 5

# Python 允許鏈式比較
print(1 < x < 10)       # True
print(1 < x < 3)        # False
print(x > 0 and x < 10) # True（等價）
```

## 邏輯運算子

```python
x, y = True, False

print(f"x and y: {x and y}")  # False
print(f"x or y: {x or y}")    # True
print(f"not x: {not x}")      # False
```

### 短路運算

```python
# and 的短路
a = False
result = a and some_function()  # some_function 不會被執行

# or 的短路
b = True
result = b or some_function()  # some_function 不會被執行
```

### 邏輯運算優先順序

```python
# not > and > or
print(not True or True and False)  # 等同於 (not True) or (True and False)
```

## 賦值運算子

```python
x = 10

x += 5     # x = x + 5
print(x)   # 15

x -= 3     # x = x - 3
print(x)   # 12

x *= 2     # x = x * 2
print(x)   # 24

x //= 5    # x = x // 5
print(x)   # 4

x **= 2    # x = x ** 2
print(x)   # 16
```

## 位元運算子

```python
a, b = 0b1100, 0b1010  # 12, 10

print(f"a & b = {bin(a & b)}")   # AND: 0b1000 (8)
print(f"a | b = {bin(a | b)}")   # OR: 0b1110 (14)
print(f"a ^ b = {bin(a ^ b)}")   # XOR: 0b0110 (6)
print(f"~a = {bin(~a)}")        # NOT: -0b1101
print(f"a << 2 = {bin(a << 2)}")  # 左移：0b110000 (48)
print(f"a >> 2 = {bin(a >> 2)}")  # 右移：0b11 (3)
```

## 成員運算子

```python
fruits = ["apple", "banana", "cherry"]

print("apple" in fruits)       # True
print("orange" in fruits)      # False
print("orange" not in fruits) # True

# 字串
text = "Hello, World!"
print("Hello" in text)         # True
print("hello" in text)         # False（大小寫敏感）
```

## 身份運算子

```python
a = [1, 2, 3]
b = a
c = [1, 2, 3]

print(a is b)     # True（同一物件）
print(a is c)     # False（不同物件，內容相同）
print(a == c)     # True（內容相同）

# 小整數快取
x = 256
y = 256
print(x is y)     # True（小整數在 Python 中會被快取）
```

## 表達式

### 基本表達式

```python
# 算術表達式
area = 3.14 * 5 ** 2

# 比較表達式
is_adult = age >= 18

# 邏輯表達式
can_vote = age >= 18 and is_citizen
```

### 條件表達式（三元運算子）

```python
age = 20

# 語法：value_if_true if condition else value_if_false
status = "成年人" if age >= 18 else "未成年人"
print(status)  # 成年人
```

## 運算子優先順序表

| 優先順序 | 運算子 | 說明 |
|---------|--------|------|
| 1 | () | 括號 |
| 2 | ** | 次方 |
| 3 | +x, -x, ~x | 正負號、位元 NOT |
| 4 | *, /, //, % | 乘除 |
| 5 | +, - | 加減 |
| 6 | <<, >> | 位元位移 |
| 7 | & | 位元 AND |
| 8 | ^ | 位元 XOR |
| 9 | \| | 位元 OR |
| 10 | ==, !=, >, <, >=, <=, is, in | 比較 |
| 11 | not | 邏輯 NOT |
| 12 | and | 邏輯 AND |
| 13 | or | 邏輯 OR |

## 練習題

1. 計算 2 的 10 次方
2. 判斷一個年份是否為閏年（能被 4 整除但不能被 100 整除，或能被 400 整除）
3. 交換兩個變數的值（不使用第三個變數）
4. 計算 BMI（體重/身高²）並判斷是否過輕/正常/過重