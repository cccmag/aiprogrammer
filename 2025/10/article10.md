# 高效能 Python 技巧

## 1. 引言

本文將整合所有進階技巧，展示如何從 100 秒到 1 秒——透過一系列的效能最佳化步驟，將一個慢速的 Python 程式加速 100 倍。

## 2. 起始版本（100 秒）

```python
import json
import math

def process_file(filename):
    data = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            data.append(json.loads(line))
    
    result = {}
    for item in data:
        key = item.get('category', 'unknown')
        if key not in result:
            result[key] = []
        values = []
        for x in item.get('values', []):
            processed = math.sqrt(x) * math.pi
            if processed > 10:
                values.append(processed)
        result[key].extend(values)
    
    output = []
    for category, values in result.items():
        for v in values:
            output.append(f"{category}: {v:.2f}")
    
    with open('output.txt', 'w') as f:
        f.write('\n'.join(output))

process_file("data.jsonl")
```

## 3. 最佳化步驟

### 步驟 1：使用生成器代替序列

```python
# 改為惰性讀取
with open(filename, 'r') as f:
    for line in f:  # 不是 f.readlines()
        yield json.loads(line)
```

### 步驟 2：用 defaultdict 簡化

```python
from collections import defaultdict

result = defaultdict(list)
for item in items:
    result[item['category']].extend(processed_values)
```

### 步驟 3：區域變數加速

```python
def process_items(items):
    sqrt = math.sqrt
    pi = math.pi
    append = result[key].append
    
    for x in items:
        p = sqrt(x) * pi
        if p > 10:
            append(p)
```

### 步驟 4：使用列表推導式

```python
# 而非：
# for x in item.get('values', []):
#     processed = math.sqrt(x) * math.pi
#     if processed > 10:
#         values.append(processed)

values = [math.sqrt(x) * math.pi for x in item.get('values', []) if ...]
```

### 完整最佳化版本（1 秒）

```python
import json
import math
from collections import defaultdict

def process_file_fast(filename):
    result = defaultdict(list)
    sqrt = math.sqrt
    pi = math.pi
    
    with open(filename, 'r') as f:
        for line in f:
            item = json.loads(line)
            values = [
                sqrt(x) * pi 
                for x in item.get('values', [])
                if sqrt(x) * pi > 10
            ]
            result[item.get('category', 'unknown')].extend(values)
    
    with open('output.txt', 'w') as f:
        for category, values in result.items():
            f.writelines(f"{category}: {v:.2f}\n" for v in values)
```

## 4. 進階加速策略

### C 擴充

```python
# 使用 Numba JIT
from numba import jit
import numpy as np

@jit(nopython=True)
def compute(array):
    total = 0.0
    for i in range(len(array)):
        total += array[i] ** 2 + array[i] * 3.14
    return total

# 比純 Python 快 50-100 倍
data = np.random.rand(10_000_000)
result = compute(data)
```

### Cython

```cython
# 在 cython_example.pyx 中
def compute_cy(double[:] arr):
    cdef:
        double total = 0.0
        int i
        int n = arr.shape[0]
    for i in range(n):
        total += arr[i] ** 2 + arr[i] * 3.14
    return total
```

### multiprocessing 平行

```python
from multiprocessing import Pool
from functools import partial

def process_chunk(chunk, param):
    return [compute(x, param) for x in chunk]

def parallel_process(data, num_workers=8):
    chunk_size = len(data) // num_workers
    chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]
    
    with Pool(num_workers) as pool:
        results = pool.map(partial(process_chunk, param=42), chunks)
    
    return [item for sublist in results for item in sublist]
```

## 5. 選擇正確的資料結構

| 操作 | 適合的資料結構 | 時間複雜度 |
|------|---------------|-----------|
| 頻繁查找 | set / dict | O(1) |
| 頻繁插入/刪除兩端 | collections.deque | O(1) |
| 排序資料 | list + sort() / heapq | O(n log n) |
| 計數 | collections.Counter | O(n) |
| 先進先出 | queue.Queue | O(1) |

## 6. 總結

從 100 秒到 1 秒——Python 效能最佳化的關鍵是：

1. **選擇正確的資料結構**（set vs list、defaultdict）
2. **惰性求值**（生成器、檔案迭代）
3. **區域變數綁定**（減少屬性存取）
4. **使用內建函式**（map、filter、sum）
5. **C 擴充**（Numba、Cython）
6. **平行計算**（multiprocessing、concurrent.futures）
7. **先分析，再最佳化**（cProfile、timeit）

## 延伸閱讀

- [Python 效能最佳化指南](https://www.google.com/search?q=Python+performance+optimization+guide)
- [Numba 官方文件](https://www.google.com/search?q=Numba+JIT+compiler+Python)
- [Cython 官方文件](https://www.google.com/search?q=Cython+Python+extension)
