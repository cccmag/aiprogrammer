# 1. Python 3.7 新特性總覽

## 概述

Python 3.7 於 2018 年 6 月發布，是 Python 3 系列的重要版本。相較於 Python 3.6，3.7 在語法、標準庫與效能方面都有顯著改進。本篇文章總覽 Python 3.7 的核心新特性。

## 語法層面

### Data Classes

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float
    label: str = ""

p = Point(1.0, 2.0)
print(p)  # Point(x=1.0, y=2.0, label='')
```

### 延後型態提示評估

```python
from __future__ import annotations

def greet(name: str) -> str:
    return f"Hello, {name}"

# 型別在執行時不會被評估，但靜態分析工具可以讀取
```

## 效能改進

### 啟動速度提升

Python 3.7 的匯入速度顯著提升，特別是 dataclasses、typing、contextlib 等常用模組。

### dict 物件效能

Python 3.7 的 dict 物件使用新的記憶體配置策略，效能提升約 20-25%。

```python
import timeit

# Python 3.6
# result: ~0.6 微秒

# Python 3.7
# result: ~0.5 微秒（快了 20%）
test_dict = {f"key_{i}": i for i in range(100)}
```

## asyncio 改進

Python 3.7 強化了 asyncio 模組：

```python
import asyncio

async def main():
    # asyncio.current_task() - 取得當前任務
    current = asyncio.current_task()
    print(f"Current task: {current}")

    # asyncio.all_tasks() - 取得所有任務
    all_tasks = asyncio.all_tasks()
    print(f"All tasks: {len(all_tasks)}")

asyncio.run(main())
```

## 上下文變數

```python
import contextvars

request_id = contextvars.ContextVar('request_id', default='')

def set_request_id(req_id):
    request_id.set(req_id)

def get_request_id():
    return request_id.get()
```

## 除錯改進

### 明確的類別定義順序

```python
class A:
    x = 1
    class B:
        y = x  # 現在可以參照到封閉作用域的變數
```

## 破壞性改變

Python 3.7 的一些破壞性改變需要留意：

1. `async` 和 `await` 成為保留關鍵字
2. `np.bool`、`np.int` 等 numpy 類型別名被移除
3. `collections.Mapping` 等抽象基類需要從 collections.abc 匯入

## 參考資源

- https://www.google.com/search?q=Python+3.7+new+features+dataclass+asyncio+2018+2019
- https://www.google.com/search?q=Python+3.7+performance+improvements+dict+startup+speed
- https://www.google.com/search?q=Python+3.7+migration+breaking+changes+from+3.6