#!/bin/bash
set -x

echo "=== Mini Transformer Demo ==="
python3 transformer.py 2>&1

echo ""
echo "=== Mini RAG Demo ==="
python3 rag.py 2>&1

echo ""
echo "=== All demos completed! ==="
