# 屬性裝飾器與封裝

## 為什麼需要屬性裝飾器？

在傳統 OOP 語言中，封裝通常透過 getter 和 setter 方法實現。Python 的 `@property` 裝飾器提供了一個更優雅的解決方案——讓方法看起來像屬性一樣。

## 從 Getter/Setter 到 Property

### Java 風格（Python 中不推薦）

```python
class Person:
    def __init__(self, name, age):
        self._name = name
        self._age = age

    def get_name(self):
        return self._name

    def set_name(self, value):
        if not value:
            raise ValueError("姓名不可為空")
        self._name = value

p = Person("Alice", 30)
p.set_name("Bob")
print(p.get_name())
```

### Python 風格（使用 @property）

```python
class Person:
    def __init__(self, name, age):
        self._name = name
        self._age = age

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value:
            raise ValueError("姓名不可為空")
        self._name = value

p = Person("Alice", 30)
p.name = "Bob"          # 像屬性一樣賦值
print(p.name)           # 像屬性一樣讀取
```

## Property 的完整形態

`@property` 可以搭配 `@setter` 和 `@deleter`：

```python
class Temperature:
    def __init__(self, celsius=0):
        self._celsius = celsius

    @property
    def celsius(self):
        """攝氏溫度（getter）"""
        print("讀取攝氏溫度")
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        """攝氏溫度（setter）"""
        print(f"設定攝氏溫度為 {value}")
        if value < -273.15:
            raise ValueError("溫度不能低於絕對零度")
        self._celsius = value

    @celsius.deleter
    def celsius(self):
        """攝氏溫度（deleter）"""
        print("刪除攝氏溫度")
        self._celsius = 0

    @property
    def fahrenheit(self):
        """華氏溫度（唯讀）"""
        return self._celsius * 9 / 5 + 32

t = Temperature(25)
print(t.celsius)     # 讀取攝氏溫度 -> 25
t.celsius = 30       # 設定攝氏溫度為 30
print(t.fahrenheit)  # 86.0
del t.celsius        # 刪除攝氏溫度 -> 重設為 0
```

## 計算屬性

Property 可以用於派生屬性（從其他屬性計算得出的值）：

```python
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    @property
    def area(self):
        return self.width * self.height

    @property
    def perimeter(self):
        return 2 * (self.width + self.height)

    @property
    def aspect_ratio(self):
        return self.width / self.height

r = Rectangle(10, 5)
print(f"面積: {r.area}")           # 50
print(f"周長: {r.perimeter}")      # 30
print(f"長寬比: {r.aspect_ratio}") # 2.0
```

## 惰性屬性（Lazy Property）

對於計算成本高的屬性，可以使用惰性求值：

```python
class LazyLoader:
    def __init__(self, url):
        self.url = url
        self._data = None

    @property
    def data(self):
        if self._data is None:
            import time, json, urllib.request
            print(f"正在從 {self.url} 載入資料...")
            time.sleep(1)  # 模擬網路延遲
            with urllib.request.urlopen(self.url) as r:
                self._data = json.loads(r.read())
            print("載入完成")
        return self._data

loader = LazyLoader("https://api.example.com/data")
print("還沒開始載入")
d1 = loader.data  # 第一次：開始載入
d2 = loader.data  # 第二次：直接使用快取
print(d1 is d2)   # True（同一個物件）
```

## 封裝的最佳實踐

### 1. 公開屬性盡量使用 Property

```python
class Product:
    def __init__(self, name, price):
        self.name = name
        self._price = 0
        self.price = price  # 使用 setter

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("價格不能為負數")
        self._price = value

    @property
    def tax(self):
        return self.price * 0.05
```

### 2. 驗證邏輯放在 Setter 中

```python
class EmailAddress:
    def __init__(self, email):
        self._email = ""
        self.email = email  # 觸發驗證

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if "@" not in value or "." not in value.split("@")[-1]:
            raise ValueError(f"無效的電子郵件: {value}")
        self._email = value

e = EmailAddress("alice@example.com")
print(e.email)  # alice@example.com
e.email = "invalid"  # ValueError
```

### 3. 不要過度封裝

不是所有屬性都需要 getter/setter。簡單的公開屬性就直接公開：

```python
# OK：不需要封裝的屬性
class Point:
    def __init__(self, x, y):
        self.x = x  # 直接公開
        self.y = y  # 直接公開

# OK：需要驗證的屬性
class Age:
    def __init__(self, value=0):
        self._value = 0
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        if v < 0 or v > 150:
            raise ValueError(f"無效的年齡: {v}")
        self._value = v
```

## 小結

`@property` 裝飾器是 Python 封裝的核心工具。它讓你可以從簡單的公開屬性開始，當需要驗證或計算邏輯時，無縫切換到方法控制，而不影響外部呼叫程式碼。

## 延伸閱讀

- [Python @property 官方文件](https://www.google.com/search?q=Python+property+decorator)
- [Python 封裝指南](https://www.google.com/search?q=Python+encapsulation+best+practices)
