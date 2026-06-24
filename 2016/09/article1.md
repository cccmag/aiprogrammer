# gprof 使用指南

## gprof 簡介

gprof（GNU Profiler）是 GCC 附帶的程式剖析工具，可以分析函數呼叫關係和執行時間。

## 基本使用方法

### 1. 編譯時加入剖析選項

```bash
gcc -pg -g -O2 program.c -o program
```

- `-pg`：產生剖析資料
- `-g`：產生除錯資訊（可選）

### 2. 執行程式

```bash
./program
```

執行後會產生 `gmon.out` 檔案。

### 3. 分析結果

```bash
gprof program gmon.out > analysis.txt
```

## 輸出格式

### Flat Profile

```
Flat profile:
Each sample counts as 0.01 seconds.
  %   cumulative   self              self     total
 time   seconds   seconds    calls  us/call  name
 45.12      0.45     0.45       10 45000.00  process_data
 30.05      0.75     0.30        5 60000.00  compute_hash
 15.02      0.90     0.15       100    1500.00  memcpy
  9.01      0.99     0.09        0     0.00    _start
```

欄位說明：
- `% time`：該函數佔用的時間百分比
- `cumulative seconds`：累計時間
- `self seconds`：該函數本身的執行時間
- `calls`：函數呼叫次數
- `name`：函數名稱

### Call Graph

```
Call graph:

index % time    self  children     called       name
                                                 <spontaneous>
[1]     45.1    0.45    0.00       10         process_data [1]
                0.30    0.00        5/5         main [2]

[2]    30.0    0.30    0.00        5            compute_hash [2]
                0.45    0.00        5/10         process_data [1]
```

## 視覺化工具

### gprof2dot

將 gprof 輸出轉換為圖形：

```bash
gprof program gmon.out | gprof2dot | dot -Tpng -o profile.png
```

## 局限性

1. **取樣誤差**：低頻率取樣可能不準確
2. **無法分析綠色**：不支援多執行緒（需要其他工具）
3. **函數計時**：無法分析函數內部的瓶頸

## 參考資料

- [gprof 官方文檔](https://www.google.com/search?q=gprof+manual)
- [gprof 使用教程](https://www.google.com/search?q=gprof+tutorial)