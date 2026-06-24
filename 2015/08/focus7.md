# 系統監控工具

系統監控是確保服務可用性的關鍵，本章介紹常用的監控工具和方法。

---

## 基礎監控

### top

```bash
# 基本使用
top

# 常用快捷鍵
# M - 按記憶體排序
# P - 按 CPU 排序
# 1 - 顯示每個 CPU
# k - 終止程序
# q - 退出
```

### htop

```bash
# 安裝
sudo apt-get install htop

# 互動式功能
htop
# F2 - 設定
# F3 - 搜尋
# F4 - 過濾
```

---

## 程序監控

### ps

```bash
# 顯示所有程序
ps aux

# 顯示樹狀結構
ps -ef --forest

# 即時顯示
watch -n 1 'ps aux | grep python'

# 顯示程序數
ps -eLf | wc -l
```

### pgrep

```bash
# 依名稱查找程序
pgrep -a python

# 顯示進程樹
pgrep -f "python script.py" | xargs pstree -p
```

---

## 資源使用

### CPU

```bash
# mpstat
mpstat -P ALL

# vmstat
vmstat 1 5

# iostat (需要 sysstat)
iostat -x 1
```

### 記憶體

```bash
# free
free -h

# vmstat
vmstat -s
```

### 磁碟 I/O

```bash
# iostat
iostat -x 2

# iotop (需要 root)
sudo iotop

# df
df -h
```

---

## 網路監控

### iftop

```bash
# 安裝
sudo apt-get install iftop

# 監控網路流量
sudo iftop

# 監控特定介面
sudo iftop -i eth0
```

### nethogs

```bash
# 安裝
sudo apt-get install nethogs

# 監控程序網路使用
sudo nethogs
```

### bmon

```bash
# 監控頻寬
bmon
```

---

## 專業監控工具

### Nagios

系統和網路監控的標準工具。

```bash
# 安裝
sudo apt-get install nagios3

# 設定檔
/etc/nagios3/
/etc/nagios3/nagios.cfg
/etc/nagios3/objects/contacts.cfg
```

設定監控主機：

```bash
# /etc/nagios3/conf.d/host.cfg
define host {
    use                     generic-host
    host_name               webserver
    address                 192.168.1.100
    check_command           check-host-alive
}
```

[搜尋 Nagios getting started](https://www.google.com/search?q=Nagios+getting+started)

---

### Zabbix

企業級監控解決方案。

```bash
# 安裝 Zabbix repository
wget http://repo.zabbix.com/zabbix/3.0/ubuntu/pool/main/z/zabbix/zabbix-release_3.0-1+trusty_all.deb
sudo dpkg -i zabbix-release_3.0-1+trusty_all.deb
sudo apt-get update
sudo apt-get install zabbix-server-mysql zabbix-frontend-php
```

[搜尋 Zabbix tutorial](https://www.google.com/search?q=Zabbix+tutorial)

---

### Prometheus + Grafana

現代化的監控和視覺化組合。

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'node'
    static_configs:
      - targets: ['localhost:9100']
```

```bash
# 啟動 Prometheus
./prometheus

# Grafana 安裝
sudo apt-get install -y grafana
sudo systemctl start grafana-server
```

[搜尋 Prometheus quick start](https://www.google.com/search?q=Prometheus+quick+start)

---

## 簡單監控腳本

```bash
#!/bin/bash
# system_monitor.sh - 簡單系統監控

echo "=== 系統監控報告 ==="
echo "時間: $(date)"
echo ""

echo "=== CPU 使用率 ==="
top -bn1 | grep "Cpu(s)" | awk '{print "使用率: " $2 "%"}'
echo ""

echo "=== 記憶體使用 ==="
free -h | awk '/^Mem:/ {print "總計: " $2 ", 使用: " $3 ", 可用: " $7}'
echo ""

echo "=== 磁碟空間 ==="
df -h / | tail -1 | awk '{print "使用率: " $5 " (" $3 "/" $2 ")"}'
echo ""

echo "=== 網路連線 ==="
ss -s | head -4
echo ""

echo "=== Top 5 程序 ==="
ps aux --sort=-%cpu | head -6 | tail -5
```

---

## 小結

有效的系統監控能幫助你及時發現問題並快速回應。

---

*作者：AI 程式人團隊*