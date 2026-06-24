# 類別定義與 __init__

## 類別的基本結構

在 Python 中，類別使用 `class` 關鍵字定義。最簡單的類別可以只有一行：

```python
class EmptyClass:
    pass
```

但實用的類別通常需要 `__init__` 方法——這是物件的建構子，在物件被建立時自動執行：

```python
class Book:
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages
        self.current_page = 0

book = Book("Python 101", "Alice", 300)
print(book.title)   # Python 101
print(book.author)  # Alice
```

## self 的本質

`self` 是 Python 類別方法的第一個參數，代表物件實體本身。當你呼叫 `book.read()` 時，Python 背後實際執行的是 `Book.read(book)`：

```python
class Book:
    def __init__(self, title):
        self.title = title
        self._read_count = 0

    def read(self):
        self._read_count += 1
        return f"閱讀 {self.title}，第 {self._read_count} 次"

book = Book("Python 101")
print(book.read())  # 閱讀 Python 101，第 1 次
print(Book.read(book))  # 完全等價的寫法
```

## 預設參數與可選參數

`__init__` 可以定義預設參數，讓物件建立更靈活：

```python
class Configuration:
    def __init__(self, host="localhost", port=8080, debug=False):
        self.host = host
        self.port = port
        self.debug = debug

config1 = Configuration()                    # 全預設
config2 = Configuration(host="example.com")  # 部分指定
config3 = Configuration(port=3000, debug=True)  # 關鍵字參數

print(config1.host)  # localhost
print(config2.host)  # example.com
print(config3.port)  # 3000
```

## 可變預設參數的陷阱

千萬不要使用可變物件作為預設參數：

```python
class BadExample:
    def __init__(self, items=[]):  # 錯誤！
        self.items = items

a = BadExample()
b = BadExample()
a.items.append("hello")
print(b.items)  # ['hello'] 同一個 list！
```

正確做法是使用 `None` 並在方法內初始化：

```python
class GoodExample:
    def __init__(self, items=None):
        self.items = items if items is not None else []
```

## 型別提示

現代 Python 建議在 `__init__` 中使用型別提示：

```python
from typing import Optional, List

class Task:
    def __init__(
        self,
        title: str,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ):
        self.title = title
        self.description = description or ""
        self.tags = tags or []
        self.completed = False

    def complete(self) -> None:
        self.completed = True

task = Task("完成報告", tags=["工作", "緊急"])
print(task.title)     # 完成報告
print(task.tags)      # ['工作', '緊急']
task.complete()
print(task.completed) # True
```

## 進階：延遲初始化

有時候物件的某些屬性在建立時無法獲得，可以使用延遲初始化：

```python
class DataLoader:
    def __init__(self, filepath):
        self.filepath = filepath
        self._data = None

    @property
    def data(self):
        if self._data is None:
            import json
            with open(self.filepath) as f:
                self._data = json.load(f)
            print(f"從 {self.filepath} 載入資料")
        return self._data

loader = DataLoader("data.json")
print(loader.data)  # 第一次存取時載入
print(loader.data)  # 第二次直接使用快取
```

## 小結

`__init__` 是 Python 類別中最重要也最常用的方法。掌握預設參數、可變物件陷阱和型別提示，可以寫出更健壯、更易維護的類別。

## 延伸閱讀

- [Python __init__ 方法](https://www.google.com/search?q=Python+__init__+method+explained)
- [Python 型別提示](https://www.google.com/search?q=Python+type+hints+tutorial)
