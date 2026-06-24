# RISC vs CISC

## 1. 引言

RISC（Reduced Instruction Set Computer）與 CISC（Complex Instruction Set Computer）是計算機架構設計的兩條不同路線。這場始於 1980 年代的架構之爭深刻影響了現代處理器的設計方向。

本文將深入比較兩種架構的設計哲學、技術特點和實際案例。

## 2. CISC 的起源與哲學

### 2.1 CISC 的設計理念

CISC 的核心理念是：讓指令盡可能強大，一條高階指令可以完成複雜的操作。

**以 x86 的 `MUL` 指令為例**：

```assembly
MUL AX, BX    ; AX = AX × BX（一次完成）
```

在 CISC 中，一條指令可以完成：
- 從記憶體載入操作數
- 執行乘法運算
- 將結果存回暫存器

### 2.2 CISC 的優缺點

**優點**：
- 指令功能強大，組合程式碼更簡潔
- 編譯器設計較簡單（因為指令語義豐富）

**缺點**：
- 指令長度可變（1-15 位元組），解碼複雜
- 管線化困難
- 單條指令執行時間不固定

## 3. RISC 的起源與哲學

### 3.1 RISC 的設計理念

RISC 的核心理念來自 Patterson 和 Hennessy 在 1980 年代的研究：精簡指令集可以讓處理器更簡單、更快。

```assembly
; RISC 風格的乘法
MUL R1, R2, R3  ; R1 = R2 × R3（所有操作數都在暫存器中）
```

**RISC 的關鍵設計原則**：

1. **Load/Store 架構**：只有 Load 和 Store 指令可以存取記憶體
2. **固定指令長度**：簡化解碼邏輯
3. **大量通用暫存器**：減少記憶體存取
4. **簡單定址模式**：通常只有暫存器和立即數定址

### 3.2 經典 RISC 案例：MIPS

MIPS 是最具代表性的 RISC 架構之一：

```python
class MIPSDecoder:
    def __init__(self):
        self.regs = [0] * 32

    def decode_r_type(self, inst):
        opcode = (inst >> 26) & 0x3F
        rs = (inst >> 21) & 0x1F
        rt = (inst >> 16) & 0x1F
        rd = (inst >> 11) & 0x1F
        shamt = (inst >> 6) & 0x1F
        funct = inst & 0x3F
        return {'type': 'R', 'rs': rs, 'rt': rt, 'rd': rd, 'funct': funct}

    def decode_i_type(self, inst):
        opcode = (inst >> 26) & 0x3F
        rs = (inst >> 21) & 0x1F
        rt = (inst >> 16) & 0x1F
        immediate = inst & 0xFFFF
        if immediate & 0x8000:
            immediate -= 0x10000  # 符號擴展
        return {'type': 'I', 'rs': rs, 'rt': rt, 'imm': immediate}
```

## 4. 深入比較

### 4.1 指令格式

```
CISC (x86): 可變長度，多種定址模式
  89 D8    MOV EAX, EBX      ; 2 位元組
  01 D8    ADD EAX, EBX      ; 2 位元組
  B8 01000000  MOV EAX, 1    ; 5 位元組

RISC (MIPS): 固定 32 位元
  000000 00001 00010 00011 00000 100000  ; ADD R3, R1, R2
```

### 4.2 程式碼大小

CISC 的優勢：同一功能的程式在 CISC 上通常比 RISC 小 20-30%。

### 4.3 管線化效率

RISC 的優勢：固定指令長度和簡單定址模式讓管線化更容易，分支預測也更精確。

### 4.4 功耗

RISC 通常更省電，因為硬體簡單，不需要複雜的解碼電路。這也是 ARM 在行動裝置市場佔主導的原因。

## 5. 現代趨勢：兩者的融合

### 5.1 x86 的 RISC 核心

現代 x86 處理器（Intel Core、AMD Ryzen）內部採用 RISC 風格的微架構：

```python
class ModernX86CPU:
    def __init__(self):
        self.micro_ops = []  # 微操作佇列

    def decode_x86_to_uops(self, x86_inst):
        """將 CISC 指令解碼為多個 RISC 風格的微操作"""
        if x86_inst['opcode'] == 'MUL':
            return [
                {'op': 'LOAD', 'src': x86_inst['src_mem'], 'dst': 'internal1'},
                {'op': 'MUL',  'src1': 'internal1', 'src2': x86_inst['src_reg']},
            ]
        elif x86_inst['opcode'] == 'ADD':
            if 'mem' in x86_inst:
                return [
                    {'op': 'LOAD', 'src': x86_inst['mem']},
                    {'op': 'ADD'},
                ]
            return [{'op': 'ADD'}]
```

### 5.2 RISC 向 CISC 學習

現代的 RISC 架構（如 ARMv8）也引入了更豐富的指令，例如：

- **ARM NEON**：SIMD 向量指令
- **RISC-V 壓縮指令**：16 位元指令版本（減少程式碼大小）
- **條件執行**：ARM 的條件執行標誌

## 6. 實際案例比較

### 6.1 計算陣列總和

**x86 (CISC)**：

```assembly
MOV ECX, 100           ; 陣列長度
XOR EAX, EAX           ; 總和 = 0
LOOP_START:
ADD EAX, [ESI+ECX*4-4] ; 從記憶體直接加到 EAX
LOOP LOOP_START        ; 自動遞減 ECX 並跳轉
```

**MIPS (RISC)**：

```assembly
ADD  R1, R0, R0        ; sum = 0
ADD  R2, R0, R0        ; i = 0
LOOP:
LW   R3, ARRAY(R2)     ; 載入陣列元素
ADD  R1, R1, R3        ; sum += element
ADDI R2, R2, 4         ; i++
BNE  R2, 400, LOOP     ; 分支
```

RISC 版本需要更多指令，但每條指令執行時間固定，管線效率更高。

## 7. 結語

RISC vs CISC 的爭論在 1990 年代達到高峰，但現代處理器已經在實踐中融合了兩者的優點。x86 在內部使用 RISC 風格的微操作，ARM 則引入了更多複雜指令。

最終，指令集架構的選擇不僅取決於技術因素，還取決於生態系統、軟體相容性和市場需求。

---

**下一步**：[GPU 架構導論](article9.md)

## 延伸閱讀

- [RISC vs CISC: The Great Debate](https://www.google.com/search?q=RISC+vs+CISC+computer+architecture+debate)
- [ARM vs x86 Architecture](https://www.google.com/search?q=ARM+vs+x86+architecture+comparison)
- [MIPS Instruction Set](https://www.google.com/search?q=MIPS+instruction+set+format+tutorial)
