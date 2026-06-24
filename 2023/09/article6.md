# 不可變性與純函數

## 無副作用的程式設計

### 不可變性（Immutability）

不可變性是指資料一旦建立就不能被修改。要改變資料，必須建立新的副本。

```python
# 可變風格
def add_item(lst, item):
    lst.append(item)  # 修改原始列表
    return lst

# 不可變風格
def add_item_immutable(lst, item):
    return lst + [item]  # 建立新列表
```

### 不可變性的好處

1. **易於推理**：一個值不會被其他地方意外修改
2. **執行緒安全**：不需要鎖來保護共享資料
3. **暫存友好**：相同的輸入總是產生相同的結果
4. **回溯簡單**：可以保留歷史版本

### 純函數（Pure Function）

純函數滿足兩個條件：
1. **相同輸入總是產生相同輸出**（不依賴外部狀態）
2. **無副作用**（不修改外部變數、不執行 I/O）

```python
# 純函數
def add(a, b):
    return a + b

# 不純函數（依賴全域狀態）
counter = 0
def increment():
    global counter
    counter += 1
    return counter

# 不純函數（副作用）
def log_and_add(a, b):
    print(f"Adding {a} + {b}")  # I/O 副作用
    return a + b
```

### 參考透明性（Referential Transparency）

**參考透明性**是指表達式可以用其計算結果替換而不影響程式行為。這是純函數的關鍵特性：

```python
# 參考透明的表達式
result = add(3, 4) + add(3, 4)
# 可以替換為：
result = 7 + 7  # 保證相同結果

# 非參考透明
result = log_and_add(3, 4) + log_and_add(3, 4)
# 無法替換：會少列印一次日誌
```

### Python 中的不可變資料結構

```python
# 不可變型別
int_val = 42      # int 不可變
str_val = "hello" # str 不可變
tup = (1, 2, 3)   # tuple 不可變
frozen = frozenset([1, 2, 3])  # frozenset 不可變

# 可變型別
lst = [1, 2, 3]   # list 可變
dct = {"a": 1}    # dict 可變
st = {1, 2, 3}    # set 可變
```

### 實務中的取捨

完全不可變在實務中並不總是可行或高效。現代的策略是：

- **Rust 的所有權系統**：透過 `mut` 關鍵字控制可變性
- **持久化資料結構**：結構共享（structural sharing）實現高效「修改」
- **凍結（freezing）**：修改完成後轉為不可變
- **局部可變性**：函數內部可變，外部不可見

### 延伸閱讀

- [純函數程式設計](https://www.google.com/search?q=pure+functional+programming+benefits)
- [不可變資料結構](https://www.google.com/search?q=immutable+data+structures+programming)
