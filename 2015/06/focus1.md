# 主題一：C 語言發展歷史

## C 語言的起源

C 語言的歷史與 Unix 作業系統的發展密切相關。

### BCPL 和 B 語言

1967 年，Martin Richards 開發了 BCPL（Basic Combined Programming Language）。1970 年，Ken Thompson 在 Bell Labs 開發了 B 語言，這是用於建立 Unix 的第一個系統程式語言。

### C 語言的誕生

1972 年，Dennis Ritchie 在 Bell Labs 發明了 C 語言。C 是作為 B 的改進版本設計的，保留了 B 的簡潔風格，同時增加了資料類型和更強大的指標支援。

C 最初是為了開發 Unix 作業系統而設計的。實際上，Unix 的早期版本是用組合語言寫的，後來被重寫為 C。

## C 標準的演進

### C89/C90（ANSI C / ISO C）

1989 年，ANSI 發布了 C89 標準（ 後來也成為 ISO C90）。這是第一個正式的 C 語言標準。

主要特性：
- 基本資料類型（int, char, float, double）
- 控制結構（if, while, for, switch）
- 函式
- 指標和陣列
- 結構和聯合
- 標準函式庫

### C99

1999 年發布的 C99 標準帶來了許多現代特性：

- `//` 單行註釋
- `inline` 函式
- 變長陣列（VLA）
- `bool` 類型（`<stdbool.h>`）
- `<inttypes.h>` 的固定寬度整數類型
- `restrict` 指標
- 複合常值（compound literals）
- `for` 迴圈初始化區塊

### C11

2011 年發布的 C11 是目前廣泛採用的標準：

- 多執行緒支援（`_Thread_local`, `<threads.h>`）
- 泛型選擇（`_Generic`）
- 匿名結構和聯合
- `_Alignas` 和 `_Alignof`
- Unicode 支援（`<uchar.h>`）
- `<stdatomic.h>` 原子操作
- 邊界檢查介面（可選）

### C17/C18

C17（也稱 C18）主要是一個錯誤修正版本，沒有引入重要的新特性。

## Unix 的 C 實現

### Ritchie 的實現

Dennis Ritchie 在 1972-1973 年間實現了第一個 C 編譯器。這個實現非常成功，導致 Unix 被重寫為 C（這是當時唯一用高階語言編寫的主要作業系統）。

### GCC 的歷史

GNU Compiler Collection（最初是 GNU C Compiler）由 Richard Stallman 於 1987 年開始開發。GCC 是目前最廣泛使用的 C 編譯器之一。

### clang/LLVM

LLVM 專案始於 2000 年，Clang 是其 C/C++/Objective-C 前端。Clang 以其快速的編譯速度和友好的錯誤訊息著稱。

## C 語言的哲學

C 語言的設計哲學體現在「信任程式員」和「不阻止任何事情」：

```c
// C 允許直接記憶體操作
int arr[10];
int *p = arr;
*(p + 5) = 100;  // 直接記憶體存取

// 這在 C 中是允許的，但也容易出錯
```

## C 的遺產

### 衍生語言

- **C++**：C 的物件導向擴展
- **Java**：語法受 C 影響
- **C#**：結合了 C 和 Java 的特性
- **Python**：核心實現使用 C
- **Rust**：吸收了 C 的概念並加入記憶體安全

### 作業系統

- **Linux**：幾乎完全用 C 編寫
- **Windows**：核心部分用 C
- **macOS**：核心用 C
- **iOS**：核心用 C

## 結論

C 語言經過四十多年的發展，仍然是系統程式設計的首選語言。理解 C 語言的歷史，有助於理解為什麼 C 是現在這個樣子，以及如何更好地使用它。