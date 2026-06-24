# 5. 執行效能改進

## Python 3.7 效能優化概述

Python 3.7 在執行效能上有多項改進，包括 dict 物件優化、啟動速度提升、以及新的除錯功能。這些改進使得 Python 3.7 在日常使用中更加順暢。

## dict 效能改進

Python 3.7 的 dict 實現採用了新的記憶體配置策略，顯著提升了效能：

```python
import timeit

# 建立大型字典
setup = """
d = {f'key_{i}': i for i in range(10000)}
"""

# 讀取效能測試
stmt = """
for k, v in d.items():
    pass
"""

time = timeit.timeit(stmt, setup, number=100)
print(f"讀取 10000 筆資料 100 次：{time:.4f} 秒")
```

### dict 插入順序保證

Python 3.7+ 保證 dict 維持插入順序：

```python
d = {"first": 1, "second": 2, "third": 3}
print(list(d.keys()))  # ['first', 'second', 'third']
```

## 啟動速度優化

Python 3.7 改善了模組匯入速度：

```python
# 測量啟動時間
import time

start = time.time()
import dataclasses
import typing
import contextlib
elapsed = time.time() - start
print(f"匯入時間：{elapsed*1000:.2f} 毫秒")
```

## __future__ 延後評估

```python
from __future__ import annotations

def greet(name: str) -> str:
    # 'str' 在執行時不會被評估，減少匯入時間
    return f"Hello, {name}"

# annotations 會被儲存為字串
print(greet.__annotations__)
# {'name': <class 'str'>, 'return': <class 'str'>}
```

## 執行緒區域變數優化

```python
import threading
import timeit

local = threading.local()

def worker():
    local.data = [1, 2, 3, 4, 5]
    return sum(local.data)

# Python 3.7+ 提升了執行緒區域變數的效能
threads = [threading.Thread(target=worker) for _ in range(10)]
```

## 簡單效能測試

```python
import timeit

# 字串格式化
format_time = timeit.timeit(
    'name = "world"; f"Hello, {name}"',
    number=100000
)

concat_time = timeit.timeit(
    'name = "world"; "Hello, " + name',
    number=100000
)

print(f"f-string: {format_time:.4f}")
print(f"concat:   {concat_time:.4f}")
```

## 快取優化

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Python 3.7+ 的 lru_cache 效能更好
print([fibonacci(i) for i in range(20)])
print(fibonacci.cache_info())
```

## 編譯相關

```python
import py_compile

# 編譯速度測試
start = timeit.timeit(
    'py_compile.compile("example.py")',
    globals={'py_compile': py_compile},
    number=100
)
print(f"編譯 100 次：{start:.4f} 秒")
```

## 參考資源

- https://www.google.com/search?q=Python+3.7+performance+improvements+dict+startup+2019
- https://www.google.com/search?q=Python+3.7+faster+dict+insertion+order+guarantee
- https://www.google.com/search?q=Python+3.7+performance+benchmark+comparison+3.6+2019