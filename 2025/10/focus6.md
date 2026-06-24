# 非同步程式設計 asyncio

## 協程與事件迴圈（2014-2026）

### 前言

非同步程式設計是處理 I/O 密集型任務的最高效方案。Python 的 `asyncio` 模組提供了一個基於事件迴圈的協程模型，讓單執行緒可以處理數萬個並發連線。

### 從同步到非同步

同步程式碼中，每個 I/O 操作都會阻塞執行緒：

```python
import time

def fetch_url(url):
    print(f"開始請求 {url}")
    time.sleep(1)  # 模擬網路延遲
    print(f"完成 {url}")
    return url

# 按順序執行 -> 總耗時約 3 秒
fetch_url("url1")
fetch_url("url2")
fetch_url("url3")
```

非同步程式碼在等待 I/O 時可以切換到其他任務：

```python
import asyncio

async def fetch_url(url):
    print(f"開始請求 {url}")
    await asyncio.sleep(1)
    print(f"完成 {url}")
    return url

# 並發執行 -> 總耗時約 1 秒
async def main():
    tasks = [fetch_url(f"url{i}") for i in range(3)]
    await asyncio.gather(*tasks)

asyncio.run(main())
```

### 事件迴圈

asyncio 的核心是事件迴圈（event loop）——一個不斷檢查是否有事件需要處理的迴圈：

```python
import asyncio

async def say_after(delay, text):
    await asyncio.sleep(delay)
    print(text)

async def main():
    # 創建任務（立即開始排程）
    task1 = asyncio.create_task(say_after(1, "Hello"))
    task2 = asyncio.create_task(say_after(2, "World"))
    
    # 等待任務完成
    await task1
    await task2

asyncio.run(main())
```

### 協程、Task 與 Future

asyncio 有三個核心概念：

```python
# 1. 協程（coroutine）：async def 函式
async def my_coro():
    return 42

# 2. Task：包裝協程並在事件迴圈中排程
async def main():
    task = asyncio.create_task(my_coro())
    result = await task
    print(result)

# 3. Future：低階的延遲結果
# 通常不需要直接使用，Task 是 Future 的子類
```

### asyncio 的適用場景

asyncio 特別適合：
- **Web 服務**：處理大量 HTTP 請求
- **網路爬蟲**：並發抓取大量頁面
- **WebSocket**：即時雙向通訊
- **資料庫查詢**：等待查詢結果時處理其他請求
- **微服務**：多個服務之間的協調

### asyncio vs 多執行緒

| 特性 | asyncio | threading |
|------|---------|-----------|
| 模型 | 協作式多工 | 搶佔式多工 |
| 切換時機 | await 處 | 任意位置 |
| 風險 | 任務不會被搶佔 | 競爭條件 |
| 並發數 | 數萬 | 數百 |
| 適合 | I/O 密集 | I/O 密集 |

### 常見陷阱

1. **不要阻塞事件迴圈**：不要在 async 函式中使用 time.sleep()，使用 asyncio.sleep()
2. **創建任務要及時 await**：否則任務可能在程式結束時被丟棄
3. **非同步生態**：需要使用 async 版本的資料庫驅動和 HTTP 用戶端
4. **調試困難**：非同步程式的錯誤訊息和堆疊追蹤較難理解

### 小結

asyncio 讓 Python 可以在單執行緒中處理大量並發 I/O 操作。它特別適合網路服務和 I/O 密集型應用，但需要整個生態的支援——資料庫驅動、HTTP 用戶端等都需要非同步版本。

---

**下一步**：[效能分析與最佳化](focus7.md)

## 延伸閱讀

- [Python asyncio 官方文件](https://www.google.com/search?q=Python+asyncio+official+documentation)
- [PEP 3156: Asynchronous IO Support](https://www.google.com/search?q=PEP+3156+asyncio)
- [Real Python: Async IO in Python](https://www.google.com/search?q=Real+Python+async+IO+guide)
