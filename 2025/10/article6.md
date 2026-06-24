# asyncio 協程基礎

## 1. 引言

非同步程式設計是處理 I/O 密集型任務的王道。Python 的 `asyncio` 模組提供了一個基於事件迴圈的協程模型，讓單執行緒可以處理數萬個並發連接。本文將建立 asyncio 的基礎知識。

## 2. 同步 vs 非同步

```python
import time

# 同步——按順序執行
def sync_fetch():
    time.sleep(1)  # 阻塞
    return "data"

start = time.time()
sync_fetch()
sync_fetch()
print(f"同步: {time.time() - start:.2f}s")  # ~2s

# 非同步——並發執行
import asyncio

async def async_fetch():
    await asyncio.sleep(1)  # 非阻塞等待
    return "data"

async def main():
    tasks = [async_fetch(), async_fetch()]
    await asyncio.gather(*tasks)

start = time.time()
asyncio.run(main())
print(f"非同步: {time.time() - start:.2f}s")  # ~1s
```

## 3. 事件迴圈

事件迴圈是 asyncio 的核心——它不斷檢查是否有事件需要處理：

```python
import asyncio

async def task(name, delay):
    print(f"{name} 開始")
    await asyncio.sleep(delay)
    print(f"{name} 結束")

async def main():
    # 創建任務並排程
    task1 = asyncio.create_task(task("A", 2))
    task2 = asyncio.create_task(task("B", 1))
    
    # 等待所有任務完成
    await task1
    await task2

asyncio.run(main())
```

## 4. 協程、Task 與 Future

```python
# 協程：async def 定義的函式
async def my_coro():
    return 42

# 協程物件
coro = my_coro()

# Task：包裝協程的排程單元
async def main():
    task = asyncio.create_task(my_coro())
    result = await task
    print(result)

# Future：低階的延遲結果
# Task 是 Future 的子類
```

## 5. awaitable 物件

三種可等待物件：

```python
# 1. 協程
async def coro():
    return 1

# 2. Task
async def main():
    task = asyncio.create_task(coro())
    result = await task

# 3. Future
import asyncio
future = asyncio.Future()
```

## 6. 並發執行模式

```python
# gather：等待所有完成
async def main():
    results = await asyncio.gather(
        fetch(1),
        fetch(2),
        fetch(3),
    )

# as_completed：依完成順序處理
async def main():
    tasks = [fetch(i) for i in range(5)]
    for coro in asyncio.as_completed(tasks):
        result = await coro
        print(f"完成: {result}")

# wait：更細粒度的控制
async def main():
    tasks = {asyncio.create_task(fetch(i)) for i in range(5)}
    done, pending = await asyncio.wait(
        tasks,
        timeout=2.0,
        return_when=FIRST_COMPLETED
    )
```

## 7. 基礎範例：並發 HTTP 請求

```python
import asyncio
import aiohttp

async def fetch_url(session, url):
    async with session.get(url) as response:
        return await response.text()

async def main():
    urls = [
        "https://python.org",
        "https://github.com",
        "https://stackoverflow.com",
    ]
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        pages = await asyncio.gather(*tasks)
        for url, page in zip(urls, pages):
            print(f"{url}: {len(page)} bytes")

asyncio.run(main())
```

## 8. 常見陷阱

1. **不要阻塞事件迴圈**：使用 `asyncio.sleep()` 而不是 `time.sleep()`
2. **不要在 async 函式中執行 CPU 密集任務**：使用 `loop.run_in_executor()`
3. **忘記 await 任務**：任務會在程式結束時被取消
4. **非同步生態**：需要使用 async 版本的資料庫驅動和 HTTP 用戶端

## 9. 總結

asyncio 讓 Python 可以在單執行緒中高效處理大量 I/O 操作。理解事件迴圈、協程、Task 和 Future 的關係是掌握非同步程式設計的關鍵。

## 延伸閱讀

- [Python asyncio 官方教學](https://www.google.com/search?q=Python+asyncio+official+tutorial)
- [PEP 492: async/await](https://www.google.com/search?q=PEP+492+async+await+Python)
