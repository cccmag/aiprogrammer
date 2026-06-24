# 流程控制

## 簡介

流程控制決定程式執行的順序。本篇介紹條件判斷和迴圈兩種主要的流程控制結構。

## 條件判斷

### if 語句

```python
age = 18

if age >= 18:
    print("成年人")
```

### if-else

```python
age = 15

if age >= 18:
    print("成年人")
else:
    print("未成年")
```

### if-elif-else

```python
score = 85

if score >= 90:
    print("A")
elif score >= 80:
    print("B")
elif score >= 70:
    print("C")
elif score >= 60:
    print("D")
else:
    print("F")
```

### 巢狀條件

```python
age = 20
has_license = True

if age >= 18:
    if has_license:
        print("可以開車")
    else:
        print("需要考駕照")
else:
    print("年齡不足")
```

### 多條件

```python
age = 25
income = 50000
credit_score = 700

if age >= 20 and income >= 30000 and credit_score >= 600:
    print("符合貸款資格")
```

## 迴圈

### for 迴圈

```python
# 遍歷列表
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)

# 遍歷數字範圍
for i in range(5):  # 0, 1, 2, 3, 4
    print(i)

for i in range(1, 6):  # 1, 2, 3, 4, 5
    print(i)

for i in range(0, 10, 2):  # 0, 2, 4, 6, 8
    print(i)
```

### while 迴圈

```python
count = 0
while count < 5:
    print(count)
    count += 1
```

### 無限迴圈

```python
while True:
    user_input = input("輸入 'quit' 離開: ")
    if user_input == "quit":
        break
```

## 迴圈控制

### break

提早結束迴圈：

```python
for i in range(10):
    if i == 5:
        break  # 當 i=5 時結束迴圈
    print(i)  # 輸出 0, 1, 2, 3, 4
```

### continue

跳過本次迭代：

```python
for i in range(5):
    if i == 2:
        continue  # 跳過 i=2
    print(i)  # 輸出 0, 1, 3, 4
```

### else 子句

迴圈正常結束時執行：

```python
for i in range(3):
    print(i)
else:
    print("迴圈正常結束")

# break 導致 else 不執行
for i in range(3):
    if i == 1:
        break
    print(i)
else:
    print("不會執行這裡")
```

## 巢狀迴圈

```python
for i in range(3):
    for j in range(3):
        print(f"({i}, {j})")
```

### 範例：九九乘法表

```python
for i in range(1, 10):
    for j in range(1, 10):
        print(f"{i} x {j} = {i*j}")
    print()
```

## 列表生成式

```python
# 基本語法
squares = [x**2 for x in range(10)]
print(squares)  # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# 帶條件
even_squares = [x**2 for x in range(10) if x % 2 == 0]
print(even_squares)  # [0, 4, 16, 36, 64]

# 巢狀
matrix = [[i*j for j in range(3)] for i in range(3)]
print(matrix)  # [[0, 0, 0], [0, 1, 2], [0, 2, 4]]
```

## 實用範例

### 找質數

```python
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

for num in range(1, 21):
    if is_prime(num):
        print(num, end=" ")  # 2 3 5 7 11 13 17 19
```

### 費氏數列

```python
n1, n2 = 0, 1
count = 0
while count < 10:
    print(n1, end=" ")
    nth = n1 + n2
    n1 = n2
    n2 = nth
    count += 1
```

### 二分搜尋

```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1

arr = [1, 3, 5, 7, 9, 11, 13, 15]
print(binary_search(arr, 7))   # 3
print(binary_search(arr, 6))  # -1
```

## 練習題

1. 寫一個猜數字遊戲
2. 計算 1+2+...+100
3. 找出列表中的最大和第二大值
4. 判斷一字串是否為迴文