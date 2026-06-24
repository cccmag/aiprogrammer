# Python 列表深度解析

## 列表的底層實作

Python 的 `list` 是動態陣列（Dynamic Array），底層使用 C 語言的 `PyObject*` 陣列儲存元素指標。初始容量約為 0，加入元素時會逐步擴充。

```python
import sys
lst = []
print(sys.getsizeof(lst))  # 56 bytes (空列表)
lst.append(1)
print(sys.getsizeof(lst))  # 88 bytes (擴充一次)
```

## 列表的擴充策略

當列表容量不足時，Python 會重新分配更大的記憶體空間。CPython 的擴充策略是大約 1.125 倍：

```python
import sys
lst = []
for i in range(100):
    lst.append(i)
    if i < 10 or i % 10 == 9:
        print(f"len={len(lst):3d}, size={sys.getsizeof(lst):4d}")
```

## 列表操作的時間複雜度

### 常用操作

| 操作 | 程式碼 | 時間複雜度 |
|------|--------|-----------|
| 索引 | `lst[i]` | O(1) |
| 尾部新增 | `lst.append(x)` | O(1)* |
| 尾部彈出 | `lst.pop()` | O(1) |
| 任意位置插入 | `lst.insert(i, x)` | O(n) |
| 任意位置刪除 | `lst.pop(i)` | O(n) |
| 包含檢查 | `x in lst` | O(n) |
| 排序 | `lst.sort()` | O(n log n) |

*平攤後為 O(1)

## 列表 vs 元組

```python
# 列表可變
lst = [1, 2, 3]
lst[0] = 99  # OK

# 元組不可變
tup = (1, 2, 3)
# tup[0] = 99  # TypeError
```

元組因為不可變，可作為字典的鍵；列表則不行。

## 列表推導式

列表推導式是 Python 標誌性的語法糖，讓程式碼更簡潔：

```python
# 傳統方式
squares = []
for i in range(10):
    squares.append(i * i)

# 列表推導式
squares = [i * i for i in range(10)]

# 含條件
evens = [i for i in range(20) if i % 2 == 0]
```

## 參考資源

- https://www.google.com/search?q=Python+list+internal+implementation+CPython
- https://www.google.com/search?q=Python+list+time+complexity

## 小結

深入理解 Python 列表的底層運作，能幫助你寫出更高效的程式碼，並在選擇資料結構時做出更明智的決定。
