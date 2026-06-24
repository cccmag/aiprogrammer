# async/await 實戰

## 1. 引言

在掌握了 asyncio 的基礎概念後，本文將深入探討 async/await 在真實世界中的應用模式與進階技巧。

## 2. TaskGroup：結構化並行

Python 3.11 引入的 `TaskGroup` 提供了結構化並行：

```python
import asyncio

async def worker(n):
    await asyncio.sleep(n)
    if n == 2:
        raise ValueError("任務 2 失敗")
    return n

async def main():
    try:
        async with asyncio.TaskGroup() as tg:
            t1 = tg.create_task(worker(1))
            t2 = tg.create_task(worker(2))
            t3 = tg.create_task(worker(3))
        # 所有任務成功完成
        print(t1.result(), t3.result())
    except* ValueError as e:
        print(f"捕獲錯誤: {e}")
```

TaskGroup 確保了：
- 所有任務在離開 context 時完成
- 如果一個任務失敗，其他任務被取消
- 異常以 ExceptionGroup 的形式拋出

## 3. 超時與取消

### 超時控制

```python
import asyncio

async def slow_operation():
    await asyncio.sleep(10)
    return "完成"

async def main():
    try:
        result = await asyncio.wait_for(
            slow_operation(),
            timeout=2.0
        )
    except asyncio.TimeoutError:
        print("操作超時!")
```

### 取消任務

```python
async def main():
    task = asyncio.create_task(slow_operation())
    await asyncio.sleep(1)
    task.cancel()  # 請求取消
    
    try:
        await task
    except asyncio.CancelledError:
        print("任務被取消")
```

## 4. 非同步 Queue

```python
import asyncio
import random

async def producer(queue):
    for i in range(10):
        await asyncio.sleep(random.random())
        await queue.put(i)
        print(f"生產: {i}")
    await queue.put(None)  # 停止信號

async def consumer(queue, name):
    while True:
        item = await queue.get()
        if item is None:
            queue.task_done()
            break
        await asyncio.sleep(random.random())
        print(f"[{name}] 消費: {item}")
        queue.task_done()

async def main():
    queue = asyncio.Queue(maxsize=3)
    
    # 同時運行生產者和消費者
    await asyncio.gather(
        producer(queue),
        consumer(queue, "A"),
        consumer(queue, "B"),
    )

asyncio.run(main())
```

## 5. 非同步上下文管理器

自訂非同步上下文管理器：

```python
import asyncio

class AsyncResource:
    async def __aenter__(self):
        print("獲取資源")
        await asyncio.sleep(0.1)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("釋放資源")
        await asyncio.sleep(0.1)
    
    async def use(self):
        await asyncio.sleep(0.1)
        return "結果"

async def main():
    async with AsyncResource() as res:
        result = await res.use()
        print(result)

asyncio.run(main())
```

## 6. 非同步迭代器

```python
import asyncio

class AsyncRange:
    def __init__(self, n):
        self.n = n
        self.i = 0
    
    def __aiter__(self):
        return self
    
    async def __anext__(self):
        if self.i >= self.n:
            raise StopAsyncIteration
        await asyncio.sleep(0.1)
        self.i += 1
        return self.i

async def main():
    async for i in AsyncRange(5):
        print(i)

asyncio.run(main())
```

## 7. 實戰：並發 Web 爬蟲

```python
import asyncio
import aiohttp
from asyncio import Semaphore

async def fetch(session, url, semaphore):
    async with semaphore:
        try:
            async with session.get(url, timeout=10) as resp:
                return url, resp.status, await resp.text()
        except Exception as e:
            return url, 0, str(e)

async def crawl(urls, concurrency=10):
    semaphore = Semaphore(concurrency)
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url, semaphore) for url in urls]
        for coro in asyncio.as_completed(tasks):
            url, status, content = await coro
            print(f"{url}: {status} ({len(content)} bytes)")

async def main():
    urls = [f"https://httpbin.org/delay/{i}" for i in range(1, 11)]
    await crawl(urls, concurrency=5)

asyncio.run(main())
```

## 8. 效能優化技巧

- **限制並發數**：使用 Semaphore 控制資源使用
- **連接池**：重用 HTTP 連線（aiohttp 自動處理）
- **避免過度建立 Task**：每個 Task 有開銷
- **使用 asyncio.run()**：正確初始化和清理事件迴圈

## 9. 總結

async/await 在真實世界中需要結合多種模式——TaskGroup、Semaphore、Queue、超時控制等。掌握這些模式是寫出生產級別非同步程式的關鍵。

## 延伸閱讀

- [PEP 729: Task Groups](https://www.google.com/search?q=PEP+729+Task+Group+Python)
- [aiohttp 官方文件](https://www.google.com/search?q=aiohttp+Python+async+HTTP)
