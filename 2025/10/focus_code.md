# Python 進階技巧綜合展示

## 概述

`advanced_python.py` 是一個展示 Python 進階核心概念的單一腳本。它實作了七個典型的進階 Python 模式：

1. **裝飾器（@timer）**——計時函式執行時間
2. **生成器（fibonacci）**——無限費氏數列生成
3. **上下文管理器（TimerContext）**——with 語句計時
4. **多執行緒（threading）**——多執行緒並行任務
5. **多程序（multiprocessing）**——行程池平行處理
6. **非同步（asyncio）**——協程非同步 I/O
7. **計時分析**——每個元件的效能測量

## 核心概念

### 1. 裝飾器

```python
def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"[timer] {func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper
```

`@timer` 裝飾器在不修改原始函式的情況下，為函式添加了計時功能。`functools.wraps` 保留原始函式的中繼資料。

### 2. 生成器

```python
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b
```

使用 `yield` 關鍵字實現惰性求值——費氏數列的值只在需要時才計算。這對於處理大數據序列特別有用。

### 3. 上下文管理器

```python
class TimerContext:
    def __enter__(self):
        self.start = time.perf_counter()
        return self
    def __exit__(self, *args):
        self.elapsed = time.perf_counter() - self.start
```

`__enter__` 和 `__exit__` 協定允許使用 `with` 語句進行資源管理。

### 4. 多執行緒與多程序

```python
# 多執行緒（適合 I/O 密集型）
threads = [threading.Thread(target=worker, args=(f"T{i}",)) for i in range(3)]
for t in threads: t.start()
for t in threads: t.join()

# 多程序（適合 CPU 密集型）
with multiprocessing.Pool(processes=3) as pool:
    results = pool.map(worker, items)
```

### 5. 非同步

```python
async def worker(name, delay):
    await asyncio.sleep(delay)
    
async def main():
    tasks = [worker("A", 0.1), worker("B", 0.2)]
    await asyncio.gather(*tasks)
    
asyncio.run(main())
```

`async/await` 實現協程式非同步 I/O，在單執行緒中處理大量並發連接。

## 元件對照

| 元件 | 適用場景 | 核心機制 | 限制 |
|------|--------|---------|------|
| 裝飾器 | 橫切關注點 | 高階函式 | 不適用非同步函式（需另處） |
| 生成器 | 惰性序列 | yield | 單向迭代 |
| 上下文管理器 | 資源管理 | enter/exit | 僅支援 with 區塊 |
| threading | I/O 密集 | GIL 限制 | 無法平行 CPU 任務 |
| multiprocessing | CPU 密集 | 獨立行程 | 通訊開銷大 |
| asyncio | 網路 I/O | 事件迴圈 | 需要 async 生態 |

## 執行結果

```
=== Decorator Demo ===
[timer] slow_square took 0.1002s
slow_square(4) = 16

=== Generator Demo ===
fibonacci first 10: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

=== Context Manager Demo ===
[context] elapsed: 0.2037s

=== Threading Demo ===
[timer] run_threads took 0.1599s

=== Multiprocessing Demo ===
[timer] run_processes took 0.0504s

=== Async Demo ===
[timer] run_async took 0.2018s
```

## 學到的教訓

1. **裝飾器**是 Python 函數式程式設計的核心——在不修改源碼的前提下增強函式行為
2. **生成器**實現惰性求值，適合處理無限或大型序列
3. **上下文管理器**讓資源管理變得優雅且安全
4. **多執行緒**受 GIL 限制，適合 I/O 密集任務
5. **多程序**繞過 GIL，適合 CPU 密集任務
6. **asyncio**在 I/O 密集型場景提供最高效率

---

## 延伸閱讀

- [完整程式碼](_code/advanced_python.py)
- [Python functools 文件](https://www.google.com/search?q=Python+functools+wraps)
- [Python asyncio 官方指南](https://www.google.com/search?q=Python+asyncio+official+documentation)
- [Real Python: Python Timer 裝飾器](https://www.google.com/search?q=Real+Python+Python+timer+decorator)
