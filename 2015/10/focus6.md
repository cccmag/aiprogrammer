# 設計模式分類與應用

## 創建型、結構型、行為型模式

### 前言

設計模式是軟體開發中常見問題的經驗總結。1994 年，GoF（Gang of Four，四人組）發表了《Design Patterns》一書，將 23 種模式分類為創建型、結構型和行為型。本期將深入探討這些模式的用途和應用場景。

### 設計模式分類總覽

```
┌─────────────────────────────────────────────────────────────────┐
│                      GoF 設計模式分類                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   創建型 (Creational)          結構型 (Structural)               │
│   處理物件建立機制            處理物件組合問題                    │
│                                                                 │
│   • Singleton                 • Adapter                         │
│   • Factory Method           • Bridge                           │
│   • Abstract Factory         • Composite                       │
│   • Builder                  • Decorator                       │
│   • Prototype               • Facade                           │
│                               • Flyweight                       │
│                               • Proxy                           │
│                                                                 │
│   行為型 (Behavioral)                                         │
│   處理物件之間的職責分配                                       │
│                                                                 │
│   • Chain of Responsibility  • State                           │
│   • Command                   • Strategy                        │
│   • Iterator                  • Template Method                 │
│   • Mediator                 • Visitor                          │
│   • Memento                                                   │
│   • Observer                                                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 創建型模式

創建型模式專注於物件的建立機制，幫助我們以更靈活的方式創建物件。

### 1. Singleton（單例模式）

**意圖**：確保一個類別只有一個實例，並提供全域存取點。

**使用場景**：
- 資料庫連線池
- 日誌記錄器
- 設定檔管理器

```python
class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

# 使用
a = Singleton()
b = Singleton()
assert a is b  # True，兩者是同一個實例
```

**優點**：
- 控制資源存取
- 確保全域唯一性

**缺點**：
- 隱藏依賴關係
- 難以測試
- 在多執行緒環境可能出問題（需要同步處理）

### 2. Factory Method（工廠方法）

**意圖**：定義建立物件的介面，但讓子類別決定要實例化哪個類別。

**使用場景**：
- 日誌系統：支援多種輸出（檔案、資料庫、網路）
- UI 元件工廠：建立不同平台的按鈕、核取方塊

```python
from abc import ABC, abstractmethod

class Dialog(ABC):
    @abstractmethod
    def create_button(self):
        pass

    def render(self):
        button = self.create_button()
        button.click()
        return button

class WindowsDialog(Dialog):
    def create_button(self):
        return WindowsButton()

class WebDialog(Dialog):
    def create_button(self):
        return WebButton()
```

**優點**：
- 避免工廠和產品之間的緊耦合
- 單一職責原則：產品建立程式碼集中在一處
- 開放/封閉原則：新增產品類型不需要修改既有工廠

### 3. Abstract Factory（抽象工廠）

**意圖**：建立一系列相關物件，而無需指定它們的具體類別。

**使用場景**：
- 跨平台的 UI 元件套裝
- 不同資料庫的 ORM 映射

```python
class GUIFactory(ABC):
    @abstractmethod
    def create_button(self):
        pass

    @abstractmethod
    def create_checkbox(self):
        pass

class WindowsFactory(GUIFactory):
    def create_button(self):
        return WindowsButton()

    def create_checkbox(self):
        return WindowsCheckbox()

class MacFactory(GUIFactory):
    def create_button(self):
        return MacButton()

    def create_checkbox(self):
        return MacCheckbox()
```

### 4. Builder（建造者模式）

**意圖**：逐步構造複雜物件。

**使用場景**：
- SQL 查詢建構器
- 文件產生器
- HTML/XML 建構

```python
class QueryBuilder:
    def __init__(self):
        self._query = {"SELECT": [], "FROM": None, "WHERE": []}

    def select(self, *fields):
        self._query["SELECT"].extend(fields)
        return self

    def from_table(self, table):
        self._query["FROM"] = table
        return self

    def where(self, condition):
        self._query["WHERE"].append(condition)
        return self

    def build(self):
        return self._query

# 使用
query = (QueryBuilder()
    .select("name", "email")
    .from_table("users")
    .where("active = true")
    .build())
```

### 5. Prototype（原型模式）

**意圖**：通過複製既有物件建立新物件。

**使用場景**：
- 物件建立成本高（例如從資料庫載入）
- 需要避免子類別膨脹

```python
import copy

class Prototype:
    def clone(self):
        return copy.deepcopy(self)

