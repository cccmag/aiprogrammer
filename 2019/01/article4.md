# contextvars 上下文變數

## contextvars 簡介

contextvars 是 Python 3.7 引入的模組，提供了一種在非同步環境中管理執行上下文的方法。

## 基本用法

```python
from contextvars import ContextVar

# 建立上下文變數
request_id: ContextVar[str] = ContextVar('request_id', default='')

# 設定值
request_id.set('abc-123')

# 取得值
print(request_id.get())  # abc-123
```

## 複寫上下文

```python
from contextvars import ContextVar

user_context: ContextVar[dict] = ContextVar('user_context', default={})

def get_user():
    return user_context.get()

# 在不同上下文中執行
import contextvars

token = user_context.set({'name': 'Alice', 'role': 'admin'})

# 只在這個上下文中生效
print(get_user())  # {'name': 'Alice', 'role': 'admin'}
```

## asyncio 中的應用

```python
import asyncio
from contextvars import ContextVar

request_id = ContextVar('request_id', default='unknown')

async def handle_request(req_id: str):
    request_id.set(req_id)
    await asyncio.sleep(0.1)
    print(f"處理請求：{request_id.get()}")

async def main():
    await asyncio.gather(
        handle_request('req-1'),
        handle_request('req-2'),
        handle_request('req-3'),
    )

asyncio.run(main())
# 輸出：
# 處理請求：req-1
# 處理請求：req-2
# 處理請求：req-3
```

## Token 機制

使用 Token 恢復先前的值：

```python
from contextvars import ContextVar

trace_id = ContextVar('trace_id', default='')

# 設定並取得 Token
token = trace_id.set('trace-abc')

# 做一些操作
print(trace_id.get())  # trace-abc

# 使用 Token 恢復
trace_id.reset(token)

print(trace_id.get())  # ''（恢復到預設值）
```

## copy_context

複製當前上下文：

```python
from contextvars import copy_context

def child_function():
    print(f"子函數：{request_id.get()}")

async def async_child():
    await asyncio.sleep(0)
    print(f"非同步子：{request_id.get()}")

request_id.set('main-trace')

# 複製上下文
ctx = copy_context()
ctx.run(child_function)

# 在新的事件迴圈中使用
asyncio.run(async_child())
```

## 實際應用：請求追蹤

```python
from contextvars import ContextVar
import uuid
import asyncio

request_id: ContextVar[str] = ContextVar('request_id')
user_id: ContextVar[str] = ContextVar('user_id')

class RequestContext:
    def __init__(self, request_id: str, user_id: str):
        self.request_id = request_id
        self.user_id = user_id
        self.token_request = None
        self.token_user = None

    def __enter__(self):
        self.token_request = request_id.set(self.request_id)
        self.token_user = user_id.set(self.user_id)
        return self

    def __exit__(self, *args):
        request_id.reset(self.token_request)
        user_id.reset(self.token_user)

async def process():
    print(f"Request: {request_id.get()}, User: {user_id.get()}")

async def main():
    with RequestContext("req-123", "user-456"):
        await process()

asyncio.run(main())
```

## 與 thread-local 比較

```python
import threading
from contextvars import ContextVar

# thread-local（每個執行緒一份）
thread_local = threading.local()
thread_local.value = "thread-data"

# contextvars（每個上下文一份，更適合 asyncio）
context_var = ContextVar('data', default='')
context_var.set('context-data')
```

## 參考資源

- https://www.google.com/search?q=Python+contextvars+tutorial+asyncio+2019
- https://www.google.com/search?q=Python+ContextVar+copy_context+token+examples+2019
- https://www.google.com/search?q=Python+contextvars+vs+threading+local+asyncio+2019