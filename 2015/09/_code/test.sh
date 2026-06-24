#!/bin/bash
set -x

cd /Users/Shared/ccc/magazine/aiprogrammer/2015/09/_code

echo "=== 執行 HTTP 客戶端 ==="
chmod +x http_client.py
python3 http_client.py

echo ""
echo "=== 執行 DNS 客戶端 ==="
chmod +x dns_client.py
python3 dns_client.py

echo ""
echo "=== 執行 TCP Echo 客戶端 ==="
chmod +x tcp_echo.py
echo "test message" | timeout 3 python3 tcp_echo.py client || echo "TCP 測試完成"

echo ""
echo "=== 執行 UDP Echo 客戶端 ==="
chmod +x udp_echo.py
timeout 3 python3 udp_echo.py client || echo "UDP 測試完成"

echo ""
echo "=== 所有 2015/09 測試完成 ==="