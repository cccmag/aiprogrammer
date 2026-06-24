# Verilog 實作範例

## 前言

理論說得再多，不如親手實作一個 Verilog 設計。本篇文章將帶領讀者用 Verilog 實作基本的數位電路，包括基本邏輯閘、組合邏輯電路和時序邏輯電路。

本範例展示：
- 基本邏輯閘
- 多工器與解碼器
- D 正反器
- 簡單的狀態機

---

## 原始碼

完整的 Verilog 程式碼請參考：[_code/verilog_examples.v](_code/verilog_examples.v)

```verilog
`timescale 1ns/1ps

module basic_gates (
    input wire a,
    input wire b,
    output wire y_and,
    output wire y_or,
    output wire y_not,
    output wire y_xor,
    output wire y_nand,
    output wire y_nor
);
    assign y_and = a & b;
    assign y_or  = a | b;
    assign y_not = ~a;
    assign y_xor = a ^ b;
    assign y_nand = ~(a & b);
    assign y_nor  = ~(a | b);
endmodule


module mux2to1 (
    input wire sel,
    input wire [1:0] d,
    output reg y
);
    always @(*) begin
        case (sel)
            1'b0: y = d[0];
            1'b1: y = d[1];
        endcase
    end
endmodule


module decoder2to4 (
    input wire [1:0] in,
    output reg [3:0] out
);
    always @(*) begin
        case (in)
            2'b00: out = 4'b0001;
            2'b01: out = 4'b0010;
            2'b10: out = 4'b0100;
            2'b11: out = 4'b1000;
        endcase
    end
endmodule


module d_flip_flop (
    input wire clk,
    input wire reset,
    input wire d,
    output reg q
);
    always @(posedge clk or posedge reset) begin
        if (reset)
            q <= 1'b0;
        else
            q <= d;
    end
endmodule


module counter8bit (
    input wire clk,
    input wire reset,
    output reg [7:0] count
);
    always @(posedge clk) begin
        if (reset)
            count <= 8'd0;
        else
            count <= count + 8'd1;
    end
endmodule


module fsm_example (
    input wire clk,
    input wire reset,
    input wire coin,
    output reg item,
    output reg change
);
    localparam S0 = 2'b00;
    localparam S1 = 2'b01;
    localparam S2 = 2'b10;

    reg [1:0] state, next_state;

    always @(posedge clk or posedge reset) begin
        if (reset)
            state <= S0;
        else
            state <= next_state;
    end

    always @(*) begin
        next_state = state;
        item = 0;
        change = 0;

        case (state)
            S0: begin
                if (coin) next_state = S1;
            end

            S1: begin
                if (coin) begin
                    next_state = S2;
                end
            end

            S2: begin
                if (coin) begin
                    next_state = S0;
                    item = 1;
                end else begin
                    next_state = S0;
                    item = 1;
                    change = 1;
                end
            end
        endcase
    end
endmodule


module adder4bit (
    input wire [3:0] a,
    input wire [3:0] b,
    output wire [4:0] sum
);
    assign sum = a + b;
endmodule


module register8bit (
    input wire clk,
    input wire reset,
    input wire load,
    input wire [7:0] d,
    output reg [7:0] q
);
    always @(posedge clk) begin
        if (reset)
            q <= 8'd0;
        else if (load)
            q <= d;
    end
