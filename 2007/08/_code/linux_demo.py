#!/usr/bin/env python3
"""
Linux 系統管理概念展示
展示常見的 Linux 管理操作
"""

def demo():
    print("=" * 50)
    print("Linux 系統管理概念展示")
    print("=" * 50)

    print("\n--- 檔案系統概念 ---")
    print("""
Linux 檔案系統結構：
/           # 根目錄
├── bin/    # 執行檔
├── etc/    # 設定檔
├── home/   # 使用者目錄
├── tmp/    # 暫存檔
├── var/    # 變動資料
├── usr/    # 使用者程式
└── root/   # 系統管理員目錄
""")

    print("\n--- 程序管理概念 ---")
    print("""
程序狀態：
R - 執行中
S - 睡眠中
D - 不可中斷的睡眠
Z - 殭屍程序
T - 停止

常用指令：
ps aux      # 顯示所有行程
top         # 互動式行程檢視
kill PID    # 終止程序
nice -n 10 cmd  # 以指定優先權執行
""")

    print("\n--- 網路設定概念 ---")
    print("""
網路介面：
eth0        # 第一張網卡
wlan0       # 無線網卡
lo          # 迴環介面

常用指令：
ifconfig    # 設定/顯示網路介面
ip addr     # 新一代網路工具
route       # 路由表
iptables    # 防火牆
""")

    print("\n--- 套件管理概念 ---")
    print("""
Debian/Ubuntu (APT):
apt-get update      # 更新套件庫
apt-get install pkg # 安裝套件
apt-cache search    # 搜尋套件

Red Hat/CentOS (YUM):
yum update          # 更新套件
yum install pkg     # 安裝套件
yum search          # 搜尋套件

Gentoo (Portage):
emerge -av pkg      # 編譯安裝
""")

    print("\n" + "=" * 50)

if __name__ == "__main__":
    demo()