# 列表與迴圈的藝術

## 列表進階操作

### 列表的高階方法

```python
numbers = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]

# 排序
print(sorted(numbers))          # [1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9]
print(sorted(numbers, reverse=True))  # [9, 6, 5, 5, 5, 4, 3, 3, 2, 1, 1]

# 自訂排序
words = ["banana", "apple", "cherry", "date"]
print(sorted(words, key=len))   # ['date', 'apple', 'banana', 'cherry']
print(sorted(words, key=lambda w: w[-1]))  # 依最後一個字母排序

# filter
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(evens)  # [4, 2, 6]

# map
doubled = list(map(lambda x: x * 2, numbers))
print(doubled[:5])  # [6, 2, 8, 2, 10]

# zip
names = ["Alice", "Bob", "Charlie"]
scores = [85, 92, 78]
pairs = list(zip(names, scores))
print(pairs)  # [('Alice', 85), ('Bob', 92), ('Charlie', 78)]
```

## 列表推導式進階

### 巢狀列表推導式

```python
# 扁平化巢狀列表
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [num for row in matrix for num in row]
print(flat)  # [1, 2, 3, 4, 5, 6, 7, 8, 9]

# 轉置矩陣
transposed = [[row[i] for row in matrix] for i in range(3)]
print(transposed)  # [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
```

### 字典推導式

```python
# 字頻統計
text = "hello world"
freq = {char: text.count(char) for char in set(text) if char != ' '}
print(freq)  # {'d': 1, 'e': 1, 'h': 1, 'l': 3, 'o': 2, 'r': 1, 'w': 1}
```

## 迭代器與生成器

### 迭代器

```python
class Counter:
    """自訂迭代器"""
    def __init__(self, limit):
        self.limit = limit
        self.count = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.count < self.limit:
            self.count += 1
            return self.count
        raise StopIteration

for num in Counter(5):
    print(num, end=" ")  # 1 2 3 4 5
```

### 生成器

```python
def fibonacci(limit):
    """費氏數列生成器"""
    a, b = 0, 1
    for _ in range(limit):
        yield a
        a, b = b, a + b

for num in fibonacci(10):
    print(num, end=" ")  # 0 1 1 2 3 5 8 13 21 34

# 生成器表達式
squares = (x**2 for x in range(10))
print(list(squares))  # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
```

## enumerate 與 zip 的進階用法

```python
items = ["蘋果", "香蕉", "橘子"]
prices = [30, 25, 45]
quantities = [3, 2, 1]

# 同時遍歷多個列表
for i, (item, price, qty) in enumerate(zip(items, prices, quantities)):
    total = price * qty
    print(f"{i+1}. {item}: ${price} × {qty} = ${total}")

# 1. 蘋果: $30 × 3 = $90
# 2. 香蕉: $25 × 2 = $50
# 3. 橘子: $45 × 1 = $45
```

## itertools：強大的迭代工具

```python
from itertools import chain, cycle, permutations, combinations

# chain：串接多個可迭代物件
list1 = [1, 2, 3]
list2 = ['a', 'b', 'c']
combined = list(chain(list1, list2))
print(combined)  # [1, 2, 3, 'a', 'b', 'c']

# permutations：排列
items = ['A', 'B', 'C']
perms = list(permutations(items, 2))
print(perms)  # [('A','B'), ('A','C'), ('B','A'), ('B','C'), ('C','A'), ('C','B')]

# combinations：組合
combs = list(combinations(items, 2))
print(combs)  # [('A','B'), ('A','C'), ('B','C')]
```

## 實戰：購物車系統

```python
class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_item(self, name, price, quantity=1):
        self.items.append({"name": name, "price": price, "qty": quantity})

    def remove_item(self, name):
        self.items = [item for item in self.items if item["name"] != name]

    def total(self):
        return sum(item["price"] * item["qty"] for item in self.items)

    def summary(self):
        if not self.items:
            return "購物車是空的"

        result = []
        for i, item in enumerate(self.items, 1):
            subtotal = item["price"] * item["qty"]
            result.append(f"{i}. {item['name']} (${item['price']}) × {item['qty']} = ${subtotal}")
        result.append(f"---\n總計：${self.total()}")
        return "\n".join(result)

cart = ShoppingCart()
cart.add_item("蘋果", 30, 3)
cart.add_item("牛奶", 95, 2)
cart.add_item("麵包", 45, 1)
print(cart.summary())
```

## 小結

列表與迴圈的結合是 Python 中最強大的程式設計模式之一。掌握列表推導式、生成器、以及 itertools 等工具，可以讓你用更少的程式碼完成更多的工作，同時保持程式碼的可讀性。

---

**延伸閱讀**

- [Python itertools 模組](https://www.google.com/search?q=Python+itertools+tutorial)
- [Python 生成器教學](https://www.google.com/search?q=Python+generators+tutorial)
