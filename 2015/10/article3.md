# 工廠模式深入解析

## 前言

工廠模式是創建型模式中最常用的模式之一，用於封裝物件的建立邏輯。

## 簡單工廠

```python
class Product:
    pass

class ProductA(Product):
    def __init__(self):
        self.name = "A"

class ProductB(Product):
    def __init__(self):
        self.name = "B"

class SimpleFactory:
    @staticmethod
    def create_product(type):
        if type == "A":
            return ProductA()
        elif type == "B":
            return ProductB()
        raise ValueError(f"Unknown type: {type}")
```

## 工廠方法模式

定義建立物件的介面，讓子類別決定實例化哪個類別。

```python
class Factory(ABC):
    @abstractmethod
    def create(self):
        pass

class FactoryA(Factory):
    def create(self):
        return ProductA()

class FactoryB(Factory):
    def create(self):
        return ProductB()
```

## 抽象工廠

建立一系列相關物件。

```python
class GUIFactory(ABC):
    @abstractmethod
    def create_button(self): pass

    @abstractmethod
    def create_checkbox(self): pass

class WindowsFactory(GUIFactory):
    def create_button(self): return WindowsButton()
    def create_checkbox(self): return WindowsCheckbox()

class MacFactory(GUIFactory):
    def create_button(self): return MacButton()
    def create_checkbox(self): return MacCheckbox()
```

## 選擇時機

- **簡單工廠**：物件類型少，建立邏輯簡單
- **工廠方法**：需要擴展建立邏輯
- **抽象工廠**：需要建立一系列相關物件

## 小結

工廠模式幫助我們將物件建立與使用分離，提高系統的可維護性和擴展性。

---

## 延伸閱讀

- [Factory Pattern](https://www.google.com/search?q=factory+pattern+design+patterns)
- [Abstract Factory Pattern](https://www.google.com/search?q=abstract+factory+pattern+example)