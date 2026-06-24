# RISC-V 處理器設計

## RISC-V 簡介

RISC-V（發音為 "risk-five"）是一個開放的指令集架構（ISA），由 UC Berkeley 的 Krste Asanović 和他的團隊在 2010 年開始開發。

### 特點

- **開放**：任何人都可以免費使用
- **精簡**：基礎指令集非常小
- **可擴展**：支援自訂擴展
- **規范化**：避免歧義

### 與其他 ISA 比較

| ISA | 類型 | 授權 |
|-----|------|-----|
| x86 | CISC | 專有（Intel/AMD） |
| ARM | RISC | 專有（ARM Holdings） |
| MIPS | RISC | 開放（MIPS Technologies 破產） |
| RISC-V | RISC | 開放（RISC-V Foundation） |

## 指令集架構

### 基本指令集

| 名稱 | 說明 | 位元數 |
|-----|------|-------|
| RV32I | 基本整數指令（32 位元） | 32 |
| RV32E | 嵌入式基本整數指令 | 32 |
| RV64I | 64 位元基本整數指令 | 64 |
| RV128I | 128 位元基本整數指令 | 128 |

### 擴展指令集

| 擴展 | 說明 |
|-----|------|
| M | 整數乘法/除法 |
| A | 原子操作 |
| F | 單精度浮點 |
| D | 雙精度浮點 |
| C | 壓縮指令（16 位元） |
| V | 向量運算 |

## 指令格式

### R 類型（Register）

```
31        25 24  20 19  15 14  12 11      7 6      0
┌───────────┬─────┬─────┬─────┬───────────┬─────┐
│  funct7   │ rs2 │ rs1 │funct3│    rd    │opcode│
└───────────┴─────┴─────┴─────┴───────────┴─────┘
```

### I 類型（Immediate）

```
31                 20 19  15 14  12 11      7 6      0
┌───────────────────┬─────┬─────┬───────────┬─────┐
│    imm[11:0]      │ rs1 │funct3│    rd    │opcode│
└───────────────────┴─────┴─────┴───────────┴─────┘
```

### 其他格式

- **S 類型**：Store 指令
- **B 類型**：分支指令
- **U 類型**：長立即數（lui, auipc）
- **J 類型**：跳轉指令

## 基本指令

### 指標載入和儲存

```assembly
# RISC-V Assembly
lw x5, 0(x3)      # x5 = mem[x3+0]
sw x5, 4(x3)      # mem[x3+4] = x5
lb x5, 0(x3)      # x5 = sign_extend(mem[x3])
lui x5, 0x12345   # x5 = 0x12345000
```

### 算術指令

```assembly
add x5, x6, x7    # x5 = x6 + x7
sub x5, x6, x7    # x5 = x6 - x7
addi x5, x6, 10   # x5 = x6 + 10
mul x5, x6, x7    # x5 = x6 * x7
div x5, x6, x7    # x5 = x6 / x7
```

### 分支指令

```assembly
beq x5, x6, label  # if (x5 == x6) goto label
bne x5, x6, label  # if (x5 != x6) goto label
blt x5, x6, label  # if (x5 < x6) goto label
bge x5, x6, label  # if (x5 >= x6) goto label
```

### 跳轉指令

```assembly
jal x1, label     # x1 = pc + 4; pc = label
jalr x1, 0(x2)    # x1 = pc + 4; pc = x2
```

## 特權模式

| 模式 | 名稱 | 用途 |
|-----|------|-----|
| 0 | User (U) | 使用者應用程式 |
| 1 | Supervisor (S) | 作業系統核心 |
| 3 | Machine (M) | 韌體、低層級控制 |

## RISC-V 記憶體映射

### 記憶體布局

```
0x0000_0000 - 0x0FFF_FFFF : FLASH / ROM
0x1000_0000 - 0x1FFF_FFFF : SRAM
0x2000_0000 - 0x3FFF_FFFF : 外設
0x4000_0000 - 0x7FFF_FFFF : QSPI Flash
0x8000_0000 -           : DRAM
```

## 開源 RISC-V 實現

### Rocket Chip

UC Berkeley 開發的參數化處理器產生器。

```scala
// Rocket Chip 配置範例
class DefaultConfig extends Config(
    new WithNMedCores(1) ++
    new WithCoherentBusTopology ++
    new BaseConfig
)
```

### BOOM（Berkeley Out-of-Order Machine）

超標量亂序執行處理器。

### PULPino

蘇黎世聯邦理工學院開發的單核處理器。

