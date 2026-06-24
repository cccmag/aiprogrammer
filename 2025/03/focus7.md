# 設計模式入門

## 什麼是設計模式？

設計模式是前人解決特定問題的經驗總結，是軟體開發中的「兵法」。1994 年出版的《Design Patterns: Elements of Reusable Object-Oriented Software》（GoF 書）歸納了 23 種經典模式，分為三大類：

- **建立型模式**：如何建立物件
- **結構型模式**：如何組合類別與物件
- **行為型模式**：如何分配職責與互動

## 工廠模式（Factory Pattern）

工廠模式封裝了物件的建立邏輯，讓客戶端不需要知道具體的類別名稱：

```python
from abc import ABC, abstractmethod

class Transport(ABC):
    @abstractmethod
    def deliver(self) -> str:
        pass

class Truck(Transport):
    def deliver(self):
        return "陸路運輸"

class Ship(Transport):
    def deliver(self):
        return "海路運輸"

class TransportFactory:
    @staticmethod
    def create(method: str) -> Transport:
        if method == "land":
            return Truck()
        elif method == "sea":
            return Ship()
        raise ValueError(f"不支援的運輸方式: {method}")

factory = TransportFactory()
t = factory.create("land")
print(t.deliver())  # 陸路運輸
```

## 單例模式（Singleton Pattern）

單例模式確保一個類別只有一個實體：

```python
class Database:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, connection_string=None):
        if not self._initialized:
            self.connection_string = connection_string
            self._initialized = True
            self.connect()

    def connect(self):
        print(f"連接到 {self.connection_string}")

    def query(self, sql):
        print(f"執行查詢: {sql}")

db1 = Database("mysql://localhost/mydb")
db2 = Database()  # 不會重新連線
print(db1 is db2)  # True
db2.query("SELECT * FROM users")  # 使用同一個實體
```

## 觀察者模式（Observer Pattern）

觀察者模式定義了一對多的依賴關係，當主體狀態改變時，所有依賴者都會收到通知：

```python
class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self, message):
        for observer in self._observers:
            observer.update(message)

class Observer:
    def __init__(self, name):
        self.name = name

    def update(self, message):
        print(f"{self.name} 收到: {message}")

newsletter = Subject()
alice = Observer("Alice")
bob = Observer("Bob")

newsletter.attach(alice)
newsletter.attach(bob)
newsletter.notify("本期雜誌已發布！")
# Alice 收到: 本期雜誌已發布！
# Bob 收到: 本期雜誌已發布！
```

## 策略模式（Strategy Pattern）

策略模式定義一系列可互換的演算法：

```python
from abc import ABC, abstractmethod

class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data):
        pass

class BubbleSort(SortStrategy):
    def sort(self, data):
        print("使用泡沫排序")
        return sorted(data)  # 簡化示範

class QuickSort(SortStrategy):
    def sort(self, data):
        print("使用快速排序")
        return sorted(data)

class MergeSort(SortStrategy):
    def sort(self, data):
        print("使用合併排序")
        return sorted(data)

class Sorter:
    def __init__(self, strategy: SortStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: SortStrategy):
        self._strategy = strategy

    def sort(self, data):
        return self._strategy.sort(data)

sorter = Sorter(BubbleSort())
data = [3, 1, 4, 1, 5]
print(sorter.sort(data))

sorter.set_strategy(QuickSort())
print(sorter.sort(data))
```

## Template Method 模式

Template Method 在父類別中定義演算法骨架，子類別實作特定步驟：

```python
from abc import ABC, abstractmethod

class DataProcessor(ABC):
    def process(self):
        self.load_data()
        self.clean_data()
        self.analyze()
        self.save_results()

    @abstractmethod
    def load_data(self):
        pass

    def clean_data(self):
        print("清洗資料（預設實作）")

    @abstractmethod
    def analyze(self):
        pass

    def save_results(self):
        print("儲存結果（預設實作）")

class CSVProcessor(DataProcessor):
    def load_data(self):
        print("讀取 CSV 檔案")

    def analyze(self):
        print("CSV 資料分析")

class JSONProcessor(DataProcessor):
    def load_data(self):
        print("讀取 JSON 檔案")

    def clean_data(self):
        print("JSON 特定清洗步驟")

    def analyze(self):
        print("JSON 資料分析")

CSVProcessor().process()
# 讀取 CSV 檔案 -> 清洗資料 -> CSV 資料分析 -> 儲存結果
```

## 小結

設計模式不是銀彈，而是工具。理解這些模式能幫助你更好地與其他開發者溝通，並在面對常見問題時有成熟的解決方案可供參考。重要的是記住：**模式是服務於設計的，而不是設計服務於模式**。

## 延伸閱讀

- [GoF 設計模式](https://www.google.com/search?q=Gang+of+Four+design+patterns)
- [Python 設計模式](https://www.google.com/search?q=Python+design+patterns+tutorial)
