# 網路除錯工具

網路問題的排查需要一系列工具來診斷和修復。

---

## 基本工具

### ping

測試網路連通性。

```bash
# 基本使用
ping google.com

# 指定次數
ping -c 4 google.com

# 指定封包大小
ping -s 100 google.com

# 持續 ping 直到 Ctrl+C
ping -c 1000 -i 0.2 google.com
```

### traceroute / tracepath

追蹤封包經過的路徑。

```bash
# Linux
traceroute google.com

# macOS/Windows
tracert google.com

# 使用 tracepath（不需要 root）
tracepath google.com
```

### mtr

結合 ping 和 traceroute。

```bash
# 即時顯示路由
mtr google.com

# 生成報告
mtr --report google.com
```

---

## 連接埠掃描

### telnet

```bash
# 測試連接
telnet example.com 80

# 測試 SMTP
telnet mail.example.com 25
```

### nc (netcat)

```bash
# 連接測試
nc -zv example.com 80

# 監聽連接埠
nc -l -p 8080

# 傳送檔案
nc -l -p 8080 > received.txt
nc host 8080 < sent.txt

# 掃描連接埠
nc -zv target 20-30
```

### nmap

```bash
# 基本掃描
nmap target.com

# 掃描常見連接埠
nmap -F target.com

# 作業系統偵測
nmap -O target.com

# 服務版本偵測
nmap -sV target.com

# 完整掃描
nmap -A target.com
```

---

## 封包分析

### tcpdump

```bash
# 監控 eth0 上的流量
sudo tcpdump -i eth0

# 儲存為 pcap 檔案
sudo tcpdump -i eth0 -w capture.pcap

# 讀取 pcap 檔案
tcpdump -r capture.pcap

# 只抓 HTTP 流量
sudo tcpdump -i eth0 port 80

# 只抓特定 IP
sudo tcpdump -i eth0 host 192.168.1.1
```

### tshark (Wireshark 命令列)

```bash
# 即時顯示
tshark -i eth0

# 只顯示 HTTP
tshark -i eth0 -Y http

# 儲存為 pcap
tshark -i eth0 -w capture.pcap
```

---

## 網路介面工具

### ifconfig / ip

```bash
# 顯示介面
ifconfig
ip addr show

# 啟用/停用介面
ifconfig eth0 up
ifconfig eth0 down
ip link set eth0 up
ip link set eth0 down

# 設定 IP
ifconfig eth0 192.168.1.100 netmask 255.255.255.0
ip addr add 192.168.1.100/24 dev eth0
```

### ethtool

```bash
# 查看介面資訊
ethtool eth0

# 查看連接狀態
ethtool -S eth0

# 設定速度
ethtool -s eth0 speed 1000 duplex full
```

---

## DNS 工具

### nslookup

```bash
nslookup example.com
nslookup -type=MX example.com
nslookup -type=TXT example.com
```

### dig

```bash
# 基本查詢
dig example.com

# 查詢特定記錄
dig example.com A
dig example.com AAAA
dig example.com MX

# 使用特定 DNS 伺服器
dig @8.8.8.8 example.com

# 反向查詢
dig -x 8.8.8.8

# 追蹤查詢過程
dig +trace example.com
```

### drill

```bash
drill example.com
drill -T example.com  # 追蹤
drill -D example.com   # DNSSEC 驗證
```

---

## 頻寬測試

### iperf

```bash
# 伺服器端
iperf -s

# 客戶端端
iperf -c server_ip

# 雙向測試
iperf -c server_ip -d
```

### speedtest-cli

```bash
speedtest-cli
speedtest-cli --simple
```

---

## 常用組合

### 診斷網頁無法存取

```bash
# 1. ping 測試
ping -c 4 example.com

# 2. DNS 解析
dig example.com
nslookup example.com

# 3. 路由追蹤
traceroute example.com

# 4. 連接埠測試
nc -zv example.com 80
nc -zv example.com 443

# 5. 封包追蹤
sudo tcpdump -i eth0 host example.com
```

### 診斷網路延遲

```bash
# 1. 本地閘道
ping 192.168.1.1

# 2. DNS 延遲
time dig example.com

# 3. HTTP 回應時間
curl -w "\nTime: %{time_total}s\n" -o /dev/null -s http://example.com

# 4. MTR 追蹤
mtr example.com
```

[搜尋 network troubleshooting commands](https://www.google.com/search?q=network+troubleshooting+commands+linux)

---

## 小結

掌握這些工具能幫助你快速診斷和解決網路問題。

---

*作者：AI 程式人團隊*