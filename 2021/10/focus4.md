# 類型標註與 mypy 靜態檢查

## 為何需要靜態類型？

Python 的動態類型帶來靈活性，但也增加了執行時錯誤的風險。類型標註允許在程式碼中明確聲明預期類型，而靜態類型檢查工具可以在執行前發現類型錯誤。

## 基本類型標註

```python
def greet(name: str) -> str:
    return f"Hello, {name}"

def add(a: int, b: int) -> int:
    return a + b

def process_items(items: list[str]) -> dict[str, int]:
    return {item: len(item) for item in items}
```

Python 3.5 引入類型標註語法，3.9+ 提供了更多內建類型的支援。

## Optional 和 Union

```python
from typing import Optional, Union

def find_user(user_id: int) -> Optional[dict]:
    """找不到時返回 None"""
    return users.get(user_id)

def parse_value(value: Union[str, int, float]) -> float:
    """支援多種輸入類型"""
    return float(value)
```

Python 3.10+ 支援更简洁的語法：`str | int` 等價於 `Union[str, int]`。

## 複雜類型

```python
from typing import TypeVar, Generic, Callable, Iterator

T = TypeVar('T')

class Stack(Generic[T]):
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()

def apply_func(f: Callable[[int], str], x: int) -> str:
    return f(x)
```

## mypy 安裝與使用

```bash
pip install mypy
mypy my_module.py
```

mypy 會分析程式碼並報告類型錯誤，無需執行代碼。

## 配置與嚴格模式

`mypy.ini` 或 `pyproject.toml` 中可以配置檢查級別：

```ini
[mypy]
python_version = 3.9
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
```

嚴格模式要求所有函式都有類型標註，適合新專案。

## 與既有程式碼共存

mypy 支援逐漸遷移到類型標註。可以從寬鬆模式開始，逐步嚴格化：

```python
from typing import ignore

def legacy_function(x):
    # type: (Any) -> Any
    return x  # type: ignore
```

## 類型標註的好處

除了靜態檢查，類型標註還能改善 IDE 支援（自動完成、定義跳轉）、提高程式碼可讀性、做為文件使用。配合 mypy，能在開發早期發現大量錯誤。