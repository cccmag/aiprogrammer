# SOLID 原則實戰指南

## 前言

SOLID 原則是 Robert C. Martin 提出的五個物件導向設計原則，已成為軟體工程領域的核心理念。本文將透過 Python 範例，深入探討每個原則的實作方式。

## 單一職責原則（SRP）

一個類別應該只有一個改變的原因。

**範例**：

```python
# 違反 SRP
class User:
    def create(self, name, email):
        self.name = name
        self.email = email

    def send_email(self, message):
        print(f"Sending email to {self.email}: {message}")

    def generate_report(self):
        print(f"Generating report for {self.name}")
```

```python
# 遵循 SRP
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

class EmailService:
    def send(self, user, message):
        print(f"Sending email to {user.email}: {message}")

class ReportGenerator:
    def generate(self, user):
        print(f"Generating report for {user.name}")
```

## 開放/封閉原則（OCP）

對擴展開放，對修改封閉。

**範例**：

```python
# 違反 OCP
def calculate_area(shape_type, params):
    if shape_type == "circle":
        return 3.14 * params["radius"] ** 2
    elif shape_type == "rectangle":
        return params["width"] * params["height"]
```

```python
# 遵循 OCP
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14 * self.radius ** 2

def total_area(shapes):
    return sum(shape.area() for shape in shapes)
```

## 里氏替換原則（LSP）

子類別可以在不破壞正確性的前提下替換父類別。

**範例**：

```python
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def set_width(self, width):
        self.width = width

    def set_height(self, height):
        self.height = height

# 如果 Square 繼承 Rectangle，可能破壞預期行為
```

## 介面隔離原則（ISP）

客戶端不應該依賴它不使用的方法。

**範例**：

```python
# 違反 ISP
class IMachine(ABC):
    @abstractmethod
    def print(self): pass

    @abstractmethod
    def scan(self): pass

    @abstractmethod
    def fax(self): pass

# 只有印表機功能的裝置被迫實作 scan 和 fax
```

```python
# 遵循 ISP
class Printer(ABC):
    @abstractmethod
    def print(self): pass

class Scanner(ABC):
    @abstractmethod
    def scan(self): pass

class AllInOneMachine(Printer, Scanner):
    def print(self): pass
    def scan(self): pass
```

## 依賴反轉原則（DIP）

高層模組不應該依賴低層模組，兩者都應該依賴抽象。

**範例**：

```python
# 違反 DIP
class MySQLDatabase:
    def query(self, sql): pass

class UserService:
    def __init__(self):
        self.db = MySQLDatabase()
```

```python
# 遵循 DIP
class Database(ABC):
    @abstractmethod
    def query(self, sql): pass

class MySQLDatabase(Database):
    def query(self, sql): pass

class UserService:
    def __init__(self, db: Database):
        self.db = db
```

## 小結

SOLID 原則幫助我們設計更好的系統。實際應用時，需要根據上下文做出判斷，而不是機械地遵循。

---

## 延伸閱讀

- [SOLID Principles with Python Examples](https://www.google.com/search?q=SOLID+principles+python+examples)
- [Uncle Bob's SOLID Principles](https://www.google.com/search?q=Robert+Martin+SOLID+principles)