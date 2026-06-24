# 本期焦點

## Python 進階技巧：並行、非同步與效能

### 引言

Python 是一門優雅的語言，但「慢」是它最常被詬病的標籤。GIL（全域直譯器鎖）、動態型別、直譯執行——這些特性讓 Python 在 CPU 密集和並行場景中表現不佳。

但這種刻板印象正在被打破。從 `asyncio` 的非同步 I/O 到 `multiprocessing` 的真實平行處理，從 JIT 編譯器到 GIL 移除實驗，Python 生態正在快速進化。

本期將深入探索 Python 進階技巧：

- **裝飾器與生成器**：重構程式碼的函數式工具
- **上下文管理器**：資源管理的優雅模式
- **多執行緒與多程序**：並行程式的兩條路徑
- **asyncio**：協程與事件迴圈
- **效能分析**：找到瓶頸並最佳化

---

### 大綱

* [程式：Python 進階技巧綜合展示](focus_code.md)
   - 裝飾器、生成器、上下文管理器
   - 多執行緒、多程序、非同步展示

1. [裝飾器（2013-2026）](focus1.md)
   - 函式裝飾器與類別裝飾器
   - functools.wraps

2. [生成器與迭代器（2001-2026）](focus2.md)
   - yield 語義與 lazy evaluation
   - generator expression

3. [上下文管理器（2006-2026）](focus3.md)
   - with 語句與 enter/exit
   - contextlib 模組

4. [多執行緒 threading（2003-2026）](focus4.md)
   - GIL 的影響與限制
   - 執行緒安全與 Lock

5. [多程序 multiprocessing（2008-2026）](focus5.md)
   - Process 與 Pool
   - 跨程序通訊

6. [非同步程式設計 asyncio（2014-2026）](focus6.md)
   - 協程與事件迴圈
   - async/await 語法

7. [效能分析與最佳化（2005-2026）](focus7.md)
   - cProfile 與 timeit
   - 記憶體分析與加速策略

---

### Python 並行模型

```
I/O 密集型 ──→ 多執行緒或 asyncio
                   ┊
CPU 密集型 ──→ 多程序或 C 擴充
                   ┊
混合型     ──→ 多程序 + asyncio
```

### 回顧

Python 的並行能力在過去二十年持續演進：

- **2001**：生成器（PEP 255）
- **2003**：threading 模組
- **2006**：上下文管理器（PEP 343）
- **2008**：multiprocessing（PEP 371）
- **2012**：concurrent.futures
- **2014**：asyncio（PEP 3156）
- **2015**：async/await（PEP 492）
- **2023**：nogil 實驗（PEP 703）
- **2026**：Python 4.0 草案

選擇哪種並行策略取決於問題類型——I/O 密集用 asyncio，CPU 密集用 multiprocessing，混合場景需要組合使用。

### 學習路徑

建議循序漸進：

1. 掌握裝飾器與生成器（函數式基礎）
2. 學會上下文管理器（資源管理）
3. 理解 GIL 與 threading 的限制
4. 學習 multiprocessing 平行處理
5. 精通 asyncio 非同步模型
6. 最後學習效能分析工具

---

**下一步**：[程式實作](focus_code.md) → [裝飾器](focus1.md)

## 延伸閱讀

- [Python 官方文件 — 並行程式設計](https://www.google.com/search?q=Python+concurrent+programming+documentation)
- [Real Python: Python Concurrency](https://www.google.com/search?q=Real+Python+concurrency+guide)
- [PEP 703: nogil](https://www.google.com/search?q=PEP+703+nogil+Python)
