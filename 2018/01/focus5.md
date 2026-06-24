# asyncio 模組實戰

## 簡介

asyncio 是 Python 3.4 引入的標準庫，專門用於編寫異步程式。Python 3.6 版本的 asyncio 已相當成熟，支援協程、任務、事件循環等功能。

## 事件循環

### 取得事件循環

```python
import asyncio

# Python 3.7+
loop = asyncio.get_event_loop()

# Python 3.10+ 不支援 get_event_loop()
# 建議使用 asyncio.run()
```

### 執行異步程式

```python
async def main():
    print("Hello")

# Python 3.7+
asyncio.run(main())

# 舊版方式
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```

## 協程

### 基本協程

```python
async def say_after(delay, message):
    await asyncio.sleep(delay)
    print(message)

async def main():
    await say_after(1, "Hello")
    await say_after(2, "World")

asyncio.run(main())
```

### 併發執行

```python
async def main():
    task1 = asyncio.create_task(say_after(1, "Hello"))
    task2 = asyncio.create_task(say_after(2, "World"))

    await task1
    await task2
```

## 異步生成器

```python
async def async_gen():
    for i in range(5):
        await asyncio.sleep(0.1)
        yield i

async def main():
    async for value in async_gen():
        print(value)
```

## 佇列（Queue）

```python
import asyncio

async def producer(queue):
    for i in range(5):
        await queue.put(i)
        await asyncio.sleep(0.5)
    await queue.put(None)  # 結束標記

async def consumer(queue):
    while True:
        item = await queue.get()
        if item is None:
            break
        print(f"Got: {item}")

async def main():
    queue = asyncio.Queue()
    await asyncio.gather(
        producer(queue),
        consumer(queue)
    )

asyncio.run(main())
```

## 鎖（Lock）

```python
import asyncio

counter = 0
lock = asyncio.Lock()

async def increment():
    global counter
    async with lock:
        counter += 1
        await asyncio.sleep(0.1)
        print(f"Counter: {counter}")

async def main():
    tasks = [increment() for _ in range(10)]
    await asyncio.gather(*tasks)

asyncio.run(main())
```

## 訊號量（Semaphore）

```python
import asyncio

semaphore = asyncio.Semaphore(2)

async def limited_task(n):
    async with semaphore:
        print(f"Task {n} starting")
        await asyncio.sleep(1)
        print(f"Task {n} finishing")

async def main():
    tasks = [limited_task(i) for i in range(5)]
    await asyncio.gather(*tasks)

asyncio.run(main())
```

## 異步上下文管理器

```python
class AsyncContextManager:
    async def __aenter__(self):
        print("Entering")
        await asyncio.sleep(0.1)
        return self

    async def __aexit__(self, *args):
        await asyncio.sleep(0.1)
        print("Exiting")

async def main():
    async with AsyncContextManager() as cm:
        print("Inside context")

asyncio.run(main())
```

## 實戰範例：異步計時器

```python
import asyncio
import time

async def timer(duration):
    start = time.time()
    while time.time() - start < duration:
        elapsed = time.time() - start
        print(f"Elapsed: {elapsed:.1f}s")
        await asyncio.sleep(0.1)
    print("Timer finished!")

async def main():
    await asyncio.create_task(timer(2))
    await asyncio.create_task(timer(1))
    print("All timers done")

asyncio.run(main())
```

## 效能考量

1. **避免阻塞** - 不要在協程中使用同步阻塞操作
2. **適當併發** - 過多併發任務會消耗過多記憶體
3. **使用連接池** - HTTP 客戶端應使用連接池
4. **取消任務** - 使用 asyncio.Task.cancel() 取消不需要的任務

## 與執行緒的比較

| 特性 | asyncio | threading |
|------|---------|-----------|
| 類型 | 單執行緒 | 多執行緒 |
| 切換 | 協作式 | 搶佔式 |
| 複雜度 | 較低 | 較高 |
| 適用場景 | I/O 密集 | CPU 密集 |