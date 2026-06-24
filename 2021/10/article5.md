# 性能測試與基準化分析

## 為何要測試性能？

功能正確不夠，效能同樣重要。性能測試幫助我們：
- 發現效能瓶頸
- 防止效能回歸
- 比較不同實現的效率
- 建立效能基線

## timeit 模組

Python 標準庫提供 `timeit` 進行簡單基準測試：

```python
import timeit

# 測量執行時間
time = timeit.timeit('sum(range(1000))', number=10000)
print(f"Time: {time:.4f} seconds")

# 測量陳述式
time = timeit.timeit(
    'sorted(data)',
    setup='import random; data = [random.random() for _ in range(1000)]',
    number=1000
)
```

## pytest-benchmark

更專業的基準測試框架：

```bash
pip install pytest-benchmark
```

```python
def test_sorting(benchmark):
    import random
    data = [random.random() for _ in range(1000)]
    result = benchmark(sorted, data)
    assert result[0] <= result[-1]
```

執行 `pytest test.py -v --benchmark-only`。

## 效能回歸檢測

將基準測試納入 CI：

```yaml
- name: Benchmark
  run: pytest benchmarks/ --benchmark-only --benchmark-compare
```

基準測試的歷史記錄可以發現效能變化趨勢。

## 分析工具

profiling 工具幫助找到瓶頸：

```python
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# 執行待測程式
do_work()

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(20)  # 前 20 行
```

## 記憶體分析

```bash
pip install memory-profiler
```

```python
@memory_profiler.profile
def memory_intensive_function():
    # ... 記憶體密集操作
    pass
```

## 常見效能模式

1. **惰性求值**：推遲計算到真正需要時
2. **快取**：儲存重複計算的結果
3. **批量操作**：減少函式呼叫開銷
4. **使用內建函式**：通常比純 Python 快

## 結論

性能測試是品質保障的重要組成部分。將基準測試加入日常開發，能及早發現效能問題，避免到最後才發現瓶頸。