# Verilog 語法詳解

## 資料型別

### wire

硬體連線，需要持續驅動。

```verilog
wire [7:0] data_bus;    // 8 位元匯流排
wire select;             // 選擇訊號
```

### reg

儲存元素，在程序區塊中賦值。

```verilog
reg [31:0] counter;     // 32 位元計數器
reg enable;              // 致能訊號
```

### 強度與強度

```verilog
wire (strong0, strong1) reset;    // 預設強度
tri1 = 1'bz;                       // 三態，強迫上拉
wor  a_or_b;                       // 有線 OR
wand data;                         // 有線 AND
```

## 運算子

### 算術運算

```verilog
+     // 加
-     // 減
*     // 乘（可能需要DSP區塊）
/     // 除（綜合可能報錯）
%     // 取餘
```

### 位元運算

```verilog
&     // 位元 AND
|     // 位元 OR
^     // 位元 XOR
~     // 位元 NOT
<<    // 左移
>>    // 右移
```

### 縮減運算

```verilog
&a    // AND 所有位元：a[0] & a[1] & ... & a[n]
|a    // OR 所有位元：a[0] | a[1] | ... | a[n]
^a    // XOR 所有位元
~&a   // NAND
~^a   // XNOR
```

### 比較運算

```verilog
==    // 等於（X/Z 會導致結果不確定）
!=    // 不等於
===   // case 等於（X/Z 視為匹配）
!==   // case 不等於
>     // 大於
<     // 小於
>=    // 大於等於
<=    // 小於等於
```

### 邏輯運算

```verilog
&&    // 邏輯 AND
||    // 邏輯 OR
!     // 邏輯 NOT
```

### 條件運算

```verilog
a ? b : c    // 三元運算子，相當於 if-else
```

## 程序區塊

### always 區塊

```verilog
// 組合邏輯
always @(*) begin
    y = a & b;
end

// 時序邏輯
always @(posedge clk) begin
    q <= d;
end

// 非同步重置
always @(posedge clk or posedge reset) begin
    if (reset)
        q <= 0;
    else
        q <= d;
end
```

### initial 區塊

僅用於模擬和測試平台。

```verilog
initial begin
    clk = 0;
    reset = 1;
    #10 reset = 0;
end
```

## 賦值規則

### 組合邏輯（使用 =）

```verilog
always @(*) begin
    y = a & b;    // 阻塞賦值
end
```

### 時序邏輯（使用 <=）

```verilog
always @(posedge clk) begin
    q <= d;       // 非阻塞賦值
end
```

### 持續賦值

```verilog
assign y = a & b;
```

## 模組結構

```verilog
module module_name #(
    parameter WIDTH = 8,
    parameter DEPTH = 16
) (
    input  wire              clk,
    input  wire              rst,
    input  wire [WIDTH-1:0]   d,
    input  wire              wr_en,
    output reg  [WIDTH-1:0]   q,
    output wire              full
);
    // 訊號宣告
    wire we;
    reg [WIDTH-1:0] mem [0:DEPTH-1];

    // 組合邏輯
    assign full = (wr_en && (write_ptr == read_ptr));
    assign we = wr_en && !full;

    // 時序邏輯
    always @(posedge clk) begin
        if (rst) begin
            q <= 0;
        end else begin
            q <= mem[read_ptr];
        end
    end

endmodule
```

## generate 語句

```verilog
genvar i;
generate
    for (i = 0; i < 8; i = i + 1) begin : gen_fifos
        fifo #(.WIDTH(WIDTH)) u_fifo (
            .clk(clk),
            .rst(rst),
            .d(d[i*WIDTH +: WIDTH]),
            .q(q[i*WIDTH +: WIDTH])
        );
    end
endgenerate
```

## 常用系統任務

```verilog
$display("a=%b, b=%b", a, b);    // 格式化輸出
$monitor("count=%d", count);     // 監控訊號變化
$time;                            // 當前模擬時間
$finish;                          // 結束模擬
$dumpfile("wave.vcd");            // 設定波形檔案
$dumpvars;                         // 記錄所有變數
$readmemh("data.hex", mem);       // 讀取十六進位檔案
$random;                          // 亂數產生
```

## 綜合指導總結

| 可綜合 | 不可綜合 |
|-------|---------|
| always @(posedge clk) | initial |
| always @(*) | delay (#10) |
| assign | force/release |
| wire/reg | while (有限制) |
| case/if/for | $display (Synthesis 會忽略) |
| function | disable |

## 參考資料

- [Verilog 語法手冊](https://www.google.com/search?q=Verilog+language+reference)
- [Verilog 綜合指南](https://www.google.com/search?q=Verilog+synthesis+guide)