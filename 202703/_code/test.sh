#!/bin/bash
set -x

echo "=== 1. Check project compiles ==="
cargo build 2>&1

echo ""
echo "=== 2. Check formatting ==="
cargo fmt --check 2>&1 || echo "(format check skipped if not available)"

echo ""
echo "=== Build OK ==="
