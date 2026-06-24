set -x
iverilog -o verilog_examples.vvp verilog_examples.v tb_verilog.v
vvp verilog_examples.vvp