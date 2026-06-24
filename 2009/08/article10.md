# 摩爾定律的延續：多核心 CPU 時代

## 前言

2009 年，個人電腦正式進入多核心時代。單核心處理器的時脈提升遇到瓶頸，晶片製造商轉向多核心架構來提升效能。

## 多核心的興起

### 處理器發展

```markdown
CPU 核心數發展：

2005年：首款消費級雙核心
- Intel Pentium D
- AMD Athlon X2

2006年：Conroe 和 Windsor
- Intel Core 2 Duo
- AMD Athlon 64 X2

2007-2008年：四核心興起
- Intel Core 2 Quad
- AMD Phenom X4

2009年：六核心和八核心
- Intel Core i7 (4核心/8線程)
- AMD Phenom II X6 (6核心)
```

### 時脈 vs 核心數

```
摩爾定律的演變：

時脈提升模式（1990s-2005s）：
2000MHz → 3000MHz → 4000MHz
（每 18 個月提升 50%）

核心數提升模式（2005s-現在）：
1 核心 → 2 核心 → 4 核心 → 8 核心
（每 18 個月核心數翻倍）
```

## 軟體挑戰

### 並行化需求

```python
# 將任務分配到多核心

import multiprocessing

def process_data_chunk(chunk):
    # 處理資料塊
    return [compute(item) for item in chunk]

def parallel_process(data, num_cores=4):
    # 分割資料
    chunks = split_into_chunks(data, num_cores)

    # 建立程序池
    with multiprocessing.Pool(num_cores) as pool:
        results = pool.map(process_data_chunk, chunks)

    # 合併結果
    return combine_results(results)
```

### GIL 問題

```python
# Python 的 GIL（全域解釋器鎖）

# 在 Python 中：
# - 同一時間只有一個執行緒執行 Python 位元組碼
# - I/O 操作會釋放 GIL
# - C 擴展可以釋放 GIL

# 解決方案：

# 1. 多程序（multiprocessing）
import multiprocessing
p = multiprocessing.Process(target=task)
p.start()

# 2. C 擴展
# 使用 Cython 或直接寫 C 擴展

# 3. 替代解釋器
# Jython, IronPython 無 GIL
```

### OpenMP

```c
// C/C++ 中的 OpenMP 並行化

#include <omp.h>

void parallel_matrix_multiply(double* A, double* B, double* C, int N) {
    #pragma omp parallel for
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            double sum = 0;
            for (int k = 0; k < N; k++) {
                sum += A[i*N+k] * B[k*N+j];
            }
            C[i*N+j] = sum;
        }
    }
}
```

## 程式設計模式

### 任務並行

```python
# 任務並行模式

import concurrent.futures

def fetch_url(url):
    return requests.get(url).content

urls = ['http://example.com/1',
        'http://example.com/2',
        'http://example.com/3']

# 使用執行緒池
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    results = executor.map(fetch_url, urls)
```

### 資料並行

```python
# 資料並行

from multiprocessing import Pool

def process_item(item):
    return expensive_computation(item)

if __name__ == '__main__':
    items = range(1000)
    with Pool(4) as pool:
        results = pool.map(process_item, items)
```

## 硬體支援

### 多核心 CPU

```python
# 檢查 CPU 核心數

import multiprocessing

print(multiprocessing.cpu_count())  # 8

# 或者
import os
print(os.cpu_count())
```

### GPU 運算

```python
# CUDA 加速

import pycuda.autoinit
import pycuda.driver as drv
import numpy as np

# 分配記憶體
a = np.random.randn(1000).astype(np.float32)
b = np.random.randn(1000).astype(np.float32)

a_gpu = drv.mem_alloc(a.nbytes)
b_gpu = drv.mem_alloc(b.nbytes)

# 複製到 GPU
drv.memcpy_htod(a_gpu, a)
drv.memcpy_htod(b_gpu, b)
```

## 結語

多核心時代的來臨，改變了軟體開發的方式。開發者需要學會並行思考，設計能夠充分利用硬體的軟體。

## 延伸閱讀

- [多核心 CPU 發展](https://www.google.com/search?q=multi+core+CPU+history+2009)
- [並行程式設計](https://www.google.com/search?q=parallel+programming+tips)
- [Python 多程序](https://www.google.com/search?q=Python+multiprocessing+tutorial)

---

*本篇文章為「AI 程式人雜誌 2009 年 8 月號」文章系列之一。*