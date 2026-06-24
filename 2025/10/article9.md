# 記憶體管理與最佳化

## 1. 引言

Python 的自動記憶體管理讓開發者不必手動分配和釋放記憶體，但這不代表記憶體問題不存在。記憶體洩漏、過度分配、碎片化都可能導致效能問題甚至程式崩潰。本文將探討 Python 的記憶體管理機制與最佳化策略。

## 2. 引用計數

Python 使用引用計數（reference counting）作為主要的記憶體管理機制——每個物件維護一個計數器，記錄有多少引用指向它：

```python
import sys

a = []
print(sys.getrefcount(a))  # 2（a + getrefcount 的參數）

b = a
print(sys.getrefcount(a))  # 3（a + b + getrefcount 的參數）

b = None
print(sys.getrefcount(a))  # 2
```

當引用計數降為 0 時，物件立即被回收。

## 3. 分代垃圾回收

引用計數無法處理循環引用（cyclic reference）——兩個物件互相引用但不再被使用：

```python
class Node:
    def __init__(self, name):
        self.name = name
        self.ref = None

# 循環引用
a = Node("A")
b = Node("B")
a.ref = b
b.ref = a

# 雖然 a 和 b 不再可達，但引用計數不為 0
# 分代 GC 會處理這種情況
a = None
b = None
```

Python 的 GC 分為三代：
- 第 0 代：新建立的物件（最常檢查）
- 第 1 代：存活過一次 GC 的物件
- 第 2 代：存活過多次 GC 的物件

## 4. 偵測記憶體洩漏

```python
import gc

# 手動觸發 GC
gc.collect()

# 獲取不可達物件的數量
print(gc.get_count())

# 停用 GC（不建議在生產環境使用）
gc.disable()

# 除錯循環引用
gc.set_debug(gc.DEBUG_LEAK)
```

## 5. weakref：弱引用

弱引用不會增加引用計數，適合快取和觀察者模式：

```python
import weakref

class Cache:
    def __init__(self):
        self._cache = {}
    
    def get(self, key):
        ref = self._cache.get(key)
        if ref is not None:
            obj = ref()
            if obj is not None:
                return obj
            # 物件已被回收
            del self._cache[key]
        return None

    def set(self, key, obj):
        self._cache[key] = weakref.ref(obj)
```

## 6. __slots__ 節省記憶體

每個 Python 物件都有一個 `__dict__` 字典來儲存屬性——這很靈活但浪費記憶體。`__slots__` 可以節省記憶體：

```python
# 沒有 __slots__
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# 使用 __slots__
class PointSlots:
    __slots__ = ('x', 'y')
    def __init__(self, x, y):
        self.x = x
        self.y = y

import sys
p1 = Point(1, 2)
p2 = PointSlots(1, 2)
print(sys.getsizeof(p1))  # 56（含 __dict__）
print(sys.getsizeof(p2))  # 48（無 __dict__）
# 在大量物件時差異更明顯
```

## 7. array 與 struct

對於大量數值資料，`array` 和 `struct` 比 list 更節省記憶體：

```python
import array
import struct

# list：每個元素是 Python 物件
list_of_ints = [i for i in range(1000)]
# 每個 Python int 約 28 bytes

# array：連續記憶體
array_of_ints = array.array('i', range(1000))
# 每個 int 僅 4 bytes

# struct：打包二進制資料
data = struct.pack('!I4s', 42, b'test')
number, text = struct.unpack('!I4s', data)
```

## 8. 記憶體最佳化策略

```python
# 1. 使用生成器代替列表
# 壞：一次建立巨量列表
all_data = [process(item) for item in huge_dataset]

# 好：惰性處理
for item in (process(x) for x in huge_dataset):
    pass

# 2. 重用物件
# 壞：每次建立新物件
for i in range(1000):
    result = expensive_function(i)

# 好：重用緩衝區
buffer = []
for i in range(1000):
    buffer.clear()
    fill_buffer(i, buffer)
    process(buffer)

# 3. 使用原地操作
# 壞：建立新 list
items = [i for i in range(1000)]
items = [x * 2 for x in items]

# 好：原地修改
for i in range(len(items)):
    items[i] *= 2
```

## 9. 總結

Python 的記憶體管理雖然自動化，但非無償。引用計數確保了即時回收，分代 GC 處理了循環引用。理解這些機制可以幫助我們寫出更節省記憶體的 Python 程式。

## 延伸閱讀

- [Python 記憶體管理官方文件](https://www.google.com/search?q=Python+memory+management+documentation)
- [Real Python: Python Memory Management](https://www.google.com/search?q=Real+Python+memory+management)