class Document(Prototype):
    def __init__(self, title, content):
        self.title = title
        self.content = content

doc1 = Document("Original", "Hello World")
doc2 = doc1.clone()
doc2.title = "Copy"
```

---

## 結構型模式

結構型模式處理物件的組合，幫助我們建立更大、更複雜的結構。

### 1. Adapter（轉接器模式）

**意圖**：將一個類別的介面轉換成另一個介面。

```python
# 既有類別
class LegacyPayment:
    def pay_with_legacy_interface(self, amount, currency):
        print(f"Legacy payment: {amount} {currency}")

# 新介面
class PaymentProcessor:
    def process_payment(self, amount):
        pass

# 轉接器
class PaymentAdapter(PaymentProcessor):
    def __init__(self, legacy):
        self.legacy = legacy

    def process_payment(self, amount):
        self.legacy.pay_with_legacy_interface(amount, "USD")
```

### 2. Bridge（橋接模式）

**意圖**：將抽象部分與實作部分分離，使兩者可以獨立變化。

```python
# 實作部分
class Renderer(ABC):
    @abstractmethod
    def render_circle(self, radius):
        pass

class CanvasRenderer(Renderer):
    def render_circle(self, radius):
        print(f"Canvas: drawing circle radius {radius}")

class SVGRenderer(Renderer):
    def render_circle(self, radius):
        print(f"SVG: <circle r='{radius}'/>")

# 抽象部分
class Shape(ABC):
    def __init__(self, renderer: Renderer):
        self.renderer = renderer

    @abstractmethod
    def draw(self):
        pass

class Circle(Shape):
    def __init__(self, radius, renderer):
        super().__init__(renderer)
        self.radius = radius

    def draw(self):
        self.renderer.render_circle(self.radius)

# 使用
canvas_circle = Circle(5, CanvasRenderer())
svg_circle = Circle(5, SVGRenderer())
```

### 3. Composite（組合模式）

**意圖**：將物件組合成樹狀結構，客戶端可以統一對待單一物件和組合物件。

```python
class Component(ABC):
    @abstractmethod
    def calculate_price(self):
        pass

class Product(Component):
    def __init__(self, price):
        self.price = price

    def calculate_price(self):
        return self.price

class Box(Component):
    def __init__(self):
        self.children = []

    def add(self, component):
        self.children.append(component)

    def calculate_price(self):
        return sum(child.calculate_price() for child in self.children)

# 使用
box = Box()
box.add(Product(10))
box.add(Product(20))
inner_box = Box()
inner_box.add(Product(5))
inner_box.add(Product(15))
box.add(inner_box)

print(box.calculate_price())  # 50
```

### 4. Decorator（裝飾者模式）

**意圖**：動態地新增職責到物件上。

```python
class Coffee:
    def cost(self):
        return 5

class CoffeeDecorator(Coffee):
    def __init__(self, coffee):
        self.coffee = coffee

    def cost(self):
        return self.coffee.cost()

class Milk(CoffeeDecorator):
    def cost(self):
        return self.coffee.cost() + 1.5

class Sugar(CoffeeDecorator):
    def cost(self):
        return self.coffee.cost() + 0.5

# 使用
coffee = Coffee()
coffee_with_milk = Milk(coffee)
coffee_with_milk_and_sugar = Sugar(Milk(coffee))
print(coffee_with_milk_and_sugar.cost())  # 7.0
```

### 5. Facade（外觀模式）

**意圖**：為複雜子系統提供統一介面。

```python
class CPU:
    def freeze(self): print("CPU: freezing...")

    def jump(self, position): print(f"CPU: jumping to {position}")

    def execute(self): print("CPU: executing...")

class Memory:
    def load(self, position, data): print(f"Memory: loading {data} to {position}")

class Disk:
    def read(self, sector, size): return "disk data"

class ComputerFacade:
    def __init__(self):
        self.cpu = CPU()
        self.memory = Memory()
        self.disk = Disk()

    def start(self):
        self.cpu.freeze()
        data = self.disk.read(0, 1024)
        self.memory.load(0, data)
        self.cpu.jump(0)
        self.cpu.execute()

# 使用者只需要與 Facade 互動
computer = ComputerFacade()
computer.start()
```

### 6. Proxy（代理模式）

**意圖**：為另一個物件提供替代或佔位。

**使用場景**：
- 延遲載入（虛擬代理）
- 存取控制（保護代理）
- 遠端物件存取（遠端代理）
- 日誌記錄（智慧參照）

```python
class RealImage:
    def __init__(self, filename):
        self.filename = filename
        self.load_from_disk()

    def load_from_disk(self):
        print(f"Loading {self.filename}")

    def display(self):
        print(f"Displaying {self.filename}")

