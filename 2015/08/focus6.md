# 自動化腳本實踐

自動化是系統管理效率的關鍵，本章介紹如何建立可靠的自動化腳本。

---

## 自動化腳本原則

### 設計原則

1. **明確性**：每個腳本只做一件事
2. **可重複性**：同樣輸入產生同樣輸出
3. **可回溯性**：記錄執行情況
4. **錯誤處理**：遇到錯誤要正確處理
5. **文件化**：註解和 README

### 錯誤處理

```bash
#!/bin/bash
set -e  # 遇到錯誤就終止
set -u  # 使用未定義變數時終止
set -o pipefail  # 管線中任何命令失敗就終止

# 錯誤處理函數
error_exit() {
    echo "錯誤: $1" >&2
    exit 1
}

# 使用範例
if [ ! -f "$file" ]; then
    error_exit "檔案不存在: $file"
fi
```

---

## Cron 自動化

### Crontab 語法

```bash
# ┌───────────── 分鐘 (0 - 59)
# │ ┌───────────── 小時 (0 - 23)
# │ │ ┌───────────── 日 (1 - 31)
# │ │ │ ┌───────────── 月 (1 - 12)
# │ │ │ │ ┌───────────── 星期 (0 - 6) (0 是星期日)
# │ │ │ │ │
# │ │ │ │ │
# * * * * * command
```

### 實用範例

```bash
# 每天凌晨 2 點執行備份
0 2 * * * /opt/backup.sh >> /var/log/backup.log 2>&1

# 每週一凌晨 3 點執行
0 3 * * 1 /opt/weekly-cleanup.sh

# 每月的第一天凌晨 4 點執行
0 4 1 * * /opt/monthly-report.sh

# 每 5 分鐘執行
*/5 * * * * /opt/monitor.sh

# 工作日下午晚上 6 點執行
0 18 * * 1-5 /opt/daily-task.sh
```

### 環境問題

```bash
# 在 crontab 中設定環境
SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
MAILTO=admin@example.com

# 使用絕對路徑
0 2 * * * /usr/bin/python3 /opt/script.py
```

---

## Ansible 簡介

### 安裝

```bash
pip install ansible
```

### Inventory 檔案

```ini
[webservers]
web1.example.com
web2.example.com

[dbservers]
db1.example.com

[all:vars]
ansible_user=admin
```

### Playbook 範例

```yaml
---
- name: 部署 Web 伺服器
  hosts: webservers
  become: yes
  tasks:
    - name: 安裝 Nginx
      apt:
        name: nginx
        state: present
        update_cache: yes

    - name: 複製設定檔
      template:
        src: nginx.conf.j2
        dest: /etc/nginx/nginx.conf
      notify:
        - restart nginx

    - name: 啟動 Nginx
      service:
        name: nginx
        state: started

  handlers:
    - name: restart nginx
      service:
        name: nginx
        state: restarted
```

### 執行

```bash
# 測試執行
ansible-playbook --check playbook.yml

# 實際執行
ansible-playbook playbook.yml
```

---

## 部署腳本範例

### 簡單部署腳本

```bash
#!/bin/bash
# deploy.sh - 部署腳本

set -e

APP_DIR="/opt/myapp"
BACKUP_DIR="/opt/backups"
REPO_URL="https://github.com/user/myapp.git"
BRANCH="main"

echo "=== 開始部署 ==="
cd $APP_DIR

# 備份
timestamp=$(date +%Y%m%d_%H%M%S)
cp -r $APP_DIR $BACKUP_DIR/backup_$timestamp

# 提取更新
git fetch origin
git reset --hard origin/$BRANCH

# 安裝依賴
npm install

# 重啟服務
systemctl restart myapp

echo "=== 部署完成 ==="
```

### 資料庫遷移腳本

```bash
#!/bin/bash
# migrate.sh - 資料庫遷移腳本

set -e

DB_NAME="myapp"
DB_USER="admin"
BACKUP_FILE="/backup/db_$(date +%Y%m%d).sql"

echo "=== 開始資料庫遷移 ==="

# 備份
pg_dump -U $DB_USER $DB_NAME > $BACKUP_FILE
echo "備份已儲存: $BACKUP_FILE"

# 執行遷移
psql -U $DB_USER -d $DB_NAME < migrations/001.sql

echo "=== 遷移完成 ==="
```

---

## 監控腳本

### 磁碟空間監控

```bash
#!/bin/bash
# check_disk.sh - 磁碟空間監控

THRESHOLD=90
ALERT_EMAIL="admin@example.com"

USAGE=$(df -h / | tail -1 | awk '{print $5}' | sed 's/%//')

if [ $USAGE -gt $THRESHOLD ]; then
    echo "警告: 根目錄使用率達到 ${USAGE}%" | mail -s "磁碟空間警告" $ALERT_EMAIL
fi
```

### 程序監控

```bash
#!/bin/bash
# check_process.sh - 程序監控

PROCESS="nginx"
EMAIL="admin@example.com"

if ! pgrep -x "$PROCESS" > /dev/null; then
    echo "$PROCESS 未執行，正在啟動..."
    systemctl start $PROCESS
    echo "$PROCESS 已重啟" | mail -s "程序監控警告" $EMAIL
fi
```

---

## 日誌管理

### 日誌輪轉 (logrotate)

```bash
# /etc/logrotate.d/myapp
/var/log/myapp/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    postrotate
        systemctl reload myapp > /dev/null 2>&1 || true
    endscript
}
```

### 集中式日誌

```bash
# 使用 rsyslog
# /etc/rsyslog.d/myapp.conf
if $programname == 'myapp' then {
    action(type="omfile" file="/var/log/myapp.log")
}
```

---

## 小結

自動化腳本是系統管理效率的關鍵，從簡單的 Cron 工作到複雜的 Ansible Playbook，都能大幅減少重複性工作。

---

*作者：AI 程式人團隊*