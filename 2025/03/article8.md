# 抽象基底類別

## 什麼是抽象基底類別？

抽象基底類別（Abstract Base Class, ABC）是一種不能直接實體化的類別，它的目的是定義子類別必須實作的方法。你可以把它想像成一份合約——繼承 ABC 的子類別必須履行合約中的所有條款。

## 為什麼需要 ABC？

### 情境：繪圖系統

假設你在設計一個繪圖系統，所有形狀都應該有 `area()` 和 `draw()` 方法。沒有 ABC 時，你可能會這樣寫：

```python
class Shape:
    def area(self):
        raise NotImplementedError

    def draw(self):
        raise NotImplementedError
```

但這個設計有兩個問題：
1. 你可以直接建立 `Shape()` 實體，但呼叫方法會噴錯
2. 子類別可能忘記實作某些方法，直到執行時才會發現

使用 ABC 解決這兩個問題：

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        pass

    @abstractmethod
    def draw(self) -> str:
        pass

# s = Shape()  # TypeError! 無法實體化抽象類別

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14159 * self.radius ** 2

    def draw(self):
        return f"繪製半徑 {self.radius} 的圓形"

class Triangle(Shape):
    def __init__(self, base, height):
        self.base = base
        self.height = height

    def area(self):
        return 0.5 * self.base * self.height

    def draw(self):
        return f"繪製底 {self.base} 高 {self.height} 的三角形"
```

## 抽象屬性

抽象類別也可以定義抽象屬性：

```python
from abc import ABC, abstractmethod

class Report(ABC):
    @property
    @abstractmethod
    def title(self) -> str:
        pass

    @property
    @abstractmethod
    def content(self) -> str:
        pass

    def display(self) -> None:
        print(f"=== {self.title} ===")
        print(self.content)

class SalesReport(Report):
    @property
    def title(self):
        return "銷售報告"

    @property
    def content(self):
        return "本月銷售額: $100,000"

class PerformanceReport(Report):
    @property
    def title(self):
        return "績效報告"

    @property
    def content(self):
        return "整體績效: A級"

report = SalesReport()
report.display()
# === 銷售報告 ===
# 本月銷售額: $100,000
```

## ABC 的進階用法

### 註冊虛擬子類別

你可以將不繼承 ABC 的類別註冊為虛擬子類別：

```python
from abc import ABC

class IterableMixin(ABC):
    @classmethod
    def __subclasshook__(cls, subclass):
        if cls is IterableMixin:
            if any("__iter__" in B.__dict__ for B in subclass.__mro__):
                return True
        return NotImplemented

class MyList:
    def __iter__(self):
        return iter([1, 2, 3])

print(isinstance(MyList(), IterableMixin))  # True
print(issubclass(MyList, IterableMixin))    # True
```

### 混合抽象與具體方法

ABC 可以同時包含抽象方法和具體方法：

```python
from abc import ABC, abstractmethod
from datetime import datetime

class Logger(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def write(self, message: str) -> None:
        pass

    def info(self, message: str) -> None:
        self._log("INFO", message)

    def error(self, message: str) -> None:
        self._log("ERROR", message)

    def _log(self, level: str, message: str) -> None:
        timestamp = datetime.now().isoformat()
        formatted = f"[{timestamp}] [{level}] {message}"
        self.write(formatted)

class FileLogger(Logger):
    def __init__(self, name, filepath):
        super().__init__(name)
        self.filepath = filepath

    def write(self, message):
        with open(self.filepath, "a") as f:
            f.write(message + "\n")

class ConsoleLogger(Logger):
    def write(self, message):
        print(message)

logger = ConsoleLogger("main")
logger.info("程式啟動")
logger.error("發生錯誤")
# [2025-03-01T10:00:00] [INFO] 程式啟動
# [2025-03-01T10:00:00] [ERROR] 發生錯誤
```

## ABC vs Protocol：如何選擇？

| 場景 | 選擇 |
|------|------|
| 需要正式繼承層次 | ABC |
| 需要預設實作 | ABC |
| 需要 isinstance 檢查 | ABC |
| 關注結構而非繼承 | Protocol |
| 需要最大彈性 | Protocol |

```python
from abc import ABC, abstractmethod
from typing import Protocol

# 正式繼承：用 ABC
class JSONSerializable(ABC):
    @abstractmethod
    def to_json(self) -> dict:
        pass

class User(JSONSerializable):
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def to_json(self):
        return {"name": self.name, "email": self.email}

# 結構子型別：用 Protocol
class Drawable(Protocol):
    def draw(self) -> str:
        ...

class Circle:
    def draw(self):
        return "○"

class Square:
    def draw(self):
        return "□"
```

## 小結

抽象基底類別是 Python OOP 中用於定義「合約」的正式工具。它確保子類別實作了必要的方法，並在編譯期（或匯入期）就能發現遺漏。對於大型專案或框架設計，ABC 是不可或缺的。

## 延伸閱讀

- [Python abc 官方文件](https://www.google.com/search?q=Python+abc+module)
- [ABC vs Protocol](https://www.google.com/search?q=Python+ABC+vs+Protocol)
