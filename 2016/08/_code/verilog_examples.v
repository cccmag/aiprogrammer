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