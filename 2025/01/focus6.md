# 列表、字典與資料集合

## 列表 (List)

列表是 Python 中最靈活的資料結構，可以存放任意型別的元素。

### 建立與存取

```python
# 建立列表
empty = []
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, True]

# 索引與切片（與字串相同）
print(numbers[0])      # 1
print(numbers[-1])     # 5
print(numbers[1:4])    # [2, 3, 4]
```

### 常用操作

```python
fruits = ["蘋果", "香蕉", "橘子"]

# 新增元素
fruits.append("葡萄")      # 在末尾添加
fruits.insert(1, "草莓")    # 在指定位置插入
print(fruits)  # ['蘋果', '草莓', '香蕉', '橘子', '葡萄']

# 刪除元素
fruits.remove("香蕉")      # 移除指定元素
popped = fruits.pop()      # 移除並回傳最後一個
del fruits[0]              # 刪除指定位置元素

# 排序與反轉
nums = [3, 1, 4, 1, 5, 9]
nums.sort()               # 原地排序
print(nums)               # [1, 1, 3, 4, 5, 9]
nums.reverse()            # 反轉
print(nums)               # [9, 5, 4, 3, 1, 1]

# 搜尋與計數
print(nums.count(1))      # 2
print(nums.index(5))      # 1
```

### 列表的進階操作

```python
# 列表推導式（再次強調，這是 Python 的精髓）
squares = [x**2 for x in range(10)]
print(squares)  # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# 巢狀列表
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
print(matrix[1][2])  # 6

# 列表複製
original = [1, 2, 3]
shallow = original.copy()  # 淺拷貝
deep = original[:]         # 另一種複製方式
```

## 字典 (Dictionary)

字典是鍵值對（key-value pair）的集合，類似於現實中的字典。

### 建立與存取

```python
# 建立字典
empty = {}
student = {
    "name": "Alice",
    "age": 25,
    "scores": [85, 90, 78]
}

# 存取元素
print(student["name"])      # Alice
print(student.get("grade", "N/A"))  # N/A (安全存取)
```

### 常用操作

```python
person = {"name": "Bob", "age": 30}

# 新增/修改
person["city"] = "台北"     # 新增
person["age"] = 31          # 修改

# 刪除
del person["city"]
removed = person.pop("age")  # 移除並回傳值

# 遍歷
for key, value in person.items():
    print(f"{key}: {value}")

# 取得所有鍵或值
print(person.keys())    # dict_keys(['name'])
print(person.values())  # dict_values(['Bob'])
```

### 字典推導式

```python
# 建立平方表
squares = {x: x**2 for x in range(5)}
print(squares)  # {0: 0, 1: 1, 2: 4, 3: 9, 4: 4}

# 過濾與轉換
original = {"a": 1, "b": 2, "c": 3, "d": 4}
filtered = {k: v for k, v in original.items() if v > 2}
print(filtered)  # {'c': 3, 'd': 4}
```

## 集合 (Set)

集合是無序的不重複元素集合。

```python
# 建立集合
empty = set()  # {} 是空字典
numbers = {1, 2, 3, 2, 1}
print(numbers)  # {1, 2, 3} (重複被移除)

# 從列表建立集合
unique = set([1, 2, 2, 3, 3, 4])
print(unique)  # {1, 2, 3, 4}
```

### 集合運算

```python
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

print(a | b)  # 聯集: {1, 2, 3, 4, 5, 6}
print(a & b)  # 交集: {3, 4}
print(a - b)  # 差集: {1, 2}
print(a ^ b)  # 對稱差: {1, 2, 5, 6}

# 常見用法：去除重複
words = ["apple", "banana", "apple", "cherry", "banana"]
unique_words = list(set(words))
print(unique_words)  # ['cherry', 'apple', 'banana']
```

## 實戰範例：學生成績管理

```python
grades = {
    "Alice": {"math": 85, "english": 92, "science": 78},
    "Bob": {"math": 90, "english": 88, "science": 95},
    "Charlie": {"math": 72, "english": 65, "science": 80}
}

def calculate_averages(grades):
    """計算每位學生的平均成績"""
    averages = {}
    for student, scores in grades.items():
        avg = sum(scores.values()) / len(scores)
        averages[student] = round(avg, 1)
    return averages

averages = calculate_averages(grades)
for student, avg in sorted(averages.items()):
    print(f"{student}: {avg}")

# Alice: 85.0
# Bob: 91.0
# Charlie: 72.3
```

## 小結

列表、字典和集合是 Python 中最常用的三種資料結構。選擇正確的資料結構可以讓程式更簡潔、執行更高效。記住：列表用於有序序列，字典用於鍵值對映射，集合用於不重複元素的運算。

---

**延伸閱讀**

- [Python 官方文件 — 資料結構](https://www.google.com/search?q=Python+data+structures+documentation)
- [Python 列表與字典技巧](https://www.google.com/search?q=Python+list+dictionary+tips)
