#!/bin/bash
# disk_analysis.sh - 磁碟使用分析

set -x

echo "=== 磁碟使用分析 ==="
echo ""

echo "【磁碟總覽】"
df -h

echo ""
echo "【目錄大小排名 (前10)】"
du -ah / 2>/dev/null | sort -rh | head -10

echo ""
echo "【大型檔案 (大於100MB)】"
find / -type f -size +100M -exec ls -lh {} \; 2>/dev/null | head -10

echo ""
echo "【磁碟 I/O 統計】"
if command -v iostat &> /dev/null; then
    iostat -x 1 1
else
    echo "iostat 未安裝"
fi

echo ""
echo "分析完成"