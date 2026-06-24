# Quartus II 開發環境

## Quartus Prime 簡介

Quartus Prime 是 Intel（原 Altera）FPGA 的主要開發軟體。

## 安裝

1. 從 Intel 官網下載 Quartus Prime Lite（免費版本）
2. 選擇要安裝的元件：
   - Quartus Prime 主體
   - ModelSim-Intel
   - Nios II EDS
   - 需要的裝置系列

## 專案建立

### 1. 新建專案

```
File → New Project Wizard
```

### 2. 設定專案

```
Directory, Name, Top-Level Entity
→ Family & Device Settings (選擇晶片型號)
→ EDA Tool Settings (設定模擬工具)
→ Summary
```

## 設計輸入

### Verilog 檔案

```verilog
module led_blink (
    input  wire clk,
    input  wire rst_n,
    output reg  led
);
    localparam CNT_MAX = 25_000_000;

    reg [31:0] cnt;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            cnt <= 32'd0;
            led <= 1'b0;
        end else if (cnt == CNT_MAX - 1) begin
            cnt <= 32'd0;
            led <= ~led;
        end else begin
            cnt <= cnt + 32'd1;
        end
    end
endmodule
```

### VHDL 檔案

```vhdl
library ieee;
use ieee.std_logic_1164.all;

entity led_blink is
    port (
        clk  : in  std_logic;
        rst_n: in  std_logic;
        led  : out std_logic
    );
end entity led_blink;

architecture rtl of led_blink is
begin
    process(clk, rst_n) begin
        if rst_n = '0' then
            led <= '0';
        elsif rising_edge(clk) then
            led <= not led;
        end if;
    end process;
end architecture rtl;
```

## 引腳分配

### GUI 方式

```
Assignments → Pin Planner
```

### QSF 方式

```tcl
set_location_assignment PIN_E1 -to clk
set_location_assignment PIN_M1 -to led
set_instance_assignment -name IOSTANDARD LVCMOS33 -to clk
set_instance_assignment -name IOSTANDARD LVCMOS33 -to led
```

## 編譯

### 完整編譯

```
Processing → Start Compilation
或按 Ctrl+L
```

### 階段性編譯

```
Analysis & Synthesis
Fitter
Assembler
TimeQuest Timing Analyzer
```

## 模擬

### 使用 ModelSim

1. **新增模擬庫**：

```
Tools → Launch Simulation Library Compiler
```

2. **設定模擬**：

```
Tools → Options → EDA Tool Options
設定 ModelSim 路徑
```

3. **執行模擬**：

```
Simulation → Run Gate Level Simulation
或
Simulation → Run RTL Simulation
```

### 波形編輯

1. 開啟 Simulate → Start Simulation
2. 選擇要模擬的模組
3. 在 Objects 視窗選擇訊號加入波形
4. 按下 Run 按鈕

## 除錯

### SignalTap Logic Analyzer

內建的邏輯分析儀：

1. **新增 SignalTap**：

```
Tools → SignalTap Logic Analyzer
```

2. **新增實例**：

```
Instance name: auto_signaltap_0
```

3. **新增訊號**：

```
雙擊空白處開啟 Node Finder
選擇要監控的訊號
```

4. **設定觸發條件**：

```
Trigger conditions
Trigger in
```

5. **燒錄並執行**：

```
File → Save
Processing → Run Analysis
```

## 程式化

### SOF 燒錄（SRAM）

```
Tools → Programmer
點擊 Start
```

### POF 燒錄（Configuration Device）

需要先將 SOF 轉換為 POF：
```
File → Convert Programming Files
選擇 Flash_loader → 選擇正確的 EPCS 型號
選擇 SOF File
Generate
```

## 常用快捷鍵

| 快捷鍵 | 功能 |
|-------|------|
| Ctrl+L | 完整編譯 |
| Ctrl+K | 重新分析與綜合 |
| Ctrl+R | 執行路由 |
| F4 | 重新整理 |

## 常見問題

### 資源使用過高

- 啟用資源共享
- 使用流水線
- 優化邏輯

### 時序違規

- 增加約束
- 流水線分割
- 使用 DSP/ RAM 原語

## 參考資料

- [Quartus Prime 使用指南](https://www.google.com/search?q=Quartus+Prime+tutorial)
- [Intel FPGA 官方網站](https://www.google.com/search?q=Intel+FPGA+official+website)