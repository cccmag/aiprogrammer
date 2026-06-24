# 繼承實戰

## 當繼承遇到實際問題

繼承是 OOP 中最強大的程式碼重用機制，但使用不當也會帶來麻煩。讓我們從一個實際案例開始，逐步探索繼承的最佳實踐。

## 案例：電子商務系統的折扣規則

假設我們需要實作一個電子商務系統的折扣引擎：

```python
from abc import ABC, abstractmethod
from typing import List

class Discount(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def apply(self, total: float) -> float:
        pass

    def description(self) -> str:
        return f"{self.name}: -${self.apply(0):.2f}"  # 示範用
```

### 具體折扣實作

```python
class PercentageDiscount(Discount):
    def __init__(self, percent: float):
        super().__init__(f"{percent}% 折扣")
        self._percent = percent

    def apply(self, total: float) -> float:
        return total * self._percent / 100

class FixedAmountDiscount(Discount):
    def __init__(self, amount: float, min_total: float = 0):
        super().__init__(f"滿 ${min_total} 折 ${amount}")
        self._amount = amount
        self._min_total = min_total

    def apply(self, total: float) -> float:
        if total >= self._min_total:
            return self._amount
        return 0

class BuyXGetYFree(Discount):
    def __init__(self, x: int, y: int, unit_price: float):
        super().__init__(f"買 {x} 送 {y}")
        self._x = x
        self._y = y
        self._unit_price = unit_price

    def apply(self, total: float) -> float:
        sets = total // (self._x * self._unit_price)
        free_items = sets * self._y
        return free_items * self._unit_price

# 使用範例
discounts: List[Discount] = [
    PercentageDiscount(10),
    FixedAmountDiscount(50, 300),
    BuyXGetYFree(3, 1, 100),
]

for d in discounts:
    print(f"{d.name}: 折扣 {d.apply(500)}")
```

## 多重繼承實戰

多重繼承是 Python 的特色，但使用時需要特別注意 MRO：

```python
class ValidateMixin:
    def validate(self):
        print("執行基本驗證")
        return True

class LogMixin:
    def log(self, message):
        print(f"[{self.__class__.__name__}] {message}")

class SaveMixin:
    def save(self):
        self.log("正在儲存")
        if self.validate():
            print("資料已儲存")
        else:
            print("儲存失敗：驗證未通過")

class User(ValidateMixin, LogMixin, SaveMixin):
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def validate(self):
        super().validate()
        if "@" not in self.email:
            self.log("電子郵件格式錯誤")
            return False
        self.log("驗證通過")
        return True

user = User("Alice", "alice@example.com")
user.save()
# [User] 正在儲存
# 執行基本驗證
# [User] 驗證通過
# 資料已儲存
```

## super() 的進階用法

`super()` 在多重繼承中會根據 MRO 決定呼叫順序：

```python
class A:
    def process(self):
        print("A.process")
        return "A"

class B(A):
    def process(self):
        print("B.process")
        result = super().process()
        return f"B({result})"

class C(A):
    def process(self):
        print("C.process")
        result = super().process()
        return f"C({result})"

class D(B, C):
    def process(self):
        print("D.process")
        result = super().process()
        return f"D({result})"

d = D()
print(d.process())
# D.process
# B.process
# C.process
# A.process
# D(B(C(A)))
print(D.__mro__)
# D -> B -> C -> A -> object
```

## 繼承的最佳實踐

### 1. 偏好多層組合而非深層繼承

```python
# 不好的設計：深層繼承
class Animal: ...
class Mammal(Animal): ...
class Dog(Mammal): ...
class PetDog(Dog): ...

# 較好的設計：組合 + Mixin
class Animal: ...
class Walker: ...
class Barker: ...
class Pet: ...

class Dog(Animal, Walker, Barker): ...
```

### 2. 使用抽象類別定義介面

```python
from abc import ABC, abstractmethod

class IPayment(ABC):
    @abstractmethod
    def pay(self, amount: float) -> bool:
        pass

class CreditCardPayment(IPayment):
    def pay(self, amount: float) -> bool:
        print(f"信用卡付款 ${amount}")
        return True
```

### 3. 避免鑽石問題

Python 的 C3 線性化已經解決了鑽石問題，但過於複雜的繼承層次仍應避免：

```python
class Base: pass
class X(Base): pass
class Y(Base): pass
class Z(X, Y): pass  # 明確的 MRO: Z -> X -> Y -> Base
```

## 小結

繼承是強大的工具，但應該謹慎使用。遵循「組合優於繼承」的原則，使用 Mixin 類別來共享行為，並利用抽象類別定義合約。記住：繼承代表的是「is-a」關係，而不是單純的程式碼重用。

## 延伸閱讀

- [Python MRO 與 C3 線性化](https://www.google.com/search?q=Python+MRO+C3+linearization)
- [組合 vs 繼承](https://www.google.com/search?q=composition+vs+inheritance+Python)
