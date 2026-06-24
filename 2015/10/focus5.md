# 軟體架構設計原則

## 高內聚、低耦合與其他核心原則

### 前言

軟體架構是系統的骨幹，決定了系統的長期可維護性和演化能力。良好的架構不是一蹴可幾的，而是在不斷演進中逐漸形成。本期將探討軟體架構的核心設計原則。

### 關注點分離（Separation of Concerns）

關注點分離是軟體架構的核心原則。它主張將系統分割成不同的部分，每個部分各自處理一個關注點。

**例如：一個電子商務系統**

```
┌─────────────────────────────────────────────────────────────────┐
│                      電子商務系統架構                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │   前端展示   │  │   訂單管理   │  │   庫存管理   │            │
│  │  (展示)     │  │  (業務)     │  │  (業務)     │            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │   會員系統   │  │   支付系統   │  │   物流系統   │            │
│  │  (業務)     │  │  (業務)     │  │  (業務)     │            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
│                                                                 │
│  ┌─────────────────────────────────────────────────────┐      │
│  │                      資料庫層                         │      │
│  └─────────────────────────────────────────────────────┘      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

每個模組只關心自己的業務邏輯，模組之間通過定義良好的介面互動。

### 高內聚（High Cohesion）

**內聚**描述了一個模組內部元素（如函數、類別）之間的相關程度。

**高內聚的特點**：
- 模組只包含與其職責相關的程式碼
- 元素之間緊密相關，共同完成一個明確的任務
- 易於理解、維護和測試

**低內聚的壞處**：

```python
# 低內聚：一個類別做太多不相關的事
class UserManager:
    def create_user(self, name, email):
        pass

    def send_email(self, message):  # 不相關
        pass

    def generate_report(self):  # 不相關
        pass

    def backup_database(self):  # 不相關
        pass
```

```python
# 高內聚：每個類別只做一件事
class UserManager:
    def create_user(self, name, email):
        pass

class EmailService:
    def send_email(self, message):
        pass

class ReportGenerator:
    def generate_report(self):
        pass

class DatabaseBackup:
    def backup(self):
        pass
```

### 低耦合（Low Coupling）

**耦合**描述了模組之間的依賴程度。

**低耦合的特點**：
- 模組之間的依賴最小化
- 一個模組的改變不應該影響其他模組
- 模組可以獨立存在和測試

**高耦合的壞處**：

```
┌─────────────────────────────────┐
│         高耦合系統               │
│                                 │
│   A ────> B ────> C ────> D     │
│    │            │               │
│    └─────┬───────┘               │
│          ▼                       │
│          E                       │
│                                 │
│  改變 A 可能影響 B, C, D, E       │
│  測試 A 需要 B, C, D, E           │
└─────────────────────────────────┘
```

```
┌─────────────────────────────────┐
│         低耦合系統               │
│                                 │
│   A      B      C      D        │
│   │      │      │      │        │
│   └──────┴──────┴──────┘        │
│              │                  │
│              ▼                  │
│              E                  │
│                                 │
│  各模組相對獨立                  │
└─────────────────────────────────┘
```

### DRY 原則（Don't Repeat Yourself）

DRY 原則主張：每一個知識片段應該在系統中只有單一、明確的表達。

**違反 DRY**：

```python
def calculate_circle_area(radius):
    return 3.14159 * radius * radius

def calculate_sphere_volume(radius):
    return (4/3) * 3.14159 * radius ** 3
```

**遵循 DRY**：

```python
PI = 3.14159

def calculate_circle_area(radius):
    return PI * radius * radius

def calculate_sphere_volume(radius):
    return (4/3) * PI * radius ** 3
```

**好處**：
- 減少維護成本：改變只需要改一處
- 提高可讀性：重複的程式碼會造成混淆
- 減少 Bug：copy-paste 是 Bug 的溫床

### YAGNI 原則（You Aren't Gonna Need It）

YAGNI 主張：不要為可能需要的功能撰寫程式碼。

**違反 YAGNI**：

```python
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def get_full_name(self):
        return self.name

    # 過度設計：「未來可能需要」
    def get_first_name(self):
        return self.name.split()[0] if self.name else ""

    def get_last_name(self):
        parts = self.name.split() if self.name else []
        return parts[-1] if len(parts) > 1 else ""

    def get_initials(self):
        # ...  更多可能永遠用不到的功能
        pass
