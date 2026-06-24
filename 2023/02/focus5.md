# 同步與死結（1965-2023）

## 競爭條件

當多個執行緒同時存取共享資料，且至少一個執行緒在寫入資料時，就會產生競爭條件（race condition）。程式的輸出取決於執行緒的執行順序，這是不確定的。

```python
counter = 0
def increment():
    global counter
    temp = counter
    temp = temp + 1
    counter = temp
```

如果兩個執行緒同時執行 increment，可能的結果是 counter 增加 1 而非 2（因為兩個執行緒都讀到了相同的初始值）。

## 互斥鎖（Mutex）

互斥鎖是最基本的同步機制：

```python
import threading
lock = threading.Lock()

def safe_increment():
    global counter
    with lock:
        temp = counter
        temp = temp + 1
        counter = temp
```

互斥鎖的兩個基本操作：lock() 取得鎖（若鎖已被持有則阻塞），unlock() 釋放鎖。

## 號誌（Semaphore）

號誌是 Dijkstra 在 1965 年提出的更通用同步機制。它是一個整數變數，支援兩個原子操作：

- **P（proberen, 測試）**：若號誌 > 0，減 1；否則阻塞
- **V（verhogen, 增加）**：加 1，若有用等待者則喚醒一個

二元號誌（0 或 1）等價於互斥鎖。計數號誌可用於管理有限資源池。

```python
import threading
semaphore = threading.Semaphore(3)

def use_resource():
    semaphore.acquire()
    # 使用資源
    semaphore.release()
```

## 管程（Monitor）

管程（Hoare 1974）是更高層次的同步抽象，將互斥鎖和條件變數封裝在一起：

- 只有一個執行緒可以在管程內部執行
- 條件變數（condition variable）允許執行緒在特定條件下等待

```python
import threading
cond = threading.Condition()

with cond:
    while not condition_met():
        cond.wait()  # 釋放鎖並等待
    # 條件滿足後繼續執行
    cond.notify()   # 喚醒一個等待執行緒
```

## 死結的必要條件

Coffman 在 1971 年歸納出死結的四個必要條件：

1. **互斥（Mutual Exclusion）**：資源一次只能被一個行程使用
2. **持有與等待（Hold and Wait）**：行程持有資源的同時等待其他資源
3. **不可搶占（No Preemption）**：資源只能由持有者自願釋放
4. **循環等待（Circular Wait）**：行程 A 等待 B 的資源，B 等待 C 的資源，C 等待 A 的資源

四個條件必須同時滿足才會產生死結。

## 死結處理策略

### 死結預防

破壞四個必要條件中的任何一個：

- 破壞互斥：使用可共享資源（如唯讀檔案）
- 破壞持有等待：行程在執行前請求所有資源
- 破壞不可搶占：允許作業系統搶占資源
- 破壞循環等待：對資源編號，要求行程按序請求

### 死結避免

銀行家演算法（Dijkstra 1965）：在每次資源分配前檢查是否會導致不安全狀態。

### 死結偵測與恢復

允許死結發生，然後：

- 定期檢查系統中是否存在循環等待
- 終止一個或多個死結行程
- 搶占資源並回滾到安全狀態

## 經典同步問題

### 生產者-消費者問題

生產者將資料放入有限緩衝區，消費者取出資料。需要使用互斥鎖和兩個號誌（空位、已滿）。

### 讀寫者問題

多個讀者可以同時讀取，但寫者必須獨佔存取。優先權策略的選擇（讀者優先或寫者優先）會影響公平性。

### 餐飲哲學家問題

五個哲學家圍坐在圓桌旁，每人之間有一根筷子。哲學家需要兩根筷子才能吃飯。這個問題展示了死結（所有人同時拿左筷）和饑餓的可能性。

## 延伸閱讀

- [Dijkstra 號誌論文](https://www.google.com/search?q=Dijkstra+semaphore+1965+paper)
- [銀行家演算法](https://www.google.com/search?q=Banker%27s+algorithm+deadlock+avoidance)
- [餐飲哲學家問題](https://www.google.com/search?q=dining+philosophers+problem+solution)
- [死結的四個必要條件](https://www.google.com/search?q=Coffman+deadlock+conditions)