class ImageProxy:
    def __init__(self, filename):
        self.filename = filename
        self._real_image = None

    def display(self):
        if self._real_image is None:
            self._real_image = RealImage(self.filename)
        self._real_image.display()

# 使用 - 真正需要時才載入
proxy = ImageProxy("photo.jpg")
print("Image created")  # 不會立即載入
proxy.display()  # 這時才載入
proxy.display()  # 第二次不需要重新載入
```

---

## 行為型模式

行為型模式處理物件之間的交互和職責分配。

### 1. Observer（觀察者模式）

**意圖**：定義一對多的依賴關係，當一個物件狀態改變時，所有依賴者都會收到通知。

```python
class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self):
        for observer in self._observers:
            observer.update(self)

class Observer:
    def update(self, subject):
        pass

class TemperatureDisplay(Observer):
    def update(self, subject):
        print(f"Temperature display: {subject.temperature}°C")

class LogWriter(Observer):
    def update(self, subject):
        print(f"Logging: {subject.temperature}°C")

# 使用
weather_station = WeatherStation()
display = TemperatureDisplay()
logger = LogWriter()

weather_station.attach(display)
weather_station.attach(logger)
weather_station.temperature = 25
weather_station.notify()
```

### 2. Strategy（策略模式）

**意圖**：定義一系列演算法，把它們一個個封裝起來，並使它們可以互相替換。

```python
class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data):
        pass

class QuickSort(SortStrategy):
    def sort(self, data):
        print("Using quick sort")
        return sorted(data)

class MergeSort(SortStrategy):
    def sort(self, data):
        print("Using merge sort")
        return sorted(data)

class Context:
    def __init__(self, strategy):
        self.strategy = strategy

    def set_strategy(self, strategy):
        self.strategy = strategy

    def execute_sort(self, data):
        return self.strategy.sort(data)

# 使用
context = Context(QuickSort())
context.execute_sort([3, 1, 2])
context.set_strategy(MergeSort())
context.execute_sort([3, 1, 2])
```

### 3. Command（命令模式）

**意圖**：將請求封裝成物件，支援可撤銷的操作。

```python
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass

class Light:
    def on(self): print("Light is ON")
    def off(self): print("Light is OFF")

class LightOnCommand(Command):
    def __init__(self, light):
        self.light = light

    def execute(self):
        self.light.on()

    def undo(self):
        self.light.off()

class RemoteControl:
    def __init__(self):
        self.history = []

    def execute_command(self, command):
        command.execute()
        self.history.append(command)

    def undo_last(self):
        if self.history:
            command = self.history.pop()
            command.undo()

# 使用
light = Light()
light_on = LightOnCommand(light)

remote = RemoteControl()
remote.execute_command(light_on)
remote.undo_last()
```

### 4. State（狀態模式）

**意圖**：允許物件在內部狀態改變時改變它的行為。

```python
class State(ABC):
    @abstractmethod
    def handle(self, context):
        pass

class StopState(State):
    def handle(self, context):
        print("Player is STOPPED")
        context.state = StopState()

class PlayState(State):
    def handle(self, context):
        print("Player is PLAYING")
        context.state = PlayState()

class PauseState(State):
    def handle(self, context):
        print("Player is PAUSED")
        context.state = PauseState()

class MediaPlayer:
    def __init__(self):
        self.state = StopState()

    def click_play(self):
        self.state.handle(self)

    def click_stop(self):
        print("Stopping...")
        self.state = StopState()

# 使用
player = MediaPlayer()
player.click_play()   # Stopped -> Playing
player.click_play()   # Playing 狀態的行為
player.click_stop()   # Back to Stopped
```

### 5. Template Method（模板方法）

**意圖**：定義演算法的骨架，將某些步驟延遲到子類別。

```python
class DataMiner(ABC):
    def mine(self):
        self.open_file()
        self.extract_data()
        self.parse_data()
        self.analyze_data()
        self.send_report()
        self.close_file()

    @abstractmethod
    def open_file(self):
        pass

    @abstractmethod
    def extract_data(self):
        pass

    def parse_data(self):
        print("Parsing data...")

    @abstractmethod
    def analyze_data(self):
        pass

    def send_report(self):
        print("Sending report...")

    @abstractmethod
    def close_file(self):
        pass

