# 死結偵測與避免

## 死結的定義

死結（deadlock）是並行系統中一組行程互相等待對方釋放資源，導致所有行程都無法繼續執行的狀態。死結是同步問題中最嚴重的錯誤之一——它導致系統部分或完全停止回應。

## 死結的必要條件

Coffman 等人在 1971 年歸納了死結的四個必要條件（缺一不可）：

### 1. 互斥（Mutual Exclusion）

資源一次只能被一個行程使用。如果資源可以共享（如唯讀檔案），就不會產生死結。

### 2. 持有並等待（Hold and Wait）

行程持有至少一個資源，同時正在等待獲取其他行程持有的資源。

### 3. 不可搶占（No Preemption）

資源不能被作業系統強制收回——只能由持有行程自願釋放。

### 4. 循環等待（Circular Wait）

存在一組行程 {P0, P1, ..., Pn}，P0 等待 P1 持有的資源，P1 等待 P2 持有的資源，...，Pn 等待 P0 持有的資源。

## 資源分配圖

資源分配圖（Resource Allocation Graph, RAG）是分析死結的圖形工具：

- 圓形節點代表行程
- 方形節點代表資源（方形內的點代表資源實例）
- 從行程到資源的邊：行程請求資源
- 從資源到行程的邊：資源已分配給行程

```
    P1 ──→ R1 (請求)
    R1 ──→ P2 (已分配)
    P2 ──→ R2 (請求)
    R2 ──→ P1 (已分配)
```

如果圖中存在循環，且循環內每個資源只有一個實例，則系統處於死結狀態。

## 銀行家演算法

銀行家演算法（Dijkstra, 1965）是經典的死結避免演算法。它在資源分配前檢查是否會導致不安全狀態。

### 資料結構

- **Available[m]**：每類資源的可用數量
- **Max[n][m]**：每個行程對每類資源的最大需求
- **Allocation[n][m]**：每個行程已分配的資源數量
- **Need[n][m]**：每個行程還需要的資源數量（Need = Max - Allocation）

### 安全性演算法

```python
def is_safe(available, allocation, need):
    n = len(allocation)
    m = len(available)
    work = available[:]
    finish = [False] * n
    safe_sequence = []

    while len(safe_sequence) < n:
        found = False
        for i in range(n):
            if not finish[i] and all(need[i][j] <= work[j] for j in range(m)):
                for j in range(m):
                    work[j] += allocation[i][j]
                finish[i] = True
                safe_sequence.append(i)
                found = True
                break
        if not found:
            return False, []
    return True, safe_sequence
```

### 資源請求演算法

當行程 Pi 請求資源 Request[i]：

1. 檢查 Request[i] ≤ Need[i]（否則錯誤）
2. 檢查 Request[i] ≤ Available（否則等待）
3. 假裝分配：更新 Available、Allocation、Need
4. 執行安全性演算法
5. 若安全 → 確實分配；若不安全 → 回滾，讓 Pi 等待

## 死結偵測

當系統不採用死結預防或避免時，需要定期偵測死結：

### 單一資源實例

使用資源分配圖的循環偵測（拓撲排序）。若圖中存在循環，則有死結。

### 多資源實例

類似銀行家演算法，但尋找「是否可以完成」：

```python
def detect_deadlock(available, allocation, request):
    n = len(allocation)
    m = len(available)
    work = available[:]
    finish = [all(allocation[i][j] == 0 for j in range(m))
              for i in range(n)]

    while True:
        found = False
        for i in range(n):
            if not finish[i] and all(request[i][j] <= work[j] for j in range(m)):
                for j in range(m):
                    work[j] += allocation[i][j]
                finish[i] = True
                found = True
        if not found:
            break

    deadlocked = [i for i in range(n) if not finish[i]]
    return deadlocked
```

## 死結恢復

當死結被偵測到後，有三種恢復方式：

### 1. 終止行程

- **終止所有死結行程**：簡單但代價高
- **逐個終止**：每終止一個就重新偵測，盡量減少損失

選擇終止哪個行程時考慮：優先權、已運算時間、還有多少資源需要完成、終止代價。

### 2. 資源搶占

- 從死結行程中選一個「受害者」
- 搶占其資源分配給其他行程
- 受害行程需要回滾到安全狀態
- 需考慮：搶占代價、避免飢餓

### 3. 手動干預

在桌面系統中，使用者可以透過任務管理器終止沒有回應的程式。

## 實際系統中的死結處理

| 系統 | 策略 | 說明 |
|------|------|------|
| Linux | 預防 | 破壞持有等待（非強制） |
| Windows | 預防 + 偵測 | 核心物件使用嚴格的鎖順序 |
| 資料庫 | 偵測 + 回滾 | 使用超時和交易回滾 |
| 嵌入式 | 預防 | 靜態分析鎖順序 |

實際的通用作業系統很少使用銀行家演算法——它的限制太嚴格（需要預知最大需求）。相反，它們依賴於設計規範（如鎖排序）來預防死結。

## 延伸閱讀

- [銀行家演算法視覺化](https://www.google.com/search?q=Banker%27s+algorithm+visualization)
- [死結偵測技術](https://www.google.com/search?q=deadlock+detection+algorithms+resource+allocation)
- [Linux 核心死結預防](https://www.google.com/search?q=Linux+kernel+deadlock+prevention+lock+ordering)
