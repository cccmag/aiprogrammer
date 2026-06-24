# 3. Type Hints 型態提示

## 型態提示概述

Type Hints（型態提示）於 Python 3.5 引入，Python 3.7 使其更加成熟。型態提示允許開發者為變數、函數參數與回傳值指定型別，靜態分析工具可以在執行前發現型別錯誤。

## 基本語法

### 變數型態

```python
from typing import List, Dict, Optional

name: str = "Alice"
age: int = 30
scores: List[int] = [90, 85, 88]
config: Dict[str, str] = {"theme": "dark"}
maybe_value: Optional[str] = None
```

### 函數型態

```python
def greet(name: str) -> str:
    return f"Hello, {name}"

def process_numbers(numbers: List[int]) -> int:
    return sum(numbers)

def find_item(
    items: List[str],
    target: str
) -> Optional[int]:
    try:
        return items.index(target)
    except ValueError:
        return None
```

## 常用型態

### Any 和 Union

```python
from typing import Any, Union

def flexible(arg: Any) -> Any:
    return arg

def int_or_str(value: Union[int, str]) -> str:
    return str(value)
```

### Callable

```python
from typing import Callable

def apply(func: Callable[[int], int], value: int) -> int:
    return func(value)

result = apply(lambda x: x * 2, 5)  # 10
```

### TypeVar 泛型

```python
from typing import TypeVar

T = TypeVar('T')

def first(items: List[T]) -> Optional[T]:
    return items[0] if items else None

name = first(["a", "b", "c"])  # type: str
```

## Dataclass 與型態

```python
from dataclasses import dataclass
from typing import List

@dataclass
class Student:
    name: str
    age: int
    courses: List[str]

student = Student("Bob", 20, ["Math", "Physics"])
print(student)
```

## 執行時型態檢查

```python
from typing import get_type_hints

def add(a: int, b: int) -> int:
    return a + b

hints = get_type_hints(add)
print(hints)  # {'a': <class 'int'>, 'b': <class 'int'>, 'return': <class 'int'>}
```

## 靜態分析工具

### mypy

```bash
pip install mypy

# 執行型態檢查
mypy my_script.py
```

### Pyright

```bash
npm install -g pyright

pyright my_script.py
```

## 與 IDE 整合

主流 IDE（VS Code、PyCharm）支援型態提示，可以提供：
- 即時型態檢查
- 自動完成建議
- 參照溯源

## 參考資源

- https://www.google.com/search?q=Python+type+hints+mypy+tutorial+2019+static+analysis
- https://www.google.com/search?q=Python+typing+TypeVar+Callable+Generic+2019
- https://www.google.com/search?q=Python+type+hints+best+practices+dataclass+2019