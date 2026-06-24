# 效能分析與最佳化

## 測量是优化的第一步（2005-2026）

### 前言

「過早最佳化是萬惡之源」——Donald Knuth。但完全不做最佳化同樣是問題。效能分析（profiling）讓我們可以基於數據而非猜測來進行最佳化。

### cProfile：統計分析

`cProfile` 是 Python 內建的統計分析器：

```python
import cProfile
import pstats

def heavy_computation():
    total = 0
    for i in range(1000000):
        total += i * i
    return total

def main():
    result = heavy_computation()
    print(result)

cProfile.run('main()', 'profile_output')

# 分析結果
p = pstats.Stats('profile_output')
p.sort_stats('cumulative').print_stats(10)
```

### timeit：精確計時

`timeit` 模組用於測量小段程式碼的執行時間：

```python
import timeit

# 測量列表推導式的效能
time_list_comp = timeit.timeit(
    '[x*x for x in range(1000)]',
    number=10000
)

# 測量 map 的效能
time_map = timeit.timeit(
    'list(map(lambda x: x*x, range(1000)))',
    number=10000
)

print(f"列表推導式: {time_list_comp:.4f}s")
print(f"map: {time_map:.4f}s")
```

### py-spy：取樣分析器

對於生產環境，`py-spy` 允許在不修改程式碼的情況下進行取樣分析：

```bash
# 分析正在運行的 Python 行程
py-spy record -o flamegraph.svg --pid 12345

# 分析啟動腳本
py-spy record -o flamegraph.svg -- python myapp.py
```

### 火焰圖解讀

火焰圖是視覺化效能瓶頸的強大工具：

- **X 軸**：函式呼叫的廣度
- **Y 軸**：呼叫堆疊深度
- **方塊寬度**：佔用時間比例
- **寬方塊**：需要關注的最佳化目標

### 常見效能策略

#### 1. 選擇正確的資料結構

```python
# 頻繁查找：用 set 代替 list
# 慢
if item in large_list: ...

# 快
if item in large_set: ...
```

#### 2. 使用內建函式

```python
# 內建函式比手動迴圈快
# 慢
total = 0
for x in range(1000):
    total += x

# 快
total = sum(range(1000))
```

#### 3. 區域變數加速

```python
# 將全域/模組級別函式儲存為區域變數
def fast():
    local_append = list.append  # 區域綁定
    result = []
    for i in range(1000):
        local_append(result, i)
    return result
```

#### 4. 避免不必要的屬性存取

```python
# 屬性存取比變數慢
# 慢
import math
for i in range(1000):
    x = math.sqrt(i)

# 快
from math import sqrt
for i in range(1000):
    x = sqrt(i)
```

### 測量真言

1. **先分析，再最佳化**——不要猜測瓶頸在哪裡
2. **一次只改一個**——確保知道哪個改變有效
3. **回歸測試**——最佳化不該改變正確性
4. **設定目標**——「快 2 倍」比「盡量快」更有效

### 小結

效能分析是效能最佳化的基礎。cProfile 告訴你「哪裡慢」，timeit 告訴你「哪個快」，py-spy 讓你在生產環境中發現瓶頸。沒有數據支撐的最佳化只是猜測。

---

**下一步**：[文章集錦](articles.md)

## 延伸閱讀

- [Python cProfile 官方文件](https://www.google.com/search?q=Python+cProfile+module+documentation)
- [py-spy 專案](https://www.google.com/search?q=py-spy+Python+sampling+profiler)
- [火焰圖工具](https://www.google.com/search?q=FlameGraph+performance+visualization)
