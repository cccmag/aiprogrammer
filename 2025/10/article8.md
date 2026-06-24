# 效能分析 cProfile

## 1. 引言

「沒有測量就沒有最佳化」——這是效能工程的第一定律。Python 提供了 cProfile、timeit、profile 等工具來幫助開發者定位效能瓶頸。本文將深入探討這些效能分析工具的使用方法。

## 2. cProfile 統計分析

`cProfile` 是 Python 內建的統計分析器，記錄每個函式的呼叫次數和執行時間：

```python
import cProfile
import pstats

def slow_function():
    total = 0
    for i in range(10_000_000):
        total += i * i
    return total

def medium_function():
    return [i ** 0.5 for i in range(100_000)]

def fast_function():
    return sum(range(1_000_000))

def main():
    slow_function()
    medium_function()
    fast_function()

# 方法 1：執行並存檔
cProfile.run('main()', 'profile_stats')

# 方法 2：讀取分析結果
p = pstats.Stats('profile_stats')
p.sort_stats('cumtime').print_stats(15)
```

## 3. 解讀分析結果

cProfile 輸出中的關鍵欄位：

| 欄位 | 含義 |
|------|------|
| ncalls | 呼叫次數 |
| tottime | 函式本身的總時間（不含子函式） |
| percall | tottime / ncalls |
| cumtime | 函式總時間（含子函式） |
| percall | cumtime / ncalls |

```python
# 常見分析模式
p = pstats.Stats('profile_stats')

# 依總時間排序
p.sort_stats('cumtime').print_stats(20)

# 依呼叫次數排序
p.sort_stats('ncalls').print_stats(20)

# 只顯示特定的函式
p.print_callers('slow_function')
```

## 4. timeit 精確計時

`timeit` 用於測量小段程式碼的執行時間，自動處理垃圾回收等干擾：

```python
import timeit

# 測量列表推導式
t1 = timeit.timeit(
    '[x ** 2 for x in range(1000)]',
    number=100000
)

# 測量 map
t2 = timeit.timeit(
    'list(map(lambda x: x ** 2, range(1000)))',
    number=100000
)

# 測量 for 迴圈
t3 = timeit.timeit('''
result = []
for x in range(1000):
    result.append(x ** 2)
''', number=100000)

print(f"列表推導式: {t1:.3f}s")
print(f"map: {t2:.3f}s")
print(f"for 迴圈: {t3:.3f}s")
```

## 5. py-spy 取樣分析

`py-spy` 是一個取樣分析器，可以在不修改程式碼的情況下分析正在運行的 Python 行程：

```bash
# 安裝
pip install py-spy

# 分析正在運行的行程
py-spy record -o flamegraph.svg --pid 12345

# 分析腳本
py-spy record -o flamegraph.svg -- python my_script.py

# 互動模式
py-spy top --pid 12345
```

## 6. 火焰圖解讀

火焰圖是視覺化效能瓶頸的強大工具：

- 從下到上：呼叫堆疊
- 方塊寬度：佔用時間比例
- 寬方塊 = 需要關注的瓶頸

```bash
# 生成火焰圖
py-spy record -o flame.svg --duration 30 -- python server.py

# 使用 Brendan Gregg 的工具生成
git clone https://github.com/brendangregg/FlameGraph
./FlameGraph/flamegraph.pl profile.txt > flame.svg
```

## 7. 實戰案例

```python
import cProfile, pstats, io

def profile_code():
    profiler = cProfile.Profile()
    profiler.enable()
    
    # 被分析的程式碼
    data = [i for i in range(1000000)]
    filtered = [x for x in data if x % 2 == 0]
    result = sum(filtered)
    
    profiler.disable()
    s = io.StringIO()
    ps = pstats.Stats(profiler, stream=s).sort_stats('cumtime')
    ps.print_stats(10)
    print(s.getvalue())

profile_code()
```

## 8. 效能分析工作流程

1. **建立基線**：在最佳化前先測量
2. **使用 cProfile**：找出最花時間的函式
3. **使用 timeit**：比較不同實作的效能
4. **驗證最佳化**：確保最佳化有效
5. **回歸測試**：確保正確性沒有受影響

## 9. 常見瓶頸模式

- **過多的屬性存取**：將屬性綁定到區域變數
- **不必要的函式呼叫**：內聯簡單操作
- **過度的記憶體分配**：使用生成器或原地操作
- **錯誤的資料結構**：頻繁查找用 set 而非 list

## 10. 總結

效能分析是效能最佳化的基礎。cProfile 幫助定位瓶頸，timeit 幫助比較方案，py-spy 可以在生產環境分析。沒有數據支撐的最佳化只是猜測。

## 延伸閱讀

- [Python cProfile 官方文件](https://www.google.com/search?q=Python+cProfile+profiling)
- [py-spy 專案](https://www.google.com/search?q=py-spy+Python+sampling+profiler)
