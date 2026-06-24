# perf 效能分析工具

## perf 簡介

perf 是 Linux 核心提供的效能分析工具，可以訪問硬體效能計數器。

## 基本命令

### 列出可用事件

```bash
perf list
```

### 統計計數

```bash
perf stat ./program
```

輸出範例：
```
Performance counter stats for './program':

    1,234,567  cycles                    #    0.00 GHz
    1,000,234  instructions              #    0.81  insn per cycle
       12,345  cache-misses              #    0.01  misses per load
           123  branch-misses            #    0.02% of all branches

    0.567890 seconds time elapsed
```

### 記錄熱門路徑

```bash
perf record -g ./program
perf report
```

### 呼叫圖分析

```bash
perf record -g --call-graph dwarf ./program
perf report
```

## 常用選項

| 選項 | 說明 |
|-----|------|
| -e | 指定要監控的事件 |
| -g | 記錄呼叫圖 |
| -p | 指定 PID |
| -a | 監控所有 CPU |
| -C | 指定監控特定 CPU |

## 常用事件

### 硬體事件

```bash
perf stat -e cycles,instructions,cache-misses ./program
perf stat -e branch-misses ./program
perf stat -e cpu-clock ./program
```

### 軟體事件

```bash
perf stat -e context-switches ./program
perf stat -e page-faults ./program
perf stat -e cpu-migrations ./program
```

### 追蹤點

```bash
perf list | grep syscalls
perf record -e syscalls:sys_enter_read ./program
```

## 火焰圖

產生火焰圖：

```bash
perf record -F 99 -g -- ./program
perf script | stackcollapse-perf.pl | flamegraph.pl > output.svg
```

## 與其他工具結合

### 使用 perf 進行熱門分析

```bash
perf record -g ./program
perf report --stdio | head -50
```

### 分析快取

```bash
perf stat -e cache-references,cache-misses ./program
```

## 參考資料

- [perf 使用指南](https://www.google.com/search?q=perf+tool+tutorial)
- [Linux 效能分析](https://www.google.com/search?q=Linux+performance+analysis+perf)