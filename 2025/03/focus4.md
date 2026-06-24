# 封裝與屬性管理

## 私有屬性與 Name Mangling

封裝是 OOP 的核心特性之一，它將資料（屬性）和操作資料的方法綁定在一起，並隱藏內部實作細節。在 Python 中，封裝是通過約定和名稱改寫機制實現的。

### 命名慣例

Python 使用底線作為命名約定來表示存取權限：

```python
class MyClass:
    def __init__(self):
        self.public = "公開的"        # 無底線：公開
        self._protected = "保護的"    # 單底線：內部使用（慣例）
        self.__private = "私有的"     # 雙底線：名稱改寫

obj = MyClass()
print(obj.public)       # 公開的
print(obj._protected)   # 保護的（但 Python 不阻止存取）
```

### Name Mangling 機制

當屬性以雙底線開頭時，Python 會自動改寫名稱，避免子類別意外覆寫：

```python
class Parent:
    def __init__(self):
        self.__secret = "密碼123"

    def get_secret(self):
        return self.__secret

class Child(Parent):
    def __init__(self):
        super().__init__()
        self.__secret = "子類別的秘密"

p = Parent()
c = Child()
print(p.get_secret())  # 密碼123
print(c.get_secret())  # 密碼123（沒有被子類別的 __secret 覆寫）

# Name mangling 後的實際名稱
print(p._Parent__secret)   # 密碼123
print(c._Child__secret)    # 子類別的秘密
```

## Property 裝飾器

`@property` 是 Python 中最優雅的封裝工具，它讓方法可以像屬性一樣存取：

```python
class Temperature:
    def __init__(self, celsius=0):
        self._celsius = celsius

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("溫度不能低於絕對零度")
        self._celsius = value

    @property
    def fahrenheit(self):
        return self._celsius * 9 / 5 + 32

    @fahrenheit.setter
    def fahrenheit(self, value):
        self._celsius = (value - 32) * 5 / 9

t = Temperature(25)
print(t.celsius)       # 25（像屬性一樣存取）
print(t.fahrenheit)    # 77.0
t.celsius = 30
print(t.fahrenheit)    # 86.0
t.fahrenheit = 100
print(t.celsius)       # 37.78
```

### 唯讀屬性

只定義 `@property` 而不定義 `@xxx.setter` 就得到唯讀屬性：

```python
class Person:
    def __init__(self, name, birth_year):
        self.name = name
        self._birth_year = birth_year

    @property
    def age(self):
        from datetime import date
        return date.today().year - self._birth_year

p = Person("Alice", 1990)
print(p.age)   # 35（計算得出）
p.age = 30     # AttributeError: can't set attribute
```

## __slots__ 優化

`__slots__` 可以限制物件允許的屬性，同時節省記憶體：

```python
class Point:
    __slots__ = ('x', 'y')  # 只允許 x 和 y 屬性

    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Point(1, 2)
print(p.x, p.y)  # 1 2
p.z = 3          # AttributeError: 'Point' object has no attribute 'z'
```

## 封裝的最佳實踐

1. **公開 API 盡量簡潔**：只暴露必要的介面，內部實作使用單底線前綴
2. **使用 Property 替代 Getter/Setter**：Python 風格不需要 Java 式的 `getX()` / `setX()`
3. **驗證邏輯放在 Setter 中**：在 `@property.setter` 中進行資料驗證
4. **謹慎使用雙底線**：`__private` 通常不需要，`_protected` 就足夠了
5. **__slots__ 只在確實需要效能優化時使用**

```python
class BankAccount:
    def __init__(self, owner):
        self.owner = owner
        self._balance = 0
        self._transactions = []

    @property
    def balance(self):
        return self._balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("存款金額必須為正數")
        self._balance += amount
        self._transactions.append(("deposit", amount))

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("提款金額必須為正數")
        if amount > self._balance:
            raise ValueError("餘額不足")
        self._balance -= amount
        self._transactions.append(("withdraw", amount))

    @property
    def transaction_log(self):
        return list(self._transactions)  # 返回副本保護資料
```

## 小結

封裝是保護物件內部狀態的第一道防線。Python 透過命名慣例、`@property` 裝飾器和 `__slots__` 提供了靈活而強大的封裝機制。

## 延伸閱讀

- [Python Property 官方文件](https://www.google.com/search?q=Python+property+decorator)
- [Python 封裝與私有屬性](https://www.google.com/search?q=Python+encapsulation+name+mangling)