```

**YAGNI 做法**：

```python
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def get_full_name(self):
        return self.name
```

等真正需要的時候再添加。

### 封裝（Encapsulation）

封裝是將資料和操作資料的方法包裝在一起，對外隱藏內部實現細節。

**好的封裝**：

```python
class BankAccount:
    def __init__(self, initial_balance=0):
        self.__balance = initial_balance  # 私有屬性

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.__balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self.__balance:
            raise ValueError("Insufficient balance")
        self.__balance -= amount

    def get_balance(self):
        return self.__balance
```

外部程式碼不能直接修改 `__balance`，必須透過定義良好的方法。

### 單一職責原則（SRP）

每個類別應該只有一個改變的原因：

```python
# 違反 SRP
class User:
    def create(self):
        pass

    def authenticate(self):
        pass

    def send_welcome_email(self):
        pass  # 這個職責應該屬於別的地方

    def generate_report(self):
        pass  # 這個職責也應該屬於別的地方
```

```python
# 遵循 SRP
class UserManager:
    def create(self):
        pass

    def authenticate(self):
        pass

class EmailService:
    def send_welcome_email(self):
        pass

class ReportGenerator:
    def generate_user_report(self):
        pass
```

### 開放/封閉原則（OCP）

軟體實體應該對擴展開放，對修改封閉：

```python
# 違反 OCP：新增形狀需要修改函數
def calculate_area(shape):
    if shape.type == "circle":
        return 3.14 * shape.radius ** 2
    elif shape.type == "square":
        return shape.side ** 2
    # 新增三角形需要修改這裡
```

```python
# 遵循 OCP：新增形狀無需修改現有程式碼
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

# 新增 Triangle 只需要建立新類別
class Triangle(Shape):
    def __init__(self, base, height):
        self.base = base
        self.height = height

    def area(self):
        return 0.5 * self.base * self.height
```

### 依賴反轉原則（DIP）

高層模組不應該依賴低層模組，兩者都應該依賴抽象：

```python
# 違反 DIP
class MySQL:
    def query(self, sql):
        pass

class UserService:
    def __init__(self):
        self.db = MySQL()  # 直接依賴具體實作

# 遵循 DIP
class Database(ABC):
    @abstractmethod
    def query(self, sql):
        pass

class MySQL(Database):
    def query(self, sql):
        pass

class UserService:
    def __init__(self, db: Database):  # 依賴抽象
        self.db = db
```

### 架構原則的協同

這些原則並非獨立，它們相互支援：

- **高內聚 + 低耦合**：內聚性高的模組之間自然耦合度低
- **DRY + SRP**：職責單一自然减少重複
- **封裝 + DIP**：封裝隱藏了變動，依賴抽象減少了變動的影響
- **YAGNI + OCP**：不提前猜測需求，但系統設計預留擴展點

### 實踐建議

1. **從小規模開始**：先在類別和函數級別應用這些原則
2. **識別反模式**：當你發現問題，反思是違反了哪個原則
3. **平衡取捨**：沒有絕對的對錯，只有適合當前情境的選擇
4. **重構改善**：現有程式碼可以逐步重構，應用這些原則
5. **團隊共識**：確保團隊對這些原則有共同的理解

### 小結

軟體架構設計原則是經過時間考驗的最佳實踐。理解並應用這些原則可以幫助我們：

- **高內聚**：每個模組職責清晰、易於理解
- **低耦合**：模組獨立、系統靈活
- **DRY**：減少重複、便於維護
- **YAGNI**：專注當下、不過度設計
- **封裝**：隱藏複雜、暴露簡潔
- **依賴反轉**：依賴抽象、降低變動影響

這些原則不是教條，而是指引。在實際應用中，需要根據上下文做出判斷，找到最適合的平衡點。

---

**下一步**：[設計模式分類與應用](focus6.md)

## 延伸閱讀

- [SOLID Principles](https://www.google.com/search?q=SOLID+principles+software+design)
- [Cohesion and Coupling](https://www.google.com/search?q=coupling+cohesion+software+design)
- [DRY Principle](https://www.google.com/search?q=DRY+principle+software+development)
- [YAGNI Principle](https://www.google.com/search?q=YAGNI+principle+extreme+programming)