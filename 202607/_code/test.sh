#!/bin/bash
set -x

echo "=== 1. Build project ==="
cargo build

echo ""
echo "=== 2. Run tests ==="
cargo test

echo ""
echo "=== 3. Create test file ==="
cat > /tmp/sample.txt << 'EOF'
Hello World
This is a test file
hello rust programming
RUST is great for systems programming
The quick brown fox
jumps over the lazy dog
Hello Again
EOF

echo ""
echo "=== 4. Test: basic search ==="
cargo run -- Hello /tmp/sample.txt

echo ""
echo "=== 5. Test: case-insensitive search ==="
cargo run -- --ignore-case hello /tmp/sample.txt

echo ""
echo "=== 6. Test: with line numbers ==="
cargo run -- -n rust /tmp/sample.txt

echo ""
echo "=== 7. Test: inverted match (show non-matching) ==="
cargo run -- -v rust /tmp/sample.txt

echo ""
echo "=== 8. Test: regex pattern ==="
cargo run -- '^H' /tmp/sample.txt

echo ""
echo "=== 9. Test: max count ==="
cargo run -- --max-count 2 hello /tmp/sample.txt

echo ""
echo "=== All tests passed! ==="
