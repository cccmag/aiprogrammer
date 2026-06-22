# LLVM 與現代編譯器基礎設施：GCC、LLVM、WebAssembly（2000s-2020s）

## 編譯器基礎設施的演進

2000 年代以前，編譯器通常與特定語言高度耦合。GCC 和後來的 LLVM 改變了這一切——它們提供了語言無關的編譯器基礎設施，使得新語言的編譯器開發成本大幅降低。

## GCC：自由軟體的編譯器巨人

### GNU Compiler Collection

1987 年，Richard Stallman 為了實現 GNU 計劃的自由軟體願景，啟動了 GCC 專案。最初 GCC 代表「GNU C Compiler」，後來擴展為「GNU Compiler Collection」。

```
GCC 架構（1990s-2000s）：

C 前端      C++ 前端      Fortran 前端    Java 前端
    │            │              │            │
    └────────────┴──────────────┴────────────┘
                        │
               ┌────────▼────────┐
               │ GENERIC / GIMPLE │（中間表示法）
               └────────┬────────┘
                        │
               ┌────────▼────────┐
               │      RTL        │（暫存器傳輸語言）
               └────────┬────────┘
                        │
               ┌────────▼────────┐
               │    後端處理      │
               │  (指令選擇、排程)│
               └────────┬────────┘
                        │
               ┌────────▼────────┐
               │ x86 │ ARM │ MIPS│...
               └────────────────┘
```

GCC 的貢獻：

1. **多語言支援**：單一後端支援多種語言前端
2. **多目標支援**：支援數十種處理器架構
3. **豐富的最佳化**：上百種最佳化 pass
4. **開源典範**：證明複雜的基礎軟體可以由社群共同開發

### GCC 的局限

隨著時間推移，GCC 的架構問題逐漸顯現：

1. **中間表示法不夠靈活**：GENERIC/GIMPLE 到 RTL 的轉換路線固定
2. **不適合做為庫**：GCC 的程式碼難以在其他專案中重用
3. **授權限制**：GPL 授權限制了某些商業使用場景
4. **模組化不足**：前端和後端的耦合較緊

## LLVM 的革命

### Chris Lattner 的碩士論文

2000 年，Chris Lattner 還是伊利諾大學香檳分校的研究生。他的碩士論文題目是「LLVM: An Infrastructure for Multi-Stage Optimization」——這篇論文後來徹底改變了編譯器世界。

```
LLVM 核心設計：

原始碼
  │
  ▼
┌────────────┐
│  前端      │  clang (C/C++), rustc (Rust), swiftc (Swift)
│  (Frontend)│
└─────┬──────┘
      │ AST
      ▼
┌────────────┐
│  中端      │  LLVM IR + Optimizer
│  (Middle)  │  - 語言無關的最佳化
└─────┬──────┘
      │ LLVM IR
      ▼
┌────────────┐
│  後端      │  x86, ARM, WebAssembly, NVPTX...
│  (Backend) │
└─────┬──────┘
      │ 機器碼
      ▼
    執行
```

### LLVM IR：語言無關的中間表示

LLVM 最大的創新是它的中間表示法（IR）：

```
// LLVM IR 範例（人類可讀的文字格式）

; 定義一個加法函式
define i32 @add(i32 %a, i32 %b) {
entry:
  %result = add i32 %a, %b
  ret i32 %result
}

; 定義一個使用 add 的 main 函式
define i32 @main() {
entry:
  %a = alloca i32         ; 分配堆疊空間
  store i32 5, i32* %a    ; a = 5
  %b = alloca i32
  store i32 3, i32* %b    ; b = 3
  
  %a_val = load i32, i32* %a
  %b_val = load i32, i32* %b
  %result = call i32 @add(i32 %a_val, i32 %b_val)
  
  ret i32 %result
}
```

LLVM IR 的三種形式：

| 形式 | 用途 | 範例檔案 |
|------|------|---------|
| 記憶體中表示 | 編譯器內部操作 | - |
| 位元碼（Bitcode） | 連結時最佳化 | `.bc` |
| 可讀文字 | 除錯與分析 | `.ll` |

