# 物件導向程式設計

## 簡介

物件導向程式設計（OOP）是一種程式設計典範，透過「類別」和「物件」來組織程式碼。Python 是多典範語言，完全支援 OOP。

## 類別與物件

### 定義類別

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        return f"Hello, I'm {self.name}"

# 建立物件
person = Person("Alice", 30)
print(person.name)    # Alice
print(person.greet()) # Hello, I'm Alice
```

### self 參數

self 指的是類別實體本身，類似其他語言的 this。

## 屬性與方法

### 實例屬性

```python
class Dog:
    def __init__(self, name, breed):
        self.name = name    # 實例屬性
        self.breed = breed

    def bark(self):          # 實例方法
        return f"{self.name} says woof!"
```

### 類別屬性

```python
class Dog:
    species = "Canis lupus familiaris"  # 類別屬性

    def __init__(self, name):
        self.name = name

print(Dog.species)  # 所有 Dog 實例共享
dog1 = Dog("Buddy")
dog2 = Dog("Max")
print(dog1.species)  # Canis lupus familiaris
print(dog2.species)
```

### 靜態方法與類別方法

```python
class MathUtil:
    @staticmethod
    def add(a, b):
        return a + b

    @classmethod
    def create_double(cls, value):
        return cls(value * 2)

print(MathUtil.add(3, 4))        # 7
```

## 封裝

### 私有屬性

```python
class BankAccount:
    def __init__(self, balance):
        self.__balance = balance  # 私有屬性（名稱重整）

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
print(account.get_balance())  # 1000
account.deposit(500)
print(account.get_balance())  # 1500
```

## 繼承

### 基本繼承

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        raise NotImplementedError

class Dog(Animal):
    def speak(self):
        return f"{self.name} says woof!"

class Cat(Animal):
    def speak(self):
        return f"{self.name} says meow!"

dog = Dog("Buddy")
cat = Cat("Whiskers")
print(dog.speak())  # Buddy says woof!
print(cat.speak())  # Whiskers says meow!
```

### 多層繼承

```python
class Pet(Dog):  # Dog 已有 Animal 的特性
    def __init__(self, name, owner):
        super().__init__(name)  # 呼叫父類別建構子
        self.owner = owner

pet = Pet("Max", "Alice")
print(pet.name)   # Max
print(pet.owner)  # Alice
```

### 多重繼承

```python
class Flyer:
    def fly(self):
        return "Flying!"

class Swimmer:
    def swim(self):
        return "Swimming!"

class Duck(Animal, Flyer, Swimmer):
    pass

duck = Duck("Donald")
print(duck.speak())  # Donald says quack!
print(duck.fly())    # Flying!
print(duck.swim())   # Swimming!
```

## 多型

```python
def make_them_speak(animals):
    for animal in animals:
        print(animal.speak())

animals = [Dog("Buddy"), Cat("Whiskers"), Dog("Max")]
make_them_speak(animals)
```

## 特殊方法

### __str__ 與 __repr__

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Point({self.x}, {self.y})"

    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"

p = Point(3, 4)
print(str(p))   # Point(3, 4)
print(repr(p))  # Point(x=3, y=4)
```

### 運算子過載

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

v1 = Vector(1, 2)
v2 = Vector(3, 4)
v3 = v1 + v2
print(v3.x, v3.y)  # 4, 6
```

## 練習題

1. 設計一個 Stack 類別，支援 push、pop、is_empty 操作
2. 設計一個計數器類別，限制最大計數值
3. 設計一個動物園類別，管理多個動物