# 主題六：並發與執行緒模型

## 為何需要並發？

- **效能**：利用多核 CPU
- **回應性**：避免 UI 凍結
- **資源利用率**：I/O 等待時處理其他任務

## 執行緒基礎

### 行程 vs 執行緒

```
行程（Process）：
+-----------+
| 記憶體空間 |
| 程式碼    |
| 資料      |
| 執行緒1   |
| 執行緒2   |  ← 執行緒共享行程記憶體
+-----------+

執行緒（Thread）：
+-----------+
| 棧       |
| 暫存器    |
| 狀態     |
+-----------+
共享：堆、程式碼、全域資料
```

### 建立執行緒

```python
import threading
import time

def worker(n):
    print(f"Worker {n} starting")
    time.sleep(1)
    print(f"Worker {n} done")

# 建立執行緒
t1 = threading.Thread(target=worker, args=(1,))
t2 = threading.Thread(target=worker, args=(2,))

t1.start()  # 啟動
t2.start()

t1.join()   # 等待完成
t2.join()

print("All workers done")
```

### 共用狀態的問題

```python
counter = 0

def increment():
    global counter
    for _ in range(1000000):
        counter += 1  # 不是原子操作！

# 兩個執行緒同時執行
t1 = threading.Thread(target=increment)
t2 = threading.Thread(target=increment)

t1.start(); t2.start()
t1.join(); t2.join()

print(counter)  # 可能不是 2000000！
```

## 同步原語

### 互斥鎖（Mutex）

```python
import threading

counter = 0
lock = threading.Lock()

def increment():
    global counter
    for _ in range(1000000):
        with lock:
            counter += 1  # 同步訪問

t1 = threading.Thread(target=increment)
t2 = threading.Thread(target=increment)

t1.start(); t2.start()
t1.join(); t2.join()

print(counter)  # 正確：2000000
```

### 讀寫鎖

```python
import threading

class RWLock:
    def __init__(self):
        self._read_ready = threading.Condition(threading.Lock())
        self._readers = 0

    def acquire_read(self):
        with self._read_ready:
            self._readers += 1

    def release_read(self):
        with self._read_ready:
            self._readers -= 1
            if self._readers == 0:
                self._read_ready.notify_all()

    def acquire_write(self):
        self._read_ready.wait_for(lambda: self._readers == 0)

    def release_write(self):
        self._read_ready.notify_all()
```

### 信號量（Semaphore）

```python
import threading

# 限制並發數量
pool = threading.Semaphore(3)

def worker(n):
    with pool:
        print(f"Worker {n} doing work")
        time.sleep(1)

for i in range(10):
    threading.Thread(target=worker, args=(i,)).start()
```

### 條件變數（Condition）

```python
import threading

class BoundedBuffer:
    def __init__(self, size):
        self.buffer = []
        self.size = size
        self.lock = threading.Lock()
        self.not_full = threading.Condition(self.lock)
        self.not_empty = threading.Condition(self.lock)

    def put(self, item):
        with self.not_full:
            while len(self.buffer) >= self.size:
                self.not_full.wait()
            self.buffer.append(item)
            self.not_empty.notify()

    def get(self):
        with self.not_empty:
            while not self.buffer:
                self.not_empty.wait()
            item = self.buffer.pop(0)
            self.not_full.notify()
            return item
```

## 全域解釋器鎖（GIL）

Python 的 GIL 限制了同一時刻只有一個執行緒執行 Python 位元組碼：

```python
# GIL 使得 CPU 密集型任務無法真正並行
def cpu_bound():
    return sum(i * i for i in range(1000000))

# 兩個執行緒不會真正並行執行
t1 = threading.Thread(target=cpu_bound)
t2 = threading.Thread(target=cpu_bound)
```

### 解決方案

```python
# 1. 使用 multiprocessing（多行程）
import multiprocessing as mp

def cpu_bound():
    return sum(i * i for i in range(1000000))

with mp.Pool(4) as pool:
    results = pool.map(cpu_bound, range(4))

# 2. 使用 C 擴展（釋放 GIL）
# 3. 使用 asyncio（I/O 密集型）
```

## Actor 模型

Actor 是並發的另一种模型，沒有共享狀態：

```python
# 使用 thespian 庫
from thespian.actors import *

class Worker(Actor):
    def receiveMessage(self, msg, sender):
        if msg == 'start':
            result = do_work()
            self.send(sender, result)

# 使用
worker = system.createActor(Worker)
system.tell(worker, 'start')
```

## Coroutine

Coroutine 是輕量級的並發，無需作業系統：

### Python asyncio

```python
import asyncio

async def fetch(url):
    # 模擬 I/O 操作
    await asyncio.sleep(1)
    return f"Data from {url}"

async def main():
    # 並發執行
    urls = ['a.com', 'b.com', 'c.com']
    tasks = [fetch(url) for url in urls]
    results = await asyncio.gather(*tasks)
    print(results)

asyncio.run(main())
```

### 生成器與协程

```python
def my_generator():
    result = yield 1
    print(f"Got: {result}")
    result = yield 2
    print(f"Got: {result}")
    yield 3

gen = my_generator()
print(next(gen))        # 1
print(gen.send(10))     # Got: 10, 輸出 2
print(gen.send(20))     # Got: 20, 輸出 3
```

## Goroutine（Go 語言）

Go 的並發模型極為簡潔：

```go
// Go 語法
func worker(msg string) {
    fmt.Println(msg)
}

func main() {
    // 啟動 goroutine
    go worker("Hello")
    go worker("World")

    // 等待
    time.Sleep(time.Second)
}
```

### Channel

```go
// channel 用於 goroutine 通訊
ch := make(chan int, 10)  // 緩衝 channel

// 發送
go func() {
    ch <- 42
}()

// 接收
value := <-ch
```

## 併發錯誤模式

### 競爭條件（Race Condition）

```python
# 競爭條件示例
# 執行緒1                  執行緒2
# read counter (5)         read counter (5)
# increment (6)            increment (7)
# write counter (6)        write counter (7)
# 期望：7                  期望：7
# 實際：可能是 6 或 7
```

### 死鎖（Deadlock）

```python
# 死鎖示例
# 執行緒1                執行緒2
# lock A                  lock B
# lock B (等待)           lock A (等待)
#                        永遠等待
```

### 避免死鎖的策略

1. **固定順序獲取鎖**
2. **使用 try_lock**
3. **設定超時**
4. **銀行家演算法**

## 並發設計原則

1. **最小化共享狀態**
2. **使用不可變資料**
3. **優先使用高層次抽象**（如 Actor、Channel）
4. **設計時考慮併發安全**
5. **使用工具檢測競爭條件**

## 小結

並發是現代程式設計的重要課題。從執行緒到 Actor，從 Coroutine 到 Goroutine，各種模型都有其適用場景。選擇合適的並發模型，能讓程式更高效、更安全。