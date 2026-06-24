# 競爭條件與互斥鎖

## 什麼是競爭條件？

競爭條件（race condition）發生於多個執行緒同時存取共享資源，且結果取決於執行緒的執行順序。當至少一個執行緒在修改資料時，未受保護的共享存取就會導致不確定的行為。

## 經典範例：計數器

```python
import threading
counter = 0

def increment():
    global counter
    for _ in range(1000000):
        temp = counter
        temp = temp + 1
        counter = temp

# 兩個執行緒同時執行 increment
t1 = threading.Thread(target=increment)
t2 = threading.Thread(target=increment)
t1.start(); t2.start()
t1.join(); t2.join()
print(counter)  # 可能不是 2000000！
```

### 為什麼會出錯？

`counter = temp` 不是原子操作。兩個執行緒可能同時讀取到相同的 `counter` 值，各自加 1，然後寫回——導致只增加 1 而非 2。

## 臨界區段

臨界區段（critical section）是程式中存取共享資源的程式碼片段。臨界區段必須滿足：

1. **互斥（Mutual Exclusion）**：同一時間只能有一個執行緒在臨界區段內
2. **前進（Progress）**：如果沒有執行緒在臨界區段，要進入的執行緒必須能夠進入
3. **有限等待（Bounded Waiting）**：執行緒等待進入臨界區段的時間必須有上限

## 互斥鎖（Mutex）

互斥鎖是最常見的同步機制：

```python
import threading
lock = threading.Lock()

def safe_increment():
    global counter
    for _ in range(1000000):
        with lock:  # acquire
            temp = counter
            temp = temp + 1
            counter = temp
        # release 在離開 with 區塊時自動執行
```

### 互斥鎖的實作

互斥鎖底層依賴硬體提供的原子指令：

- **Test-and-Set（TSL）**：原子地讀取並設置一個記憶體位置
- **Compare-and-Swap（CAS）**：原子地比較並交換
- **Load-Link / Store-Conditional（LL/SC）**：ARM/PowerPC 使用

```python
# CAS 的 Python 類比（實際上不是原子的）
class AtomicLock:
    def __init__(self):
        self.flag = False

    def acquire(self):
        while True:
            # 原子操作：如果 flag == False，設置為 True 並返回 True
            if self.atomic_compare_and_swap(False, True):
                return

    def release(self):
        self.flag = False
```

## 自旋鎖（Spinlock）

自旋鎖是一種特殊的互斥鎖——當鎖被持有時，等待的執行緒會「忙等待」（不斷循環檢查鎖狀態）：

```python
class Spinlock:
    def __init__(self):
        self.locked = False

    def acquire(self):
        while self.atomic_test_and_set(self.locked):
            pass  # 忙等待

    def release(self):
        self.locked = False
```

### 何時使用自旋鎖？

- 鎖被持有的時間極短（數十個指令）
- 不希望執行緒被排程器暫停（如在核心中斷處理程式）
- 多核心系統（其他核心可以在等待期間完成工作）

**缺點**：單核心系統中自旋鎖浪費 CPU 時間。

## 讀寫鎖（RWLock）

讀寫鎖允許多個讀者同時讀取，但寫者必須獨佔：

```python
import threading
rwlock = threading.RLock()  # Python 無原生 RWLock，以 RLock 近似

class RWLock:
    def __init__(self):
        self.readers = 0
        self.lock = threading.Lock()

    def acquire_read(self):
        with self.lock:
            self.readers += 1

    def release_read(self):
        with self.lock:
            self.readers -= 1

    def acquire_write(self):
        self.lock.acquire()

    def release_write(self):
        self.lock.release()
```

## RCU（Read-Copy-Update）

RCU 是 Linux 核心中的一種高效同步機制，讀者不需要鎖：

- 讀者：直接讀取資料，無需同步
- 寫者：複製資料、修改副本、更新指標、等待所有現有讀者完成後釋放舊資料

RCU 適合讀取頻繁、寫入稀少的場景（如路由表）。

## 延伸閱讀

- [競爭條件範例與解法](https://www.google.com/search?q=race+condition+example+solution)
- [互斥鎖的硬體實作](https://www.google.com/search?q=mutex+hardware+implementation+TSL+CAS)
- [Linux RCU 機制](https://www.google.com/search?q=Linux+kernel+RCU+read+copy+update)
