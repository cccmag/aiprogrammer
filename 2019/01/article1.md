# async/await 深入解析

## 協程基礎

async/await 是 Python 3.5 引入的協程語法，Python 3.7 進一步最佳化。協程是一種可在執行中暫停並恢復的函數。

```python
async def greet():
    print("Hello")
    await asyncio.sleep(0)
    print("World")

asyncio.run(greet())
```

## 事件迴圈

事件迴圈是協程的執行引擎：

```python
import asyncio

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

async def task():
    print("在事件迴圈中執行")

loop.run_until_complete(task())
loop.close()
```

## 建立任務

asyncio.create_task() 用於排程協程執行：

```python
async def my_task(n):
    print(f"任務 {n} 開始")
    await asyncio.sleep(0.1)
    print(f"任務 {n} 完成")
    return n

async def main():
    task1 = asyncio.create_task(my_task(1))
    task2 = asyncio.create_task(my_task(2))

    results = await asyncio.gather(task1, task2)
    print(f"結果：{results}")

asyncio.run(main())
```

## 取消任務

```python
async def long_task():
    try:
        while True:
            print("工作中...")
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print("任務被取消")
        raise

async def main():
    task = asyncio.create_task(long_task())
    await asyncio.sleep(3)
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        print("已完成取消處理")
```

## 等待多個任務

```python
async def wait_all():
    await asyncio.sleep(2)
    return "all done"

async def wait_first():
    async def delayed():
        await asyncio.sleep(5)
        return "first"

    result = await asyncio.wait_for(delayed(), timeout=3)
    return result
```

## 執行緒整合

在執行緒池中執行同步程式碼：

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

def blocking_operation():
    import time
    time.sleep(1)
    return "blocking result"

async def main():
    loop = asyncio.get_event_loop()
    executor = ThreadPoolExecutor()

    result = await loop.run_in_executor(
        executor,
        blocking_operation
    )
    print(f"結果：{result}")

asyncio.run(main())
```

## 錯誤處理

```python
async def might_fail():
    raise ValueError("測試錯誤")

async def main():
    try:
        await might_fail()
    except ValueError as e:
        print(f"捕獲錯誤：{e}")

asyncio.run(main())
```

## 參考資源

- https://www.google.com/search?q=Python+async+await+asyncio+tutorial+coroutine+event+loop+2019
- https://www.google.com/search?q=Python+asyncio+create_task+gather+wait+examples+2019
- https://www.google.com/search?q=Python+asyncio+best+practices+error+handling+cancellation+2019