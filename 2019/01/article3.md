# Dataclass 進階用法

## Frozen 不可變資料類別

frozen=True 使資料類別不可修改：

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Point:
    x: float
    y: float

p = Point(1.0, 2.0)
# p.x = 3.0  # FrozenInstanceError
```

## field 工廠函數

使用 field() 自訂欄位行為：

```python
from dataclasses import dataclass, field
from typing import List

@dataclass
class Team:
    name: str
    members: List[str] = field(default_factory=list)
    active: bool = True

team = Team("Engineering")
team.members.append("Alice")
print(team)
```

## compare 與 repr 選項

```python
from dataclasses import dataclass, field

@dataclass
class Config:
    name: str
    # 不參與比較
    secret: str = field(default="", compare=False)
    # 不顯示在 repr
    internal_id: int = field(default=0, repr=False)

config = Config("app", secret="xyz", internal_id=123)
print(config)  # Config(name='app', secret='xyz')
print(config == Config("app", "xyz", 0))  # True（忽略 internal_id）
```

## post_init 初始化

在 __post_init__ 中進行額外初始化：

```python
from dataclasses import dataclass, field

@dataclass
class Circle:
    radius: float
    center_x: float
    center_y: float
    # 自動計算的欄位
    area: float = field(init=False)

    def __post_init__(self):
        import math
        self.area = math.pi * self.radius ** 2

c = Circle(1.0, 0.0, 0.0)
print(f"Area: {c.area:.2f}")  # 3.14
```

## 繼承

dataclass 支援繼承：

```python
from dataclasses import dataclass, field

@dataclass
class Animal:
    name: str
    age: int

@dataclass
class Dog(Animal):
    breed: str
    commands: List[str] = field(default_factory=list)

dog = Dog("Buddy", 3, "Golden Retriever", ["sit", "stay"])
print(dog.name)  # Buddy
```

## 自動方法

@dataclass 自動生成：
- __init__
- __repr__
- __eq__
- __hash__（如果 frozen=True）

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float

p1 = Point(1.0, 2.0)
p2 = Point(1.0, 2.0)
print(p1 == p2)  # True（自動生成 __eq__）
print(hash(p1))  # 可雜湊
```

## 與 namedtuple 比較

```python
from dataclasses import dataclass
from typing import NamedTuple

# NamedTuple - 不可變、較輕量
class PointNT(NamedTuple):
    x: float
    y: float

# Dataclass - 可變、可自訂
@dataclass
class PointDC:
    x: float
    y: float

# NamedTuple 不能有方法，Dataclass 可以
@dataclass
class PointWithMethod:
    x: float
    y: float

    def distance_from_origin(self) -> float:
        return (self.x**2 + self.y**2) ** 0.5
```

## 實際應用：資料傳輸物件

```python
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class UserDTO:
    id: int
    username: str
    email: str
    created_at: datetime
    is_active: bool = True
    bio: Optional[str] = None

user = UserDTO(
    id=1,
    username="alice",
    email="alice@example.com",
    created_at=datetime.now()
)
```

## 參考資源

- https://www.google.com/search?q=Python+dataclass+frozen+field+tutorial+advanced+2019
- https://www.google.com/search?q=Python+dataclass+post_init+inheritance+examples+2019
- https://www.google.com/search?q=Python+dataclass+vs+namedtuple+performance+comparison+2019