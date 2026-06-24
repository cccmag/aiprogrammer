# Python 類別與物件

## 類別基礎

```python
class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def bark(self):
        return f"{self.name} says Woof!"

    def get_info(self):
        return f"{self.name} is {self.age} years old"

my_dog = Dog("Buddy", 3)
print(my_dog.bark())
print(my_dog.get_info())
```

## 類別屬性與實例屬性

```python
class Cat:
    species = "Felis catus"  # 類別屬性（所有實例共用）

    def __init__(self, name):
        self.name = name  # 實例屬性

cat1 = Cat("Whiskers")
cat2 = Cat("Fluffy")

print(cat1.species)  # Felis catus
print(cat2.species)  # Felis catus
print(cat1.name)     # Whiskers
```

## 繼承

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        raise NotImplementedError

class Dog(Animal):
    def speak(self):
        return f"{self.name} says Woof!"

class Cat(Animal):
    def speak(self):
        return f"{self.name} says Meow!"

dog = Dog("Buddy")
cat = Cat("Whiskers")
print(dog.speak())
print(cat.speak())
```

## 多重繼承

```python
class Flyable:
    def fly(self):
        return f"{self.name} is flying!"

class Swimmable:
    def swim(self):
        return f"{self.name} is swimming!"

class Duck(Animal, Flyable, Swimmable):
    pass

duck = Duck("Donald")
print(duck.speak())
print(duck.fly())
print(duck.swim())
```

## 魔術方法

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

    def __len__(self):
        return 2

    def __getitem__(self, index):
        return [self.x, self.y][index]

v1 = Vector(1, 2)
v2 = Vector(3, 4)
print(v1 + v2)
print(len(v1))
print(v1[0])
```

## 封裝

```python
class BankAccount:
    def __init__(self, balance):
        self.__balance = balance  # 私有屬性（名稱改編）

    def get_balance(self):
        return self.__balance

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

account = BankAccount(1000)
print(account.get_balance())
account.deposit(500)
print(account.get_balance())
```

## 靜態方法與類別方法

```python
class MathUtils:
    @staticmethod
    def add(a, b):
        return a + b

    @classmethod
    def create_zero_vector(cls, dim):
        return cls([0] * dim)

print(MathUtils.add(1, 2))
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

rect = Rectangle(5, 3)
print(rect.area())
```

## 總結

Python 的 OOP 特性完整且靈活。掌握類別、繼承、魔術方法和封裝，能編寫結構清晰的程式碼。