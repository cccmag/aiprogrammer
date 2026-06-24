# 主題二：Python 3.5 新特性

## Python 3.5 概述

Python 3.5 於 2015 年 9 月正式發布，是 Python 3 系列的又一重要里程碑。這個版本帶來了多個顯著的新特性，特別是 `async`/`await` 語法深受社群期待。

## PEP 492：async 和 await

這是 Python 3.5 最重要的新特性，為非同步程式設計提供了原生支援。

### Coroutine 語法

```python
# 定義一個 coroutine
async def fetch_data():
    # 模擬非同步操作
    await asyncio.sleep(1)
    return "data"

# 呼叫 coroutine
async def main():
    result = await fetch_data()
    print(result)

# 執行
import asyncio
asyncio.run(main())
```

### 與生成器的區別

```python
# 生成器
def my_generator():
    yield 1
    yield 2

# Async coroutine
async def my_coroutine():
    await asyncio.sleep(0)
    yield 1  # 不允許在普通 async 函式中 yield
```

### 協程的應用場景

```python
import asyncio

async def fetch_url(url):
    """模擬網頁請求"""
    await asyncio.sleep(0.5)  # 模擬 I/O 延遲
    return f"Result from {url}"

async def main():
    urls = ['http://example.com', 'http://test.com', 'http://demo.com']

    # 並發執行多個協程
    tasks = [fetch_url(url) for url in urls]
    results = await asyncio.gather(*tasks)

    for result in results:
        print(result)

asyncio.run(main())
```

## PEP 484：Type Hints

Type Hints 為 Python 提供了靜態類型檢查的可能：

```python
def greet(name: str) -> str:
    return f"Hello, {name}"

def process_numbers(numbers: list[int]) -> int:
    return sum(numbers)

# 複雜類型
from typing import Dict, List, Optional

def word_count(text: str) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for word in text.split():
        counts[word] = counts.get(word, 0) + 1
    return counts
```

### typing 模組

```python
from typing import List, Dict, Tuple, Optional, Union, Callable

# 巢狀類型
Matrix = List[List[float]]

# 可選類型
def find_user(user_id: int) -> Optional[str]:
    users = {1: "Alice", 2: "Bob"}
    return users.get(user_id)

# 聯合類型
def parse_input(value: Union[str, int]) -> str:
    return str(value)

# 可呼叫類型（函式作為參數）
def apply(func: Callable[[int], int], value: int) -> int:
    return func(value)
```

## PEP 465：矩陣乘法運算子

```python
import numpy as np

A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

# 傳統方式
C = np.dot(A, B)

# Python 3.5+ 方式
C = A @ B

print(C)
# [[19 22]
#  [43 50]]
```

## PEP 471：os.scandir()

更高效的目錄遍歷：

```python
import os

# 舊方式（遍歷所有條目）
for entry in os.listdir('.'):
    if os.path.isfile(entry):
        print(f"File: {entry}")

# 新方式（scandir 更高效）
for entry in os.scandir('.'):
    if entry.is_file():
        print(f"File: {entry.name}")
```

`scandir()` 的優勢在於它返回的是目錄條目的 `DirEntry` 物件，這些物件緩存了 `is_file()` 和 `is_dir()` 的結果，避免了額外的系統調用。

## 其他改進

### 序列解包增強

```python
# 更靈活的解包
first, *middle, last = [1, 2, 3, 4, 5]
print(middle)  # [2, 3, 4]

# 在函式呼叫中使用
print(*[1, 2, 3], *[4, 5, 6])  # 1 2 3 4 5 6
```

### yield from 增強（Python 3.3 已有）

```python
def generator():
    yield from [1, 2, 3]
    yield from (4, 5, 6)
```

### 數學運算增強

```python
# 內建的 int.from_bytes 和 int.to_bytes
data = (255).to_bytes(2, byteorder='big')
print(data)  # b'\\xff\\x01'

recovered = int.from_bytes(data, byteorder='big')
print(recovered)  # 65281
```

## 升級注意事項

### 向後相容性

Python 3.5 基本上與 Python 3.4 相容，但注意：
- `async` 和 `await` 成為保留關鍵字
- 不能使用這些名稱作為變數或函式名稱

### 對未來的影響

Python 3.5 的 async/await 為 Python 的非同步程式設計開闢了新篇章，後續版本在此基礎上持續改進。

## 結論

Python 3.5 是一個重要的版本，特別是 async/await 語法為非同步程式設計帶來了極大的便利。Type Hints 也為日後的靜態類型檢查工具鋪平了道路。