### PicoRV32

一個小型的 RISC-V 軟核。

```verilog
module picorv32 #(
    parameter ENABLE_COUNTERS = 1
) (
    input clk,
    input resetn,
    ...
);
    // 實現程式碼
endmodule
```

## 簡化 RISC-V 核實現

### 單循環實現

```verilog
module rv32i_core (
    input clk,
    input rst,
    input [31:0] instr,
    input [31:0] mem_rdata,
    output reg [31:0] mem_addr,
    output reg [31:0] mem_wdata,
    output reg mem_valid,
    output reg mem_write
);

    reg [31:0] pc;
    reg [31:0] regs [0:31];
    reg [31:0] mem [0:1023];

    wire [6:0] opcode = instr[6:0];
    wire [4:0] rd = instr[11:7];
    wire [2:0] funct3 = instr[14:12];
    wire [6:0] funct7 = instr[31:25];

    wire [31:0] imm_i = {{20{instr[31]}}, instr[31:20]};
    wire [31:0] imm_s = {{20{instr[31]}}, instr[31:25], instr[11:7]};

    always @(posedge clk) begin
        if (!rst) begin
            pc <= 0;
        end else begin
            case (opcode)
                7'b0110111: begin // lui
                    regs[rd] <= {instr[31:12], 12'b0};
                end

                7'b0010111: begin // auipc
                    regs[rd] <= pc + {instr[31:12], 12'b0};
                end

                7'b1101111: begin // jal
                    regs[rd] <= pc + 4;
                    pc <= pc + {{12{instr[31]}}, instr[31], instr[19:12], instr[20], instr[30:21], 1'b0};
                end

                7'b1100111: begin // jalr
                    regs[rd] <= pc + 4;
                    pc <= (regs[rd] + imm_i) & ~1;
                end

                7'b1100011: begin // branch
                    if (funct3 == 3'b000 && regs[instr[19:15]] == regs[instr[24:20]])
                        pc <= pc + {{19{instr[31]}}, instr[31], instr[7], instr[30:25], instr[11:8], 1'b0};
                end

                7'b0000011: begin // load
                    mem_addr <= regs[instr[19:15]] + imm_i;
                    mem_valid <= 1;
                end

                7'b0100011: begin // store
                    mem_addr <= regs[instr[19:15]] + imm_s;
                    mem_wdata <= regs[instr[24:20]];
                    mem_write <= 1;
                end

                7'b0010011: begin // imm
                    case (funct3)
                        3'b000: regs[rd] <= regs[instr[19:15]] + imm_i;
                        3'b010: regs[rd] <= $signed(regs[instr[19:15]]) < $signed(imm_i);
                        3'b111: regs[rd] <= regs[instr[19:15]] & imm_i;
                        3'b110: regs[rd] <= regs[instr[19:15]] | imm_i;
                        3'b001: regs[rd] <= regs[instr[19:15]] << instr[24:20];
                    endcase
                end

                7'b0110011: begin // reg-reg
                    case ({funct7, funct3})
                        10'b0000000000: regs[rd] <= regs[instr[19:15]] + regs[instr[24:20]];
                        10'b0100000000: regs[rd] <= regs[instr[19:15]] - regs[instr[24:20]];
                        10'b0000000001: regs[rd] <= regs[instr[19:15]] * regs[instr[24:20]];
                        default: regs[rd] <= 0;
                    endcase
                end
            endcase
        end
    end
endmodule
```

## 開發工具

### RISC-V 工具鏈

```bash
# 安裝 riscv-tools
git clone https://github.com/riscv/riscv-tools.git
./build.sh

# 編譯程式
riscv64-unknown-elf-gcc -o firmware.elf firmware.c

# 模擬
spike pk firmware.elf
```

### 使用 GNU Toolchain

```bash
riscv64-unknown-elf-gcc \
    -march=rv32ima \
    -mabi=ilp32 \
    -o program.elf program.c

riscv64-unknown-elf-objdump -d program.elf > program.dis
```

## 未來展望

- **更廣泛的生態系統**：作業系統、編譯器、調試工具
- **安全擴展**：硬體安全功能
- **向量指令**：高效能計算
- **客製化加速**：領域特定架構

## 參考資料

- [RISC-V 官方網站](https://www.google.com/search?q=RISC-V+official+website)
- [RISC-V 指令集規範](https://www.google.com/search?q=RISC-V+ISA+specification)
- [RISC-V 軟核實現](https://www.google.com/search?q=RISC-V+softcore+implementation)