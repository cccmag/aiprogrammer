# Python 3.5 async/await 實戰

## 前言

Python 3.5 引入的 `async`/`await` 語法為 Python 的非同步程式設計帶來了革命性的變化。本文將詳細介紹這個新特性的使用方法和應用場景。

## 基礎概念

### 同步 vs 非同步

```python
# 同步：任務順序執行
def sync_task():
    result1 = do_task_1()  # 等待完成
    result2 = do_task_2(result1)  # 等待完成
    return result2

# 非同步：任務可以並發執行
async def async_task():
    result1 = await do_task_1_async()  # 可以切換
    result2 = await do_task_2_async(result1)  # 可以切換
    return result2
```

## async/await 語法

### 定義非同步函式

```python
import asyncio

# 使用 async def 定義 coroutine
async def fetch_data(url):
    """模擬網頁請求"""
    await asyncio.sleep(1)  # 非同步等待
    return f"Data from {url}"

# 呼叫 coroutine
async def main():
    result = await fetch_data("http://example.com")
    print(result)

# 執行
asyncio.run(main())
```

### await 表達式

```python
async def process():
    # await 只能在 async 函式中使用
    result = await some_coroutine()
    return result
```

## asyncio 模組

### 基本使用

```python
import asyncio

async def say_hello():
    print("Hello!")
    await asyncio.sleep(1)
    print("World!")

async def main():
    await say_hello()

asyncio.run(main())
```

### 並發執行多個 coroutines

```python
import asyncio

async def task(name, seconds):
    print(f"{name} 開始")
    await asyncio.sleep(seconds)
    print(f"{name} 完成")
    return f"{name} 完成"

async def main():
    # 建立任務
    t1 = asyncio.create_task(task("任務1", 2))
    t2 = asyncio.create_task(task("任務2", 1))

    # 並發執行
    result1 = await t1
    result2 = await t2

    print(result1, result2)

asyncio.run(main())
```

### asyncio.gather

```python
import asyncio

async def fetch(url):
    await asyncio.sleep(0.5)
    return f"Result from {url}"

async def main():
    urls = [
        "http://example.com/1",
        "http://example.com/2",
        "http://example.com/3"
    ]

    # 同時執行所有 coroutines
    results = await asyncio.gather(*[fetch(url) for url in urls])

    for result in results:
        print(result)

asyncio.run(main())
```

## 實際應用場景

### 併發 HTTP 請求

```python
import asyncio
import aiohttp

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def fetch_all(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        return await asyncio.gather(*tasks)

async def main():
    urls = [
        "https://httpbin.org/get",
        "https://httpbin.org/get?page=1",
        "https://httpbin.org/get?page=2"
    ]

    results = await fetch_all(urls)
    for result in results:
        print(f"收到 {len(result)} 位元組")

asyncio.run(main())
```

### 計時器

```python
import asyncio

async def delayed_greeting(name, delay):
    await asyncio.sleep(delay)
    return f"Hello, {name}!"

async def main():
    # 並發執行三個計時任務
    results = await asyncio.gather(
        delayed_greeting("Alice", 2),
        delayed_greeting("Bob", 1),
        delayed_greeting("Charlie", 3)
    )

    for result in results:
        print(result)

asyncio.run(main())
```

### 佇列處理

```python
import asyncio
import random

async def producer(queue):
    for i in range(5):
        item = random.randint(1, 100)
        await queue.put(item)
        print(f"產生：{item}")
        await asyncio.sleep(0.5)

async def consumer(queue, name):
    while True:
        item = await queue.get()
        print(f"{name} 處理：{item}")
        await asyncio.sleep(1)
        queue.task_done()

async def main():
    queue = asyncio.Queue()

    # 啟動生產者和消費者
    await asyncio.gather(
        producer(queue),
        consumer(queue, "消費者 A"),
        consumer(queue, "消費者 B")
    )

asyncio.run(main())
```

## 與舊式 API 的比較

### 回呼地獄

```python
# 舊式回呼風格（避免使用）
def fetch_data(callback):
    do_async_task(callback)

def handle_result(result):
    process_result(result, handle_processed)

# async/await 更加直觀
async def fetch_and_process():
    result = await fetch_data_async()
    return await process_async(result)
```

## 錯誤處理

```python
import asyncio

async def risky_task():
    raise ValueError("發生錯誤")

async def main():
    try:
        result = await risky_task()
    except ValueError as e:
        print(f"捕捉到錯誤：{e}")

asyncio.run(main())
```

## 與同步程式碼的橋接

```python
import asyncio
import threading

async def async_task():
    await asyncio.sleep(1)
    return "非同步結果"

def run_in_thread():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        result = loop.run_until_complete(async_task())
        print(result)
    finally:
        loop.close()

# 在執行緒中執行非同步程式碼
thread = threading.Thread(target=run_in_thread)
thread.start()
thread.join()
```

## 結論

async/await 語法讓 Python 的非同步程式設計變得更加直觀和優雅。雖然在 2015 年這個特性還比較新，但已經展現出巨大的潛力。