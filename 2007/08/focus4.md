# 主題四：資料中心與 Linux

## 伺服器作業系統霸主

2007 年，Linux 在資料中心市場已經確立了霸主地位。從網頁伺服器到資料庫、從雲端運算到高效能計算，Linux 執行著世界上大多數的關鍵任務基礎設施。

## Linux 在伺服器市場的優勢

### 為什麼資料中心選擇 Linux

```bash
# Linux 的核心優勢

1. 穩定性
   - 可連續運作數年不需要重啟
   - 成熟的錯誤處理機制
   - 廣泛的社群和企業支援

2. 效能
   - 可高度最佳化
   - 低資源消耗
   - 優秀的行程和記憶體管理

3. 安全性
   - 及時的安全更新
   - 嚴格的權限模型
   - SeLinux 等進階安全機制

4. 彈性
   - 可根據需求裁剪
   - 支援從嵌入式到超級電腦
   - 廣泛的硬體支援
```

### 市場佔有率

2007 年的伺服器作業系統市場：

```markdown
市場佔有率（估計）：
- Linux:         ~30%
- Windows Server: ~40%
- Unix (AIX, HP-UX, Solaris): ~15%
- 其他:           ~15%

成長趨勢：Linux 持續上升，Unix 下降
```

## Web 伺服器

### Apache HTTP Server

2007 年最廣泛使用的網頁伺服器：

```bash
# 安裝
sudo apt-get install apache2

# 主要設定檔
/etc/apache2/apache2.conf    # 主設定檔
/etc/apache2/sites-available/ # 站台設定
/etc/apache2/mods-available/  # 模組設定

# 常用指令
sudo apache2ctl start
sudo apache2ctl stop
sudo apache2ctl restart
sudo apache2ctl graceful
```

### Nginx 的興起

2007 年 Nginx 開始受到關注：

```nginx
# Nginx 設定範例
worker_processes 4;
error_log /var/log/nginx/error.log;

events {
    worker_connections 1024;
}

http {
    server {
        listen 80;
        server_name example.com;
        root /var/www/html;

        location / {
            index index.html index.htm;
        }

        location /api/ {
            proxy_pass http://localhost:8000;
        }
    }
}
```

## 資料庫伺服器

### MySQL

2007 年最流行的開源資料庫：

```bash
# 安裝
sudo apt-get install mysql-server

# 設定檔
/etc/mysql/my.cnf

# 重要參數
# max_connections=100
# innodb_buffer_pool_size=1G
# query_cache_size=64M
```

### PostgreSQL

功能豐富的物件關聯式資料庫：

```bash
# 安裝
sudo apt-get install postgresql

# 設定檔
/etc/postgresql/8.2/main/postgresql.conf
/etc/postgresql/8.2/main/pg_hba.conf

# 服務管理
sudo service postgresql start
sudo service postgresql stop
```

## 雲端運算

### Amazon EC2

2007 年 Amazon EC2 已經正式商用：

```bash
# EC2 命令列工具
ec2-describe-instances      # 列出執行個體
ec2-run-instances ami-xxxx    # 啟動執行個體
ec2-terminate-instances i-xxxx # 終止執行個體

# 常用 AMI
# Amazon Linux AMI
# Ubuntu Server
# Red Hat Enterprise Linux
```

### 虛擬化技術

```bash
# Xen
# 開源虛擬化解決方案
# 支援半虛擬化和全虛擬化
xm create vm.cfg
xm list
xm shutdown vm

# KVM
# 全虛擬化支援
# 整合到 Linux 核心
kvm -m 512 -cdrom image.iso
```

### 雲端儲存

```bash
# Amazon S3
# Simple Storage Service
s3cmd put file.txt s3://mybucket/
s3cmd get s3://mybucket/file.txt

# 開源替代方案
# OpenStack Swift
# Ceph
```

## 高效能計算 (HPC)

### 叢集運算

```bash
# MPI (Message Passing Interface)
# 用於平行計算
mpirun -np 4 ./parallel_program

# PBS (Portable Batch System)
# 工作排程器
qsub job_script.sh
qstat -a
qdel job_id

# Condor
# 工作站叢集管理
condor_submit job.submit
condor_q
```

### TOP500 超級電腦

```bash
# 2007 年 6 月 TOP500：
# Linux 佔據了大多數位置

作業系統分布：
- Linux: ~85%
- Unix: ~14%
- 其他: ~1%

# 知名超級電腦
# IBM BlueGene/L (LLNL)
# Crimson (IBM)
```

## 負載平衡和高可用性

###負載平衡

```bash
# LVS (Linux Virtual Server)
ipvsadm -A -t 192.168.1.100:80 -s rr
ipvsadm -a -t 192.168.1.100:80 -r 192.168.1.10 -m
ipvsadm -a -t 192.168.1.100:80 -r 192.168.1.11 -m

# HAProxy
# 應用層負載平衡
haproxy -f haproxy.cfg
```

### 高可用性

```bash
# Heartbeat
# 監控和故障轉移
ha-log | less
ha-admin show nodes

# Corosync + Pacemaker
# 企業級高可用性解決方案
crm_mon -1
crm configure show
```

## 系統監控

### 監控工具

```bash
# Nagios
# 企業級監控
# 監控主機、服務、網路

# Munin
# 效能監控和圖表

# Cacti
# 基於 RRDtool 的監控

# Ganglia
# HPC 叢集監控
```

## 結語

Linux 在資料中心的霸主地位並非偶然。其穩定性、效能、安全性和彈性使其成為執行關鍵任務應用的理想選擇。從小型網站到超級電腦，從傳統資料庫到雲端運算，Linux 繼續定義著現代資料中心的標準。

---

*延伸閱讀：*
- [Linux 伺服器管理](https://developers.google.com/search/?q=linux+server+administration)
- [雲端運算平台](https://developers.google.com/search/?q=cloud+computing+platforms)