# asyncio 深入：事件迴圈

## 前言

asyncio 是 Python 3.4 引入的標準庫，用於編寫並發程式。

## 基本概念

```python
import asyncio

async def hello():
    print("Hello")
    await asyncio.sleep(1)
    print("World")

asyncio.run(hello())
```

## 事件迴圈

```python
# 獲取事件迴圈
loop = asyncio.get_event_loop()

# 執行協程
loop.run_until_complete(hello())

# 關閉迴圈
loop.close()
```

## 任務排程

```python
async def task1():
    return "Task 1"

async def task2():
    return "Task 2"

async def main():
    # 建立任務
    t1 = asyncio.create_task(task1())
    t2 = asyncio.create_task(task2())

    # 並發執行
    results = await asyncio.gather(t1, t2)
    print(results)

asyncio.run(main())
```

## 延伸閱讀

- [Python asyncio 文檔](https://www.google.com/search?q=python+asyncio+tutorial)