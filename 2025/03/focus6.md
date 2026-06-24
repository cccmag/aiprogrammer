# 抽象類別與介面

## 為什麼需要抽象？

當你設計一個系統時，常常需要定義一組「必須實作的方法」，但實作細節留給子類別決定。例如「所有動物都必須會叫，但每種動物叫聲不同」。抽象類別正是為此而生。

抽象類別無法被直接實體化——它只是一個合約，要求子類別實作特定的方法。

## Python 的 abc 模組

Python 的 `abc`（Abstract Base Classes）模組提供了定義抽象類別的正式機制：

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        pass

    @abstractmethod
    def perimeter(self) -> float:
        pass

    def describe(self) -> str:
        return f"面積: {self.area()}, 周長: {self.perimeter()}"
```

任何繼承 `Shape` 的類別都必須實作 `area()` 和 `perimeter()`：

```python
class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14159 * self.radius ** 2

    def perimeter(self):
        return 2 * 3.14159 * self.radius

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

shapes = [Circle(5), Rectangle(3, 4)]
for s in shapes:
    print(s.describe())
# 面積: 78.53975, 周長: 31.4159
# 面積: 12, 周長: 14

# 抽象類別無法實體化
s = Shape()  # TypeError!
```

## Protocol：結構子型別

Python 3.8+ 引入的 `Protocol` 提供了另一種抽象方式——結構子型別。你不需要顯式繼承，只要類別有對應的方法就自動符合協議：

```python
from typing import Protocol

class Drawable(Protocol):
    def draw(self) -> str:
        ...

class Circle:
    def draw(self):
        return "繪製圓形"

class Square:
    def draw(self):
        return "繪製正方形"

class Dog:
    def bark(self):
        return "汪汪"

def render(shape: Drawable):
    print(shape.draw())

render(Circle())   # 繪製圓形（符合 Drawable 協議）
render(Square())   # 繪製正方形（符合 Drawable 協議）
render(Dog())      # 靜態型別檢查會報錯，但執行沒問題
```

## 抽象方法與屬性

抽象類別也可以定義抽象屬性：

```python
from abc import ABC, abstractmethod

class Employee(ABC):
    def __init__(self, name):
        self.name = name

    @property
    @abstractmethod
    def salary(self) -> float:
        pass

    def work(self) -> str:
        return f"{self.name} 正在工作，薪資為 {self.salary}"

class FullTimeEmployee(Employee):
    def __init__(self, name, monthly_salary):
        super().__init__(name)
        self._monthly_salary = monthly_salary

    @property
    def salary(self):
        return self._monthly_salary

class HourlyEmployee(Employee):
    def __init__(self, name, rate, hours):
        super().__init__(name)
        self.rate = rate
        self.hours = hours

    @property
    def salary(self):
        return self.rate * self.hours
```

## 抽象類別 vs Protocol

| 特性 | ABC | Protocol |
|------|-----|----------|
| 繼承需求 | 必須顯式繼承 | 不需要繼承 |
| 執行期檢查 | `isinstance()` 可用 | 需要 `@runtime_checkable` |
| 靜態檢查 | 支援 | 支援 |
| 預設實作 | 可提供 | 不可提供 |
| 彈性 | 較低 | 較高 |

## 實際應用範例

```python
from abc import ABC, abstractmethod
from typing import List

class DataSource(ABC):
    @abstractmethod
    def fetch(self) -> List[dict]:
        pass

    @abstractmethod
    def transform(self, data: List[dict]) -> List[dict]:
        pass

    def pipeline(self) -> List[dict]:
        data = self.fetch()
        return self.transform(data)

class CSVSoure(DataSource):
    def __init__(self, path):
        self.path = path

    def fetch(self):
        import csv
        with open(self.path) as f:
            return list(csv.DictReader(f))

    def transform(self, data):
        return [row for row in data if row.get("active") == "true"]

class APISoure(DataSource):
    def __init__(self, url):
        self.url = url

    def fetch(self):
        import urllib.request, json
        with urllib.request.urlopen(self.url) as r:
            return json.loads(r.read())

    def transform(self, data):
        return [item for item in data if item.get("status") == "ok"]

sources = [CSVSoure("data.csv"), APISoure("https://api.example.com/data")]
for src in sources:
    result = src.pipeline()
    print(f"處理 {len(result)} 筆資料")
```

## 小結

抽象類別與 Protocol 是 Python 中實現「設計合約」的兩種主要方式。ABC 提供了正式的繼承結構，Protocol 提供了更靈活的結構子型別。選擇哪一種取決於你的具體需求——需要嚴格的層次結構用 ABC，需要靈活性用 Protocol。

## 延伸閱讀

- [Python abc 模組](https://www.google.com/search?q=Python+abc+module)
- [Python Protocol 指南](https://www.google.com/search?q=Python+Protocol+typing)
