# 文章集錦

## Python 進階技巧專輯

### 程式相關（10 篇）

#### 1. [裝飾器實作與應用](article1.md)

深入探討 Python 裝飾器的實作原理——從最簡單的函式裝飾器到帶參數的裝飾器，再到類別裝飾器。包含 functools.wraps 的重要性、裝飾器疊加的行為、以及常見應用場景（計時、日誌、權限檢查）。

#### 2. [生成器與 yield](article2.md)

生成器的底層機制——yield 如何暫停函式狀態、send 與 throw 的雙向通訊、yield from 的委託模式。包含管線（pipeline）模式的實戰案例，以及生成器在處理大型檔案和無限序列中的應用。

#### 3. [自訂上下文管理器](article3.md)

深入 __enter__ 和 __exit__ 協定——異常處理、資源清理、contextlib 工具庫。包含資料庫連線管理、檔案鎖定、計時器等實際案例。

#### 4. [執行緒安全與鎖](article4.md)

Python threading 的執行緒安全機制——Lock、RLock、Semaphore、Condition、Event。深入分析 GIL 的影響、競爭條件的偵測與預防、死鎖的避免策略。包含生產者-消費者問題的實作。

#### 5. [行程池與平行處理](article5.md)

multiprocessing 模組的進階用法——Process、Pool、Queue、Pipe。包含共享記憶體、跨程序狀態同步、以及與 concurrent.futures 的整合。比較多執行緒與多程序的效能差異。

#### 6. [asyncio 協程基礎](article6.md)

async/await 語法的核心概念——事件迴圈、協程、task、future。從同步程式碼到非同步的遷移路徑、asyncio 的執行模型、以及常見的陷阱。包含基礎的 HTTP 請求並發案例。

#### 7. [async/await 實戰](article7.md)

asyncio 在真實世界的應用——asyncio.gather 與 TaskGroup、超時與取消、非同步 Queue、非同步上下文管理器、非同步迭代器。包含 Web API 爬蟲的完整案例。

#### 8. [效能分析 cProfile](article8.md)

Python 效能分析工具——cProfile 的統計分析、timeit 的精確計時、py-spy 的取樣分析。包含火焰圖的生成與解讀、以及如何從分析結果定位效能瓶頸。

#### 9. [記憶體管理與最佳化](article9.md)

Python 記憶體管理機制——引用計數、垃圾回收（分代 GC）、記憶體池（PyMalloc）。包含記憶體洩漏的偵測、弱引用（weakref）的使用、__slots__ 的節省效果、array 與 struct 的替代方案。

#### 10. [高效能 Python 技巧](article10.md)

綜合效能策略——選擇正確的資料結構、使用內建函式與標準庫、lazy import、C 擴充（Cython、cffi）、JIT 編譯（Numba、PyPy）。包含一個從 100 秒到 1 秒的最佳化案例。
