#!/bin/bash
# Test script for year review

cd "$(dirname "$0")"

echo "Running 2009 Technology Year in Review..."
echo ""

python3 year_review.py

echo ""
echo "Test complete!"