### SSA 形式

LLVM IR 使用靜態單賦值（Static Single Assignment, SSA）形式——每個變數只能被賦值一次：

```
// 非 SSA 形式
x = 5;
x = x + 1;  // x 被賦值兩次！

// SSA 形式（LLVM IR）
x1 = 5;
x2 = add x1, 1;  // 每個版本都是新的變數

// φ (phi) 節點：合併不同路徑的值
; if (cond) then a=1 else a=2
entry:
  %cond = ...
  br i1 %cond, label %then, label %else

then:
  %a1 = add i32 1, 0
  br label %merge

else:
  %a2 = add i32 2, 0
  br label %merge

merge:
  %a = phi i32 [%a1, %then], [%a2, %else]  ; φ 節點
```

SSA 的優勢：
- 每個變數的定義和使用關係清晰
- 簡化了許多最佳化分析（常量傳播、死碼消除）
- 易於增量更新

### Clang：LLVM 的 C/C++ 前端

2007 年，Apple 資助開發了 Clang——基於 LLVM 的 C/C++/Objective-C 編譯器。

```c
// Clang 的編譯流程

// clang -O2 -S example.c -o example.s

// 1. 詞法分析 → Token 串
// 2. 語法分析 → AST
// 3. 語義分析 → 帶型別資訊的 AST
// 4. AST 降級 → LLVM IR
// 5. LLVM 最佳化 → 最佳化後的 IR
// 6. 機器碼生成 → 組合語言

// Clang 的錯誤訊息品質：
// 比起 GCC 的模糊錯誤，Clang 提供精確的：
// - 錯誤位置（行號 + 列號）
// - 錯誤原因（明確的文字描述）
// - 修復建議（fix-it hints）
```

Clang 相對於 GCC 的優勢：

| 特性 | GCC | Clang |
|------|-----|-------|
| 編譯速度 | 較慢 | 快 2-3 倍 |
| 錯誤訊息 | 模糊 | 清晰、彩色 |
| 模組化 | 弱 | 強（可作為庫使用） |
| 記憶體使用 | 較高 | 較低 |
| 授權 | GPL | Apache 2.0 |

### LLVM 的殺手應用

**1. 連結時最佳化（LTO）：**

```
// 傳統編譯：每個 .c 檔案單獨編譯
// LTO：所有檔案一起最佳化

file1.c ──► file1.o ──┐
file2.c ──► file2.o ──┤──► linker ──► executable
file3.c ──► file3.o ──┘     │
                              │ LTO：在連結時進行跨檔案最佳化
                              ▼
                        更高效的執行檔

// 跨檔案內聯！
// 如果 file1.c 定義了函式 f()
// 且 file2.c 調用了 f()
// LTO 可以將 f() 內聯到 file2.c 中！
```

**2. 即時編譯引擎：**

LLVM 可以作為 JIT 引擎使用——這是它最初被設計時的關鍵應用：

```c
// LLVM ORC JIT 使用範例（現代版本）
#include "llvm/ExecutionEngine/Orc/LLJIT.h"

using namespace llvm;

int main() {
    // 建立 JIT 實例
    auto JIT = orc::LLJITBuilder().create();
    
    // 載入 IR 模組
    auto M = parseIRFile("module.ll", ...);
    
    // 編譯並執行
    JIT->addIRModule(std::move(M));
    
    // 查找並調用函式
    auto Addr = JIT->lookup("main");
    auto *Main = (int(*)())(intptr_t)Addr;
    return Main();
}
```

## 基於 LLVM 的語言

LLVM 的成功使得許多新語言選擇 LLVM 作為後端：

### Rust

Rust 編譯器 rustc 使用 LLVM 作為後端：

```rust
// Rust 程式碼
fn fibonacci(n: u32) -> u32 {
    match n {
        0 | 1 => n,
        _ => fibonacci(n-1) + fibonacci(n-2),
    }
}

// LLVM IR（經過 rustc 編譯後）
// rustc --emit llvm-ir fibonacci.rs
```

