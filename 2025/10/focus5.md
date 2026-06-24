# 多程序 multiprocessing

## 繞過 GIL 的平行計算（2008-2026）

### 前言

當你需要真正的平行處理時——利用多核心 CPU 同時執行多個任務——Python 的 `multiprocessing` 模組是標準答案。它透過建立多個獨立的 Python 行程來繞過 GIL 的限制。

### 行程 vs 執行緒

```python
from multiprocessing import Process

def cpu_heavy(n):
    total = 0
    for i in range(n):
        total += i * i
    return total

if __name__ == "__main__":
    # 多行程：真正的平行
    p1 = Process(target=cpu_heavy, args=(10_000_000,))
    p2 = Process(target=cpu_heavy, args=(10_000_000,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
```

與執行緒不同，每個行程有自己的 GIL，因此可以真正地同時執行。

### Process 與 Pool

對於大量任務，`Pool` 提供了方便的平行映射：

```python
import multiprocessing as mp

def square(n):
    return n * n

if __name__ == "__main__":
    with mp.Pool(processes=4) as pool:
        results = pool.map(square, range(10))
        # 或者非同步版本
        async_result = pool.map_async(square, range(10))
        results = async_result.get()
    print(results)  # [0, 1, 4, 9, ...]
```

`Pool.map` 自動將任務分配給行程池中的可用行程。

### Queue：行程間通訊

行程之間不共享記憶體，需要透過序列化來傳遞資料：

```python
import multiprocessing as mp

def worker(q):
    q.put("來自子行程的訊息")

if __name__ == "__main__":
    q = mp.Queue()
    p = mp.Process(target=worker, args=(q,))
    p.start()
    print(q.get())  # 來自子行程的訊息
    p.join()
```

`Queue` 和 `Pipe` 是 multiprocessing 提供的行程間通訊機制。

### 共享記憶體

雖然行程不共享記憶體，但 multiprocessing 提供了共享記憶體的方式：

```python
import multiprocessing as mp

def increment(counter):
    for _ in range(100):
        counter.value += 1

if __name__ == "__main__":
    counter = mp.Value('i', 0)
    processes = [mp.Process(target=increment, args=(counter,)) for _ in range(4)]
    for p in processes: p.start()
    for p in processes: p.join()
    print(counter.value)  # 400
```

### concurrent.futures 統一介面

Python 3.2 引入了 `concurrent.futures`，提供了統一的執行緒/行程池介面：

```python
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import time

def io_task(url):
    time.sleep(0.1)  # 模擬網路請求
    return url

def cpu_task(n):
    return sum(i*i for i in range(n))

# I/O 密集型 → 多執行緒（或 asyncio）
with ThreadPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(io_task, ["url1", "url2", "url3"]))

# CPU 密集型 → 多行程
with ProcessPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(cpu_task, [10_000_000, 20_000_000]))
```

### 什麼時候用 multiprocessing

- **CPU 密集型計算**：影像處理、數值模擬、資料分析
- **需要平行處理**：任務可以獨立執行
- **大資料處理**：可以分割為獨立區塊

### 注意事項

1. **啟動開銷**：每個行程需要載入 Python 直譯器
2. **通訊開銷**：傳遞資料需要序列化/反序列化
3. **全域狀態**：行程間不共享全域變數
4. **跨平台**：Unix 用 `fork`，Windows 用 `spawn`

### 小結

multiprocessing 是 Python 中實現真實平行計算的標準方案。透過建立多個獨立行程，它可以繞過 GIL 的限制，充分利用多核心 CPU 的運算能力。

---

**下一步**：[非同步程式設計 asyncio](focus6.md)

## 延伸閱讀

- [Python multiprocessing 官方文件](https://www.google.com/search?q=Python+multiprocessing+module+documentation)
- [concurrent.futures 官方指南](https://www.google.com/search?q=Python+concurrent+futures+documentation)
- [Real Python: Multiprocessing in Python](https://www.google.com/search?q=Real+Python+multiprocessing+guide)
