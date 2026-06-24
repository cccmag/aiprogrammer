# CPU 內部結構：ALU、控制單元、暫存器

## 前言

CPU（Central Processing Unit）是計算機的大腦。它由三個核心元件組成：算術邏輯單元（ALU）、控制單元（Control Unit）和暫存器（Registers）。這三個元件協同工作，執行儲存在記憶體中的指令序列。

## 算術邏輯單元（ALU）

### 功能概述

ALU 負責執行所有的算術和邏輯運算。它是一個組合電路——輸出只取決於當前的輸入，沒有狀態儲存能力。

**典型 ALU 支援的運算**：

| 類別 | 運算 | 說明 |
|------|------|------|
| 算術 | ADD, SUB, MUL, DIV | 加減乘除 |
| 邏輯 | AND, OR, XOR, NOT | 位元邏輯運算 |
| 移位 | SHL, SHR, ROL, ROR | 左移、右移、旋轉 |
| 比較 | CMP, TEST | 比較與測試 |

### ALU 的內部結構

一個 n 位元 ALU 通常由 n 個全加器（Full Adder）和組合邏輯電路構成。ALU 的輸入包括兩個 n 位元操作數和一個運算選擇信號（opcode），輸出包括 n 位元結果和一組狀態標誌（Status Flags）：

```
        操作數 A        操作數 B
            │              │
            ▼              ▼
        ┌────────────────────┐
        │                    │
運算選擇──→        ALU        │──→ 結果
        │                    │
        └────────┬───────────┘
                 │
          ┌──────┴──────┐
          │  狀態標誌器   │
          └──────┬──────┘
                 │
           Zero Carry Negative Overflow
```

**狀態標誌（Status Flags）**：

- **Zero（ZF）**：結果為零時設為 1
- **Carry（CF）**：加法進位或減法借位時設為 1
- **Negative（NF）**：結果為負數時設為 1
- **Overflow（OF）**：溢位時設為 1

## 控制單元（Control Unit）

### 功能概述

控制單元負責解碼指令並產生控制信號，協調 CPU 各元件的運作。它不執行資料運算，而是告訴其他元件何時做什麼。

### 指令解碼流程

```
指令記憶體 → 指令暫存器 → 控制單元 → 控制信號
```

控制單元讀取指令後，解析其中的操作碼（opcode）和操作數，然後產生對應的控制信號：

1. **暫存器寫入信號**：決定哪些暫存器寫入結果
2. **ALU 運算選擇**：決定 ALU 執行哪種運算
3. **記憶體讀寫信號**：控制資料記憶體的存取
4. **多工器選擇**：控制資料路徑中的選擇器

### 硬佈線 vs 微程式控制

| 特性 | 硬佈線控制 | 微程式控制 |
|------|-----------|-----------|
| 速度 | 快 | 慢 |
| 靈活性 | 低 | 高（可修改） |
| 設計複雜度 | 高 | 低 |
| 典型應用 | RISC 處理器 | CISC 處理器（早期） |

## 暫存器

### 暫存器檔案

暫存器是 CPU 內部的超高速儲存單元，通常由正反器（Flip-Flop）構成。暫存器的存取速度遠快於主記憶體，但數量有限。

**常見的暫存器類型**：

```python
class Registers:
    def __init__(self, num_regs=32, bits=64):
        self.regs = [0] * num_regs
        self.pc = 0          # 程式計數器
        self.ir = 0          # 指令暫存器
        self.mdr = 0         # 記憶體資料暫存器
        self.mar = 0         # 記憶體位址暫存器
        self.flags = {       # 狀態標誌
            'zero': False, 'carry': False,
            'negative': False, 'overflow': False,
        }
```

**程式設計師可見暫存器**：

- **通用暫存器**：儲存運算元和中間結果（如 x86 的 RAX、RBX）
- **程式計數器（PC）**：指向下一條指令的位址
- **堆疊指標（SP）**：指向堆疊頂端
- **狀態暫存器**：儲存條件碼和處理器狀態

**程式設計師不可見暫存器**：

- **指令暫存器（IR）**：儲存正在解碼的指令
- **記憶體位址暫存器（MAR）**：儲存待存取的記憶體位址
- **記憶體資料暫存器（MDR）**：儲存從記憶體讀取的資料

## 資料路徑（Datapath）

資料路徑是 CPU 內部資料傳輸的通道，由匯流排、多工器和暫存器組成。一條典型的 RISC 指令在資料路徑中的流動如下：

1. PC 指向指令記憶體 → 提取指令到 IR
2. 控制單元解碼 IR → 讀取暫存器檔案
3. ALU 執行運算 → 結果寫回暫存器
4. PC 更新為下一條指令位址

## 小結

ALU、控制單元和暫存器是 CPU 的三個基本構成單元。ALU 負責計算，控制單元負責指揮，暫存器負責快速資料儲存。這三個元件的協同工作構成了計算機執行指令的基礎。

---

**下一步**：[指令集與管線化](focus3.md)

## 延伸閱讀

- [CPU Design - ALU and Control Unit](https://www.google.com/search?q=CPU+ALU+control+unit+design)
- [Computer Organization - Datapath](https://www.google.com/search?q=computer+organization+datapath)
- [MIPS 單週期資料路徑](https://www.google.com/search?q=MIPS+single+cycle+datapath)
