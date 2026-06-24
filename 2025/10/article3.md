# 自訂上下文管理器

## 1. 引言

上下文管理器（Context Manager）是 Python 中管理資源的標準模式。從檔案操作到資料庫交易，從執行緒鎖到網路連線，`with` 語句讓資源管理變得安全且優雅。本文將探討如何自訂上下文管理器。

## 2. __enter__ 與 __exit__ 協定

任何實作了 `__enter__` 和 `__exit__` 方法的物件都可以作為上下文管理器：

```python
class DatabaseSession:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
    
    def __enter__(self):
        self.connection = connect(self.db_name)
        return self.connection
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.connection.rollback()
        else:
            self.connection.commit()
        self.connection.close()
        return False
```

## 3. 異常處理策略

`__exit__` 方法的返回值決定了異常的處理方式：

```python
class IgnoreException:
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type == ValueError:
            print(f"忽略 ValueError: {exc_val}")
            return True  # 抑制異常
        return False  # 不抑制其他異常

with IgnoreException():
    int("hello")  # ValueError 被忽略
```

## 4. @contextmanager 裝飾器

`contextlib` 提供了更簡潔的選擇：

```python
from contextlib import contextmanager

@contextmanager
def transaction(db):
    db.begin()
    try:
        yield db
    except:
        db.rollback()
        raise
    else:
        db.commit()
```

## 5. contextlib 實用工具

### closing：自動呼叫 close

```python
from contextlib import closing
import urllib.request

with closing(urllib.request.urlopen("https://python.org")) as page:
    data = page.read()
# 自動呼叫 page.close()
```

### suppress：忽略特定異常

```python
from contextlib import suppress

with suppress(FileNotFoundError):
    os.remove("tmp.txt")  # 如果檔案不存在，不報錯
```

### nullcontext：不需要資源的佔位

```python
from contextlib import nullcontext

# 條件式啟用/停用上下文管理器
ctx = profile if enable_profiling else nullcontext()
with ctx:
    run_expensive_function()
```

## 6. 非同步上下文管理器

Python 3.7+ 支援非同步上下文管理器：

```python
import asyncio

class AsyncDatabase:
    async def __aenter__(self):
        self.conn = await connect_async()
        return self.conn
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.conn.close()

async def main():
    async with AsyncDatabase() as db:
        await db.query("SELECT * FROM users")
```

## 7. 實戰案例：計時器

```python
import time
from contextlib import contextmanager

@contextmanager
def timer(label=""):
    start = time.perf_counter()
    yield
    elapsed = time.perf_counter() - start
    print(f"[{label}] {elapsed:.4f}s")

with timer("資料處理"):
    data = [i**2 for i in range(10_000_000)]
```

## 8. 上下文管理器的組合

多個上下文管理器可以巢狀或平行組合：

```python
# 巢狀
with open("a.txt") as f1:
    with open("b.txt") as f2:
        pass

# Python 3.1+ 平行
with open("a.txt") as f1, open("b.txt") as f2:
    pass

# Python 3.10+ 括號分組
with (
    open("a.txt") as f1,
    open("b.txt") as f2,
):
    pass
```

## 9. 總結

上下文管理器是 Python 資源管理的標準模式。自訂上下文管理器讓你可以封裝任何「開始-結束」的邏輯模式，確保資源總是能被正確釋放。

## 延伸閱讀

- [PEP 343: The "with" Statement](https://www.google.com/search?q=PEP+343+with+statement+Python)
- [Python contextlib 文件](https://www.google.com/search?q=Python+contextlib+documentation)
