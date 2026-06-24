# 指令集與管線化

## 前言

指令集架構（ISA）是計算機架構中軟體與硬體的交界。它定義了處理器可以執行的所有指令、暫存器集合、記憶體模型和異常處理機制。同一套 ISA 可以有不同的微架構實作，相同的程式碼可以在不同實作上執行。

## 指令集架構

### RISC vs CISC

指令集架構主要分為兩大陣營：

| 特性 | RISC | CISC |
|------|------|------|
| 指令長度 | 固定（通常 32 位元） | 可變（1-15 位元組） |
| 指令數量 | 少（約 50-100 條） | 多（約 200-1000 條） |
| 定址模式 | 少（通常 1-2 種） | 多（5-10 種） |
| 記憶體存取 | Load/Store 架構 | 任意指令可存取記憶體 |
| 典型代表 | ARM, RISC-V, MIPS | x86, 68k, VAX |

RISC 的核心理念是「簡單就是快」：精簡的指令集使管線化更容易，編譯器可以更有效地利用暫存器。

### MIPS 指令格式範例

MIPS 是三種基本指令格式的代表：

```
R-type:   opcode(6) | rs(5) | rt(5) | rd(5) | shamt(5) | func(6)
I-type:   opcode(6) | rs(5) | rt(5) | immediate(16)
J-type:   opcode(6) | address(26)
```

**R-type 範例**：`ADD rd, rs, rt` → `rd = rs + rt`

## 五階級管線

### 管線化的基本概念

管線化（Pipelining）是將指令執行分解為多個階段，每個階段由獨立的硬體單元並行處理不同的指令。類似於工廠的組裝線。

### 五階級 RISC 管線

典型的 RISC 處理器使用五階級管線：

```
IF:  指令提取（Instruction Fetch）
ID:  指令解碼與暫存器讀取（Instruction Decode）
EX:  執行或位址計算（Execute）
MEM: 資料記憶體存取（Memory Access）
WB:  結果寫回暫存器（Write Back）
```

### 管線加速比

理想情況下，k 階級管線可以將吞吐量提升 k 倍：

```
理想加速比 = k（管線階級數）
CPI（理想管線化）= 1
```

但實際上，管線冒險（Hazard）會降低加速比。

## 管線冒險

### 三種冒險類型

**1. 結構冒險（Structural Hazard）**

硬體資源不足導致指令無法同時執行。例如，馮紐曼架構中指令和資料共用同一記憶體，導致 IF 和 MEM 階段衝突。

解決方案：分離的指令快取與資料快取（哈佛架構）。

**2. 資料冒險（Data Hazard）**

指令之間的資料依賴關係導致管線停頓。例如：

```assembly
ADD R1, R2, R3  ; R1 = R2 + R3
SUB R4, R1, R5  ; 需要 R1 的值
```

R1 在 ADD 的 WB 階段才被寫入，但 SUB 在 ID 階段就需要讀取 R1。

解決方案：
- **轉發（Forwarding）**：將 ALU 結果直接轉發給下一條指令，不需等到 WB
- **管線停頓（Stall）**：插入 NOP 等待資料準備好

**3. 控制冒險（Control Hazard）**

分支指令導致不確定下一條指令的位址。

解決方案：
- **分支預測**：預測分支是否跳轉
- **分支延遲槽**：在分支指令後插入無關指令

### 資料轉發示意圖

```
時脈週期:  1     2     3     4     5
ADD:     IF   ID   EX   MEM   WB
SUB:          IF   ID   EX    MEM   WB
                  └──→ 轉發
```

沒有轉發時，SUB 需要在 ID 階段停頓兩個週期等待 ADD 完成。

## 分支預測

### 靜態分支預測

- 向前分支預測不跳轉（常見於 if-else）
- 向後分支預測跳轉（常見於迴圈）

### 動態分支預測

使用分支歷史表（Branch History Table）記錄分支結果：

- **1 位元預測**：記錄上次結果，但雙層迴圈會預測錯誤兩次
- **2 位元預測**：使用有限狀態機，需要連續兩次錯誤才翻轉預測
- **全域歷史預測**：結合多個分支的歷史進行預測

## 小結

管線化是提升處理器效能的關鍵技術。雖然管線冒險會降低部分效能增益，但透過轉發、分支預測和編譯器最佳化，現代處理器可以達到接近每週期一條指令的效能。

---

**下一步**：[記憶體階層](focus4.md)

## 延伸閱讀

- [Pipelining in Computer Architecture](https://www.google.com/search?q=pipelining+computer+architecture)
- [Branch Prediction Techniques](https://www.google.com/search?q=branch+prediction+techniques)
- [RISC vs CISC Comparison](https://www.google.com/search?q=RISC+vs+CISC+architecture)