Rust 受益於 LLVM：
- 利用 LLVM 的最佳化 pass（inline, loop unrolling, vectorization）
- LLVM 的目標支援（x86, ARM, RISC-V, WebAssembly）
- LTO 和 PGO（Profile-Guided Optimization）

### Swift

Apple 的 Swift 語言也使用了 LLVM：

```swift
// Swift 程式碼
func greet(name: String) -> String {
    return "Hello, \(name)!"
}
```

Swift 對 LLVM 的貢獻：
- SIL（Swift Intermediate Language）：建立在 LLVM IR 之上的高階 IR
- 編譯器架構的模組化設計
- 穩定的 ABI（Application Binary Interface）

## WebAssembly 的崛起

### 從 LLVM 到瀏覽器

2015 年，Mozilla、Google、Microsoft 和 Apple 開始了一個新專案——WebAssembly（WASM）。WebAssembly 是一種低階的虛擬指令集架構，可以在瀏覽器中以接近原生的速度執行。

```
// C 程式碼
int add(int a, int b) {
    return a + b;
}

// 使用 LLVM + Emscripten 編譯為 WebAssembly
// clang --target=wasm32 -O2 -c add.c -o add.wasm

// WebAssembly 文字格式 (.wat)
(module
  (func $add (param $a i32) (param $b i32) (result i32)
    local.get $a
    local.get $b
    i32.add)
  (export "add" (func $add)))
```

### WebAssembly 的設計目標

1. **快速**：接近原生執行速度
2. **安全**：沙箱執行環境
3. **開放**：W3C 標準，所有瀏覽器支援
4. **可除錯**：人類可讀的文字格式

### LLVM 在 WASM 生態中的角色

LLVM 是 WebAssembly 生態系統的關鍵基礎設施：

```
// 現有程式碼 → LLVM → WebAssembly

任何 LLVM 支援的語言：
  C/C++, Rust, Swift, Kotlin, Go, Zig...
       │
       ▼
    LLVM 前端
       │
       ▼
    LLVM IR
       │
       ▼
    LLVM WASM 後端
       │
       ▼
    .wasm 檔案
```

## 編譯器基礎設施的開源生態

2020 年代的編譯器生態系統已經非常豐富：

```
┌─────────────────────────────────────────────────────┐
│              編譯器基礎設施生態                       │
├─────────────────────────────────────────────────────┤
│                                                     │
│  LLVM 生態：                                        │
│  ┌─────────────────────────────────────────────┐   │
│  │ 後端：x86, ARM, AArch64, RISC-V, WASM, ... │   │
│  │ 前端：Clang, rustc, swiftc, flang, ...     │   │
│  │ 工具：lld (linker), as (assembler), ...    │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
│  GCC 生態：                                         │
│  ┌─────────────────────────────────────────────┐   │
│  │ 後端：數十種架構，包括罕見的嵌入式平台       │   │
│  │ 前端：C, C++, Fortran, Ada, Go, BRIG        │   │
│  │ 工具：binutils (as, ld, ar, objdump...)     │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
│  其他：                                             │
│  ┌─────────────────────────────────────────────┐   │
│  │ MLIR：多層級 IR，深度學習編譯器            │   │
│  │ CIRCT：硬體編譯器基礎設施                   │   │
│  │ TVM：深度學習模型編譯器                     │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## 結語

LLVM 的誕生是編譯器技術的一個重要轉折點。它提供了一個開放的、模組化的編譯器基礎設施，大大降低了開發新語言的門檻。今天，幾乎所有重要的新語言（Rust、Swift、Zig、Julia）都建立在 LLVM 之上。

下一篇文章將探討 AI 時代的編譯器——機器學習如何正在改變編譯器的設計和實現。

---

## 延伸閱讀

- [Chris Lattner: LLVM 架構](https://www.google.com/search?q=Chris+Lattner+LLVM+architecture)
- [LLVM 官方教學：Kaleidoscope](https://www.google.com/search?q=LLVM+kaleidoscope+tutorial)
- [WebAssembly 設計文件](https://www.google.com/search?q=WebAssembly+design+goals)

---

*本篇文章為「AI 程式人雜誌 2026 年 4 月號」歷史回顧系列之六。*
