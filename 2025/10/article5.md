# 行程池與平行處理

## 1. 引言

當任務需要大量 CPU 運算時，Python 的多執行緒因為 GIL 的限制無法充分利用多核心。這時需要 multiprocessing——透過建立多個獨立行程來實現真實的平行計算。

## 2. 行程 vs 執行緒

行程與執行緒的核心差異：

```python
# 執行緒：共享記憶體，受 GIL 限制
import threading
shared_data = []  # 執行緒共享

# 行程：獨立記憶體，無 GIL 限制
import multiprocessing as mp
# 每個行程有獨立的記憶體空間
```

## 3. Pool：行程池

`Pool` 是最常用的抽象——管理一組工作行程：

```python
import multiprocessing as mp
import time

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

if __name__ == "__main__":
    numbers = range(100000, 110000)
    
    # 序列版本
    start = time.time()
    serial = [is_prime(n) for n in numbers]
    print(f"序列: {time.time() - start:.2f}s")
    
    # 平行版本（使用 4 個行程）
    start = time.time()
    with mp.Pool(processes=4) as pool:
        parallel = pool.map(is_prime, numbers)
    print(f"平行: {time.time() - start:.2f}s")
```

## 4. Pool.map 與變體

Pool 提供了多種任務分派方法：

```python
with mp.Pool(4) as pool:
    # map：阻塞，收集結果
    results = pool.map(func, items)
    
    # map_async：非阻塞
    async_result = pool.map_async(func, items)
    results = async_result.get(timeout=10)
    
    # imap：惰性版本，結果漸進返回
    for result in pool.imap(func, items):
        process(result)
    
    # apply：單一任務
    result = pool.apply(func, args=(x,))
    
    # apply_async：非阻塞單一任務
    async_result = pool.apply_async(func, args=(x,))
    result = async_result.get()
```

## 5. Queue：行程間通訊

使用 `multiprocessing.Queue` 在行程間傳遞資料：

```python
import multiprocessing as mp

def worker(task_queue, result_queue):
    while True:
        task = task_queue.get()
        if task is None:  # 停止信號
            break
        result_queue.put(task ** 2)

if __name__ == "__main__":
    tasks = mp.Queue()
    results = mp.Queue()
    
    # 啟動 4 個工作行程
    workers = [mp.Process(target=worker, args=(tasks, results)) for _ in range(4)]
    for w in workers: w.start()
    
    # 分派任務
    for i in range(100):
        tasks.put(i)
    for _ in range(4):
        tasks.put(None)  # 停止信號
    
    for w in workers: w.join()
    
    # 收集結果
    while not results.empty():
        print(results.get())
```

## 6. 共享記憶體

multiprocessing 提供了 `Value` 和 `Array` 用於共享記憶體：

```python
import multiprocessing as mp

def increment(counter, lock):
    for _ in range(1000):
        with lock:
            counter.value += 1

if __name__ == "__main__":
    counter = mp.Value('i', 0)  # 'i' = signed int
    lock = mp.Lock()
    
    processes = [mp.Process(target=increment, args=(counter, lock)) for _ in range(10)]
    for p in processes: p.start()
    for p in processes: p.join()
    
    print(counter.value)  # 10000
```

## 7. concurrent.futures 統一介面

Python 3.2 提供的統一高階介面：

```python
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

def task(n):
    return sum(i*i for i in range(n))

# 切換執行緒/行程只需要改這一行
with ProcessPoolExecutor(max_workers=4) as executor:
    futures = [executor.submit(task, 10_000_000) for _ in range(8)]
    for future in futures:
        print(future.result())
```

## 8. 平行處理策略

**資料平行**：將大資料分割為獨立區塊：
- 影像處理：每個區塊獨立濾波
- 數值模擬：每個參數空間獨立計算
- 資料分析：每個分割區獨立聚合

**任務平行**：不同任務同時執行：
- Web 爬蟲：同時抓取多個 URL
- 資料庫查詢：同時執行多個查詢
- 檔案處理：同時壓縮多個檔案

## 9. 總結

multiprocessing 讓 Python 可以實現真正的平行計算。Pool 提供了高階抽象，Queue 和共享記憶體提供了行程間通訊機制。選擇正確的平行策略可以大幅提升 CPU 密集型任務的效能。

## 延伸閱讀

- [Python multiprocessing 官方文件](https://www.google.com/search?q=Python+multiprocessing+Pool+documentation)
- [concurrent.futures 官方指南](https://www.google.com/search?q=Python+concurrent+futures+ProcessPoolExecutor)
