# 多型與鴨子型別

## 多型的本質

多型（Polymorphism）來自希臘語「poly」（多）和「morph」（形態），意思是「多種形態」。在 OOP 中，多型允許不同類別的物件對同一訊息做出不同回應。

## 靜態多型 vs 動態多型

### 靜態多型（編譯期）

Python 不直接支援，但可以透過函式重載模擬：

```python
# Python 使用預設參數實現類似效果
def greet(name, greeting=None):
    if greeting:
        return f"{greeting}, {name}!"
    return f"Hello, {name}!"

print(greet("Alice"))        # Hello, Alice!
print(greet("Bob", "嗨"))    # 嗨, Bob!
```

### 動態多型（執行期）

這是 Python 的核心多型機制：

```python
class Cat:
    def sound(self):
        return "喵喵"

class Dog:
    def sound(self):
        return "汪汪"

class Cow:
    def sound(self):
        return "哞哞"

def animal_sound(animal):
    return animal.sound()

animals = [Cat(), Dog(), Cow()]
for a in animals:
    print(animal_sound(a))
```

## 鴨子型別（Duck Typing）

「如果它走路像鴨子、叫聲像鴨子，那它就是鴨子。」這句話完美概括了 Python 的多型哲學：**不需要顯式繼承，只要有相同的方法即可**。

```python
class Duck:
    def quack(self):
        return "呱呱呱！"

class Person:
    def quack(self):
        return "我在模仿鴨子叫！"

class Robot:
    def quack(self):
        return "嗶嗶，鴨子模式啟動"

def make_it_quack(thing):
    return thing.quack()

for entity in [Duck(), Person(), Robot()]:
    print(make_it_quack(entity))
```

### 更實用的範例

```python
class JSONSerializer:
    def serialize(self, data):
        import json
        return json.dumps(data, ensure_ascii=False)

class XMLSerializer:
    def serialize(self, data):
        parts = []
        for key, value in data.items():
            parts.append(f"<{key}>{value}</{key}>")
        return "<data>" + "".join(parts) + "</data>"

class CSVSerializer:
    def serialize(self, data):
        return ",".join(str(v) for v in data.values())

def export_data(serializer, data):
    result = serializer.serialize(data)
    print(f"輸出: {result}")
    return result

data = {"name": "Alice", "age": 30}
export_data(JSONSerializer(), data)
export_data(XMLSerializer(), data)
export_data(CSVSerializer(), data)
```

## isinstance() 與鴨子型別的取捨

有時候你需要檢查物件類型：

```python
def process_data(data):
    if isinstance(data, list):
        return [item * 2 for item in data]
    elif isinstance(data, dict):
        return {k: v * 2 for k, v in data.items()}
    else:
        return data
```

但鴨子型別的倡導者會說：不要檢查類型，直接嘗試操作：

```python
def process_data(data):
    try:
        return [item * 2 for item in data]
    except TypeError:
        try:
            return {k: v * 2 for k, v in data.items()}
        except TypeError:
            return data
```

## Python 的 Protocol 與靜態鴨子型別

Python 3.8+ 的 `Protocol` 讓鴨子型別可以接受靜態檢查：

```python
from typing import Protocol

class Flyable(Protocol):
    def fly(self) -> str:
        ...

class Bird:
    def fly(self):
        return "鳥兒飛翔"

class Airplane:
    def fly(self):
        return "飛機飛行"

class Fish:
    def swim(self):
        return "魚兒游泳"

def let_it_fly(thing: Flyable):
    print(thing.fly())

let_it_fly(Bird())      # OK
let_it_fly(Airplane())  # OK
let_it_fly(Fish())      # 型別檢查會報錯（但執行沒問題）
```

## 鴨子型別的實際應用

### 策略模式

```python
def quick_sort(data):
    print("快速排序")
    return sorted(data)

def merge_sort(data):
    print("合併排序")
    return sorted(data)

def sort_data(sort_func, data):
    return sort_func(data)

data = [3, 1, 4, 1, 5]
sort_data(quick_sort, data)
sort_data(merge_sort, data)
```

### Iterator 協議

任何實作了 `__iter__` 和 `__next__` 的物件都可以在 `for` 迴圈中使用：

```python
class CountDown:
    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        self.current -= 1
        return self.current + 1

for n in CountDown(5):
    print(n)  # 5, 4, 3, 2, 1
```

## 小結

多型與鴨子型別是 Python 最靈活的特性之一。它們讓你可以寫出通用的、可復用的程式碼，而不需要拘泥於繼承層次。記住：**不要檢查它是不是鴨子，讓它叫叫看就知道了。**

## 延伸閱讀

- [Python Duck Typing](https://www.google.com/search?q=Python+duck+typing)
- [Python Protocol](https://www.google.com/search?q=Python+typing+Protocol)
