# 搜尋演算法：線性、二分、雜湊

## 線性搜尋（Linear Search）

最直覺的搜尋方式：從頭到尾逐一比對。資料不需排序，但效率較低。

```python
def linear_search(arr, target):
    for i, val in enumerate(arr):
        if val == target:
            return i
    return -1
```

- 最佳：O(1)
- 平均：O(n)
- 最差：O(n)

適用於小資料集或未排序資料。

## 二分搜尋（Binary Search）

二分搜尋每次將搜尋範圍縮減一半，效率極高，但要求資料必須已排序。

```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

- 時間複雜度：O(log n)
- 空間複雜度：O(1)

## 雜湊搜尋（Hash Search）

雜湊表（Hash Table）透過雜湊函數將鍵（Key）映射到陣列索引，達到接近 O(1) 的存取速度。Python 的 `dict` 和 `set` 底層就是雜湊表。

```python
phone_book = {
    "Alice": "0912-345-678",
    "Bob": "0987-654-321",
    "Charlie": "0922-333-444"
}
print(phone_book["Alice"])  # O(1) 平均
```

### 碰撞處理

不同鍵可能產生相同雜湊值，常見處理方式：
- **鏈結法（Chaining）**：同一槽用鏈結串列儲存多筆資料
- **開放定址法（Open Addressing）**：尋找下一個空槽

## 演算法對比

| 方法 | 時間 | 是否需要排序 | 適用場景 |
|------|------|-------------|---------|
| 線性搜尋 | O(n) | 否 | 小資料集 |
| 二分搜尋 | O(log n) | 是 | 靜態有序資料 |
| 雜湊搜尋 | O(1) 平均 | 否 | 大量鍵值對存取 |

## 參考資源

- https://www.google.com/search?q=searching+algorithms+linear+binary+hash
- https://www.google.com/search?q=Python+dict+hash+table+implementation

## 小結

選擇搜尋演算法時，要考慮資料量、是否排序、以及讀寫比例，才能達到最佳效能。
