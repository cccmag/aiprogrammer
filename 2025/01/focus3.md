# 流程控制：if/else、for、while

## 什麼是流程控制？

程式預設是從上到下依序執行每一行程式碼。流程控制讓我們能夠改變這個順序，根據條件選擇不同的執行路徑，或重複執行某些程式碼區塊。

## 條件判斷：if/elif/else

條件判斷讓程式能夠根據不同的情況做出不同的反應。

### 基本語法

```python
age = 18

if age >= 18:
    print("你已成年")
else:
    print("你未成年")
```

### if/elif/else 鏈

```python
score = 85

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"

print(f"你的等第是：{grade}")  # B
```

### 巢狀條件

```python
temperature = 25
is_raining = False

if temperature > 20:
    if is_raining:
        print("帶傘出門，天氣溫暖")
    else:
        print("適合出門走走")
else:
    print("記得保暖")
```

### 條件表達式（三元運算子）

```python
x = 10
result = "正數" if x > 0 else "負數或零"
print(result)  # 正數
```

## 迴圈：for

`for` 迴圈用於遍歷可迭代物件（如列表、字串、範圍）。

### 基本用法

```python
# 遍歷列表
fruits = ["蘋果", "香蕉", "橘子"]
for fruit in fruits:
    print(f"我喜歡吃{fruit}")

# 遍歷字串
for char in "Python":
    print(char)  # P, y, t, h, o, n

# 使用 range()
for i in range(5):
    print(i)  # 0, 1, 2, 3, 4

for i in range(2, 10, 3):
    print(i)  # 2, 5, 8
```

### enumerate：同時取得索引與值

```python
names = ["Alice", "Bob", "Charlie"]
for index, name in enumerate(names):
    print(f"{index}: {name}")
# 0: Alice
# 1: Bob
# 2: Charlie
```

### 列表推導式

列表推導式是 Python 中建立列表的簡潔方式：

```python
# 傳統方式
squares = []
for i in range(1, 6):
    squares.append(i ** 2)
print(squares)  # [1, 4, 9, 16, 25]

# 列表推導式
squares = [i ** 2 for i in range(1, 6)]
print(squares)  # [1, 4, 9, 16, 25]

# 加上條件
even_squares = [i ** 2 for i in range(1, 11) if i % 2 == 0]
print(even_squares)  # [4, 16, 36, 64, 100]
```

## 迴圈：while

`while` 迴圈在條件成立時持續執行。

### 基本用法

```python
# 倒數計時
count = 5
while count > 0:
    print(count)
    count -= 1
print("發射！")
```

### 無窮迴圈

```python
# 使用者輸入直到正確為止
while True:
    password = input("請輸入密碼：")
    if password == "python123":
        print("密碼正確！")
        break
    else:
        print("密碼錯誤，請重試")
```

## 跳躍控制

### break：跳出迴圈

```python
for i in range(100):
    if i == 5:
        break
    print(i)  # 0, 1, 2, 3, 4
```

### continue：跳過本次迭代

```python
for i in range(10):
    if i % 2 == 0:
        continue  # 跳過偶數
    print(i)  # 1, 3, 5, 7, 9
```

### else 子句

Python 的迴圈可以附帶 `else` 子句，在迴圈正常結束時執行：

```python
for n in range(2, 10):
    for x in range(2, n):
        if n % x == 0:
            print(f"{n} = {x} * {n//x}")
            break
    else:
        print(f"{n} 是質數")
```

## 實戰範例：猜數字遊戲

```python
import random

target = random.randint(1, 100)
attempts = 0

while True:
    guess = int(input("猜一個數字 (1-100)："))
    attempts += 1

    if guess < target:
        print("太小了！")
    elif guess > target:
        print("太大了！")
    else:
        print(f"恭喜！你猜了 {attempts} 次！")
        break
```

## 小結

流程控制是讓程式變得「聰明」的關鍵。透過條件判斷，程式可以做出決策；透過迴圈，程式可以重複執行任務。掌握這些基礎後，你就能寫出真正有用的程式了。

---

**延伸閱讀**

- [Python 官方文件 — 流程控制](https://www.google.com/search?q=Python+control+flow+documentation)
- [Python 迴圈技巧](https://www.google.com/search?q=Python+loop+techniques)
