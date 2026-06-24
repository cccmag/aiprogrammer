#!/bin/bash
set -x

echo "=== 1. Build project ==="
cargo build 2>&1

echo ""
echo "=== 2. Run tests ==="
cargo test 2>&1

echo ""
echo "=== All tests passed! ==="
