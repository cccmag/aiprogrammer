# 排程演算法比較：FCFS、SJF、RR

## 引言

CPU 排程是作業系統的核心功能之一。排程演算法決定了在任一時刻哪個行程獲得 CPU 使用權，直接影響系統的效能和使用者體驗。

## 先到先服務（FCFS）

### 原理

FCFS 是最簡單的排程演算法。行程按照到達就緒佇列的順序執行，非搶占式。

### Python 實作

```python
def fcfs(processes):
    # processes: [(name, arrival, burst)]
    sorted_procs = sorted(processes, key=lambda x: x[1])
    time = 0
    for name, at, bt in sorted_procs:
        if time < at:
            time = at
        print(f"{name}: start={time}, finish={time+bt}")
        time += bt
```

### 分析

- 優點：實現簡單，公平
- 缺點：平均等待時間長，短行程可能被長行程阻塞（護理效應）
- 平均等待時間：O(n²) 量級，取決於行程到達順序

## 最短工作優先（SJF）

### 原理

選擇服務時間最短的行程執行。可以是非搶占式或搶占式（SRTF——最短剩餘時間優先）。

### Python 實作

```python
def sjf(processes):
    n = len(processes)
    ready = []
    queue = sorted(processes, key=lambda x: x[1])
    time = 0
    i = 0
    while i < n or ready:
        while i < n and queue[i][1] <= time:
            ready.append(queue[i]); i += 1
        if not ready:
            time = queue[i][1]; continue
        ready.sort(key=lambda x: x[2])
        name, at, bt = ready.pop(0)
        print(f"{name}: start={time}, finish={time+bt}")
        time += bt
```

### 分析

- 優點：平均等待時間最小（理論最優）
- 缺點：需要預知服務時間；可能導致長行程飢餓
- SJF 的最優性可以通過交換論證（exchange argument）證明

## 時間片輪轉（RR）

### 原理

每個行程獲得一個固定時間片（time quantum）。就緒行程以循環方式排隊。

### Python 實作

```python
def rr(processes, quantum):
    remaining = {p: bt for p, _, bt in processes}
    time = 0
    queue = deque(p for p, _, _ in processes)
    while any(remaining.values()):
        p = queue.popleft()
        run = min(quantum, remaining[p])
        remaining[p] -= run
        time += run
        if remaining[p] > 0:
            queue.append(p)
        print(f"{p}: ran {run}, remaining {remaining[p]}")
```

### 分析

- 優點：回應時間短，互動性好，公平
- 缺點：上下文切換開銷，時間片選擇困難
- 時間片選擇至關重要：10-100ms 是典型值

## 實驗比較

以四個行程的典型場景比較：

```python
processes = [("P1", 0, 5), ("P2", 1, 3), ("P3", 2, 8), ("P4", 3, 2)]
```

| 演算法 | 平均等待時間 | 平均周轉時間 | 特點 |
|--------|------------|------------|------|
| FCFS | 5.8 | 11.8 | 護理效應 |
| SJF | 4.0 | 10.0 | 最優平均等待 |
| RR (q=2) | 7.2 | 12.2 | 公平互動 |

## 結論

沒有完美的排程演算法。選擇取決於系統目標：

- 批次系統：SJF 或 FCFS
- 互動系統：RR 或多層回饋佇列
- 即時系統：優先權排程 + 截止時間保證

現代作業系統（如 Linux CFS）採用混合策略，結合多層回饋佇列和動態優先權調整。

## 延伸閱讀

- [CPU 排程演算法視覺化](https://www.google.com/search?q=CPU+scheduling+visualization+tool)
- [Linux CFS 排程器設計](https://www.google.com/search?q=Linux+CFS+scheduler+design+vruntime)
- [排程演算法數學分析](https://www.google.com/search?q=scheduling+algorithm+analysis+FCFS+SJF+RR)
