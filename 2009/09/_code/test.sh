#!/bin/bash
# Test script for MongoDB demo

cd "$(dirname "$0")"

echo "Running MiniDB Document Database Demo..."
echo ""

python3 mongodb_demo.py

echo ""
echo "Test complete!"