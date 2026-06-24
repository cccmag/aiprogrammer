# 多執行緒 threading

## GIL 枷鎖下的並行（2003-2026）

### 前言

多執行緒（multithreading）是程式設計中最常見的並行模型。在 Python 中，threading 模組提供了與作業系統執行緒的介面。但 Python 的多執行緒有一個重要的限制——GIL（全域直譯器鎖）。

### GIL：Python 的雙面刃

GIL 是 CPython 直譯器中的一個互斥鎖，確保在任何時刻只有一個執行緒執行 Python 位元組碼：

```python
import threading
import time

def count(n):
    while n > 0:
        n -= 1

# 創建兩個執行緒
t1 = threading.Thread(target=count, args=(10_000_000,))
t2 = threading.Thread(target=count, args=(10_000_000,))

start = time.time()
t1.start()
t2.start()
t1.join()
t2.join()
print(f"雙執行緒: {time.time() - start:.2f}s")

# 由於 GIL，這兩個執行緒實際上無法平行執行
# CPU 密集任務：雙執行緒不一定比單執行緒快
```

這意味著對於 CPU 密集型的任務，Python 的多執行緒無法利用多核心。

### threading 的基本使用

```python
import threading

def worker(name, count):
    for i in range(count):
        print(f"[{name}] step {i}")

# 創建執行緒
threads = []
for i in range(3):
    t = threading.Thread(target=worker, args=(f"T{i}", 5))
    threads.append(t)
    t.start()

# 等待所有執行緒完成
for t in threads:
    t.join()
```

### Lock：執行緒安全

當多個執行緒存取共享資料時，需要使用鎖來避免競爭條件：

```python
import threading

counter = 0
lock = threading.Lock()

def increment():
    global counter
    for _ in range(100000):
        with lock:
            counter += 1
        # 不使用鎖：
        # counter += 1   ← 非執行緒安全

threads = [threading.Thread(target=increment) for _ in range(10)]
for t in threads: t.start()
for t in threads: t.join()
print(f"計數器: {counter}")  # 總是 1000000
```

### RLock 與死鎖

`RLock`（可重入鎖）允許同一個執行緒多次獲取鎖，避免死鎖：

```python
lock = threading.RLock()  # 可重入

def recursive(n):
    with lock:
        if n > 0:
            recursive(n - 1)

# 如果用 threading.Lock()，上述程式碼會死鎖
# 因為同一個執行緒不能兩次獲取普通的 Lock
```

### Condition 與生產者消費者

Condition 物件讓執行緒可以在特定條件下等待和通知：

```python
import threading, time, random

queue = []
condition = threading.Condition()

def producer():
    for i in range(5):
        with condition:
            queue.append(i)
            print(f"生產: {i}")
            condition.notify()
        time.sleep(random.random())

def consumer():
    while True:
        with condition:
            while not queue:
                condition.wait()
            item = queue.pop(0)
            print(f"消費: {item}")
```

### 什麼時候用 threading

- **I/O 密集型任務**：GIL 在 I/O 等待時會釋放，所以多執行緒對網路請求、檔案讀寫有效
- **GUI 應用**：保持介面響應
- **混合工作負載**：有等待也有計算

### 小結

Python 的 threading 受 GIL 限制，不適合 CPU 密集的平行計算，但對於 I/O 密集型和需要保留響應性的場景仍然非常實用。理解 GIL 的機制是正確使用 Python 多執行緒的關鍵。

---

**下一步**：[多程序 multiprocessing](focus5.md)

## 延伸閱讀

- [Python threading 官方文件](https://www.google.com/search?q=Python+threading+module+documentation)
- [GIL 介紹與分析](https://www.google.com/search?q=Python+GIL+global+interpreter+lock+explained)
- [Real Python: Threading in Python](https://www.google.com/search?q=Real+Python+threading+guide)
