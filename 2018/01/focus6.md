# 型別提示工具鏈

## 簡介

Python 的型別提示需要配合靜態型別檢查工具才能發揮最大效用。本篇介紹 Python 生態系中最常用的型別檢查工具：mypy、pyright 以及 IDE 整合。

## mypy

### 簡介

mypy 是 Python 官方開發的靜態型別檢查器，由 Dropbox 資助開發，是目前最廣泛使用的 Python 型別檢查工具。

### 安裝

```bash
pip install mypy
```

### 基本使用

```bash
mypy your_module.py
mypy your_directory/
```

### 範例

```python
# example.py
def add(a: int, b: int) -> int:
    return a + b

print(add("1", "2"))  # 型別錯誤
```

```bash
$ mypy example.py
example.py:5: error: Argument 1 to "add" has incompatible type "str"; expected "int"
```

### 配置文件

```ini
# mypy.ini
[mypy]
python_version = 3.6
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
```

### 嚴格模式

```bash
mypy --strict your_module.py
```

## pyright

### 簡介

pyright 由 Microsoft 開發，是一個快速的 Python 型別檢查器，使用 TypeScript 編寫，可作為 VS Code 擴展或命令行工具。

### 安裝

```bash
npm install -g pyright
```

### 基本使用

```bash
pyright your_module.py
```

### 功能特點

- 極快的檢查速度
- 完整的 PEP 484 支援
- 智慧型錯誤訊息
- 可自訂規則

## 第三方型別擴展

### typing_extensions

```bash
pip install typing_extensions
```

```python
from typing_extensions import Literal, TypedDict

Mode = Literal["r", "w", "a"]
```

### attrs

```bash
pip install attrs
```

```python
from attrs import define, field

@define
class Point:
    x: int
    y: int
    label: str = ""

p = Point(1, 2, label="origin")
```

### pydantic

```bash
pip install pydantic
```

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int
    email: str | None = None

user = User(name="Alice", age=30)
```

## IDE 整合

### VS Code

推薦擴展：

- Python（Microsoft）- 完整 Python 支援
- Pylance - 基於 pyright 的語言伺服器
- mypy-type-checker - mypy VS Code 整合

### PyCharm

PyCharm 內建對型別提示的支援，提供：

- 即時型別檢查
- 自動完成
- 快速修復建議

### 編輯器設定

```json
{
    "python.analysis.typeCheckingMode": "basic",
    "python.analysis.autoImportComplete": true
}
```

## 熱門庫的型別支援

### 已完全支援

- numpy
- pandas
- django
- flask
- requests
- pytest

### 部分支援

```python
# 使用 TYPE_CHECKING 避免循環導入
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from some_module import SomeType

def func(x: "SomeType") -> None: ...
```

## 遷移策略

### 1. 增量遷移

```bash
mypy --ignore-missing-imports your_module.py
```

### 2. 嚴格度逐步提升

```python
# 逐步新增型別
def process(data):
    # 階段1: 不知道型別
    return data

def process(data: list):
    # 階段2:只知道列表類型
    return data

def process(data: list[int]) -> int:
    # 階段3:完整型別
    return sum(data)
```

### 3. 第三方庫型別存根

```bash
pip install types-requests
pip install types-Pillow
```

## 最佳實踐

1. **從新專案開始** - 新專案直接使用完整型別提示
2. **使用 strict 模式** - 盡可能開啟嚴格檢查
3. **善用 ignore comments** - 特殊情況下使用 `# type: ignore`
4. **定期檢查** - 將 mypy/pyright 整合至 CI
5. **文件化複雜型別** - 註解複雜的泛型結構