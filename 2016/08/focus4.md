# 序向邏輯電路

## 序向邏輯特性

序向邏輯電路（Sequential Logic Circuit）的輸出不僅取決於當前輸入，還取決於過去的狀態。這些電路具有記憶能力。

```
           ┌──────────────┐
輸入 ──────→│ 組合邏輯電路 │──→ 輸出
           │              │
           └──←─ 記憶元素 ←──┘
```

## 正反器（Flip-Flop）

正反器是序向邏輯電路的基本 building block，能儲存一位元資料。

### SR 正反器

```
        ┌──┐
   S ───┤  ├── Q
   R ───┤  ├── Q'
        └──┘

SR = 00: 保持
SR = 01: Q = 0 (RESET)
SR = 10: Q = 1 (SET)
SR = 11: 不允許（不穩定）
```

### D 正反器

在時脈邊緣時將 D 輸入傳到輸出。

```
        ┌──┐
   D ───┤  ├── Q
   CLK ─┤  ├── Q'
        └──┘

時脈上升邊緣：Q = D
其它時間：保持
```

### JK 正反器

SR 正反器的改良，解決了不穩定問題。

```
        ┌──┐
   J ───┤  ├── Q
   K ───┤  ├── Q'
   CLK ─┘

JK = 00: 保持
JK = 01: RESET (Q=0)
JK = 10: SET (Q=1)
JK = 11: 切換 (Q = Q')
```

### T 正反器

每次觸發時反轉輸出。

```
        ┌──┐
   T ───┤  ├── Q
   CLK ─┤  ├── Q'
        └──┘

T = 0: 保持
T = 1: 切換 (Q = Q')
```

## 暫存器（Register）

多個正反器組合儲存多位元資料。

### N 位元暫存器

```
D[0] ─→ D Q ─→ Q[0] ─┐
                      │
D[1] ─→ D Q ─→ Q[1] ─┼──→ Q[N-1:0]
     ...              │
D[N-1] ─→ D Q ─→ Q[N-1] ┘
      │
CLK ──┘
```

### 移位暫存器

資料可以在時脈邊緣時左右移動。

```
左移：Q[n] = Q[n+1]
右移：Q[n] = Q[n-1]
```

類型：
- **SISO**：序列輸入，序列輸出
- **SIPO**：序列輸入，並列輸出
- **PISO**：並列輸入，序列輸出
- **PIPO**：並列輸入，並列輸出

## 計數器（Counter）

在時脈脈衝下，計數值會遞增或遞減。

### 同步二進位計數器

```
模 8 計數器：

CLK │ Q2 │ Q1 │ Q0 │ 十進位
────┼────┼────┼────┼───────
 0  │ 0  │ 0  │ 0  │   0
 1  │ 0  │ 0  │ 1  │   1
 2  │ 0  │ 1  │ 0  │   2
 3  │ 0  │ 1  │ 1  │   3
 4  │ 1  │ 0  │ 0  │   4
 5  │ 1  │ 0  │ 1  │   5
 6  │ 1  │ 1  │ 0  │   6
 7  │ 1  │ 1  │ 1  │   7
 8  │ 0  │ 0  │ 0  │   0 ( rollover )
```

### 漣波計數器（Ripple Counter）

每級的正反器輸出作為下一級的時脈。

```
         ┌───┐
CLK ──→──┤ T ├───────┬───┐
         └───┘       │   │
                    └───┘
```

缺點：累計傳播延遲

### 可程式計數器

可以設定初始值和終止值。

```verilog
module counter #(
    parameter WIDTH = 8,
    parameter MAX = 100
)(
    input clk,
    input reset,
    input [WIDTH-1:0] load_value,
    input load,
    output reg [WIDTH-1:0] count
);
    always @(posedge clk or posedge reset) begin
        if (reset)
            count <= 0;
        else if (load)
            count <= load_value;
        else if (count == MAX)
            count <= 0;
        else
            count <= count + 1;
    end
endmodule
```

## 狀態機（State Machine）

狀態機用於描述具有有限狀態的系統行為。

### 摩爾機（Moore Machine）

輸出只取決於當前狀態。

```
輸入 → [組合邏輯] → [狀態暫存器] → 輸出
              ↑                    │
              └─────── 狀態 ←──────┘
```

### 米莉機（Mealy Machine）

輸出取決於當前狀態和輸入。

```
輸入 → [組合邏輯] ─────────────→ 輸出
         ↓                       ↑
輸入 → [狀態暫存器] → 狀態 ─────┘
```

### 範例：簡易自動販賣機

```
狀態：
S0: 等待投幣
S1: 已投 5 元
S2: 已投 10 元

輸入：5元、10元、 reset
輸出：商品、出找回
```

```verilog
module vending_fsm (
    input clk,
    input reset,
    input coin_5,
    input coin_10,
    output reg give_item,
    output reg give_change
);

    parameter S0 = 2'b00;
    parameter S1 = 2'b01;
    parameter S2 = 2'b10;

    reg [1:0] state, next_state;

    always @(posedge clk or posedge reset) begin
        if (reset)
            state <= S0;
        else
            state <= next_state;
    end

    always @(*) begin
        next_state = state;
        give_item = 0;
        give_change = 0;

        case (state)
            S0: begin
                if (coin_5) begin
                    next_state = S1;
                end else if (coin_10) begin
                    next_state = S2;
                end
            end

            S1: begin
                if (coin_5) begin
                    next_state = S2;
                end else if (coin_10) begin
                    next_state = S0;
                    give_item = 1;
                end
            end

            S2: begin
                if (coin_5) begin
                    next_state = S0;
                    give_item = 1;
                end else if (coin_10) begin
                    next_state = S0;
                    give_item = 1;
                    give_change = 1;
                end
            end
        endcase
    end
endmodule
```

## 時序分析基礎

### 最大時脈頻率

```
f_max = 1 / (t_setup + t_clk→Q + t_comb_delay)
```

### 設定時間違規（Setup Violation）

資料在時脈邊緣後改變，來不及穩定。

### 保持時間違規（Hold Violation）

資料在時脈邊緣前改變，破壞了原有資料。

## 同步設計原則

1. **所有正反器使用同一時脈**
2. **輸入必須满足 setup/hold 時間**
3. **避免 combinational loop**
4. **使用時序約束描述設計意圖**

## 參考資料

- [序向邏輯電路](https://www.google.com/search?q=sequential+logic+circuit+tutorial)
- [正反器與暫存器](https://www.google.com/search?q=flip+flop+register+explained)
- [狀態機設計](https://www.google.com/search?q=state+machine+design+FPGA)