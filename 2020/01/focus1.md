# 1. Python 3.8 新特性

## 概述

Python 3.8 於 2019 年 10 月發布，是 2020 年初最值得關注的 Python 版本。相較於 Python 3.7，3.8 在效能、語法與標準庫方面都有顯著改進。本篇文章介紹對日常開發最有影響的新特性。

## Walrus 運算子（海象運算子）

賦值運算式（Assignment Expressions）使用 `:=` 語法，可以在表達式內部同時賦值與使用變數。這解決了長期以來需要在語句前先賦值、然後才能使用的冗長程式碼問題。

```python
# 傳統方式：需要分開賦值
if n := len(data) > 10:
    print(f"資料筆數 {n} 超過 10")

# Walrus 運算子：在一個表達式中完成
while (line := input("請輸入：")) != "quit":
    print(f"您輸入了：{line}")

# 更有意義的範例：列表推到式中的重複計算
data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# 原本需要兩行程式碼
squared = [x**2 for x in data]
filtered = [y for y in squared if y > 25]
print(filtered)

# 使用 walrus 運算子（在此範例中較少用，但語法展示目的）
```

## 位置參數限定（Positional-Only Parameters）

現在可以使用 `/` 來區分位置參數與關鍵字參數。這對於設計 API 介面特別有用，可以確保某些參數無法被作為關鍵字傳遞，保護內部實作細節。

```python
def pow(base, exp, *, mod=None):
    result = base ** exp
    if mod:
        return result % mod
    return result

# 位置參數限定範例
def greet(name, /, greeting="Hello"):
    return f"{greeting}, {name}!"

print(greet("World"))
print(greet("Python", greeting="Hi"))
```

## f-string 診斷增強

在 Python 3.8 中，當 f-string 包含 `=` 時，會自動輸出變數名稱與其值，大幅簡化了偵錯過程。

```python
x = 42
y = 99

# Python 3.8+：f-string 診斷
print(f"{x=}")  # 輸出：x=42
print(f"{x + y=}")  # 輸出：x + y=141

# 對比傳統方式
print(f"x={x}, y={y}")
```

## Typing 改進

`typing.Literal` 允許限定參數只能是特定的值集合。`typing TypedDict` 增強了型態提示的表達能力。

```python
from typing import Literal, TypedDict

def move(direction: Literal["up", "down", "left", "right"], steps: int) -> None:
    print(f"向 {direction} 移動 {steps} 步")

class Config(TypedDict):
    host: str
    port: int
    debug: bool

config: Config = {"host": "localhost", "port": 8080, "debug": True}
```

## 其他顯著改進

### multiprocessing Shared Memory
現在可以使用 `multiprocessing.shared_memory` 在程序間共享記憶體，無需建立檔案或伺服器。

```python
from multiprocessing import Process, shared_memory
import numpy as np

a = np.array([1, 2, 3, 4, 5], dtype=np.float64)
shm = shared_memory.SharedMemory(create=True, size=a.nbytes)
b = np.ndarray(a.shape, dtype=np.float64, buffer=shm.buf)
b[:] = a[:]

print(f"共享記憶體名稱：{shm.name}")
```

### typing.Protocol 改進
Protocol 現在支援變異運算子，讓結構化子類型（Structural Subtyping）更易使用。

## 升級考量

Python 3.8 需要注意的相容性問題：
1. 某些第三方套件可能尚未支援 Python 3.8
2. `async` 作為變數名的使用受到更多限制
3. `datetime.utcnow()` 被標記為廢棄，建議使用 `datetime.now(timezone.utc)`

## 參考資源

- https://www.google.com/search?q=Python+3.8+new+features+walrus+operator+positional+only+2019+2020
- https://www.google.com/search?q=Python+3.8+f-string+debug+assignment+expression+tutorial
- https://www.google.com/search?q=Python+3.8+upgrade+migration+guide+compatibility+considerations