#!/bin/bash
# Test script for functional programming examples

set -x

echo "=== Functional Programming Examples Test ==="
echo ""

echo "=== Python Functional Examples ==="
python3 python/functional.py || echo "Python functional failed"
python3 python/closures.py || echo "Python closures failed"
python3 python/memoization.py || echo "Python memoization failed"
python3 python/higher_order.py || echo "Python higher order failed"

echo ""
echo "=== All tests completed ==="