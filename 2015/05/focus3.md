# 主題三：語法基礎與資料型態

## Python 基本語法

### 縮排與語法結構

Python 使用縮排來定義程式碼區塊，這是 Python 與其他語言最顯著的區別：

```python
if x > 0:
    print("x 是正數")
    if x > 10:
        print("x 大於 10")
else:
    print("x 是非正數")
```

### 註釋

```python
# 單行註釋

"""
多行字串常被用作多行註釋
這不會影響程式執行
"""

'''
也可以使用單引號
'''
```

## 變數與資料型態

### 基本資料型態

```python
# 數值
age = 25           # int（整數）
price = 19.99      # float（浮點數）
is_valid = True    # bool（布林值）

# 字串
name = "張小明"
message = '你好'

# None（空值）
result = None
```

### 動態型態

Python 是動態型態語言，變數型態在執行時決定：

```python
x = 10       # int
x = "hello"  # 現在是 str
print(x)     # hello
```

## 運算子

### 算術運算子

```python
a, b = 10, 3

print(a + b)   # 13 加
print(a - b)   # 7  減
print(a * b)   # 30 乘
print(a / b)   # 3.333... 除
print(a // b)  # 3  整除
print(a % b)   # 1  取餘
print(a ** b)  # 1000 次方
```

### 比較運算子

```python
print(5 == 5)    # True  等於
print(5 != 3)    # True  不等於
print(5 > 3)     # True  大於
print(5 < 3)     # False 小於
print(5 >= 5)    # True  大於等於
print(5 <= 3)    # False 小於等於
```

### 邏輯運算子

```python
x, y = True, False

print(x and y)   # False
print(x or y)    # True
print(not x)     # False
```

### 位元運算子

```python
a, b = 5, 3  # 5 = 0101, 3 = 0011

print(a & b)   # 1  (0001) AND
print(a | b)   # 7  (0111) OR
print(a ^ b)   # 6  (0110) XOR
print(~a)      # -6 反碼
print(a << 1)  # 10 (1010) 左移
print(a >> 1)  # 2  (0010) 右移
```

## 控制流程

### if 陳述

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

print(f"成績等级：{grade}")  # B
```

### for 迴圈

```python
# 遍歷列表
fruits = ["蘋果", "香蕉", "橘子"]
for fruit in fruits:
    print(fruit)

# 使用 range
for i in range(5):
    print(i)  # 0, 1, 2, 3, 4

# enumerate：同時取得索引和值
for index, fruit in enumerate(fruits):
    print(f"{index}: {fruit}")
```

### while 迴圈

```python
count = 0
while count < 5:
    print(count)
    count += 1
```

### 迴圈控制

```python
# break：提前結束迴圈
for i in range(10):
    if i == 5:
        break
    print(i)  # 0, 1, 2, 3, 4

# continue：跳過本次迭代
for i in range(5):
    if i == 2:
        continue
    print(i)  # 0, 1, 3, 4

# else：迴圈正常結束時執行
for i in range(3):
    print(i)
else:
    print("迴圈正常結束")
```

## 資料結構

### List（列表）

```python
# 列表是可變的有序序列
numbers = [1, 2, 3, 4, 5]
numbers.append(6)      # 新增
numbers.insert(0, 0)   # 插入
numbers.pop()          # 移除最後一個
numbers.remove(3)      # 移除第一個 3
print(numbers[0])      # 取得元素
print(numbers[1:3])    # 切片
print(len(numbers))    # 長度
```

### Tuple（元組）

```python
# 元組是不可變的有序序列
point = (10, 20)
x, y = point  # 解包

# 單元素元組需要逗號
single = (42,)  # 不是 (42)
```

### Dict（字典）

```python
# 鍵值對
person = {
    "name": "張小明",
    "age": 28,
    "city": "台北"
}

print(person["name"])           # 讀取
person["email"] = "zhang@example.com"  # 新增
del person["city"]              # 刪除
print(person.get("age", 0))     # 安全讀取

# 遍歷
for key, value in person.items():
    print(f"{key}: {value}")
```

### Set（集合）

```python
# 無序、不重複
colors = {"紅", "綠", "藍"}
colors.add("黃")      # 新增
colors.remove("紅")   # 移除（不存在會錯誤）
colors.discard("黑")  # 移除（不存在不錯誤）

# 集合運算
a = {1, 2, 3}
b = {2, 3, 4}
print(a & b)  # {2, 3} 交集
print(a | b)  # {1, 2, 3, 4} 聯集
print(a - b)  # {1} 差集
print(a ^ b)  # {1, 4} 對稱差集
```

## 字串處理

```python
s = "Hello, World!"

# 基本操作
print(s.upper())           # HELLO, WORLD!
print(s.lower())           # hello, world!
print(s.split(","))        # ['Hello', ' World!']
print(s.replace("World", "Python"))
print(s.strip())          # 去除空白
print(s.startswith("Hello"))  # True
print("World" in s)       # True

# 格式化
name = "張小明"
age = 28
print(f"{name} 是 {age} 歲")  # f-string（Python 3.6+）
print("{} 是 {} 歲".format(name, age))
print("%s 是 %d 歲" % (name, age))
```

## 類型轉換

```python
# 顯式類型轉換
int("42")      # "42" -> 42
float("3.14")  # "3.14" -> 3.14
str(42)        # 42 -> "42"
bool(1)        # True
list("abc")    # ['a', 'b', 'c']
```

## 運算子優先順序

```
()           # 括號
**           # 指數
+ , -        # 正負號
* , / , // , %  # 乘除
+ , -        # 加減
== , != , > , < , >= , <=  # 比較
not          # 邏輯非
and          # 邏輯且
or           # 邏輯或
```