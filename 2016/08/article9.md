# 時序分析與時序約束

## 時序分析基礎

時序分析確保設計在指定時脈頻率下正確運作。

## 時序路徑

### 4 種基本路徑

1. **Register to Register**：時脈到時脈（最常見）
2. **Port to Register**：輸入到暫存器
3. **Register to Port**：暫存器到輸出
4. **Port to Port**：輸入到輸出

## 時序參數

### 正反器參數

| 參數 | 說明 |
|-----|------|
| t_clk→Q | 時脈邊緣到輸出有效的延遲 |
| t_setup | 資料在時脈前必須穩定的時間 |
| t_hold | 資料在時脈後必須保持的時間 |

### 資料路徑延遲

```
t_data = t_clk→Q + t_comb + t_net
```

- t_comb：組合邏輯延遲
- t_net：網路延遲

## 時序約束

### 創建時脈

```tcl
# 基礎時脈
create_clock -name sys_clk -period 10.0 [get_ports clk]

# 衍生時脈
create_generated_clock -name clk_div2 \
    -source [get_ports clk] -divide_by 2 [get_pins clk_divider/out]
```

### 設定輸入延遲

```tcl
set_input_delay -clock sys_clk -max 2.0 [all_inputs]
set_input_delay -clock sys_clk -min 0.5 [all_inputs]
```

### 設定輸出延遲

```tcl
set_output_delay -clock sys_clk -max 3.0 [all_outputs]
set_output_delay -clock sys_clk -min 1.0 [all_outputs]
```

### 設定_false_path

```tcl
# 异步訊號不需要時序約束
set_false_path -from [get_ports reset_async]

# 特定路徑忽略
set_false_path -from reg1 -to reg2
```

### 設定_multicycle_path

```tcl
# 兩周期路徑
set_multicycle_path -setup -from reg1 -to reg2 2
set_multicycle_path -hold -from reg1 -to reg2 1
```

## 時序報告分析

### 查看報告

```tcl
# 報告時序
report_timing

# 報告最差路徑
report_timing -max_paths 10

# 報告時序違規
report_timing -max_delay
```

### 報告解讀

```
Slack (setup): 2.456ns
  Source: u_counter/count_reg[7] (FF)
  Destination: u_counter/count_reg[0] (FF)

  Data Path Delay: 7.544ns
    Cell Delay: 5.123ns
    Net Delay: 2.421ns

  Clock Path Skew: 0.089ns
  Clock Uncertainty: 0.100ns
```

## 常見時序問題

### Setup Violation

資料到達太慢，來不及在時脈邊緣前穩定。

```
解決方法：
- 流水線分割
- 减少邏輯層級
- 使用 DSP/ RAM 原語
- 提高時脈頻率（不建議）
```

### Hold Violation

資料改變太快，在時脈邊緣後很快就改變。

```
解決方法：
- 增加組合邏輯延遲
- 使用時脈延遲
- 調整佈局
```

## 約束編輯器

### 在 Quartus 中

```
Assignments → Settings → Timing Analyzer
```

### 在 Vivado 中

```
Open Synthesized Design → Report Timing Summary
```

## 高級約束

### 速度-grade 約束

```tcl
# 設定不同速度等級的約束
set_input_delay -clock sys_clk -max 2.0 \
    -add_delay [get_ports data_in]
```

### 時脈群組

```tcl
# 非同步時脈
create_clock -name clk_a -period 10.0 [get_pins clk_a]
create_clock -name clk_b -period 8.0 [get_pins clk_b]

set_clock_groups -async -group clk_a -group clk_b
```

## 參考資料

- [時序分析基礎](https://www.google.com/search?q=timing+analysis+tutorial)
- [SDC 約束](https://www.google.com/search?q=SDC+constraints+tutorial)
- [FPGA 時序優化](https://www.google.com/search?q=FPGA+timing+optimization)