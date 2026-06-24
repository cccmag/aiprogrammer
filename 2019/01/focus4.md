# 4. Dataclasses 資料類別

## Dataclass 概述

Python 3.7 引入的 `@dataclass` 裝飾器大幅簡化了資料類別的建立。dataclass 自動生成 `__init__`、`__repr__`、`__eq__`、`__hash__` 等方法，減少了樣板程式碼。

## 基本用法

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float

p = Point(1.0, 2.0)
print(p)           # Point(x=1.0, y=2.0)
print(p.x, p.y)     # 1.0 2.0
```

## 自動生成方法

```python
from dataclasses import dataclass

@dataclass
class Employee:
    name: str
    department: str
    salary: float

e1 = Employee("Alice", "Engineering", 90000)
e2 = Employee("Bob", "Marketing", 75000)

print(e1)
# Employee(name='Alice', department='Engineering', salary=90000)

print(e1 == e1)      # True（自動生成 __eq__）
print(e1 == e2)      # False
```

## 欄位預設值

```python
from dataclasses import dataclass, field

@dataclass
class User:
    name: str
    email: str
    active: bool = True
    roles: list = field(default_factory=list)

user = User("Carol", "carol@example.com")
print(user)
# User(name='Carol', email='carol@example.com', active=True, roles=[])
```

## 欄位選項

```python
from dataclasses import dataclass, field

@dataclass
class Config:
    name: str
    timeout: int = 30
    max_retries: int = field(default=3, repr=False)
    optional: str = field(default="", compare=False)

config = Config("myapp")
print(config)
# Config(name='myapp', timeout=30, optional='')
```

## Frozen（不可變）Dataclass

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class ImmutablePoint:
    x: float
    y: float

p = ImmutablePoint(1.0, 2.0)
# p.x = 3.0  # FrozenInstanceError: cannot assign to field 'x'
```

## 繼承

```python
from dataclasses import dataclass

@dataclass
class Animal:
    name: str
    age: int

@dataclass
class Dog(Animal):
    breed: str
    commands: list = field(default_factory=list)

dog = Dog("Buddy", 3, "Golden Retriever", ["sit", "stay"])
print(dog)
# Dog(name='Buddy', age=3, breed='Golden Retriever', commands=[])
```

## 與 NamedTuple 比較

```python
from dataclasses import dataclass
from typing import NamedTuple

# NamedTuple
class PointNT(NamedTuple):
    x: float
    y: float

# Dataclass
@dataclass
class PointDC:
    x: float
    y: float

# Dataclass 可以有預設值、mutable 欄位
# NamedTuple 是不可變的，較輕量
```

## post_init 初始化

```python
from dataclasses import dataclass, field

@dataclass
class Circle:
    radius: float
    center_x: float
    center_y: float
    area: float = field(init=False)

    def __post_init__(self):
        import math
        self.area = math.pi * self.radius ** 2

c = Circle(1.0, 0.0, 0.0)
print(f"Area: {c.area}")  # 3.14159...
```

## 參考資源

- https://www.google.com/search?q=Python+dataclass+tutorial+2019+@dataclass+fields
- https://www.google.com/search?q=Python+dataclass+vs+namedtuple+frozen+2019+comparison
- https://www.google.com/search?q=Python+dataclass+best+practices+post_init+field+default_factory