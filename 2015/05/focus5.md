# 主題五：物件導向程式設計

## 類別基礎

### 定義類別

```python
class Person:
    """人類別"""

    def __init__(self, name, age):
        """建構函式"""
        self.name = name
        self.age = age

    def greet(self):
        """問候方法"""
        return f"你好，我是{self.name}"

    def birthday(self):
        """生日"""
        self.age += 1
        return f"生日快樂！現在是 {self.age} 歲"

# 創建物件
person = Person("張小明", 28)
print(person.greet())
print(person.birthday())
```

### self 參數

`self` 代表類別的實例本身，類似於其他語言中的 `this`：

```python
class Counter:
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1
        return self.count

c1 = Counter()
c2 = Counter()

c1.increment()
c1.increment()
print(c1.count)  # 2
print(c2.count)  # 0（各自獨立）
```

## 屬性與方法

### 實例屬性

```python
class Dog:
    def __init__(self, name, breed):
        self.name = name      # 實例屬性
        self.breed = breed

    def bark(self):
        return f"{self.name} 說：汪汪！"
```

### 類別屬性

```python
class Dog:
    species = "犬科"  # 類別屬性，所有實例共享

    def __init__(self, name, breed):
        self.name = name
        self.breed = breed

dog1 = Dog("小黑", "狼犬")
dog2 = Dog("小白", "貴賓")

print(dog1.species)  # 犬科
print(dog2.species)  # 犬科

Dog.species = "哺乳動物"
print(dog1.species)  # 哺乳動物（所有實例都改變）
```

### 方法類型

```python
class MyClass:
    class_attr = "類別屬性"

    def __init__(self, value):
        self.value = value    # 實例屬性

    def instance_method(self):
        """實例方法"""
        return f"實例方法，value={self.value}"

    @classmethod
    def class_method(cls):
        """類別方法"""
        return f"類別方法，class_attr={cls.class_attr}"

    @staticmethod
    def static_method():
        """靜態方法"""
        return "靜態方法，不需要實例"
```

## 封裝

### 私有屬性

Python 使用命名慣例來表示私有屬性：

```python
class BankAccount:
    def __init__(self, balance):
        self.__balance = balance  # 私有屬性（名稱重整）

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            return True
        return False

    def withdraw(self, amount):
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            return True
        return False

    def get_balance(self):
        return self.__balance

account = BankAccount(1000)
account.deposit(500)
print(account.get_balance())  # 1500

# 無法直接存取 __balance
# print(account.__balance)  # AttributeError
```

### 屬性裝飾器

```python
class Person:
    def __init__(self, name):
        self.__name = name

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if value:
            self.__name = value

    @name.deleter
    def name(self):
        del self.__name

person = Person("張小明")
print(person.name)    # 呼叫 getter
person.name = "李小華"  # 呼叫 setter
```

## 繼承

### 基本繼承

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return "..."

class Dog(Animal):
    def speak(self):
        return f"{self.name} 說：汪汪！"

class Cat(Animal):
    def speak(self):
        return f"{self.name} 說：喵喵！"

dog = Dog("小黑")
cat = Cat("小咪")
print(dog.speak())  # 小黑說：汪汪！
print(cat.speak())  # 小咪說：喵喵！
```

### 多層繼承

```python
class Pet(Dog):
    def play(self):
        return f"{self.name} 在玩玩具"

pet = Pet("小白")
print(pet.speak())   # 來自 Dog 類別
print(pet.play())    # 來自 Pet 類別
print(pet.name)      # 來自 Animal 類別
```

### super() 函式

```python
class Animal:
    def __init__(self, name):
        self.name = name

class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)  # 呼叫父類別建構函式
        self.breed = breed

    def speak(self):
        return f"{self.name}（{self.breed}）說：汪汪！"
```

### 多重繼承

```python
class A:
    def method(self):
        return "A"

class B:
    def method(self):
        return "B"

class C(A, B):
    pass

c = C()
print(c.method())  # A（優先使用第一個父類別的方法）
```

## 多型

```python
class Shape:
    def area(self):
        raise NotImplementedError

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14159 * self.radius ** 2

shapes = [Rectangle(5, 3), Circle(2)]
for shape in shapes:
    print(shape.area())  # 多型：同一介面，不同實作
```

## 特殊方法

### 魔術方法

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Vector({self.x}, {self.y})"

    def __repr__(self):
        return f"Vector({self.x!r}, {self.y!r})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __len__(self):
        return 2

    def __getitem__(self, index):
        return [self.x, self.y][index]

v1 = Vector(1, 2)
v2 = Vector(3, 4)
print(v1 + v2)  # Vector(4, 6)
print(len(v1))  # 2
```

### 其他常用特殊方法

```python
__init__      # 初始化
__str__       # str() 轉換
__repr__      # 開發者表示
__eq__        # ==
__ne__        # !=
__lt__, __le__, __gt__, __ge__  # <, <=, >, >=
__add__, __sub__, __mul__, __div__  # +, -, *, /
__call__      # 讓實例可呼叫
__iter__      # 迭代支援
__next__      # 下一個元素
__enter__, __exit__  # with 語句支援
```

## 抽象類別

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

    @abstractmethod
    def perimeter(self):
        pass

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

# 無法直接實例化抽象類別
# shape = Shape()  # TypeError

rect = Rectangle(5, 3)
print(rect.area())  # 15
```

## 結論

Python 的物件導向程式設計提供了完整的 OOP 特性，包括封裝、繼承、多型。善用這些特性可以寫出結構良好的程式碼。