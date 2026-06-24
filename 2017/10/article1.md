# Python 3.7 發布：async/await 與資料類增強

## 前言

Python 3.7 於 2018 年 6 月正式發布，帶來了多項重要的新特性。雖然本期介紹的是 10 月號，但 Python 3.7 的內容在 2017 年底就已經開始被社群討論。本篇文章將深入探討 Python 3.7 的新特性及其對開發者的影響。

## async/await 的改進

### 延遲物件屬性訪問

Python 3.7 引入了一個微小但重要的改進——允許在物件屬性訪問中使用 `yield from`：

```python
# Python 3.6 中無法這樣做
class MyClass:
    @property
    def attr(self):
        return self._attr

# Python 3.7 允許延遲屬性
```

### asyncio 的增強

Python 3.7 對 asyncio 模組進行了多項增強：

```python
# 更簡潔的異步上下文管理
import asyncio

async def main():
    # Python 3.7 新增
    async with asyncio.timeout(10):
        await some_async_operation()
```

## Data Classes

Python 3.7 最重要的新特性之一是 Data Classes：

```python
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Point:
    x: float
    y: float
    label: Optional[str] = None

@dataclass
class Rectangle:
    top_left: Point
    bottom_right: Point

    @property
    def width(self) -> float:
        return self.bottom_right.x - self.top_left.x

    @property
    def height(self) -> float:
        return self.bottom_right.y - self.top_left.y

# 使用範例
p1 = Point(0, 0, "origin")
p2 = Point(10, 10)
rect = Rectangle(p1, p2)

print(f"Width: {rect.width}, Height: {rect.height}")
```

Data Classes 的優勢：
- 自動生成 `__init__`、`__repr__`、`__eq__`
- 減少樣板程式碼
- 提高程式碼可讀性

## 內部引用延遲

Python 3.7 允許從類型提示中引用尚未定義的類：

```python
# Python 3.6 需要使用字串引號
class Tree:
    def __init__(self, left: 'Tree' = None, right: 'Tree' = None):
        self.left = left
        self.right = right

# Python 3.7 可以直接引用
class Tree:
    def __init__(self, left: 'Tree' = None, right: 'Tree' = None):
        ...
```

## 開發體驗改善

### 較少的納米秒

Python 3.7 優化了時間函數的效能：

```python
import time

# Python 3.7 中更快
start = time.perf_counter()
# ... some operations
end = time.perf_counter()
print(f"Elapsed: {end - start}")
```

### 斷言追蹤

```python
# Python 3.7 的錯誤訊息更清晰
def divide(a, b):
    assert a > 0, "a must be positive"
    return a / b

divide(-1, 2)
# AssertionError: a must be positive
# 追蹤資訊更詳細
```

## 對深度學習的影響

Python 3.7 對深度學習框架有重要意義：

```python
# TensorFlow/PyTorch 都建議使用 Python 3.7
# 因為：
# 1. asyncio 支援更完善
# 2. 效能更好
# 3. typing 增強有利於類型檢查

import torch
import tensorflow as tf

print(f"PyTorch version: {torch.__version__}")
print(f"TensorFlow version: {tf.__version__}")
```

## 遷移指南

### 從 Python 3.6 遷移

1. **檢查依賴**：確保所有庫都支援 Python 3.7
2. **使用 dataclasses**：重構現有類別
3. **更新 asyncio**：利用新的 timeout 功能
4. **類型提示**：逐步添加類型提示

```python
# 建議的遷移步驟
# 1. 測試現有程式碼
python3.7 -m pytest tests/

# 2. 檢查警告
python3.7 -W all script.py

# 3. 更新類型提示
```

## 結論

Python 3.7 的發布標誌著 Python 在現代軟體開發中的持續進化。Data Classes、asyncio 增強和開發者體驗的改善，使 Python 繼續保持其作為熱門程式語言的地位。對於深度學習開發者來說，Python 3.7 提供了更好的效能和更現代的非同步程式設計支援。

---

**延伸閱讀**

- [Python 3.7 Release Notes](https://www.google.com/search?q=Python+3.7+release+notes)
- [Data Classes in Python](https://www.google.com/search?q=Python+dataclasses+tutorial)
- [Python 3.7 for Machine Learning](https://www.google.com/search?q=Python+3.7+deep+learning)