endmodule
```

---

## 測試平台

[_code/tb_verilog.v](_code/tb_verilog.v)

```verilog
`timescale 1ns/1ps

module tb_basic_gates;
    reg a, b;
    wire y_and, y_or, y_not, y_xor, y_nand, y_nor;

    basic_gates uut (.a(a), .b(b), .y_and(y_and), .y_or(y_or),
                     .y_not(y_not), .y_xor(y_xor), .y_nand(y_nand), .y_nor(y_nor));

    initial begin
        $dumpfile("tb_basic_gates.vcd");
        $dumpvars(0, tb_basic_gates);

        $display("Testing Basic Gates");
        a = 0; b = 0; #10;
        $display("a=%b, b=%b -> AND=%b, OR=%b, NOT=%b, XOR=%b", a, b, y_and, y_or, y_not, y_xor);

        a = 0; b = 1; #10;
        $display("a=%b, b=%b -> AND=%b, OR=%b, NOT=%b, XOR=%b", a, b, y_and, y_or, y_not, y_xor);

        a = 1; b = 0; #10;
        $display("a=%b, b=%b -> AND=%b, OR=%b, NOT=%b, XOR=%b", a, b, y_and, y_or, y_not, y_xor);

        a = 1; b = 1; #10;
        $display("a=%b, b=%b -> AND=%b, OR=%b, NOT=%b, XOR=%b", a, b, y_and, y_or, y_not, y_xor);

        #10 $finish;
    end
endmodule


module tb_counter;
    reg clk, reset;
    wire [7:0] count;

    counter8bit uut (.clk(clk), .reset(reset), .count(count));

    always #5 clk = ~clk;

    initial begin
        $dumpfile("tb_counter.vcd");
        $dumpvars(0, tb_counter);

        clk = 0;
        reset = 1;
        #10 reset = 0;

        #200 $finish;
    end

    always @(posedge clk) begin
        $display("count = %d", count);
    end
endmodule


module tb_fsm;
    reg clk, reset, coin;
    wire item, change;

    fsm_example uut (.clk(clk), .reset(reset), .coin(coin), .item(item), .change(change));

    always #5 clk = ~clk;

    initial begin
        $dumpfile("tb_fsm.vcd");
        $dumpvars(0, tb_fsm);

        clk = 0;
        reset = 1;
        coin = 0;

        #10 reset = 0;
        #10 coin = 1;
        #10 coin = 0;
        #10 coin = 1;
        #10 coin = 0;
        #10 coin = 1;
        #10 coin = 0;

        #50 $finish;
    end
endmodule
```

---

## 編譯與執行

使用 Icarus Verilog 編譯和執行：

```bash
# 編譯
iverilog -o tb_basic_gates.vvp tb_verilog.v

# 執行
vvp tb_basic_gates.vvp

# 查看波形
gtkwave tb_basic_gates.vcd
```

---

## 輸出範例

```
Testing Basic Gates
a=0, b=0 -> AND=0, OR=0, NOT=1, XOR=0
a=0, b=1 -> AND=0, OR=1, NOT=1, XOR=1
a=1, b=0 -> AND=0, OR=1, NOT=0, XOR=1
a=1, b=1 -> AND=1, OR=1, NOT=0, XOR=0
```

---

## 設計說明

### 基本邏輯閘

使用持續賦值（`assign`）描述 combinational 邏輯。

### 多工器

使用 `always @(*)` 程序區塊和 `case` 語句描述 combinational 邏輯。

### D 正反器

在時脈上升邊緣更新輸出，使用非阻塞賦值（`<=`）。

### 計數器

使用時脈驅動的 always 區塊，在每個時脈邊緣遞增計數。

### 狀態機

標準的兩段式狀態機：
- 第一段：時脈同步的狀態更新
- 第二段：組合邏輯的下一狀態和輸出計算

---

## 延伸練習

有興趣的讀者可以嘗試以下改進：

1. **設計 4 選 1 多工器**
2. **設計 3 對 8 解碼器**
3. **設計可清除和可預置的計數器**
4. **設計帶有超時功能的狀態機**
5. **設計一個簡單的 UART 發送器**

---

## 結語

這個範例涵蓋了 Verilog 的核心概念：

- 模組定義和實例化
- 持續賦值與程序賦值
- Combinational 邏輯與時序邏輯
- 狀態機設計
- 測試平台編寫

掌握這些基礎，你就可以開始設計更複雜的數位系統。

詳細的技術背景請參考：
- [數位邏輯基礎](focus1.md) — 數位與類比、進位制
- [布林代數與邏輯閘](focus2.md) — 邏輯運算
- [組合邏輯電路](focus3.md) — 多工器、解碼器
- [序向邏輯電路](focus4.md) — 正反器、計數器
- [FPGA 開發流程](focus6.md) — 設計、模擬、實現