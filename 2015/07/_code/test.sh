#!/bin/bash
set -x

cd /Users/Shared/ccc/magazine/aiprogrammer/2015/07/_code

echo "=== 執行 Git 工作流程範例 ==="
chmod +x git_workflow.sh
./git_workflow.sh

echo ""
echo "=== 執行 Git Python 範例 ==="
chmod +x git_python.py
python3 git_python.py

echo ""
echo "=== 所有 2015/07 測試完成 ==="