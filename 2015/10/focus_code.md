# SOLID 原則與設計模式範例

## 概述

本程式展示 SOLID 原則的 Python 實現以及常見的設計模式。透過實際程式碼，你將看到如何將抽象的設計原則應用到實際開發中。

## 專案結構

```
_code/
├── solid_principles.py    # SOLID 原則範例
├── design_patterns.py     # 設計模式範例
└── test.sh                # 測試執行腳本
```

## SOLID 原則範例

### 1. 單一職責原則（SRP）

```python
# 違反 SRP：類別承擔多個職責
class UserManager:
    def create_user(self, name, email):
        pass

    def send_email(self, message):
        pass

    def generate_report(self):
        pass

# 遵循 SRP：每個類別只負責一件事
class UserManager:
    def create_user(self, name, email):
        pass

class EmailService:
    def send_email(self, message):
        pass

class ReportGenerator:
    def generate_report(self):
        pass
```

### 2. 開放/封閉原則（OCP）

```python
# 違反 OCP：新增類型需要修改函數
def calculate_area(shape_type, params):
    if shape_type == "circle":
        return 3.14 * params["radius"] ** 2

# 遵循 OCP：對擴展開放
class Shape(ABC):
    @abstractmethod
    def area(self):
        pass
```

### 3. 依賴反轉原則（DIP）

```python
# 違反 DIP：直接依賴具體類別
class MySQLDatabase:
    def query(self): pass

class UserService:
    def __init__(self):
        self.db = MySQLDatabase()

# 遵循 DIP：依賴抽象
class Database(ABC):
    @abstractmethod
    def query(self): pass

class UserService:
    def __init__(self, db: Database):
        self.db = db
```

## 設計模式範例

### 觀察者模式

```python
class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def notify(self, data):
        for observer in self._observers:
            observer.update(data)
```

### 工廠模式

```python
class Factory(ABC):
    @abstractmethod
    def create(self):
        pass

class ConcreteFactory(Factory):
    def create(self):
        return Product()
```

### 策略模式

```python
class Strategy(ABC):
    @abstractmethod
    def execute(self, data):
        pass

class Context:
    def __init__(self, strategy):
        self.strategy = strategy

    def run(self, data):
        return self.strategy.execute(data)
```

## 執行方式

```bash
cd _code
python3 solid_principles.py
python3 design_patterns.py
./test.sh
```

## 延伸挑戰

1. 為 SRP 範例添加實際的資料庫操作
2. 實現完整的觀察者模式，支援取消訂閱
3. 實現一個簡單的策略工廠，根據配置選擇策略

---

## 延伸閱讀

- [完整程式碼](_code/solid_principles.py)
- [設計模式完整程式碼](_code/design_patterns.py)
- [SOLID Principles Guide](https://www.google.com/search?q=SOLID+principles+python+tutorial)