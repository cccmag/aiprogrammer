# async/await 異步編程

## 簡介

Python 3.4 引入 asyncio 模組，Python 3.5 新增 async/await 語法，Python 3.6 進一步完善異步程式設計支援。async/await 讓編寫並發程式更加直觀和簡單。

## 基本概念

### 同步 vs 異步

```python
# 同步執行 - 依序完成每個任務
def sync_tasks():
    task1()
    task2()
    task3()

# 異步執行 - 可同時處理任務
async def async_tasks():
    await task1()
    await task2()
    await task3()
```

### 定義異步函式

```python
import asyncio

async def hello():
    print("Hello!")
    await asyncio.sleep(1)
    print("World!")

# 執行異步函式
asyncio.run(hello())
```

## 異步函式規則

1. 使用 `async def` 定義異步函式
2. 使用 `await` 等待異步操作完成
3. 異步函式回傳 Coroutine 物件
4. 只能在異步函式內使用 `await`

## 等待多個任務

### asyncio.gather

```python
import asyncio

async def task1():
    await asyncio.sleep(1)
    return "Task 1"

async def task2():
    await asyncio.sleep(2)
    return "Task 2"

async def main():
    results = await asyncio.gather(task1(), task2())
    print(results)  # ['Task 1', 'Task 2']

asyncio.run(main())
```

### asyncio.create_task

```python
async def main():
    task1 = asyncio.create_task(task1())
    task2 = asyncio.create_task(task2())

    result1 = await task1
    result2 = await task2
```

## asyncio 常用功能

### sleep

```python
async def demo():
    print("Start")
    await asyncio.sleep(0.5)  # 暫停 0.5 秒
    print("End")
```

### 併發執行

```python
async def fetch(url):
    await asyncio.sleep(0.1)
    return f"Data from {url}"

async def main():
    urls = ["a.com", "b.com", "c.com"]
    tasks = [fetch(url) for url in urls]
    results = await asyncio.gather(*tasks)
    print(results)
```

## 錯誤處理

```python
async def risky_task():
    raise ValueError("Error!")

async def main():
    try:
        await risky_task()
    except ValueError as e:
        print(f"Caught: {e}")
```

## 與同步程式混合

```python
import asyncio
import time

def sync_function():
    return "sync result"

async def async_function():
    return "async result"

async def main():
    # 同步函式可直接呼叫
    sync_result = sync_function()

    # 異步函式需 await
    async_result = await async_function()

    print(sync_result, async_result)

asyncio.run(main())
```

## 常見應用場景

1. **網路請求** - 使用 aiohttp 進行異步 HTTP 請求
2. **檔案操作** - 使用 aiofiles 進行異步檔案讀寫
3. **資料庫操作** - 使用 asyncpg、aiomysql
4. **網頁伺服器** - 使用 aiohttp、FastAPI

## 範例：異步 HTTP 請求

```python
import asyncio
import aiohttp

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def main():
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, "https://python.org")
        print(f"Downloaded {len(html)} bytes")

asyncio.run(main())
```