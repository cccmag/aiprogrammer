#!/bin/bash
set -x

cd /Users/Shared/ccc/magazine/aiprogrammer/2015/08/_code

echo "=== 執行系統資訊腳本 ==="
chmod +x system_info.py
python3 system_info.py

echo ""
echo "=== 執行程序管理腳本 ==="
chmod +x process_manager.py
python3 process_manager.py

echo ""
echo "=== 執行網路診斷腳本 ==="
chmod +x network_diag.py
python3 network_diag.py

echo ""
echo "=== 執行磁碟分析腳本 ==="
chmod +x disk_analysis.sh
./disk_analysis.sh

echo ""
echo "=== 所有 2015/08 測試完成 ==="