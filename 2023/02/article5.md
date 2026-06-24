# 號誌與管程

## 號誌（Semaphore）

號誌是 Edsger Dijkstra 在 1965 年提出的同步機制。它是一個整數變數，支援兩個原子操作：

- **P 操作（proberen, 測試）**：若號誌 > 0，減 1 並繼續；否則阻塞
- **V 操作（verhogen, 增加）**：加 1，若有等待的執行緒則喚醒一個

### 號誌的類型

**二元號誌（Binary Semaphore）**：值只能為 0 或 1，等價於互斥鎖。

**計數號誌（Counting Semaphore）**：值代表可用資源的數量，用於管理有限資源池。

### Python 範例

```python
import threading
semaphore = threading.Semaphore(3)  # 最多 3 個執行緒同時訪問

def access_resource(tid):
    semaphore.acquire()
    print(f"執行緒 {tid} 正在使用資源")
    # 使用資源...
    semaphore.release()

threads = [threading.Thread(target=access_resource, args=(i,))
           for i in range(10)]
for t in threads: t.start()
for t in threads: t.join()
```

### 號誌的應用

1. **互斥**：二元號誌保護臨界區段
2. **同步**：確保操作以特定順序執行
3. **資源計數**：管理有限數量的資源實例
4. **生產者-消費者**：協調生產者和消費者的進度

### 生產者-消費者問題

```python
from collections import deque
empty = threading.Semaphore(5)   # 緩衝區空位數量
full = threading.Semaphore(0)    # 緩衝區已滿數量
mutex = threading.Semaphore(1)   # 保護緩衝區存取
buffer = deque()

def producer():
    item = produce()
    empty.acquire()
    mutex.acquire()
    buffer.append(item)
    mutex.release()
    full.release()

def consumer():
    full.acquire()
    mutex.acquire()
    item = buffer.popleft()
    mutex.release()
    empty.release()
    consume(item)
```

## 管程（Monitor）

管程是 C. A. R. Hoare 在 1974 年提出的更高層次同步抽象。它將互斥鎖和條件變數封裝在同一個單元中。

### 管程的組成

- **互斥鎖**：確保同一時間只有一個執行緒在管程內執行
- **條件變數**：允許執行緒在特定條件下等待
- **信號操作**：喚醒等待特定條件的執行緒

### Python 條件變數

```python
import threading
cond = threading.Condition()

class BoundedBuffer:
    def __init__(self, size):
        self.buffer = deque(maxlen=size)
        self.cond = threading.Condition()

    def put(self, item):
        with self.cond:
            while len(self.buffer) == self.buffer.maxlen:
                self.cond.wait()  # 緩衝區滿，等待
            self.buffer.append(item)
            self.cond.notify()    # 喚醒等待的消費者

    def get(self):
        with self.cond:
            while len(self.buffer) == 0:
                self.cond.wait()  # 緩衝區空，等待
                item = self.buffer.popleft()
            self.cond.notify()    # 喚醒等待的生產者
            return item
```

### 條件變數的關鍵細節

- `wait()` 在等待前釋放互斥鎖，喚醒後重新獲得
- 使用 `while` 而非 `if` 檢查條件——防止假喚醒（spurious wakeup）
- `notify()` 喚醒一個等待執行緒，`notify_all()` 喚醒所有

## 號誌 vs 管程

| 特點 | 號誌 | 管程 |
|------|------|------|
| 抽象層次 | 低階 | 高階 |
| 易用性 | 容易出錯（配對問題） | 比較安全 |
| 靈活性 | 高（可用於行程間同步） | 受限於行程內 |
| 條件管理 | 需要手動管理 | 內建條件變數 |
| 錯誤風險 | 遺漏 V 操作會導致死結 | 結構化，不易出錯 |

## 現代語言中的同步原語

| 語言 | 互斥鎖 | 號誌 | 條件變數 | 高階抽象 |
|------|--------|------|---------|---------|
| C (pthreads) | pthread_mutex_t | sem_t | pthread_cond_t | — |
| C++ | mutex | counting_semaphore | condition_variable | lock_guard |
| Java | synchronized | Semaphore | Condition | BlockingQueue |
| Python | threading.Lock | Semaphore | Condition | Queue |
| Go | sync.Mutex | — | sync.Cond | channel |
| Rust | std::sync::Mutex | sema::Semaphore | Condvar | mpsc channel |

## 延伸閱讀

- [Dijkstra 號誌原論文](https://www.google.com/search?q=Dijkstra+semaphore+1965+paper+Cooperating+Sequential+Processes)
- [Hoare 管程原論文](https://www.google.com/search?q=Hoare+monitor+1974+paper+operating+systems)
- [生產者-消費者問題比較](https://www.google.com/search?q=producer+consumer+problem+semaphore+vs+monitor)
