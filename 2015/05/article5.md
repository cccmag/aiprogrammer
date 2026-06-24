# namedtuple 與 dataclasses

## namedtuple

`namedtuple` 是 Python 標準庫 `collections` 中的一個工廠函式，用於創建類似元組但帶有欄位名稱的類別。

### 基本用法

```python
from collections import namedtuple

# 定義 namedtuple
Point = namedtuple('Point', ['x', 'y'])

# 創建實例
p = Point(10, 20)

# 透過欄位名存取
print(p.x, p.y)  # 10 20

# 透過索引存取
print(p[0], p[1])  # 10 20

# 解包
x, y = p
print(x, y)  # 10 20
```

### 為何使用 namedtuple

```python
# 普通元組：需要記住位置含義
point = (10, 20)
print(point[0], point[1])  # 需要知道 0 是 x，1 是 y

# namedtuple：欄位有意義的名稱
Point = namedtuple('Point', ['x', 'y'])
point = Point(10, 20)
print(point.x, point.y)  # 名稱明確
```

### 預設值

```python
from collections import namedtuple

# 使用 defaults 參數（Python 3.7+）
User = namedtuple('User', ['name', 'age', 'city'], defaults=['Unknown', 0, 'Unknown'])
user = User(name="張小明")
print(user)  # User(name='張小明', age=0, city='Unknown')
```

### _replace 方法

```python
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])
p = Point(10, 20)

# 創建修改後的副本（Immutable）
p2 = p._replace(x=30)
print(p)   # Point(x=10, y=20) - 不變
print(p2)  # Point(x=30, y=20)
```

### 使用情境

```python
# 座標系統
Coordinate = namedtuple('Coordinate', ['latitude', 'longitude'])

# 顏色
Color = namedtuple('Color', ['red', 'green', 'blue'])
white = Color(255, 255, 255)

# 學生記錄
Student = namedtuple('Student', ['name', 'id', 'gpa'])
student = Student('王小美', 'S12345', 3.8)
```

## dataclasses（Python 3.7+）

`dataclass` 是 Python 3.7 引入的新功能，自動生成 `__init__`、`__repr__`、`__eq__` 等特殊方法。

### 基本用法

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: int
    y: int

p = Point(10, 20)
print(p)  # Point(x=10, y=20)
print(p.x, p.y)  # 10 20
```

### 自動生成方法

```python
from dataclass import dataclass

@dataclass
class User:
    name: str
    age: int
    email: str

# 自動生成 __init__
user = User("張小明", 28, "zhang@example.com")

# 自動生成 __repr__
print(user)  # User(name='張小明', age=28, email='zhang@example.com')

# 自動生成 __eq__
user2 = User("張小明", 28, "zhang@example.com")
print(user == user2)  # True
```

### 預設值

```python
from dataclasses import dataclass, field

@dataclass
class Product:
    name: str
    price: float
    quantity: int = 0
    discount: float = 0.0

# 創建實例
p = Product("筆記型電腦", 45000)
print(p)  # Product(name='筆記型電腦', price=45000, quantity=0, discount=0.0)
```

### 巢狀 dataclass

```python
from dataclasses import dataclass
from typing import List

@dataclass
class Address:
    city: str
    district: str
    zip_code: str

@dataclass
class Person:
    name: str
    address: Address
    hobbies: List[str] = field(default_factory=list)

address = Address("台北市", "大安區", "106")
person = Person("張小明", address, ["閱讀", "游泳"])

print(person.name)  # 張小明
print(person.address.city)  # 台北市
```

### 欄位選項

```python
from dataclasses import dataclass, field

@dataclass
class Employee:
    id: int
    name: str
    email: str = field(repr=False)  # 不在 repr 中顯示
    salary: float = field(compare=False)  # 不參與比較
    active: bool = field(default=True)

emp = Employee(1, "王小明", "wang@example.com", 50000)
print(repr(emp))  # Employee(id=1, name='王小小明', email='...') 可能因 repr=False 而不顯示
```

### 比較

| 特性 | namedtuple | dataclass |
|------|------------|-----------|
| 不可變性 | 預設不可變 | 需加 `@dataclass(frozen=True)` |
| 類型提示 | 需要 | 需要 |
| 自動方法 | 有限 | 完整 |
| 繼承 | 複雜 | 簡單 |
| 記憶體 | 較小 | 稍大 |
| Python 版本 | 2.6+ | 3.7+ |

## 選擇建議

使用 `namedtuple`：
- 需要輕量、不可變的資料結構
- 類似於結構體的簡單用途
- 需要元組的全部特性（解包等）

使用 `dataclass`：
- 需要更多自訂行為
- 需要巢狀結構
- 需要可變資料
- 需要多種自動方法