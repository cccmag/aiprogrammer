# UART 通訊協定實作

## UART 簡介

UART（Universal Asynchronous Receiver/Transmitter）是一種常用的序列通訊協定。

## 通訊格式

```
START  D0  D1  D2  D3  D4  D5  D6  D7  PARITY  STOP
  ↓    ↓   ↓   ↓   ↓   ↓   ↓   ↓   ↓   ↓       ↓
  0    1   0   1   1   0   1   0   1   0        1
```

## 參數

| 參數 | 說明 |
|-----|------|
| Baud Rate | 傳輸速率（如 9600、115200） |
| Data Bits | 資料位元（5-9，通常為 8） |
| Stop Bits | 停止位元（1 或 2） |
| Parity | 同位檢查（None/Odd/Even） |

### 常用配置

```
9600 8N1：9600 波特，8 資料位元，無同位，1 停止位元
115200 8N1：115200 波特，8 資料位元，無同位，1 停止位元
```

## 位元時間計算

```
1 位元時間 = 1 / Baud Rate

9600 bps:  1 位元時間 = 104.17µs
115200 bps: 1 位元時間 = 8.68µs
```

## Verilog UART 發送器

```verilog
module uart_tx (
    input wire clk,
    input wire reset,
    input wire [7:0] tx_data,
    input wire tx_start,
    output reg tx_busy,
    output reg tx
);

    parameter CLKS_PER_BIT = 868;  // 50MHz / 115200 = 434.6

    localparam IDLE = 3'd0,
               START = 3'd1,
               DATA = 3'd2,
               STOP = 3'd3,
               CLEANUP = 3'd4;

    reg [2:0] state = IDLE;
    reg [15:0] clk_count = 0;
    reg [2:0] bit_index = 0;

    always @(posedge clk) begin
        if (reset) begin
            state <= IDLE;
            tx <= 1'b1;
            clk_count <= 0;
            bit_index <= 0;
            tx_busy <= 1'b0;
        end else begin
            case (state)
                IDLE: begin
                    tx <= 1'b1;
                    clk_count <= 0;
                    bit_index <= 0;

                    if (tx_start) begin
                        state <= START;
                        tx_busy <= 1'b1;
                    end
                end

                START: begin
                    tx <= 1'b0;

                    if (clk_count < CLKS_PER_BIT - 1)
                        clk_count <= clk_count + 1;
                    else begin
                        clk_count <= 0;
                        state <= DATA;
                    end
                end

                DATA: begin
                    tx <= tx_data[bit_index];

                    if (clk_count < CLKS_PER_BIT - 1)
                        clk_count <= clk_count + 1;
                    else begin
                        clk_count <= 0;

                        if (bit_index < 7)
                            bit_index <= bit_index + 1;
                        else
                            state <= STOP;
                    end
                end

                STOP: begin
                    tx <= 1'b1;

                    if (clk_count < CLKS_PER_BIT - 1)
                        clk_count <= clk_count + 1;
                    else begin
                        clk_count <= 0;
                        state <= CLEANUP;
                    end
                end

                CLEANUP: begin
                    tx_busy <= 1'b0;
                    state <= IDLE;
                end
            endcase
        end
    end
endmodule
```

## Verilog UART 接收器

```verilog
module uart_rx (
    input wire clk,
    input wire reset,
    input wire rx,
    output reg [7:0] rx_data,
    output reg rx_valid
);

    parameter CLKS_PER_BIT = 868;

    localparam IDLE = 3'd0,
               START = 3'd1,
               DATA = 3'd2,
               STOP = 3'd3,
               CLEANUP = 3'd4;

    reg [2:0] state = IDLE;
    reg [15:0] clk_count = 0;
    reg [2:0] bit_index = 0;

    always @(posedge clk) begin
        if (reset) begin
            state <= IDLE;
            rx_data <= 0;
            clk_count <= 0;
            bit_index <= 0;
            rx_valid <= 1'b0;
        end else begin
            case (state)
                IDLE: begin
                    rx_valid <= 1'b0;
                    clk_count <= 0;
                    bit_index <= 0;

                    if (rx == 1'b0)
                        state <= START;
                end

                START: begin
                    if (clk_count == (CLKS_PER_BIT - 1) / 2) begin
                        if (rx == 1'b0) begin
                            clk_count <= 0;
                            state <= DATA;
                        end else
                            state <= IDLE;
                    end else
                        clk_count <= clk_count + 1;
                end

                DATA: begin
                    if (clk_count < CLKS_PER_BIT - 1)
                        clk_count <= clk_count + 1;
                    else begin
                        clk_count <= 0;
                        rx_data[bit_index] <= rx;

                        if (bit_index < 7)
                            bit_index <= bit_index + 1;
                        else begin
                            bit_index <= 0;
                            state <= STOP;
                        end
                    end
                end

                STOP: begin
                    if (clk_count < CLKS_PER_BIT - 1)
                        clk_count <= clk_count + 1;
                    else begin
                        rx_valid <= 1'b1;
                        clk_count <= 0;
                        state <= CLEANUP;
                    end
                end

                CLEANUP: begin
                    state <= IDLE;
                end
            endcase
        end
    end
endmodule
```

## 測試平台

```verilog
module tb_uart;

    reg clk, reset;
    reg [7:0] tx_data;
    reg tx_start;
    wire tx, tx_busy;
    wire [7:0] rx_data;
    wire rx_valid;

    uart_tx tx_inst (
        .clk(clk),
        .reset(reset),
        .tx_data(tx_data),
        .tx_start(tx_start),
        .tx_busy(tx_busy),
        .tx(tx)
    );

    uart_rx rx_inst (
        .clk(clk),
        .reset(reset),
        .rx(tx),
        .rx_data(rx_data),
        .rx_valid(rx_valid)
    );

    always #8.68 clk = ~clk;  // ~115200 baud

    initial begin
        $dumpfile("tb_uart.vcd");
        $dumpvars(0, tb_uart);

        clk = 0;
        reset = 1;
        tx_data = 0;
        tx_start = 0;

        #100 reset = 0;
        #100 tx_data = 8'hA5;
        tx_start = 1;
        #10 tx_start = 0;

        wait(rx_valid);
        $display("Received: %h", rx_data);

        #1000 $finish;
    end
endmodule
```

## 參考資料

- [UART 通訊協定](https://www.google.com/search?q=UART+communication+protocol)
- [UART 硬體實現](https://www.google.com/search?q=UART+hardware+implementation+FPGA)