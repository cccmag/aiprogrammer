# 2. asyncio 非同步程式設計

## asyncio 模組概述

asyncio 是 Python 的非同步程式設計框架，於 Python 3.4 引入，Python 3.7 大幅強化。asyncio 讓開發者能夠用同步的方式撰寫非同步程式碼，大幅簡化了併發程式的開發。

## 基本概念

### Coroutine 協程

協程是一種可以在執行中途暫停的函數：

```python
async def fetch_data():
    print("開始獲取資料")
    await asyncio.sleep(1)  # 模擬 I/O 操作
    return {"data": "結果"}

async def main():
    result = await fetch_data()
    print(f"獲取到：{result}")

asyncio.run(main())
```

### Task 任務

Task 用於併發執行協程：

```python
async def task1():
    await asyncio.sleep(1)
    return "Task 1 完成"

async def task2():
    await asyncio.sleep(2)
    return "Task 2 完成"

async def main():
    # 建立任務
    t1 = asyncio.create_task(task1())
    t2 = asyncio.create_task(task2())

    # 並行執行
    results = await asyncio.gather(t1, t2)
    print(results)

asyncio.run(main())
```

## Python 3.7 新 API

### asyncio.create_task()

```python
async def demo():
    # Python 3.7+ 新語法
    task = asyncio.create_task(async_operation())
    result = await task
    return result
```

### asyncio.current_task()

```python
async def identify():
    current = asyncio.current_task()
    print(f"目前任務：{current}")
    print(f"任務名稱：{current.get_name()}")

asyncio.run(identify())
```

### asyncio.all_tasks()

```python
async def list_all_tasks():
    all_tasks = asyncio.all_tasks()
    for task in all_tasks:
        print(f"  任務：{task}")
```

## 常見模式

### 並發下載

```python
import asyncio
import aiohttp

async def fetch_url(session, url):
    async with session.get(url) as response:
        return await response.text()

async def fetch_all(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        return await asyncio.gather(*tasks)

urls = [
    "https://api.example.com/data/1",
    "https://api.example.com/data/2",
    "https://api.example.com/data/3",
]

asyncio.run(fetch_all(urls))
```

### 訊息佇列

```python
async def producer(queue):
    for i in range(5):
        await queue.put(i)
        print(f"生產：{i}")
    await queue.put(None)  # 結束訊號

async def consumer(queue):
    while True:
        item = await queue.get()
        if item is None:
            break
        print(f"消費：{item}")

async def main():
    queue = asyncio.Queue()
    await asyncio.gather(
        producer(queue),
        consumer(queue)
    )

asyncio.run(main())
```

## 錯誤處理

```python
async def might_fail():
    raise ValueError("發生錯誤")

async def main():
    try:
        await might_fail()
    except ValueError as e:
        print(f"捕獲錯誤：{e}")

asyncio.run(main())
```

## 同步與非同步橋接

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

def blocking_io():
    # 同步 I/O 操作
    import time
    time.sleep(1)
    return "Blocking result"

async def main():
    loop = asyncio.get_event_loop()
    executor = ThreadPoolExecutor()

    # 在執行緒池中執行同步操作
    result = await loop.run_in_executor(
        executor,
        blocking_io
    )
    print(f"結果：{result}")

asyncio.run(main())
```

## 參考資源

- https://www.google.com/search?q=Python+asyncio+tutorial+2019+async+await+concurrent
- https://www.google.com/search?q=Python+3.7+asyncio+create_task+current_task+new+API
- https://www.google.com/search?q=Python+asyncio+best+practices+error+handling+2019