# FPGA 開發流程

## FPGA 簡介

現場可程式化邏輯閘陣列（Field-Programmable Gate Array, FPGA）是一種可由使用者程式化的積體電路。

### 與 ASIC 的比較

| 特性 | FPGA | ASIC |
|-----|------|-----|
| 開發週期 | 短（數週） | 長（數月到數年） |
| 成本 | 低（少量） | 高（大量才划算） |
| 效能 | 較低 | 較高 |
| 彈性 | 可反覆修改 | 固定 |
| 功耗 | 較高 | 較低 |

### FPGA 廠商

- **Xilinx**：Virtex、Kintex、Artix、 Spartan 系列
- **Intel（原 Altera）**：Stratix、Arria、Cyclone、MAX 系列
- **Lattice**：ECP、iCE、LatticeEC 系列
- **Microsemi**：ProASIC、IGLOO 系列

## 開發流程

```
設計輸入 → 功能模擬 → 綜合 → 實現 → 時序模擬 → 燒錄
```

### 1. 設計輸入

可以使用多種方式：

#### 原理圖輸入

傳統方式，現在較少使用。

#### HDL 設計

使用 Verilog 或 VHDL 描述電路。

```verilog
module adder (
    input [7:0] a,
    input [7:0] b,
    output [8:0] sum
);
    assign sum = a + b;
endmodule
```

#### IP 核

使用預先設計好的功能區塊。

```
- 運算單元（乘法器、DSP）
- 記憶體（RAM、ROM、FIFO）
- 通訊介面（UART、SPI、I2C）
- 處理器（Nios II、MicroBlaze）
```

### 2. 功能模擬

驗證設計功能是否正確。

```verilog
module tb;
    reg [7:0] a, b;
    wire [8:0] sum;

    adder uut (.a(a), .b(b), .sum(sum));

    initial begin
        $dumpfile("tb.vcd");
        $dumpvars;

        a = 0; b = 0;
        #10 a = 10; b = 20;
        #10 a = 255; b = 1;
        #10 $finish;
    end

    initial $monitor("a=%d, b=%d, sum=%d", a, b, sum);
endmodule
```

使用 Icarus Verilog 模擬：

```bash
# 編譯
iverilog -o tb.vvp tb.v adde
r.v

# 執行
vvp tb.vvp

# 產生波形
gtkwave tb.vcd
```

### 3. 綜合（Synthesis）

將 HDL 轉換為邏輯閘網表。

- **去除未使用的邏輯**
- **資源共享**
- **優化邏輯**
- **產生 EDIF 或 NGC 檔案**

### 4. 實現（Implementation）

包括：

#### 翻譯（Translate）

合併多個 netlist 為單一資料庫。

#### 映射（Map）

將邏輯對應到 FPGA 的實際資源。

```
LUT + FF → CLB/Slice/LAB
```

#### 放置（Place）

將每個 CLB 放置在晶片上的特定位置。

#### 路由（Route）

連接各 CLB 之間的訊號線。

### 5. 時序分析

驗證設計是否滿足時序約束。

```tcl
# SDC 約束檔案範例
create_clock -name clk -period 10.0 [get_ports clk]
set_input_delay -clock clk -max 2.0 [all_inputs]
set_output_delay -clock clk -max 2.0 [all_outputs]
```

關鍵路徑分析：
```
Slack = Required Time - Arrival Time
Slack > 0: 滿足時序
Slack < 0: 時序違規
```

### 6. 燒錄（Programming）

將設計下載到 FPGA。

#### 程式檔案格式

| 格式 | 用途 |
|-----|------|
| .bit (Xilinx) | 單次燒錄 |
| .rbf | 原始位元組檔案 |
| .mcs | PROM 燒錄檔 |
| .sof (Intel) | 單次燒錄 |
| .pof (Intel) | PROM 燒錄檔 |

#### JTAG 燒錄

```bash
# Xilinx
impact -batch script.txt

# Intel
quartus_pgm -c 1 -m jtag -o "p;output_file.sof"
```

## 開發工具

### Xilinx 工具鏈

| 工具 | 用途 |
|-----|------|
| Vivado | 主要 IDE（7 系列以上） |
| ISE | 舊款 FPGA（已停產） |
| SDK | 嵌入式軟體開發 |

### Intel（原 Altera）工具鏈

| 工具 | 用途 |
|-----|------|
| Quartus Prime | 主要 IDE |
| ModelSim-Intel | 模擬 |
| Nios II EDS | 嵌入式處理器開發 |

### 開源工具

| 工具 | 用途 |
|-----|------|
| Icarus Verilog | Verilog 模擬 |
| Verilator | 高效能模擬 |
| Yosys | 綜合 |
| nextpnr | 放置路由 |
| IceStorm | Lattice FPGA 工具鏈 |

## FPGA 資源

### 基本邏輯資源

```
Slice / CLB
├── LUT（查表表）    // 實現任意布林函數
├── FF（正反器）     // 儲存狀態
├── MUX（多工器）    // 訊號選擇
└── 進位鏈           // 快速進位
```

### 特殊資源

| 資源 | 說明 |
|-----|------|
| Block RAM | 大容量嵌入式記憶體 |
| DSP Slice | 硬體乘法器/累加器 |
| CMT/PLL | 時脈管理 |
| SelectIO | 高速 I/O |
| GTP/GTX | 高速序列收發器 |

## 設計範例：LED 閃爍

```verilog
module led_blink (
    input clk,
    input rst,
    output reg led
);
    parameter CNT_MAX = 25_000_000; // 100MHz / 2 = 1Hz

    reg [31:0] cnt;

    always @(posedge clk) begin
        if (rst) begin
            cnt <= 0;
            led <= 0;
        end else if (cnt == CNT_MAX - 1) begin
            cnt <= 0;
            led <= ~led;
        end else begin
            cnt <= cnt + 1;
        end
    end
endmodule
```

約束檔案（Xilinx XDC）：

```tcl
create_clock -period 10.000 -name sys_clk -waveform {0.000 5.000} -add [get_ports clk]
set_property PACKAGE_PIN E3 [get_ports clk]
set_property IOSTANDARD LVCMOS33 [get_ports clk]

set_property PACKAGE_PIN H5 [get_ports led]
set_property IOSTANDARD LVCMOS33 [get_ports led]
```

## 除錯技巧

### ChipScope/SignalTap

在設計中加入邏輯分析儀 IP。

```verilog
wire [7:0] debug_data;
assign debug_data = {a, b, sum};

ila_0 ila_inst (
    .clk(clk),
    .probe0(debug_data)
);
```

### 設計最佳化

- **時序**：流水線、平行化、模組化
- **資源**：资源共享、記憶體優化
- **功耗**：時閘、無效邏輯消除

## 參考資料

- [FPGA 設計流程](https://www.google.com/search?q=FPGA+design+flow+tutorial)
- [Xilinx Vivado 教學](https://www.google.com/search?q=Xilinx+Vivado+tutorial)
- [Quartus 使用指南](https://www.google.com/search?q=Quartus+Prime+tutorial)