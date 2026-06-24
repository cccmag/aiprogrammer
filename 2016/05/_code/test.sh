#!/bin/bash
# Test script for Programming Language Implementation examples

set -x

echo "=== Programming Language Implementation Test ==="
echo ""

echo "=== Memory Management Examples ==="
python3 memory/simple_alloc.py || echo "simple_alloc failed"
python3 memory/reference_count.py || echo "reference_count failed"
python3 memory/gc_simulation.py || echo "gc_simulation failed"

echo ""
echo "=== Virtual Machine Examples ==="
python3 vm/stack_vm.py || echo "stack_vm failed"
python3 vm/bytecode_gen.py || echo "bytecode_gen failed"

echo ""
echo "=== Threading Examples ==="
python3 threading/mutex_demo.py || echo "mutex_demo failed"
python3 threading/producer_consumer.py || echo "producer_consumer failed"

echo ""
echo "=== All tests completed ==="