class PDFDataMiner(DataMiner):
    def open_file(self): print("Opening PDF")
    def extract_data(self): print("Extracting from PDF")
    def analyze_data(self): print("Analyzing PDF data")
    def close_file(self): print("Closing PDF")

class CSVDataMiner(DataMiner):
    def open_file(self): print("Opening CSV")
    def extract_data(self): print("Extracting from CSV")
    def analyze_data(self): print("Analyzing CSV data")
    def close_file(self): print("Closing CSV")
```

### 6. Iterator（迭代器模式）

**意圖**：提供一種方式順序存取集合元素，而不暴露底層表示。

```python
class Iterator(ABC):
    @abstractmethod
    def __next__(self):
        pass

    @abstractmethod
    def has_next(self):
        pass

class ArrayIterator(Iterator):
    def __init__(self, collection):
        self.collection = collection
        self.position = 0

    def __next__(self):
        if not self.has_next():
            raise StopIteration
        result = self.collection[self.position]
        self.position += 1
        return result

    def has_next(self):
        return self.position < len(self.collection)

class ListIterator(Iterator):
    def __init__(self, collection):
        self.collection = collection
        self.position = 0

    def __next__(self):
        if not self.has_next():
            raise StopIteration
        result = self.collection[self.position]
        self.position += 1
        return result

    def has_next(self):
        return self.position < len(self.collection)

# 使用
data = [1, 2, 3]
iterator = ArrayIterator(data)
while iterator.has_next():
    print(next(iterator))
```

### 7. Chain of Responsibility（責任鏈模式）

**意圖**：將請求沿著處理者鏈傳遞，直到有處理者處理它。

```python
class Handler(ABC):
    def __init__(self):
        self.next_handler = None

    def set_next(self, handler):
        self.next_handler = handler
        return handler

    @abstractmethod
    def handle(self, request):
        pass

class AuthenticationHandler(Handler):
    def handle(self, request):
        if request.get("authenticated"):
            print("Authenticated")
            if self.next_handler:
                return self.next_handler.handle(request)
        else:
            print("Authentication failed")

class ValidationHandler(Handler):
    def handle(self, request):
        if request.get("valid"):
            print("Validated")
            if self.next_handler:
                return self.next_handler.handle(request)
        else:
            print("Validation failed")

# 使用
auth = AuthenticationHandler()
validation = ValidationHandler()
auth.set_next(validation)

request = {"authenticated": True, "valid": True}
auth.handle(request)
```

---

## 模式選擇指南

| 需求場景 | 推薦模式 |
|---------|---------|
| 確保唯一實例 | Singleton |
| 需要工廠建立物件 | Factory Method / Abstract Factory |
| 逐步建構複雜物件 | Builder |
| 複製既有物件 | Prototype |
| 轉接不相容介面 | Adapter |
| 分離抽象與實作 | Bridge |
| 統一對待整體與部分 | Composite |
| 動態新增職責 | Decorator |
| 簡化複雜子系統 | Facade |
| 控制資源存取 | Proxy |
| 狀態改變時通知觀察者 | Observer |
| 多種演算法可以替換 | Strategy |
| 封裝請求為物件 | Command |
| 狀態影響行為 | State |
| 定義演算法骨架 | Template Method |
| 順序存取集合 | Iterator |
| 請求沿鏈傳遞 | Chain of Responsibility |

---

## 模式使用建議

1. **不要過度使用**：模式是工具，不是目標
2. **理解而非背誦**：理解模式的意圖和適用場景
3. **保持簡單**：如果簡單的程式碼就能解決問題，不要用模式
4. **警惕反模式**：不當使用模式會造成過度設計
5. **持續重構**：隨著需求變化，模式選擇可能需要調整

---

## 小結

設計模式是寶貴的軟體設計經驗寶庫。掌握這些模式可以幫助我們：

- **創建型**：靈活建立物件，控制建立細節
- **結構型**：組合物件形成更大結構
- **行為型**：管理物件之間的交互

但重要的是理解模式的意圖和適用場景，而不是機械地套用。在實際開發中，保持程式碼簡單、可讀、可維護比遵循任何模式都更重要。

---

**下一步**：[程式碼品質與技術債務](focus7.md)

## 延伸閱讀

- [Design Patterns: Elements of Reusable Object-Oriented Software](https://www.google.com/search?q=Design+Patterns+Gang+of+Four+book)
- [Design Patterns Refactoring Guru](https://www.google.com/search?q=refactoring+guru+design+patterns)
- [Learning JavaScript Design Patterns](https://www.google.com/search?q=javascript+design+patterns+addy+osmani)