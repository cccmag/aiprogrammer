# Python 類型檢查：mypy 實戰

## 前言

Python 是動態類型語言，但這不代表我們不能享受型別安全的好處。mypy 提供了可選的靜態類型檢查，讓我們能在開發時發現類型相關的錯誤，同時保持 Python 的靈活性。

## 為什麼需要類型檢查？

### 動態類型的問題

```python
# 沒有類型提示時
def process_data(data):
    return data.lower()  # 如果 data 是數字，執行時才會錯誤

result = process_data(123)  # 運行時錯誤！
```

### 類型提示的好處

```python
from typing import List

def process_data(data: str) -> str:
    return data.lower()

# 靜態分析工具可以提前發現問題
result = process_data(123)  # mypy 會報錯！
```

## 開始使用 mypy

### 安裝

```bash
pip install mypy
```

### 基本使用

```bash
# 檢查檔案
mypy mymodule.py

# 檢查整個目錄
mypy src/

# 嚴格模式
mypy --strict mymodule.py
```

### 忽略某些檔案

```ini
# setup.cfg 或 mypy.ini
[mypy]
python_version = 3.8
warn_return_any = True
warn_unused_configs = True
ignore_missing_imports = True

[mypy-tests.*]
ignore_errors = True
```

## 類型標註語法

### 基本類型

```python
from typing import List, Dict, Set, Tuple, Optional

# 變數類型標註
name: str = "Alice"
age: int = 30
score: float = 98.5
is_active: bool = True

# 容器類型
names: List[str] = ["Alice", "Bob"]
scores: Dict[str, int] = {"Alice": 90, "Bob": 85}
unique_ids: Set[int] = {1, 2, 3}
coordinates: Tuple[float, float] = (10.5, 20.3)

# 可選類型
middle_name: Optional[str] = None
# 或使用 Union
from typing import Union
result: Union[str, None] = None
```

### 函數類型標註

```python
from typing import List

def greet(name: str) -> str:
    return f"Hello, {name}!"

def add_numbers(a: int, b: int) -> int:
    return a + b

def process_list(items: List[int]) -> List[int]:
    return [x * 2 for x in items]

def find_item(items: List[str], target: str) -> Optional[int]:
    for i, item in enumerate(items):
        if item == target:
            return i
    return None
```

### Callable 和其他高階類型

```python
from typing import Callable, Iterator, Generator

# 可呼叫物件
def apply_func(func: Callable[[int], int], value: int) -> int:
    return func(value)

# 迭代器和生成器
def fibonacci(n: int) -> Iterator[int]:
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

def generate_squares(count: int) -> Generator[int, None, None]:
    for i in range(count):
        yield i ** 2
```

### 自訂類別

```python
class User:
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age
    
    def greet(self) -> str:
        return f"Hello, I'm {self.name}"

def create_user(name: str, age: int) -> User:
    return User(name, age)

user: User = create_user("Alice", 30)
```

## 整合到開發流程

### CI/CD 中整合 mypy

```yaml
# .github/workflows/type-check.yml
name: Type Check

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  mypy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.8'
      - name: Install mypy
        run: pip install mypy
      - name: Run mypy
        run: mypy src/
```

### VS Code 整合

```json
// .vscode/settings.json
{
    "python.linting.enabled": true,
    "python.linting.mypyEnabled": true,
    "python.linting.mypyArgs": ["--strict", "--ignore-missing-imports"],
    "python.formatting.provider": "black"
}
```

### 逐步遷移現有專案

```ini
# 從寬鬆開始，逐漸嚴格
[mypy]
python_version = 3.8
ignore_missing_imports = True

# 或在特定檔案加入
# mypy: ignore-errors
```

## 常見問題和解決方案

### 第三方庫沒有類型標註

```python
# 使用 stub 檔案
# types-requests.pyi
from typing import Any
def get(url: str, **kwargs: Any) -> Any: ...

# 或使用 cast
from typing import cast
import some_library
result = cast(SomeType, some_library.some_function())
```

### 動態特性

```python
from typing import Any

# 當你需要繞過類型檢查時
value: Any = some_dynamic_value
value.any_method()  # 不會報錯

# 或使用 # type: ignore
result = some_function()  # type: ignore
```

### 泛型

```python
from typing import TypeVar, Generic, List

T = TypeVar('T')

class Stack(Generic[T]):
    def __init__(self) -> None:
        self._items: List[T] = []
    
    def push(self, item: T) -> None:
        self._items.append(item)
    
    def pop(self) -> T:
        return self._items.pop()
    
    def is_empty(self) -> bool:
        return len(self._items) == 0

# 使用
stack: Stack[int] = Stack()
stack.push(42)
```

## 延伸閱讀

- [mypy 官方文件](https://www.google.com/search?q=mypy+Python+static+typing+documentation)
- [Python typing 模块](https://www.google.com/search?q=Python+typing+module+documentation)
- [mypy 配置文件](https://www.google.com/search?q=mypy+configuration+file+setup)
- [Python typing 教程](https://www.google.com/search?q=Python+type+hints+tutorial+mypy)

---

*本篇文章為「AI 程式人雜誌 2020 年 10 月號」文章集錦之一。*