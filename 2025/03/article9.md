# 單例模式與工廠模式

## 建立型設計模式

在 GoF 的 23 種設計模式中，建立型模式（Creational Patterns）專注於物件的建立機制。本期介紹最實用的兩種：單例模式和工廠模式。

## 單例模式（Singleton）

單例模式確保一個類別只有一個實體，並提供全域存取點。

### 經典實作

```python
class Database:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, host=None, port=None):
        if not self._initialized:
            self.host = host or "localhost"
            self.port = port or 5432
            self._connected = False
            self._initialized = True

    def connect(self):
        if not self._connected:
            print(f"連接到 {self.host}:{self.port}")
            self._connected = True
        return self

    def query(self, sql):
        print(f"執行查詢: {sql}")
        return []

db1 = Database(host="prod-server", port=5432)
db1.connect()
db2 = Database()
print(db1 is db2)  # True
print(db2.host)    # prod-server（同一個實體）
```

### Module-Level Singleton

Python 模組本身就是單例，這是最簡單的實現方式：

```python
# config.py
class _Config:
    def __init__(self):
        self.debug = False
        self.api_key = ""

    def load_from_env(self):
        import os
        self.debug = os.environ.get("DEBUG", "false").lower() == "true"
        self.api_key = os.environ.get("API_KEY", "")

config = _Config()

# main.py
from config import config
config.load_from_env()
print(config.debug)
```

### 裝飾器實作

```python
def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance

@singleton
class Logger:
    def __init__(self):
        self._logs = []

    def log(self, message):
        self._logs.append(message)
        print(f"[LOG] {message}")

logger1 = Logger()
logger2 = Logger()
print(logger1 is logger2)  # True
```

## 工廠模式（Factory）

工廠模式將物件的建立邏輯封裝起來，客戶端不需要知道具體類別的名稱。

### 簡單工廠

```python
from abc import ABC, abstractmethod

class Notification(ABC):
    @abstractmethod
    def send(self, message: str) -> str:
        pass

class EmailNotification(Notification):
    def send(self, message):
        return f"發送郵件: {message}"

class SMSNotification(Notification):
    def send(self, message):
        return f"發送簡訊: {message}"

class PushNotification(Notification):
    def send(self, message):
        return f"發送推播: {message}"

class NotificationFactory:
    @staticmethod
    def create(channel: str) -> Notification:
        factories = {
            "email": EmailNotification,
            "sms": SMSNotification,
            "push": PushNotification,
        }
        cls = factories.get(channel.lower())
        if not cls:
            raise ValueError(f"不支援的通知管道: {channel}")
        return cls()

# 使用
factory = NotificationFactory()
notif = factory.create("email")
print(notif.send("Hello!"))
```

### 工廠方法模式

將工廠方法定義在抽象類別中，由子類別決定要建立哪種物件：

```python
from abc import ABC, abstractmethod

class Document(ABC):
    @abstractmethod
    def open(self):
        pass

    @abstractmethod
    def save(self):
        pass

class PDFDocument(Document):
    def open(self):
        return "開啟 PDF 文件"

    def save(self):
        return "儲存 PDF 文件"

class WordDocument(Document):
    def open(self):
        return "開啟 Word 文件"

    def save(self):
        return "儲存 Word 文件"

class Application(ABC):
    @abstractmethod
    def create_document(self) -> Document:
        pass

    def new_document(self):
        doc = self.create_document()
        print(doc.open())
        return doc

class PDFApp(Application):
    def create_document(self):
        return PDFDocument()

class WordApp(Application):
    def create_document(self):
        return WordDocument()

app = PDFApp()
doc = app.new_document()  # 開啟 PDF 文件
```

### 工廠模式的最佳實踐

```python
from abc import ABC, abstractmethod
from typing import Dict, Type

class Plugin(ABC):
    @abstractmethod
    def execute(self, data):
        pass

class PluginRegistry:
    _plugins: Dict[str, Type[Plugin]] = {}

    @classmethod
    def register(cls, name: str):
        def decorator(plugin_cls: Type[Plugin]):
            cls._plugins[name] = plugin_cls
            return plugin_cls
        return decorator

    @classmethod
    def create(cls, name: str, **kwargs) -> Plugin:
        plugin_cls = cls._plugins.get(name)
        if not plugin_cls:
            raise ValueError(f"未知的外掛: {name}")
        return plugin_cls(**kwargs)

@PluginRegistry.register("encrypt")
class EncryptPlugin(Plugin):
    def execute(self, data):
        return f"加密: {data}"

@PluginRegistry.register("compress")
class CompressPlugin(Plugin):
    def execute(self, data):
        return f"壓縮: {data}"

plugin = PluginRegistry.create("encrypt")
print(plugin.execute("Hello"))
```

## 小結

單例模式確保了全域唯一的實體，適合管理共享資源（資料庫連線、設定檔）。工廠模式封裝了物件的建立邏輯，讓系統更易於擴展。這兩種模式是 Python 開發中最實用的設計模式之一。

## 延伸閱讀

- [Singleton Pattern in Python](https://www.google.com/search?q=Python+singleton+pattern)
- [Factory Pattern in Python](https://www.google.com/search?q=Python+factory+pattern)
