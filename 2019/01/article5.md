# 資料處理與 asyncio

## 非同步資料處理概述

asyncio 不只能用於網路 I/O，也適合檔案處理、數據轉換等 CPU-bound 操作的併發執行。

## 基本非同步處理

```python
import asyncio
import json

async def process_file(filename: str) -> dict:
    await asyncio.sleep(0.1)  # 模擬 I/O
    with open(filename) as f:
        return json.load(f)

async def main():
    files = ["data1.json", "data2.json", "data3.json"]
    results = await asyncio.gather(*[
        process_file(f) for f in files
    ])
    return results
```

## asyncio 執行緒池

對於真正的 CPU-bound 操作，使用執行緒池：

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

def cpu_intensive_task(data: list) -> int:
    return sum(x * 2 for x in data)

async def main():
    loop = asyncio.get_event_loop()
    executor = ThreadPoolExecutor(max_workers=4)

    data_chunks = [
        list(range(1000)),
        list(range(1000, 2000)),
        list(range(2000, 3000)),
    ]

    tasks = [
        loop.run_in_executor(executor, cpu_intensive_task, chunk)
        for chunk in data_chunks
    ]

    results = await asyncio.gather(*tasks)
    print(f"總和：{sum(results)}")
```

## 非同步批量處理

```python
import asyncio

async def fetch_item(item_id: int) -> dict:
    await asyncio.sleep(0.01)
    return {"id": item_id, "data": f"item_{item_id}"}

async def fetch_batch(item_ids: list, batch_size: int = 10):
    results = []
    for i in range(0, len(item_ids), batch_size):
        batch = item_ids[i:i + batch_size]
        tasks = [fetch_item(id) for id in batch]
        batch_results = await asyncio.gather(*tasks)
        results.extend(batch_results)
        print(f"已處理 {len(results)} 項目")
    return results

async def main():
    item_ids = range(1, 51)
    results = await fetch_batch(list(item_ids))
    print(f"總共處理：{len(results)}")
```

## 速率限制

控制併發數量：

```python
import asyncio
from asyncio import Semaphore

async def rate_limited_task(semaphore: Semaphore, task_id: int):
    async with semaphore:
        await asyncio.sleep(0.1)
        return f"Task {task_id} 完成"

async def main():
    semaphore = Semaphore(3)  # 最多 3 個併發
    tasks = [
        rate_limited_task(semaphore, i)
        for i in range(10)
    ]
    results = await asyncio.gather(*tasks)
    for r in results:
        print(r)
```

## 進度追蹤

```python
import asyncio
from typing import List

async def process_with_progress(items: List[int]) -> List[int]:
    results = []
    total = len(items)

    for i, item in enumerate(items):
        await asyncio.sleep(0.01)
        results.append(item * 2)

        if (i + 1) % 10 == 0:
            print(f"進度：{i+1}/{total} ({(i+1)*100//total}%)")

    return results

async def main():
    items = list(range(100))
    results = await process_with_progress(items)
    print(f"完成：{len(results)} 項目處理")
```

## 錯誤處理與重試

```python
import asyncio

async def unreliable_operation():
    import random
    if random.random() < 0.7:
        raise ValueError("Random failure")
    return "Success"

async def retry_operation(max_retries: int = 3, delay: float = 0.1):
    for attempt in range(max_retries):
        try:
            return await unreliable_operation()
        except ValueError as e:
            if attempt < max_retries - 1:
                print(f"重試 {attempt + 1}/{max_retries}")
                await asyncio.sleep(delay)
            else:
                raise

asyncio.run(retry_operation())
```

## 參考資源

- https://www.google.com/search?q=Python+asyncio+data+processing+tutorial+concurrent+2019
- https://www.google.com/search?q=Python+asyncio+ThreadPoolExecutor+CPU+bound+tasks+2019
- https://www.google.com/search?q=Python+asyncio+batch+processing+rate+limiting+progress+2019