# 執行緒安全與鎖

## 1. 引言

當多個執行緒同時存取共享資料時，競爭條件（race condition）就可能發生。執行緒安全是並行程式設計中最基本的課題。本文將探討 Python 中的執行緒安全機制。

## 2. 競爭條件的本質

```python
import threading

counter = 0

def increment():
    global counter
    for _ in range(100000):
        temp = counter      # 讀取
        counter = temp + 1  # 寫入

# 兩個執行緒同時執行
t1 = threading.Thread(target=increment)
t2 = threading.Thread(target=increment)
t1.start(); t2.start()
t1.join(); t2.join()
# 結果不一定等於 200000！
```

問題在於 `counter += 1` 不是原子操作——它包含了讀取-修改-寫入三個步驟。

## 3. Lock（互斥鎖）

最基本的同步原語：

```python
lock = threading.Lock()

def safe_increment():
    global counter
    for _ in range(100000):
        with lock:           # 獲取鎖
            counter += 1     # 臨界區
        # 釋放鎖
```

## 4. RLock（可重入鎖）

同一個執行緒可以多次獲取 RLock：

```python
lock = threading.RLock()

def recursive(n):
    with lock:
        if n > 0:
            recursive(n - 1)
```

如果用普通 Lock，同一個執行緒再次獲取會導致死鎖。

## 5. Semaphore（訊號量）

控制同時存取資源的執行緒數量：

```python
semaphore = threading.Semaphore(3)  # 最多 3 個同時存取

def access_resource():
    with semaphore:
        # 最多 3 個執行緒同時執行這裡
        use_resource()
```

## 6. Condition（條件變數）

讓執行緒在特定條件下等待或通知：

```python
import threading, time, random

class BoundedBuffer:
    def __init__(self, size):
        self.buffer = []
        self.size = size
        self.cond = threading.Condition()
    
    def put(self, item):
        with self.cond:
            while len(self.buffer) >= self.size:
                self.cond.wait()  # 緩衝區滿了，等待
            self.buffer.append(item)
            self.cond.notify()    # 通知消費者
    
    def get(self):
        with self.cond:
            while not self.buffer:
                self.cond.wait()  # 緩衝區空了，等待
            item = self.buffer.pop(0)
            self.cond.notify()    # 通知生產者
            return item
```

## 7. Event（事件）

用於執行緒間的簡單信號通知：

```python
event = threading.Event()

def waiter():
    print("等待事件...")
    event.wait()  # 阻塞直到事件被設定
    print("事件已觸發!")

def setter():
    time.sleep(2)
    print("觸發事件")
    event.set()

threading.Thread(target=waiter).start()
threading.Thread(target=setter).start()
```

## 8. GIL 與執行緒安全

GIL 確保了 Python 位元組碼層級的原子性，但這並不夠：

```python
# 這行在 Python 中不是原子的！
counter += 1
# 實際執行：
# 1. LOAD_FAST counter
# 2. LOAD_CONST 1
# 3. BINARY_OP (+=)
# 4. STORE_FAST counter
```

GIL 在執行緒數目少時開銷可忽略，但在多核心 CPU 密集場景中會成為瓶頸。

## 9. 無鎖程式設計

某些情況下可以用 `threading.local()` 避免鎖：

```python
local_data = threading.local()

def worker():
    local_data.counter = 0
    for i in range(100):
        local_data.counter += i
```

每個執行緒有自己的獨立副本，不需要鎖。

## 10. 死鎖預防

死鎖發生的四個必要條件：
1. 互斥
2. 持有並等待
3. 不可搶佔
4. 循環等待

預防策略包括鎖定順序統一、使用超時、優先使用 RLock。

## 11. 總結

執行緒安全是並行程式設計的基礎。Python 提供了 Lock、RLock、Semaphore、Condition、Event 等多種同步原語。理解 GIL 的限制對於設計正確的並行程式至關重要。

## 延伸閱讀

- [Python threading 官方文件](https://www.google.com/search?q=Python+threading+lock+documentation)
- [Real Python: Python Thread Safety](https://www.google.com/search?q=Real+Python+thread+safety)
