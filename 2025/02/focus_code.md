# 程式碼解說：`_code/algorithms.py`

本期所有演算法實作都集中在單一檔案 `_code/algorithms.py` 中，由 `demo()` 函數統一呼叫展示。

## 檔案結構

```
_code/algorithms.py
├── Stack 類別        — 堆疊實作 (LIFO)
├── Queue 類別        — 佇列實作 (FIFO)
├── binary_search()   — 二分搜尋
├── quicksort()       — 快速排序
├── fibonacci_dp()    — 費氏數列 DP
└── demo()            — 展示主程式
```

## Stack 類別

使用 Python 內建 `list` 實作堆疊。`append()` 與 `pop()` 操作均為 O(1)。

```python
s = Stack()
s.push(5)
value = s.pop()
```

## Queue 類別

同樣使用 `list` 實作了簡易佇列。`enqueue()` 使用 `append()` (O(1))，`dequeue()` 使用 `pop(0)` (O(n))。在實務中應使用 `collections.deque` 以達到 O(1) 的 `popleft()`。

```python
q = Queue()
q.enqueue('A')
item = q.dequeue()
```

## binary_search()

經典的迭代式二分搜尋。使用雙指標 `left` 和 `right` 逐步縮小搜尋範圍。時間複雜度 O(log n)。若找不到目標則回傳 -1。

## quicksort()

採用分治法的簡潔實作。以中間元素為 pivot，使用列表推導式分割為小於、等於、大於三部分，再遞迴排序。時間複雜度平均 O(n log n)。

## fibonacci_dp()

使用動態規劃的 Bottom-up 方式計算費氏數列。建立長度為 n+1 的陣列 `dp`，逐步填入費氏數值。時間複雜度 O(n)，空間複雜度 O(n)。

## 執行方式

```bash
bash _code/test.sh
```

或直接執行：

```bash
python3 _code/algorithms.py
```

## 參考資源

- https://www.google.com/search?q=Python+stack+queue+implementation+guide
- https://www.google.com/search?q=Python+quicksort+code+walkthrough
