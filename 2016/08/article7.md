# RISC-V 指令集架構

## RISC-V 基本概念

RISC-V 是一個基於精簡指令集電腦原則的開放指令集架構。

## 指令格式

### 基本格式

```
RV32I 基本整數指令：

R 類型：op rd, rs1, rs2
31      25 24  20 19  15 14  12 11      7 6      0
┌────────┬─────┬─────┬─────┬─────────┬──────┐
│ funct7 │ rs2 │ rs1 │funct3│   rd   │opcode│
└────────┴─────┴─────┴─────┴─────────┴──────┘

I 類型：op rd, rs1, imm[11:0]
31                      20 19  15 14  12 11      7 6      0
┌─────────────────────────┬─────┬─────┬─────────┬──────┐
│   imm[11:0]             │ rs1 │funct3│   rd   │opcode│
└─────────────────────────┴─────┴─────┴─────────┴──────┘

S 類型：op rs2, rs1, imm
31        25 24  20 19  15 14  12 11      7 6      0
┌────────┬─────┬─────┬─────┬───────────────────┬──────┐
│imm[11:5]│ rs2 │ rs1 │funct3│  imm[4:0]        │opcode│
└────────┴─────┴─────┴─────┴───────────────────┴──────┘
```

## RV32I 基本指令

### 指標操作

| 指令 | 格式 | 說明 |
|-----|------|-----|
| lw | I | 載入字組 |
| lh | I | 載入半字（符號擴展） |
| lhu | I | 載入半字（零擴展） |
| lb | I | 載入位元組（符號擴展） |
| lbu | I | 載入位元組（零擴展） |
| sw | S | 儲存字組 |
| sh | S | 儲存半字 |
| sb | S | 儲存位元組 |

### 算術操作

| 指令 | 格式 | 說明 |
|-----|------|-----|
| add | R | 加法 |
| sub | R | 減法 |
| addi | I | 加立即數 |
| lui | U | 載入高位立即數 |
| auipc | U | 加 PC 到立即數 |

### 邏輯操作

| 指令 | 格式 | 說明 |
|-----|------|-----|
| and | R | 位元 AND |
| or | R | 位元 OR |
| xor | R | 位元 XOR |
| andi | I | AND 立即數 |
| ori | I | OR 立即數 |
| xori | I | XOR 立即數 |

### 移位操作

| 指令 | 格式 | 說明 |
|-----|------|-----|
| sll | R | 左移 |
| srl | R | 右移（邏輯） |
| sra | R | 右移（算術） |
| slli | I | 左移立即數 |
| srli | I | 右移立即數（邏輯） |
| srai | I | 右移立即數（算術） |

### 分支指令

| 指令 | 條件 | 說明 |
|-----|------|-----|
| beq | rs1 == rs2 | 相等分支 |
| bne | rs1 != rs2 | 不等分支 |
| blt | rs1 < rs2 (signed) | 小於分支 |
| bge | rs1 >= rs2 (signed) | 大於等於分支 |
| bltu | rs1 < rs2 (unsigned) | 無符號小於分支 |
| bgeu | rs1 >= rs2 (unsigned) | 無符號大於等於分支 |

### 跳轉指令

| 指令 | 說明 |
|-----|-----|
| jal | 跳轉並連結 |
| jalr | 跳轉並連結暫存器 |

## 擴展指令集

### M 擴展：乘法和除法

```assembly
mul   x5, x6, x7    # x5 = x6 * x7
mulh  x5, x6, x7    # 高位乘法（Signed × Signed）
div   x5, x6, x7    # x5 = x6 / x7
rem   x5, x6, x7    # x5 = x6 % x7
```

### A 擴展：原子操作

```assembly
amoadd.w  x5, x6, (x7)   # x5 = mem[x7]; mem[x7] += x6
amoswap.w x5, x6, (x7)    # x5 = mem[x7]; mem[x7] = x6
lr.w      x5, (x6)        # 載入保留
sc.w      x5, x6, (x7)    # 條件儲存
```

### F/D 擴展：浮點

```assembly
flw    fa0, 0(x2)     # 載入單精度
fsw    fa0, 0(x2)     # 儲存單精度
fadd.s fa0, fa1, fa2  # 單精度加法
fmul.s fa0, fa1, fa2  # 單精度乘法
fcvt.w.s a0, fa0      # 浮點轉整數
```

### C 擴展：壓縮指令

16 位元長度的常見指令簡化版本：

```assembly
# 完整指令
add x5, x6, x7

# 壓縮指令
c.add x5, x6    # 32 位元 → 16 位元
```

## 特權指令

### M 模式（Machine Mode）

```assembly
csrrw  t0, mstatus, t1    # 讀寫 CSR
csrr   t0, mstatus         # 讀取 CSR
csrw   mstatus, t0         # 寫入 CSR
```

### 異常處理

```assembly
mret    # 從機器模式返回
ecall   # 觸發環境呼叫
ebreak  # 觸發除錯斷點
```

## 組合多個擴展

範例：`RV32IMAFDC`

- **I**：基本整數指令
- **M**：乘法/除法
- **A**：原子操作
- **F**：單精度浮點
- **D**：雙精度浮點
- **C**：壓縮指令

## 參考資料

- [RISC-V 指令集規範](https://www.google.com/search?q=RISC-V+ISA+specification)
- [RISC-V 指令格式](https://www.google.com/search?q=RISC-V+instruction+format)