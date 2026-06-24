# 上下文管理器 with

## 資源管理的優雅模式（2006-2026）

### 前言

上下文管理器（context manager）是 Python 中管理資源的標準模式。無論是檔案操作、資料庫連線、鎖定機制，還是網路請求，`with` 語句提供了一個統一的介面來確保資源的正確獲取和釋放。

### with 語句

最常見的上下文管理器是檔案操作：

```python
# 傳統方式
f = open("file.txt", "r")
try:
    data = f.read()
finally:
    f.close()

# 使用 with
with open("file.txt", "r") as f:
    data = f.read()
# 離開 with 區塊時自動關閉檔案
```

`with` 語句保證了即使在區塊中發生異常，`__exit__` 方法也會被呼叫。

### 自訂上下文管理器

任何實作了 `__enter__` 和 `__exit__` 方法的類別都可以作為上下文管理器：

```python
class ManagedFile:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
    
    def __enter__(self):
        self.file = open(self.filename, self.mode)
        return self.file
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()
        # 返回 False 表示不抑制異常
        # 返回 True 表示抑制異常
        return False

with ManagedFile("test.txt", "w") as f:
    f.write("Hello, World!")
```

### __exit__ 的異常處理

`__exit__` 方法接收三個參數——異常型別、異常值、追蹤資訊：

```python
class DatabaseConnection:
    def __enter__(self):
        self.conn = connect_to_db()
        return self.conn
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            # 發生異常，回滾交易
            self.conn.rollback()
        else:
            # 正常結束，提交交易
            self.conn.commit()
        self.conn.close()
        return False  # 不吞沒異常
```

### contextlib 模組

Python 的 `contextlib` 提供了實用工具來簡化上下文管理器的建立：

```python
from contextlib import contextmanager

@contextmanager
def managed_file(filename, mode):
    f = open(filename, mode)
    try:
        yield f
    finally:
        f.close()

with managed_file("test.txt", "w") as f:
    f.write("Hello!")
```

`@contextmanager` 裝飾器將一個生成器函式轉換為上下文管理器——`yield` 之前的程式碼在 `__enter__` 執行，之後的在 `__exit__` 執行。

### 巢狀上下文管理器

多個 `with` 可以巢狀或合併：

```python
# 巢狀寫法
with open("a.txt") as f1:
    with open("b.txt") as f2:
        data = f1.read() + f2.read()

# 合併寫法（Python 2.7+）
with open("a.txt") as f1, open("b.txt") as f2:
    data = f1.read() + f2.read()
```

### 常見應用場景

1. **檔案操作**：自動關閉檔案
2. **資料庫連線**：自動提交/回滾
3. **執行緒鎖**：自動獲取/釋放鎖
4. **網路請求**：自動關閉連線
5. **臨時檔案**：自動刪除
6. **目錄切換**：自動恢復
7. **效能計時**：自動計算時間

### 小結

上下文管理器提供了一種統一且安全的資源管理模式。`with` 語句讓程式碼更簡潔、更安全——不再需要記得在 `finally` 區塊中釋放資源。Python 標準庫中的檔案、鎖、資料庫連線等都實作了上下文管理器協定。

---

**下一步**：[多執行緒 threading](focus4.md)

## 延伸閱讀

- [PEP 343: The "with" Statement](https://www.google.com/search?q=PEP+343+with+statement+Python)
- [Python contextlib 官方文件](https://www.google.com/search?q=Python+contextlib+module+documentation)
- [Real Python: Context Managers](https://www.google.com/search?q=Real+Python+context+managers)
