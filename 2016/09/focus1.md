# 效能分析基礎

## 為什麼要 Profiling？

Profiling 是識別效能瓶頸的系統性方法。盲目優化可能浪費時間在不重要的程式碼上。

## Profiling 方法

### 取樣法（Sampling）

定時中斷 CPU，記錄當前執行的程式碼位置。

```bash
# 使用 perf 進行取樣
perf record -g ./my_program
perf report

# 使用 gprof
gcc -pg -o my_program my_program.c
./my_program
gprof my_program gmon.out
```

### 儀器法（Instrumentation）

在函數入口和出口加入計時程式碼。

```c
#include <time.h>

struct timespec start, end;

clock_gettime(CLOCK_MONOTONIC, &start);
// 要測量的程式碼
clock_gettime(CLOCK_MONOTONIC, &end);

double elapsed = (end.tv_sec - start.tv_sec) +
                 (end.tv_nsec - start.tv_nsec) / 1e9;
```

## 常用 Profiling 工具

### gprof（GNU Profiler）

```bash
# 編譯時開啟 profiling
gcc -pg -g -O2 program.c -o program

# 執行（會產生 gmon.out）
./program

# 分析結果
gprof program gmon.out
```

輸出範例：
```
Flat profile:
Each sample counts as 0.01 seconds.
  %   cumulative   self              self     total
 time   seconds   seconds    calls  us/call  name
 45.12      0.45     0.45       10 45000.00  process_data
 30.05      0.75     0.30        5 60000.00  compute_hash
```

### perf（Linux Performance Tools）

```bash
# 列出可用事件
perf list

# 記錄熱門指令
perf stat -e instructions,cycles,cache-misses ./program

# 熱門路徑分析
perf record -g ./program
perf report

# 呼叫圖分析
perf record -g --call-graph dwarf ./program
```

### Valgrind / Callgrind

```bash
# 記憶體分析
valgrind --tool=memcheck ./program

# 快取分析
valgrind --tool=cachegrind ./program

# 呼叫圖
valgrind --tool=callgrind ./program
cg_annotate callgrind.out.*
```

### Intel VTune Amplifier

```bash
# 收集熱門函數
vtune -collect hotspots ./program

# 分析快取
vtune -collect memory-access ./program

# 分析並行
vtune -collect threading ./program
```

## 微架構計數器

### 常見事件

| 事件 | 說明 |
|-----|------|
| cycles | 時脈週期數 |
| instructions | 指令數 |
| cache-misses | 快取未命中 |
| branch-misses | 分支預測失敗 |
| stalls | 管線停頓 |

### 使用 perf 收集

```bash
# 硬體事件
perf stat -e cycles,instructions,cache-references,cache-misses ./program

# 查看特定微架構事件
perf list | grep "cpu/event"

# 記錄並分析
perf record -e cpu/event=0x08,name=cache-miss/ ./program
perf report
```

## 火焰圖（Flame Graph）

Brendan Gregg 開發的視覺化工具：

```bash
# 產生火焰圖
perf record -F 99 -g -- ./program
perf script | stackcollapse-perf.pl | flamegraph.pl > output.svg
```

火焰圖的 Y 軸代表呼叫堆疊深度，X 軸代表執行時間。較寬的區塊表示該函數佔用更多 CPU 時間。

## 分析流程

### 1. 識別候選區域

使用取樣 profiler 找到最耗時的函數。

### 2. 儀器測量

在可疑函數中加入精確計時。

### 3. 分析瓶頸

確定是 CPU 密集還是記憶體密集。

### 4. 假設並驗證

提出假設，進行修改，測量效果。

## 避免 Profiling 陷阱

1. **過早優化**：先測量，再優化
2. **忽視瓶頸轉移**：優化一處可能產生新的瓶頸
3. **忽視真實資料**：使用代表性資料測試
4. **過度依賴平均**：關注分佈，不只是平均值

## 參考資料

- [gprof 使用指南](https://www.google.com/search?q=gprof+tutorial)
- [perf 工具使用](https://www.google.com/search?q=Linux+perf+tutorial)
- [火焰圖教程](https://www.google.com/search?q=flame+graph+tutorial)