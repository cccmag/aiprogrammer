# 系統呼叫與中斷

## 什麼是系統呼叫？

系統呼叫（system call）是使用者態程式請求作業系統核心服務的程式化介面。當應用程式需要執行特權操作（如讀寫檔案、建立行程、分配記憶體）時，必須通過系統呼叫進入核心態。

## 用戶態 vs 核心態

現代 CPU 提供至少兩種執行特權層級：

- **用戶態（User Mode）**：受限執行模式，無法執行特權指令（如中斷關閉、I/O 操作、MMU 配置）
- **核心態（Kernel Mode）**：完全特權模式，可以執行所有 CPU 指令

這種隔離確保了系統安全——應用程式無法隨意操作硬體或破壞其他程式的記憶體。

## 系統呼叫的執行流程

```
應用程式 (用戶態)
  │ 呼叫 read(fd, buf, len)
  ▼
C 標準函式庫 (glibc)
  │ 封裝系統呼叫
  ▼
核心 (核心態)
  │ 執行系統呼叫處理函式 sys_read()
  ▼
返回用戶態
```

### 步驟詳解

1. 應用程式呼叫標準函式庫（如 `read()`）
2. 標準函式庫將參數放入指定暫存器
3. 執行 `int 0x80`（x86）或 `syscall`（x86-64）指令觸發軟體中斷
4. CPU 切換到核心態，跳轉到中斷處理程式
5. 核心根據系統呼叫編號呼叫對應的處理函式
6. 處理完成後，返回用戶態

## 常見系統呼叫

| 系統呼叫 | Linux | Windows | 功能 |
|---------|-------|---------|------|
| 行程控制 | fork() | CreateProcess | 建立行程 |
| 檔案操作 | open() | CreateFile | 開啟檔案 |
| 讀取 | read() | ReadFile | 從檔案讀取 |
| 寫入 | write() | WriteFile | 寫入檔案 |
| 記憶體 | mmap() | MapViewOfFile | 記憶體映射 |
| IPC | pipe() | CreatePipe | 行程間通訊 |
| 網路 | socket() | WSASocket | 建立 socket |

## 中斷

中斷是硬體或軟體發送給 CPU 的信號，通知有事件需要處理。

### 中斷類型

- **硬體中斷**：由外部設備產生（鍵盤輸入、網路封包到達、磁碟 I/O 完成）
- **軟體中斷**：由 CPU 指令觸發（除零錯誤、系統呼叫）
- **例外（Exception）**：由指令執行錯誤觸發（頁錯誤、段錯誤）

### 中斷向量表

中斷向量表（IVT/IDT）是一個陣列，每個條目對應一個中斷向量號，儲存對應的中斷處理程式位址：

```
中斷 0：除法錯誤（Divide Error）
中斷 3：斷點（Breakpoint）
中斷 14：頁錯誤（Page Fault）
中斷 32-255：可遮蔽中斷（IRQ 0-223）
```

### 中斷處理流程

1. CPU 完成當前指令
2. CPU 檢查中斷請求線，讀取中斷向量號
3. CPU 保存當前上下文（CS、EIP、EFLAGS 到堆疊）
4. CPU 根據中斷向量號查詢 IDT，取得中斷處理程式入口
5. CPU 切換到核心態，執行中斷處理程式
6. 處理完成後執行 `iret` 指令恢復上下文

## Linux 的 syscall 指令

x86-64 架構使用 `syscall`/`sysret` 指令對來優化系統呼叫：

```
syscall 指令：
  1. 將 RIP 複製到 RCX（用於返回）
  2. 將 RFLAGS 複製到 R11
  3. 從 MSR（LSTAR）載入新的 RIP（核心入口）
  4. 切換到核心態（CPL 0）

系統呼叫編號和參數：
  rax = 系統呼叫編號
  rdi = 第一個參數
  rsi = 第二個參數
  rdx = 第三個參數
  r10 = 第四個參數
  r8  = 第五個參數
  r9  = 第六個參數
```

## 延伸閱讀

- [Linux 系統呼叫表](https://www.google.com/search?q=Linux+system+call+table+x86-64)
- [x86 中斷與異常](https://www.google.com/search?q=x86+interrupt+descriptor+table+IDT)
- [Linux 中斷處理](https://www.google.com/search?q=Linux+kernel+interrupt+handling)
