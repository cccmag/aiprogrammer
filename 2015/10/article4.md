# 觀察者模式與事件驅動

## 前言

觀察者模式定義了一對多的依賴關係，當一個物件狀態改變時，所有依賴都會收到通知。

## 基本實現

```python
class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self, message=None):
        for observer in self._observers:
            observer.update(message)

class Observer:
    def update(self, message):
        pass
```

## Python 中的觀察者

```python
class Event:
    def __init__(self):
        self._handlers = []

    def subscribe(self, handler):
        self._handlers.append(handler)

    def unsubscribe(self, handler):
        self._handlers.remove(handler)

    def emit(self, *args):
        for handler in self._handlers:
            handler(*args)

# 使用
on_click = Event()
on_click.subscribe(lambda x: print(f"Handler 1: {x}"))
on_click.subscribe(lambda x: print(f"Handler 2: {x}"))
on_click.emit("clicked!")
```

## 事件驅動架構

觀察者模式是事件驅動架構的基礎：

- **DOM 事件**：點擊、輸入、滾動
- **訊息系統**：發布/訂閱模式
- **Redux**：Flux 架構中的狀態管理

## 應用場景

1. **GUI 程式**：按鈕點擊、選單選擇
2. **即時通訊**：新訊息通知
3. **股價更新**：金融資料監控
4. **社交網路**：狀態更新、粉絲通知

## 小結

觀察者模式幫助我們建立鬆耦合的系統，元件之間通過事件進行通信，而不是直接依賴。

---

## 延伸閱讀

- [Observer Pattern](https://www.google.com/search?q=observer+pattern+design+patterns)
- [Event-Driven Architecture](https://www.google.com/search?q=event+driven+architecture+patterns)