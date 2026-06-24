# 系統安全與權限

系統安全是 Linux 管理的重要課題，本章介紹基本的安全設定和使用者管理。

---

## 使用者管理

### 新增使用者

```bash
# 基本新增
useradd username

# 完整設定
useradd -m -s /bin/bash -c "User Comment" username

# 選項說明
# -m: 建立家目錄
# -s: 設定 shell
# -c: 註釋
```

### 刪除使用者

```bash
userdel username
userdel -r username  # 刪除家目錄
```

### 修改使用者

```bash
# 改密碼
passwd username

# 改 shell
usermod -s /bin/zsh username

# 加入群組
usermod -aG sudo username
```

### 鎖定帳號

```bash
# 鎖定
usermod -L username

# 解鎖
usermod -U username
```

---

## 群組管理

```bash
# 新增群組
groupadd developers

# 刪除群組
groupdel developers

# 修改群組
groupmod -n newname oldname

# 查看群組成員
groups username

# 顯示使用者所屬群組
id username
```

---

## sudo 設定

### 安裝 sudo

```bash
apt-get install sudo
```

### 設定檔 (/etc/sudoers)

```bash
# 給予使用者完整權限
username ALL=(ALL) ALL

# 免密碼 sudo
username ALL=(ALL) NOPASSWD: ALL

# 給予群組權限
%sudo ALL=(ALL) ALL

# 特定命令
username ALL=(ALL) /usr/bin/systemctl restart nginx
```

### 使用 visudo

```bash
# 安全編輯 sudoers 檔案
visudo
```

---

## 檔案權限安全性

### SUID/SGID 風險

```bash
# 查找所有 SUID 檔案
find / -perm +4000 -type f 2>/dev/null

# 查找所有 SGID 檔案
find / -perm +2000 -type f 2>/dev/null

# 移除危險的 SUID
chmod -s /usr/bin/passwd  # 不建議，會影響功能
```

### 全域可寫檔案

```bash
# 查找全域可寫檔案
find / -perm -002 -type f 2>/dev/null

# 查找全域可寫目錄
find / -perm -002 -type d 2>/dev/null
```

### 重要檔案權限

```bash
# /etc/shadow (只讀給 root)
chmod 400 /etc/shadow

# /etc/passwd (可讀)
chmod 644 /etc/passwd

# /etc/sudoers (只讀)
chmod 440 /etc/sudoers

# SSH 金鑰
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_rsa
chmod 644 ~/.ssh/id_rsa.pub
```

---

## SELinux

### 狀態

```bash
# 查看狀態
getenforce

# 暫時停用
setenforce 0

# 永久設定 (/etc/selinux/config)
SELINUX=disabled
```

### 上下文

```bash
# 查看檔案安全上下文
ls -Z /var/www/html

# 改變上下文
chcon -R -t httpd_sys_content_t /var/www/html

# 恢復預設上下文
restorecon -R /var/www/html
```

---

## 防火墙

### iptables 基本設定

```bash
# 預設策略
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

# 允許已建立的連線
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# 允許本地迴圈
iptables -A INPUT -i lo -j ACCEPT

# 允許 SSH
iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# 允許 HTTP/HTTPS
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j ACCEPT
```

---

## 系統安全檢查

### 檢查開機服務

```bash
# SysV init
chkconfig --list

# systemd
systemctl list-unit-files --type=service | grep enabled
```

### 檢查異常登入

```bash
# 查看最近登入
last
lastlog

# 查看失敗的登入
faillog
```

### 檢查監聽中的埠

```bash
# 確認只有必要的服務在監聽
ss -ltn
```

---

## 安全性更新

### 自動更新

```bash
# Ubuntu/Debian
apt-get install unattended-upgrades
dpkg-reconfigure unattended-upgrades

# CentOS/RHEL
yum install yum-cron
systemctl enable yum-cron
```

---

## 小結

系統安全需要持續關注，從使用者權限到網路存取，每個環節都需要注意。

---

*作者：AI 程式人團隊*