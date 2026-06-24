# 程序管理與監控

程序是 Linux 系統運行的核心單元，學會管理程序是系統管理的基本技能。

---

## 基本概念

### 程序結構

```
程序 (Process)
├── PID (Process ID)
├── PPID (Parent PID)
├── 狀態 (State)
├── 記憶體映射
└── 檔案描述符
```

### 程序狀態

| 狀態 | 說明 |
|------|------|
| R | 執行中或可執行 |
| S | 可中斷的睡眠 |
| D | 不可中斷的等待 |
| Z | 殭屍程序 |
| T | 暫停或追蹤 |

---

## 檢視程序

### ps 命令

```bash
# 基本用法
ps

# 顯示所有程序
ps aux

# 顯示樹狀結構
ps -ef --forest

# 顯示程序樹
pstree

# 特定使用者的程序
ps -u username

# 格式化輸出
ps -eo pid,ppid,user,comm,%cpu,%mem
```

### top 命令

```bash
# 互動式介面
top

# 常見快捷鍵
# M - 按記憶體排序
# P - 按 CPU 排序
# q - 退出
# k - 終止程序
# r - 調整優先權

# 批次模式
top -b -n 5 > top_output.txt

# 只顯示特定程序
top -p 1234
```

### 其他工具

```bash
# 即時程序檢視
htop

# 顯示程序樹
pstree -a

# 顯示執行中的程序
running
```

---

## 管理程序

### 啟動程序

```bash
# 前台執行
./myapp

# 後台執行
./myapp &

# 脫離終端機執行
nohup ./myapp > output.log 2>&1 &
```

### 終止程序

```bash
# 優雅終止
kill -TERM 1234

# 強制終止
kill -KILL 1234

# 依名稱終止
killall myapp

# 依名稱終止（更温和）
pkill myapp

# 查找並終止
ps aux | grep myapp | grep -v grep | awk '{print $2}' | xargs kill
```

### 信號

| 信號 | 數值 | 說明 |
|------|------|------|
| SIGHUP | 1 | 掛斷 |
| SIGINT | 2 | 中斷 (Ctrl+C) |
| SIGTERM | 15 | 優雅終止 |
| SIGKILL | 9 | 強制終止 |

---

## 程序優先權

```bash
# 查看優先權
ps -eo pid,ni,comm

# 調整優先權（範圍 -20 到 19）
nice -n 10 ./myapp

# 調整執行中程序的優先權
renice -n 5 -p 1234
renice -n -5 -u username
```

---

## systemd

### 基本指令

```bash
# 檢視服務狀態
systemctl status nginx

# 啟動服務
sudo systemctl start nginx

# 停止服務
sudo systemctl stop nginx

# 重新啟動
sudo systemctl restart nginx

# 重新載入設定
sudo systemctl reload nginx

# 啟用開機啟動
sudo systemctl enable nginx

# 停用開機啟動
sudo systemctl disable nginx
```

### 服務單元檔案

```ini
[Unit]
Description=My Application
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/myapp
Restart=always

[Install]
WantedBy=multi-user.target
```

### 檢視日誌

```bash
# 查看服務日誌
journalctl -u nginx

# 即時檢視
journalctl -f

# 查看開機日誌
journalctl -b

# 查看錯誤日誌
journalctl -p err
```

---

## 傳統 SysV init

```bash
# 啟動服務
/etc/init.d/nginx start

# 停止服務
/etc/init.d/nginx stop

# 重新啟動
/etc/init.d/nginx restart

# 設定開機啟動
chkconfig nginx on
```

---

## Cron 排程

### 基本語法

```
分 時 日 月 星期 命令
*   *  *  *  *     command
```

### 範例

```bash
# 每天早上 3 點執行
0 3 * * * /backup.sh

# 每小時執行
0 * * * * /hourly.sh

# 每週一執行
0 0 * * 1 /weekly.sh

# 每月的第一天執行
0 0 1 * * /monthly.sh
```

### 管理 Crontab

```bash
# 編輯 crontab
crontab -e

# 查看 crontab
crontab -l

# 刪除 crontab
crontab -r
```

---

## 小結

程序管理是 Linux 系統管理的核心技能，從基本的 ps、kill 到現代的 systemd，都需要掌握。

---

*作者：AI 程式人團隊*