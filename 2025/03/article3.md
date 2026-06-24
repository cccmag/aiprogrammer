# 實體方法與類別方法

## 三種方法的區別

Python 類別中有三種方法：實體方法、類別方法和靜態方法。它們的主要區別在於第一個參數的意義：

```python
class MethodDemo:
    def instance_method(self):
        """實體方法：可以存取物件的所有屬性"""
        return f"實體方法，self={self}"

    @classmethod
    def class_method(cls):
        """類別方法：可以存取類別屬性和其他類別方法"""
        return f"類別方法，cls={cls}"

    @staticmethod
    def static_method():
        """靜態方法：不可以存取類別或實體，純工具函式"""
        return "靜態方法，沒有特殊參數"
```

## 實體方法（Instance Method）

實體方法是最常見的方法類型。它的第一個參數是 `self`，代表呼叫該方法的物件實體：

```python
class Counter:
    def __init__(self):
        self._count = 0

    def increment(self, amount=1):
        self._count += amount

    def get_count(self):
        return self._count

c = Counter()
c.increment(5)
print(c.get_count())  # 5
```

## 類別方法（Class Method）

類別方法使用 `@classmethod` 裝飾器，第一個參數是 `cls`，代表類別本身。它們常用於替代建構子：

```python
class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    @classmethod
    def from_string(cls, date_str):
        """從 'YYYY-MM-DD' 字串建立 Date 物件"""
        parts = date_str.split("-")
        return cls(int(parts[0]), int(parts[1]), int(parts[2]))

    @classmethod
    def today(cls):
        """建立今天的 Date 物件"""
        from datetime import date
        t = date.today()
        return cls(t.year, t.month, t.day)

    def __repr__(self):
        return f"Date({self.year}, {self.month}, {self.day})"

d1 = Date(2025, 3, 1)
d2 = Date.from_string("2025-03-15")
d3 = Date.today()
print(d1)  # Date(2025, 3, 1)
print(d2)  # Date(2025, 3, 15)
print(d3)  # 今天的日期
```

類別方法的另一個重要用途是追蹤所有建立的實體：

```python
class Employee:
    _all_employees = []

    def __init__(self, name):
        self.name = name
        Employee._all_employees.append(self)

    @classmethod
    def all(cls):
        return list(cls._all_employees)

    @classmethod
    def count(cls):
        return len(cls._all_employees)

emp1 = Employee("Alice")
emp2 = Employee("Bob")
emp3 = Employee("Charlie")
print(Employee.count())  # 3
print([e.name for e in Employee.all()])  # ['Alice', 'Bob', 'Charlie']
```

## 靜態方法（Static Method）

靜態方法使用 `@staticmethod` 裝飾器，沒有 `self` 或 `cls` 參數。它們本質上是放在類別命名空間中的普通函式：

```python
class MathUtils:
    @staticmethod
    def is_even(n):
        return n % 2 == 0

    @staticmethod
    def factorial(n):
        if n <= 1:
            return 1
        return n * MathUtils.factorial(n - 1)

    @staticmethod
    def fibonacci(n):
        a, b = 0, 1
        for _ in range(n):
            a, b = b, a + b
        return a

print(MathUtils.is_even(4))     # True
print(MathUtils.factorial(5))   # 120
print(MathUtils.fibonacci(10))  # 55
```

## 何時使用哪一種？

實體方法是最常見的選擇，當方法需要存取物件的狀態時使用。

類別方法適合：
- 替代建構子（`from_string`、`from_json` 等）
- 存取或修改類別變數
- 實現工廠模式

靜態方法適合：
- 工具函式，與類別相關但不需要存取類別狀態
- 替代全域函式，將相關函式組織在類別命名空間中

```python
class FileHandler:
    def __init__(self, path):
        self.path = path
        self._file = None

    def open(self):
        """實體方法：需要物件狀態"""
        self._file = open(self.path)

    @classmethod
    def from_env(cls, env_var="FILE_PATH"):
        """類別方法：替代建構子"""
        import os
        path = os.environ.get(env_var, "/tmp/default.txt")
        return cls(path)

    @staticmethod
    def is_valid_path(path):
        """靜態方法：純工具函式"""
        import os
        return os.path.exists(path)
```

## 小結

三種方法各有用途：實體方法操作物件狀態，類別方法操作類別狀態，靜態方法組織相關函式。選擇正確的方法類型，可以讓你的類別設計更清晰、更符合語意。

## 延伸閱讀

- [Python @classmethod](https://www.google.com/search?q=Python+classmethod)
- [Python @staticmethod](https://www.google.com/search?q=Python+staticmethod)
