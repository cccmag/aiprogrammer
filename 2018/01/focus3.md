# 型別提示與型別檢查

## 簡介

Python 是動態型別語言，但 Python 3.5 引入了型別提示（Type Hints），Python 3.6 進一步增強了這項功能。型別提示讓程式設計師可以明確標註變數、函式參數和回傳值的預期型別。

## 基本語法

### 變數型別提示

```python
name: str = "Alice"
age: int = 30
height: float = 165.5
is_student: bool = False

# 巢狀型別
scores: list = [90, 85, 88]
info: dict = {"name": "Bob", "age": 25}
data: tuple = (1, 2, 3)
```

### 函式型別提示

```python
def greet(name: str) -> str:
    return f"Hello, {name}!"

def add(a: int, b: int) -> int:
    return a + b

def process_data(data: list, factor: float) -> dict:
    return {"result": sum(data) * factor}
```

### 可選型別

```python
from typing import Optional, List, Dict

def find_user(user_id: int) -> Optional[str]:
    if user_id > 0:
        return "found"
    return None

def parse_list(items: List[str]) -> List[int]:
    return [len(item) for item in items]
```

## typing 模組

### 常見型別

```python
from typing import List, Dict, Set, Tuple, Optional, Union, Any, Callable

# List[int] 表示整數列表
numbers: List[int] = [1, 2, 3]

# Dict[str, int] 表示鍵為字串、值為整數的字典
ages: Dict[str, int] = {"Alice": 30, "Bob": 25}

# Union 表示多種可能型別
Id = Union[int, str]

# Any 表示任意型別
def log(message: Any): ...
```

### Callable（函式型別）

```python
from typing import Callable

def apply(func: Callable[[int, int], int], a: int, b: int) -> int:
    return func(a, b)

result = apply(lambda x, y: x + y, 3, 4)  # 7
```

### TypeVar（泛型）

```python
from typing import TypeVar

T = TypeVar('T')

def first(lst: List[T]) -> Optional[T]:
    return lst[0] if lst else None
```

## 執行時的型別檢查

```python
def greet(name: str) -> str:
    if not isinstance(name, str):
        raise TypeError("name must be a string")
    return f"Hello, {name}!"
```

## 型別檢查工具

### mypy

```bash
pip install mypy
mypy your_module.py
```

### pyright

```bash
npm install -g pyright
pyright your_module.py
```

### 範例輸出

```python
# example.py
def add(a: int, b: int) -> int:
    return a + b

result = add("1", "2")  # mypy 會報錯
```

```bash
$ mypy example.py
example.py:5: error: Argument 1 to "add" has incompatible type "str"; expected "int"
```

## 型別提示的優點

1. **提高程式碼可讀性** - 明確標注預期型別
2. **及早發現錯誤** - 靜態檢查可發現潛在 bug
3. **更好的 IDE 支援** - 自動完成與錯誤提示
4. **文件化作用** - 作為程式碼文件的一部分
5. **重構幫助** - 更容易理解介面

## 注意事項

- 型別提示是可选的，不會影響程式執行
- 不當的型別提示不會引發執行錯誤
- 建議使用 mypy 或 pyright 進行檢查