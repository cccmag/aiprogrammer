# SOLID 原則詳解

## 物件導向設計的五大原則

### 前言

SOLID 原則是由 Robert C. Martin 在 2000 年代初提出的一系列設計原則。這五個原則幫助開發者創建更易於維護、擴展和理解的軟體系統。讓我們逐一深入探討。

### 1. 單一職責原則（SRP）

**定義**：一個類別應該只有一個改變的原因。

**核心概念**：

每個類別應該只負責一件事。如果一個類別承擔了多個職責，那麼當需求變更時，這個類別可能會因為不同原因而需要修改。這會增加程式碼的脆弱性。

**違反範例**：

```python
class UserManager:
    def create_user(self, name, email):
        # 建立使用者
        pass

    def send_email(self, user, message):
        # 傳送電子郵件
        pass

    def generate_report(self):
        # 產生報表
        pass

    def connect_database(self):
        # 連線資料庫
        pass
```

這個 `UserManager` 违反了 SRP，因為它同時處理：
- 使用者管理
- 電子郵件傳送
- 報表生成
- 資料庫連線

**正確範例**：

```python
class UserManager:
    def create_user(self, name, email):
        pass

class EmailService:
    def send_email(self, user, message):
        pass

class ReportGenerator:
    def generate_report(self):
        pass

class DatabaseConnection:
    def connect(self):
        pass
```

每個類別只有一個職責，未來的需求變更只會影響相關的類別。

### 2. 開放/封閉原則（OCP）

**定義**：軟體實體應該對擴展開放，對修改封閉。

**核心概念**：

設計良好的模組應該可以在不改變現有程式碼的情況下擴展新功能。這通常通過介面、抽象類別和多型來實現。

**違反範例**：

```python
class Shape:
    def draw_circle(self):
        pass

    def draw_square(self):
        pass

def draw_all_shapes(shapes):
    for shape in shapes:
        if shape.type == "circle":
            shape.draw_circle()
        elif shape.type == "square":
            shape.draw_square()
```

每當新增形狀時，都需要修改 `draw_all_shapes` 函數。

**正確範例**：

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def draw(self):
        pass

class Circle(Shape):
    def draw(self):
        print("Drawing a circle")

class Square(Shape):
    def draw(self):
        print("Drawing a square")

def draw_all_shapes(shapes):
    for shape in shapes:
        shape.draw()  # 不需要修改這個函數就能支援新形狀
```

新增形狀時，只需建立新的子類別，無需修改現有程式碼。

### 3. 里氏替換原則（LSP）

**定義**：子類別物件應該可以在不改變程式正確性的前提下替換父類別物件。

**核心概念**：

這個原則要求子類別必須遵守父類別的契約。如果子類別改變了父類別的行為，可能會導致意料之外的錯誤。

**違反範例**：

```python
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def set_width(self, width):
        self.width = width

    def set_height(self, height):
        self.height = height

    def area(self):
        return self.width * self.height

class Square(Rectangle):
    def set_width(self, width):
        self.width = width
        self.height = width  # 正方形的寬高必須相同

    def set_height(self, height):
        self.width = height
        self.height = height
```

```python
def increase_width(rectangle, amount):
    original_height = rectangle.height  # 假設 width 和 height 是獨立的
    rectangle.set_width(rectangle.width + amount)
    assert rectangle.height == original_height  # 這會對正方形失敗！
```

**正確做法**：

確保子類別遵守父類別的所有契約，或者使用更抽象的類別層級設計。

### 4. 介面隔離原則（ISP）

**定義**：客戶端不應該依賴它不使用的介面。

**核心概念**：

大型、笨重的介面應該被分解成更小、更具體的介面。類別只需要知道它們需要的方法。

**違反範例**：

```python
class Machine(ABC):
    @abstractmethod
    def print(self, document):
        pass

    @abstractmethod
    def scan(self, document):
        pass

    @abstractmethod
    def fax(self, document):
        pass

class AllInOnePrinter(Machine):
    def print(self, document):
        pass

    def scan(self, document):
        pass

    def fax(self, document):
        pass

class SimplePrinter(Machine):
    def print(self, document):
        pass

    def scan(self, document):
        raise NotImplementedError("Simple printer cannot scan")

    def fax(self, document):
        raise NotImplementedError("Simple printer cannot fax")
```

`SimplePrinter` 被迫實作它不需要的方法。

**正確範例**：

```python
class Printer(ABC):
    @abstractmethod
    def print(self, document):
        pass

class Scanner(ABC):
    @abstractmethod
    def scan(self, document):
        pass

class Fax(ABC):
    @abstractmethod
    def fax(self, document):
        pass

class AllInOnePrinter(Printer, Scanner, Fax):
    def print(self, document):
        pass

    def scan(self, document):
        pass

    def fax(self, document):
        pass

class SimplePrinter(Printer):
    def print(self, document):
        pass
```

每個類別只實作它需要的介面。

### 5. 依賴反轉原則（DIP）

**定義**：高層模組不應該依賴低層模組。兩者都應該依賴抽象。

**核心概念**：

依賴應該指向抽象，而不是具體實作。這減少了模組之間的耦合度。

**違反範例**：

```python
class MySQLDatabase:
    def connect(self):
        pass

    def query(self, sql):
        pass

class UserService:
    def __init__(self):
        self.database = MySQLDatabase()  # 直接依賴具體實作

    def get_user(self, user_id):
        self.database.connect()
        return self.database.query(f"SELECT * FROM users WHERE id = {user_id}")
```

如果未來要更換資料庫，需要修改 `UserService`。

**正確範例**：

```python
from abc import ABC, abstractmethod

class Database(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def query(self, sql):
        pass

class MySQLDatabase(Database):
    def connect(self):
        pass

    def query(self, sql):
        pass

class UserService:
    def __init__(self, database: Database):  # 依賴抽象
        self.database = database

    def get_user(self, user_id):
        self.database.connect()
        return self.database.query(f"SELECT * FROM users WHERE id = {user_id}")
```

現在切換資料庫只需要傳入不同的實作，不需要修改 `UserService`。

### SOLID 原則的協同效應

SOLID 原則不是獨立運作的，它們相互增強：

- **SRP + ISP**：都強調小而專一的程式碼單元
- **OCP + LSP + DIP**：共同實現可擴展且穩定的設計
- **DIP + SRP**：依賴抽象幫助分離職責

### 實踐建議

1. **從小處開始**：不需要一開始就完美的設計，但在每次修改時思考是否符合 SOLID 原則
2. **識別壞味道**：當你發現修改一個類別很困難、或是修改影響範圍太大時，可能違反了某個原則
3. **重構而非重新設計**：在現有程式碼上應用 SOLID 原則，通過重構逐步改善
4. **平衡與判斷**：SOLID 是指南，不是法律。有時偏離原則是合理的工程決策

### 小結

SOLID 原則提供了判斷軟體設計優劣的框架。遵循這些原則可以幫助我們創建更易於維護、擴展和理解的系統。但這些原則不是絕對的真理，它們是幫助我們做出更好設計決策的工具。

---

**下一步**：[MVC 架構模式](focus2.md)

## 延伸閱讀

- [SOLID Principles in Python](https://www.google.com/search?q=SOLID+principles+python+implementation)
- [Uncle Bob SOLID articles](https://www.google.com/search?q=Robert+Martin+SOLID+principles)
- [Design Principles from GoF](https://www.google.com/search?q=Design+Patterns+Gang+of+Four+principles)