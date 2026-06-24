`timescale 1ns/1ps

module tb_basic_gates;
    reg a, b;
    wire y_and, y_or, y_not, y_xor, y_nand, y_nor;

    basic_gates uut (.a(a), .b(b), .y_and(y_and), .y_or(y_or),
                     .y_not(y_not), .y_xor(y_xor), .y_nand(y_nand), .y_nor(y_nor));

    initial begin
        $dumpfile("tb_basic_gates.vcd");
        $dumpvars(0, tb_basic_gates);

        $display("=== Testing Basic Gates ===");
        a = 0; b = 0; #10;
        $display("a=%b, b=%b -> AND=%b, OR=%b, NOT=%b, XOR=%b, NAND=%b, NOR=%b",
                 a, b, y_and, y_or, y_not, y_xor, y_nand, y_nor);

        a = 0; b = 1; #10;
        $display("a=%b, b=%b -> AND=%b, OR=%b, NOT=%b, XOR=%b, NAND=%b, NOR=%b",
                 a, b, y_and, y_or, y_not, y_xor, y_nand, y_nor);

        a = 1; b = 0; #10;
        $display("a=%b, b=%b -> AND=%b, OR=%b, NOT=%b, XOR=%b, NAND=%b, NOR=%b",
                 a, b, y_and, y_or, y_not, y_xor, y_nand, y_nor);

        a = 1; b = 1; #10;
        $display("a=%b, b=%b -> AND=%b, OR=%b, NOT=%b, XOR=%b, NAND=%b, NOR=%b",
                 a, b, y_and, y_or, y_not, y_xor, y_nand, y_nor);

        #10 $finish;
    end
endmodule


module tb_mux;
    reg sel;
    reg [1:0] d;
    wire y;

    mux2to1 uut (.sel(sel), .d(d), .y(y));

    initial begin
        $dumpfile("tb_mux.vcd");
        $dumpvars(0, tb_mux);

        $display("=== Testing 2:1 Multiplexer ===");
        sel = 0; d = 2'b01; #10;
        $display("sel=%b, d=%b -> y=%b", sel, d, y);

        sel = 1; d = 2'b10; #10;
        $display("sel=%b, d=%b -> y=%b", sel, d, y);

        #10 $finish;
    end
endmodule


module tb_decoder;
    reg [1:0] in;
    wire [3:0] out;

    decoder2to4 uut (.in(in), .out(out));

    initial begin
        $dumpfile("tb_decoder.vcd");
        $dumpvars(0, tb_decoder);

        $display("=== Testing 2:4 Decoder ===");
        in = 2'b00; #10;
        $display("in=%b -> out=%b", in, out);

        in = 2'b01; #10;
        $display("in=%b -> out=%b", in, out);

        in = 2'b10; #10;
        $display("in=%b -> out=%b", in, out);

        in = 2'b11; #10;
        $display("in=%b -> out=%b", in, out);

        #10 $finish;
    end
endmodule


module tb_dff;
    reg clk, reset, d;
    wire q;

    d_flip_flop uut (.clk(clk), .reset(reset), .d(d), .q(q));

    always #5 clk = ~clk;

    initial begin
        $dumpfile("tb_dff.vcd");
        $dumpvars(0, tb_dff);

        clk = 0;
        reset = 1;
        d = 0;

        #10 reset = 0;
        #10 d = 1;
        #10 d = 0;
        #10 d = 1;
        #10 d = 0;

        #50 $finish;
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

        $display("=== Testing 8-bit Counter ===");
        clk = 0;
        reset = 1;

        #10 reset = 0;
        #10 $display("count=%d", count);
        #10 $display("count=%d", count);
        #10 $display("count=%d", count);
        #10 $display("count=%d", count);

        #100 $finish;
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

        $display("=== Testing FSM ===");

        clk = 0;
        reset = 1;
        coin = 0;

        #10 reset = 0;
        #10 $display("state=S0, coin=%b, item=%b, change=%b", coin, item, change);

        coin = 1;
        #10 coin = 0;
        #10 $display("state=S1, coin=%b, item=%b, change=%b", coin, item, change);

        coin = 1;
        #10 coin = 0;
        #10 $display("state=S2, coin=%b, item=%b, change=%b", coin, item, change);

        #50 $finish;
    end
endmodule


module tb_adder;
    reg [3:0] a, b;
    wire [4:0] sum;

    adder4bit uut (.a(a), .b(b), .sum(sum));

    initial begin
        $dumpfile("tb_adder.vcd");
        $dumpvars(0, tb_adder);

        $display("=== Testing 4-bit Adder ===");
        a = 4'd5; b = 4'd3; #10;
        $display("%d + %d = %d", a, b, sum);

        a = 4'd15; b = 4'd1; #10;
        $display("%d + %d = %d", a, b, sum);

        a = 4'd8; b = 4'd8; #10;
        $display("%d + %d = %d", a, b, sum);

        #10 $finish;
    end
endmodule