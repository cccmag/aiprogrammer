# 魔術方法入門

## 什麼是魔術方法？

魔術方法（Magic Methods）是 Python 中以雙底線開頭和結尾的特殊方法，例如 `__init__`、`__str__`、`__add__`。它們讓你的類別可以與 Python 的內建語法和函式互動。

## 10 個必學魔術方法

### 1. `__init__`：建構子

幾乎每個類別都會用到的方法，在物件建立時自動呼叫：

```python
class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email
```

### 2. `__str__` 與 `__repr__`：字串表示

這兩個方法決定了物件如何被轉換為字串：

```python
class Book:
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year

    def __str__(self):
        """給使用者看：print() 和 str() 使用"""
        return f"《{self.title}》- {self.author}"

    def __repr__(self):
        """給開發者看：除錯和互動式環境使用"""
        return f"Book(title={self.title!r}, author={self.author!r}, year={self.year})"

b = Book("Python 101", "Alice", 2025)
print(str(b))   # 《Python 101》- Alice
print(repr(b))  # Book(title='Python 101', author='Alice', year=2025)
```

### 3. `__len__`：長度

讓你的物件可以使用 `len()` 函式：

```python
class Team:
    def __init__(self, name):
        self.name = name
        self._members = []

    def add(self, member):
        self._members.append(member)

    def __len__(self):
        return len(self._members)

    def __bool__(self):
        return len(self) > 0

team = Team("AI 開發組")
print(bool(team))     # False
team.add("Alice")
team.add("Bob")
print(len(team))      # 2
print(bool(team))     # True
```

### 4. `__getitem__` 與 `__setitem__`：索引存取

讓你的物件可以使用 `obj[key]` 語法：

```python
class SimpleDict:
    def __init__(self):
        self._data = {}

    def __getitem__(self, key):
        return self._data.get(key, None)

    def __setitem__(self, key, value):
        self._data[key] = value

    def __contains__(self, key):
        return key in self._data

d = SimpleDict()
d["name"] = "Alice"
print(d["name"])     # Alice
print("name" in d)   # True
```

### 5. `__call__`：可呼叫物件

讓物件可以像函式一樣被呼叫：

```python
class Counter:
    def __init__(self):
        self.count = 0

    def __call__(self):
        self.count += 1
        return self.count

counter = Counter()
print(counter())  # 1
print(counter())  # 2
print(counter())  # 3
```

### 6. `__add__`、`__sub__`、`__mul__`：算術運算子

```python
class Money:
    def __init__(self, amount, currency="TWD"):
        self.amount = amount
        self.currency = currency

    def __add__(self, other):
        if self.currency != other.currency:
            raise ValueError("貨幣不同無法相加")
        return Money(self.amount + other.amount, self.currency)

    def __sub__(self, other):
        if self.currency != other.currency:
            raise ValueError("貨幣不同無法相減")
        return Money(self.amount - other.amount, self.currency)

    def __mul__(self, factor):
        return Money(self.amount * factor, self.currency)

    def __repr__(self):
        return f"Money({self.amount}, {self.currency})"

m1 = Money(100)
m2 = Money(50)
print(m1 + m2)  # Money(150, TWD)
print(m1 - m2)  # Money(50, TWD)
print(m1 * 3)   # Money(300, TWD)
```

### 7. `__eq__` 與 `__hash__`：相等性與雜湊

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

p1 = Point(1, 2)
p2 = Point(1, 2)
p3 = Point(3, 4)

print(p1 == p2)     # True
print(p1 == p3)     # False
print({p1, p2, p3}) # {Point(3, 4), Point(1, 2)}
```

### 8. `__iter__` 與 `__next__`：迭代器

```python
class Fibonacci:
    def __init__(self, max_count):
        self.max_count = max_count
        self.count = 0
        self.a, self.b = 0, 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.count >= self.max_count:
            raise StopIteration
        self.count += 1
        self.a, self.b = self.b, self.a + self.b
        return self.a

for n in Fibonacci(10):
    print(n, end=" ")  # 1 1 2 3 5 8 13 21 34 55
```

### 9. `__enter__` 與 `__exit__`：上下文管理器

```python
class Timer:
    def __enter__(self):
        import time
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        import time
        elapsed = time.time() - self.start
        print(f"耗時: {elapsed:.4f} 秒")
        return False  # 不處理異常

with Timer():
    sum(range(1000000))
# 耗時: 0.0123 秒
```

### 10. `__bool__`：布林值判斷

```python
class Task:
    def __init__(self, title, completed=False):
        self.title = title
        self.completed = completed

    def __bool__(self):
        return self.completed

t1 = Task("完成報告")
t2 = Task("買牛奶", completed=True)

if t1:
    print("t1 已完成")  # 不會執行
if t2:
    print("t2 已完成")  # t2 已完成
```

## 小結

魔術方法是 Python OOP 的殺手級功能。它們讓自訂類別可以融入 Python 的語言生態，使用起來就像內建類型一樣自然。從 `__init__` 開始，逐步掌握這些方法，你的 Python 程式碼將更加優雅。

## 延伸閱讀

- [Python 資料模型官方文件](https://www.google.com/search?q=Python+data+model+magic+methods)
- [Python 魔術方法大全](https://www.google.com/search?q=Python+magic+methods+cheatsheet)
