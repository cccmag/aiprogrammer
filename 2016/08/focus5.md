# Verilog HDL 入門

## 什麼是 Verilog？

Verilog 是一種硬體描述語言（HDL），用於描述和模擬數位電路。與軟體語言不同，Verilog 程式最終會被綜合成實際的硬體邏輯閘。

## 模組基本結構

```verilog
module module_name (
    input  wire a,      // 輸入宣告
    input  wire b,
    output wire y       // 輸出宣告
);

    // 電路描述

endmodule
```

## 資料型別

### 線網（wire）

表示硬體連線，需要持續驅動。

```verilog
wire [7:0] data_bus;   // 8 位元匯流排
wire select;            // 1 位元選擇訊號
```

### 暫存器（reg）

表示儲存元素，在 процедурном block 中賦值。

```verilog
reg [31:0] counter;     // 32 位元計數器
reg enable;             // 1 位元致能
```

### 向量

```verilog
reg [7:0] byte_data;    // [7] 是 MSB，[0] 是 LSB
wire [15:0] addr;      // 16 位元位址
```

## 基本邏輯閘

### AND

```verilog
and and_gate (out, a, b);           // 實例化
assign y = a & b;                    // 持續賦值
```

### OR

```verilog
or or_gate (out, a, b);
assign y = a | b;
```

### NOT

```verilog
not not_gate (out, in);
assign y = ~a;
```

### XOR

```verilog
xor xor_gate (out, a, b);
assign y = a ^ b;
```

### NAND / NOR / XNOR

```verilog
assign y = ~(a & b);   // NAND
assign y = ~(a | b);   // NOR
assign y = ~(a ^ b);   // XNOR
```

## 持續賦值（Continuous Assignment）

用於 combinational 邏輯，相當於硬體連線。

```verilog
assign y = (a & b) | c;

assign sum = a + b;        // 加法
assign carry = a & b;      // AND
```

## 程序區塊（Procedural Blocks）

### always 區塊

```verilog
always @(*) begin
    // 組合邏輯
end

always @(posedge clk) begin
    // 正反器
end
```

### initial 區塊

用於測試平台初始化。

```verilog
initial begin
    clk = 0;
    reset = 1;
    #10 reset = 0;
end
```

## 賦值類型

### 阻塞賦值（Blocking）

```verilog
a = b;
c = a;  // c 會得到 b 的值
```

### 非阻塞賦值（Non-Blocking）

```verilog
a <= b;
c <= a;  // c 會得到 a 的舊值
```

**規則**：
- 在 always @(posedge clk) 中使用 `<=`
- 在組合邏輯 always @(*) 中使用 `=`

## 條件語句

### if-else

```verilog
always @(*) begin
    if (sel == 2'b00)
        y = a;
    else if (sel == 2'b01)
        y = b;
    else
        y = c;
end
```

### case

```verilog
always @(*) begin
    case (sel)
        2'b00:    y = a;
        2'b01:    y = b;
        2'b10:    y = c;
        default:  y = 0;
    endcase
end
```

### casez / casex

```verilog
casez (pattern)
    4'b11??: result = 1;    // ? 為不關心
    4'b10??: result = 2;
endcase
```

## 迴圈

### for 迴圈

```verilog
always @(*) begin
    y = 0;
    for (i = 0; i < 8; i = i + 1) begin
        if (a[i])
            y = y + (1 << i);
    end
end
```

### while、repeat、forever

```verilog
// 少用，主要用於測試平台
```

## 模組實例化

```verilog
module top (
    input wire clk,
    input wire [7:0] data_in,
    output wire [7:0] data_out
);

    wire [7:0] mid;

    my_module instance1 (
        .clk(clk),
        .data_in(data_in),
        .data_out(mid)
    );

    my_module instance2 (
        .clk(clk),
        .data_in(mid),
        .data_out(data_out)
    );

endmodule
```

## 優先碼編碼

```verilog
parameter IDLE = 3'b000;
parameter READ = 3'b001;
parameter WRITE = 3'b010;
parameter BUSY = 3'b100;
```

## 常用運算子

| 運算子 | 說明 |
|-------|------|
| + - * / | 算術運算 |
| % | 模除 |
| & | 位元 AND |
| \| | 位元 OR |
| ^ | 位元 XOR |
| ~ | 位元 NOT |
| << >> | 移位 |
| == != | 邏輯等式 |
| === !== | case 等式 |
| ?: | 三元運算 |

## 測試平台（Testbench）

```verilog
`timescale 1ns/1ps

module tb_example;

    reg clk;
    reg [7:0] a, b;
    wire [7:0] y;

    my_module uut (
        .a(a),
        .b(b),
        .y(y)
    );

    always #5 clk = ~clk;  // 100MHz 時脈

    initial begin
        $dumpfile("waveform.vcd");
        $dumpvars(0, tb_example);

        clk = 0;
        a = 0;
        b = 0;

        #10 a = 5;
        #10 b = 3;
        #10 $display("a=%d, b=%d, y=%d", a, b, y);

        #50 $finish;
    end

endmodule
```

## 綜合指導

### 可綜合的結構

```verilog
// 組合邏輯
always @(*) begin
    case (sel)
        // ...
    endcase
end

// 時序邏輯
always @(posedge clk) begin
    if (reset)
        q <= 0;
    else
        q <= d;
end
```

### 不可綜合的結構

- `initial` 區塊（除了 ROM/RAM 初始化）
- `delay` (#10)（僅用於模擬）
- `force` / `release`

## Synthesisable 範例

### 多工器

```verilog
module mux4to1 (
    input [1:0] sel,
    input [3:0] d,
    output reg y
);
    always @(*) begin
        case (sel)
            2'b00: y = d[0];
            2'b01: y = d[1];
            2'b10: y = d[2];
            2'b11: y = d[3];
        endcase
    end
endmodule
```

### D 正反器

```verilog
module dff (
    input clk,
    input reset,
    input d,
    output reg q
);
    always @(posedge clk) begin
        if (reset)
            q <= 0;
        else
            q <= d;
    end
endmodule
```

### 同步計數器

```verilog
module counter (
    input clk,
    input reset,
    output reg [7:0] count
);
    always @(posedge clk) begin
        if (reset)
            count <= 8'd0;
        else
            count <= count + 8'd1;
    end
endmodule
```

## 參考資料

- [Verilog 語法](https://www.google.com/search?q=verilog+syntax+tutorial)
- [Verilog 綜合指南](https://www.google.com/search?q=verilog+synthesis+guide)
- [Verilog 測試平台](https://www.google.com/search?q=verilog+testbench+tutorial)