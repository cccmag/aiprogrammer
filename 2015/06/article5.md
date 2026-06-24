# 除錯工具與技術

## GDB 基本使用

### 啟動 GDB

```bash
# 編譯時加入除錯資訊
gcc -g program.c -o program

# 啟動 GDB
gdb ./program
# 或
gdb -tui ./program  # TUI 模式，有視覺化介面
```

### 基本命令

```gdb
(gdb) run              # 執行
(gdb) break main       # 在 main 設斷點
(gdb) break 10         # 在第 10 行設斷點
(gdb) break func       # 在函式設斷點
(gdb) continue         # 繼續執行
(gdb) next             # 單步執行（不進函式）
(gdb) step             # 單步執行（進函式）
(gdb) print var        # 印出變數
(gdb) print *ptr       # 印出指標指向的值
(gdb) watch var        # 監視變數變化
(gdb) backtrace        # 顯示呼叫堆疊
(gdb) frame 1          # 切換到框架 1
(gdb) info locals      # 顯示區域變數
(gdb) info args        # 顯示函式參數
(gdb) quit             # 離開
```

### 條件斷點

```gdb
(gdb) break foo.c:20 if x > 10
```

### 後續附著

```gdb
(gdb) attach <pid>
(gdb) detach
```

## Valgrind

### 安裝和使用

```bash
# 安裝
# sudo apt install valgrind

# 基本使用
valgrind --leak-check=full ./program
```

### 記憶體錯誤檢測

- 無效記憶體讀寫
- 使用未初始化的記憶體
- 記憶體洩漏
- 雙重釋放

### 輸出範例

```
==12345== Memcheck, a memory error detector
==12345== Invalid write of size 4
==12345==    at 0x...: main (test.c:5)
==12345== HEAP SUMMARY:
==12345==    in use at exit: 0 bytes in 0 blocks
```

## AddressSanitizer

### 編譯選項

```bash
gcc -fsanitize=address -g program.c -o program
./program
```

### 檢測問題

- 緩衝區溢位
- 記憶體洩漏
- 使用後釋放
- 堆疊緩衝區溢位

## LLDB

LLVM 的除錯器：

```bash
lldb ./program
(lldb) breakpoint set --name main
(lldb) run
(lldb) next
(lldb) frame variable
```

## 核心傾印

### 啟用核心傾印

```bash
# 檢查限制
ulimit -c

# 設定大小
ulimit -c unlimited

# 設定核心傾印檔案名稱
echo "/tmp/core.%e.%p" | sudo tee /proc/sys/kernel/core_pattern
```

### 分析核心傾印

```bash
# 發生段錯誤後
gdb ./program /tmp/core.program.1234
(gdb) bt  # 顯示錯誤時的堆疊
```

## 靜態分析

### GCC/Clang 警告

```bash
gcc -Wall -Wextra -pedantic -Werror program.c
```

### cppcheck

```bash
# 安裝
# sudo apt install cppcheck

# 執行
cppcheck --enable=all program.c
```

### clang static analyzer

```bash
scan-build gcc -c program.c
```

## 常見錯誤與修復

### 段錯誤

使用 GDB 找到發生段錯誤的位置。

### 記憶體洩漏

使用 Valgrind 的 leak-check。

### 緩衝區溢位

使用 AddressSanitizer 或 Valgrind。

## 結論

熟練使用除錯工具是 C 程式設計師必備的技能。建議從 GDB 開始，逐步學習其他工具。