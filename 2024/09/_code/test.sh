#!/bin/bash
set -x

cd "$(dirname "$0")"

echo "=== Run API Design Demo ==="
node api_design.js

echo ""
echo "=== Demo finished ==="
