# Type Hints 實戰

## 型態提示基礎

Type Hints 讓 Python 程式碼更加清晰，靜態分析工具可以在執行前發現錯誤：

```python
def add_numbers(a: int, b: int) -> int:
    return a + b

result: int = add_numbers(1, 2)
```

## 常用類型

### 簡單類型

```python
name: str = "Alice"
age: int = 30
height: float = 5.6
is_active: bool = True
```

### 集合類型

```python
from typing import List, Dict, Set, Tuple

names: List[str] = ["Alice", "Bob", "Carol"]
ages: Dict[str, int] = {"Alice": 30, "Bob": 25}
unique_ids: Set[int] = {1, 2, 3}
point: Tuple[int, int] = (10, 20)
```

### 可選類型

```python
from typing import Optional

def find_user(user_id: int) -> Optional[str]:
    users = {1: "Alice", 2: "Bob"}
    return users.get(user_id)
```

## 函數型別

```python
from typing import Callable

def apply_function(
    func: Callable[[int], int],
    value: int
) -> int:
    return func(value)

result = apply_function(lambda x: x * 2, 5)
```

## 泛型

```python
from typing import TypeVar, Generic

T = TypeVar('T')

class Stack(Generic[T]):
    def __init__(self) -> None:
        self._items: List[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()

stack: Stack[int] = Stack()
stack.push(1)
```

## Protocol 結構化子類型

```python
from typing import Protocol

class Renderable(Protocol):
    def render(self) -> str:
        ...

def render_all(items: List[Renderable]) -> None:
    for item in items:
        print(item.render())
```

## 與 dataclass 整合

```python
from dataclasses import dataclass
from typing import List

@dataclass
class Student:
    name: str
    age: int
    courses: List[str]

student = Student("Bob", 20, ["Math", "Physics"])
```

## 靜態檢查工具

### mypy

```bash
# 安裝
pip install mypy

# 檢查
mypy my_script.py

# 嚴格模式
mypy --strict my_script.py
```

### Pyright

```bash
# 安裝
npm install -g pyright

# 檢查
pyright my_script.py
```

## 實際應用

```python
from typing import List, Optional

def process_data(
    raw_data: List[dict],
    filter_key: str,
    limit: Optional[int] = None
) -> List[dict]:
    filtered = [
        item for item in raw_data
        if filter_key in item
    ]
    if limit:
        filtered = filtered[:limit]
    return filtered
```

## 參考資源

- https://www.google.com/search?q=Python+type+hints+mypy+tutorial+static+analysis+2019
- https://www.google.com/search?q=Python+typing+TypeVar+Protocol+Generic+advanced+2019
- https://www.google.com/search?q=Python+type+hints+best+practices+dataclass+Real+world+2019