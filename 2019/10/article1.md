# Python 3.8 新特性：賦值表達式與位置-only 參數

## 前言

Python 3.8 於 2019 年 10 月正式發布，這是 Python 語言的又一重要里程碑。本篇文章將深入探討 Python 3.8 的新特性，特別是備受期待的賦值表達式和位置-only 參數。

## 賦值表達式（Assignment Expressions）

### 傳統方式的限制

在 Python 3.8 之前，我們經常需要這樣寫程式碼：

```python
# 傳統方式：需要兩行
if len(data) > 10:
    print(f"Data too long: {len(data)}")

# 或者使用 walrus operator 的變通方法
print(f"Data too long: {len(data)}") if (n := len(data)) > 10 else None
```

### Walrus Operator

Python 3.8 引入的 `:=` 運算子稱為「walrus operator」（海象運算子，因為看起來像海象的眼睛和牙齒）：

```python
# 新的賦值表達式
if (n := len(data)) > 10:
    print(f"Data too long: {n}")
```

### 實際應用場景

**場景 1：檔案讀取**

```python
# 傳統方式
while True:
    line = f.readline()
    if not line:
        break
    process(line)

# 使用 walrus operator
while (line := f.readline()):
    process(line)
```

**場景 2：正規表示式匹配**

```python
# 傳統方式
match = re.search(pattern, text)
if match:
    print(f"Found: {match.group(1)}")

# 使用 walrus operator
if (match := re.search(pattern, text)):
    print(f"Found: {match.group(1)}")
```

**場景 3：列表推導式中的重複使用**

```python
# 傳統方式
results = [f(x) for x in data]
filtered = [r for r in results if r > 0]

# 使用 walrus operator
filtered = [r for x in data if (r := f(x)) > 0]
```

### 注意事項

```python
# 注意：賦值表達式需要括號
# 正確
(n := len(data))

# 錯誤
n := len(data)
```

## 位置-only 參數（Positional-Only Parameters）

### 問題的由來

Python 一直沒有語法方式來指定某些參數只能作為位置參數。這導致了一些問題：

```python
def func(a, b, /, c, d):
    # / 之前的是位置-only 參數
    # / 和 * 之间的是普通參數
    # * 之後的是關鍵字-only 參數
    pass
```

### 語法說明

```
def f(a, b, /, c, d, *, e, f):
    pass

# a, b：只能用位置調用
# c, d：可以用位置或關鍵字調用
# e, f：只能用關鍵字調用
```

### 實際應用

**場景 1：保護 API 穩定性**

```python
def create_user(name, /, age=None, **kwargs):
    # name 只能位置傳遞，確保 API 穩定性
    pass

create_user("John", 30)  # 正確
create_user(name="John", age=30)  # 錯誤
```

**場景 2：與 C 擴展相容**

```python
# math.sqrt 的 C 實現可能需要位置-only 參數
import math
math.sqrt(4)  # 始終有效
```

## 其他重要新特性

### 改進的 Typing

Python 3.8 對 typing 模組進行了擴展：

```python
from typing import TypedDict, Literal

class Point(TypedDict):
    x: int
    y: int

def move(direction: Literal["up", "down", "left", "right"]) -> Point:
    pass
```

### f-strings 支援 = 說明符

```python
x = 10
# Python 3.8 之前
print(f"x = {x}")

# Python 3.8
print(f"{x = }")  # 輸出：x = 10
```

### multiprocessing Shared Memory

```python
from multiprocessing import shared_memory
import numpy as np

shm = shared_memory.SharedMemory(name="my_shm", create=True, size=64)
arr = np.ndarray((8, 8), dtype=np.float64, buffer=shm.buf)
```

## 效能改進

Python 3.8 帶來了多項效能改進：

| 改進 | 影響 |
|------|------|
| pickle 優化 | 序列化速度提升約 10% |
| 加快啟動速度 | 縮短 Python 程式啟動時間 |
| AST 優化 | 減少記憶體使用 |

## 結論

Python 3.8 的新特性為開發者提供了更多工具和靈活性。賦值表達式讓程式碼更加簡潔，位置-only 參數則為 API 設計提供了更好的控制力。建議開發者儘早升級以享受這些新特性帶來的好處。

---

**延伸閱讀**

- [Python 3.8 Release Notes](https://www.google.com/search?q=Python+3.8+release+notes+2019)
- [Assignment Expressions PEP 572](https://www.google.com/search?q=PEP+572+Python+walrus+operator)
- [Positional-Only Parameters PEP 570](https://www.google.com/search?q=PEP+570+Python+positional+only)