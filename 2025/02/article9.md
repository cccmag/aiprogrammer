# 雜湊表與字典實作

## 雜湊表的核心概念

雜湊表（Hash Table）是一種透過鍵（Key）直接存取值的資料結構。它使用雜湊函數將鍵映射到陣列的某個位置，達到平均 O(1) 的存取速度。

## Python 字典底層

Python 的 `dict` 是高度最佳化的雜湊表實作。從 Python 3.6 開始，字典會保留插入順序。

```python
d = {}
d["name"] = "Alice"
d["age"] = 25
d["city"] = "Taipei"
print(d)  # {'name': 'Alice', 'age': 25, 'city': 'Taipei'}
```

## 自製簡易雜湊表

```python
class SimpleHashTable:
    def __init__(self, size=10):
        self.size = size
        self.table = [[] for _ in range(size)]

    def _hash(self, key):
        return hash(key) % self.size

    def set(self, key, value):
        idx = self._hash(key)
        for i, (k, _) in enumerate(self.table[idx]):
            if k == key:
                self.table[idx][i] = (key, value)
                return
        self.table[idx].append((key, value))

    def get(self, key):
        idx = self._hash(key)
        for k, v in self.table[idx]:
            if k == key:
                return v
        raise KeyError(key)

    def delete(self, key):
        idx = self._hash(key)
        for i, (k, _) in enumerate(self.table[idx]):
            if k == key:
                del self.table[idx][i]
                return
        raise KeyError(key)

ht = SimpleHashTable()
ht.set("apple", 100)
ht.set("banana", 200)
print(ht.get("apple"))    # 100
print(ht.get("banana"))   # 200
```

## 碰撞處理

雜湊衝突不可避免，常見處理方式：

### 1. 鏈結法（Chaining）

每個陣列槽存放一個鏈結串列（或 Python 列表），多個鍵對應到同一槽時串在一起。

### 2. 開放定址法（Open Addressing）

發生衝突時尋找下一個空槽，常見策略：
- 線性探測：`(hash(key) + i) % size`
- 二次探測：`(hash(key) + i²) % size`

```python
class LinearProbeHashTable:
    def __init__(self, size=10):
        self.size = size
        self.keys = [None] * size
        self.values = [None] * size

    def set(self, key, value):
        idx = hash(key) % self.size
        while self.keys[idx] is not None:
            if self.keys[idx] == key:
                self.values[idx] = value
                return
            idx = (idx + 1) % self.size
        self.keys[idx] = key
        self.values[idx] = value
```

## 字典的應用

- 快取（Memoization）
- 計數器（Counter）
- 資料庫索引
- JSON 物件解析

## 參考資源

- https://www.google.com/search?q=Python+dict+internal+implementation
- https://www.google.com/search?q=hash+table+collision+resolution+techniques

## 小結

雜湊表是電腦科學中最重要的資料結構之一，Python 字典的高效能讓它成為日常開發不可或缺的工具。
