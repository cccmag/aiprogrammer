# 網路設定與除錯

網路是 Linux 系統的重要組成部分，本章介紹網路設定和故障排除的方法。

---

## 基本網路概念

### OSI 層級

| 層級 | 功能 | 範例 |
|------|------|------|
| 應用層 | 網路服務 | HTTP, FTP |
| 傳輸層 | 可靠傳輸 | TCP, UDP |
| 網路層 | 路徑選擇 | IP, ICMP |
| 鏈路層 | 實體傳輸 | Ethernet |

### IP 位址

- **IPv4**：32 位元，如 192.168.1.1
- **IPv6**：128 位元，如 2001:db8::1

---

## 網路設定

### 傳統指令 (ifconfig)

```bash
# 顯示網路介面
ifconfig
ifconfig -a
ifconfig eth0

# 設定 IP
ifconfig eth0 192.168.1.100

# 設定子網路遮罩
ifconfig eth0 netmask 255.255.255.0

# 啟用/停用介面
ifconfig eth0 up
ifconfig eth0 down
```

### 新式指令 (ip)

```bash
# 顯示 IP 位址
ip addr show
ip addr

# 新增 IP
ip addr add 192.168.1.100/24 dev eth0

# 刪除 IP
ip addr del 192.168.1.100/24 dev eth0

# 顯示路由表
ip route show
ip route

# 新增路由
ip route add default via 192.168.1.1

# 顯示網路介面
ip link show
ip link set eth0 up
ip link set eth0 down
```

### DNS 設定

```bash
# /etc/resolv.conf
nameserver 8.8.8.8
nameserver 8.8.4.4

# 測試 DNS
nslookup example.com
dig example.com
```

---

## 網路測試

### ping

```bash
# 基本使用
ping google.com

# 指定次數
ping -c 4 google.com

# 指定間隔
ping -i 2 google.com

# 指定封包大小
ping -s 100 google.com
```

### traceroute

```bash
traceroute google.com
traceroute -n google.com    # 不解析主機名
```

### mtr

```bash
mtr google.com              # 結合 ping 和 traceroute
```

---

## 網路連線

### telnet

```bash
telnet google.com 80
```

### nc (netcat)

```bash
# 連接至埠
nc -zv google.com 80

# 監聽埠
nc -l -p 1234

# 傳送檔案
nc -l -p 1234 > received.txt
nc host 1234 < sent.txt
```

---

## 網路統計

### netstat

```bash
# 顯示所有連線
netstat -a

# 顯示 TCP 連線
netstat -at

# 顯示 UDP 連線
netstat -au

# 顯示監聽中的埠
netstat -ln

# 顯示程式關聯
netstat -tp

# 顯示網路介面統計
netstat -i

# 顯示路由表
netstat -r
```

### ss (socket statistics)

```bash
# 顯示 TCP 連線
ss -t

# 顯示監聽中的 sockets
ss -lt

# 顯示進程
ss -tp

# 顯示摘要
ss -s
```

---

## 防火牆

### iptables

```bash
# 顯示規則
sudo iptables -L -n

# 允許輸入
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT

# 封鎖 IP
sudo iptables -A INPUT -s 192.168.1.100 -j DROP

# 拒絕輸入
sudo iptables -A INPUT -j REJECT

# 儲存規則
sudo iptables-save > /etc/iptables/rules.v4

# 清除所有規則
sudo iptables -F
```

### ufw (Uncomplicated Firewall)

```bash
# 啟用
sudo ufw enable

# 停用
sudo ufw disable

# 允許連線
sudo ufw allow 80/tcp
sudo ufw allow http

# 拒絕連線
sudo ufw deny 23/tcp

# 刪除規則
sudo ufw delete allow 80/tcp

# 檢視狀態
sudo ufw status
```

---

## 網路工具

### curl

```bash
curl http://example.com
curl -X GET http://example.com/api
curl -d "param=value" http://example.com/api
curl -H "Content-Type: application/json" http://example.com/api
```

### wget

```bash
wget http://example.com/file.zip
wget -O output.html http://example.com
wget -c http://example.com/largefile.zip   # 繼續下載
```

### ssh

```bash
ssh user@host
ssh -p 2222 user@host
ssh -i key.pem user@host
```

---

## 網路診斷流程

1. **檢查本機網路**
   ```bash
   ip addr show
   ip route show
   ```

2. **檢查 DNS**
   ```bash
   nslookup example.com
   ```

3. **測試閘道**
   ```bash
   ping 192.168.1.1
   ```

4. **測試外部連線**
   ```bash
   ping 8.8.8.8
   ping google.com
   ```

5. **檢查埠**
   ```bash
   ss -ltn
   telnet host port
   ```

---

## 小結

網路故障排除需要系統性的方法，從本機設定到網路路徑逐步排查。

---

*作者：AI 程式人團隊*