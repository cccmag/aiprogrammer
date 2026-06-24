# Python 3.7 新特性： dataclass 與 async

## 前言

Python 3.7 於 2018 年 6 月發布，带來了多項改進。本篇文章聚焦於 `dataclass` 裝飾器和 `async` 增強，這兩個特性对 AI 開發者特別實用。

## dataclass 裝飾器

### 為什麼需要 dataclass？

傳統 Python 類定義資料模型較為繁瑣：

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
```

### dataclass 解決方案

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float

    def distance_from_origin(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

# 自動獲得 __init__, __repr__, __eq__
p1 = Point(3.0, 4.0)
p2 = Point(3.0, 4.0)
print(p1)  # Point(x=3.0, y=4.0)
print(p1 == p2)  # True
print(p1.distance_from_origin())  # 5.0
```

### dataclass 進階選項

```python
from dataclasses import dataclass, field

@dataclass
class Dataset:
    name: str
    samples: list = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
    processed: bool = False

    def add_sample(self, sample):
        self.samples.append(sample)
        self.processed = False
```

### AI 應用範例

```python
from dataclasses import dataclass
from typing import List
import numpy as np

@dataclass
class TrainingExample:
    input_ids: List[int]
    attention_mask: List[int]
    labels: int = -100

@dataclass
class Batch:
    input_ids: np.ndarray
    attention_mask: np.ndarray
    labels: np.ndarray
```

## async 增強

### Python 3.7 的 async 改進

```python
import asyncio

async def fetch_data(url):
    """非同步獲取資料"""
    await asyncio.sleep(1)  # 類比 I/O 操作
    return {"url": url, "data": "sample"}

async def main():
    # 並行執行多個任務
    urls = ["url1", "url2", "url3"]
    results = await asyncio.gather(*[fetch_data(u) for u in urls])
    return results

# 執行
asyncio.run(main())
```

### async 在資料處理中的應用

```python
async def process_batch(data_generator, batch_size=32):
    """非同步批次處理"""
    batch = []
    async for item in data_generator:
        batch.append(item)
        if len(batch) >= batch_size:
            yield batch
            batch = []
    if batch:
        yield batch
```

## 結論

Python 3.7 的新特性讓資料模型的定義更加簡潔，非同步程式設計更加直覺。對 AI 開發者而言，這些改進能顯著提升程式碼的可讀性和維護性。

---

**延伸閱讀**

- [Python 3.7 dataclass 文檔](https://www.google.com/search?q=Python+3.7+dataclass)
- [Python async await 教程](https://www.google.com/search?q=Python+async+await+tutorial)