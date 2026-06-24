# 行程管理與系統監控

## 行程的概念

行程 (Process) 是正在執行的程式實例。每個行程有唯一的 PID (Process ID)，包含程式碼、資料、堆疊和執行狀態。

```
行程狀態：
R (Running)    執行中或可執行
S (Sleeping)   休眠中 (等待事件)
D (Uninterruptible) 不可中斷休眠
Z (Zombie)     殭屍行程 (已終止但父行程未回收)
T (Stopped)    已停止
```

## ps：行程快照

`ps` 是最基本的行程檢視工具，提供當前瞬間的行程快照。

```bash
ps aux           # BSD 風格，顯示所有行程
ps -ef           # 標準風格
ps aux --sort=-%mem  # 依記憶體使用排序
ps aux | grep python  # 搜尋特定行程
```

### ps 輸出欄位說明

```
USER   PID  %CPU %MEM    VSZ   RSS  COMMAND
root     1   0.0  0.1 170088 10348  /sbin/init
```

- **PID**: 行程 ID
- **%CPU**: CPU 使用率
- **%MEM**: 記憶體使用率
- **VSZ**: 虛擬記憶體大小 (KB)
- **RSS**: 實際記憶體大小 (KB)

## top 與 htop：即時監控

### top

```bash
top                   # 即時行程檢視
top -u alice          # 只看特定使用者
top -p 1234,5678      # 只看特定 PID
```

按下 `h` 可以查看互動指令：`k` 終止行程、`r` 修改優先權、`q` 離開。

### htop

`htop` 是 `top` 的現代化替代品，提供彩色輸出、滑鼠支援和更直觀的介面。

```python
# Python 模擬 ps aux
import subprocess

def get_processes():
    result = subprocess.run(["ps", "aux"], capture_output=True, text=True)
    lines = result.stdout.strip().split("\n")
    processes = []
    for line in lines[1:]:  # 跳過標題行
        parts = line.split(None, 10)
        if len(parts) >= 11:
            processes.append({
                "user": parts[0], "pid": int(parts[1]),
                "cpu": float(parts[2]), "mem": float(parts[3]),
                "command": parts[10],
            })
    return processes

procs = get_processes()
print(f"目前有 {len(procs)} 個行程")
top_cpu = sorted(procs, key=lambda p: p["cpu"], reverse=True)[:3]
for p in top_cpu:
    print(f"  {p['pid']:>6}  {p['cpu']:>5.1f}%  {p['command'][:50]}")
```

## kill：終止行程

```bash
kill 1234              # 終止 PID 1234
kill -9 1234           # 強制終止 (SIGKILL)
kill -15 1234          # 優雅終止 (SIGTERM)
kill -HUP 1234         # 重新載入設定 (SIGHUP)
killall nginx          # 終止所有 nginx 行程
pkill -u alice         # 終止某使用者的行程
```

## systemd：現代服務管理

```bash
systemctl start nginx      # 啟動服務
systemctl stop nginx       # 停止服務
systemctl restart nginx    # 重啟服務
systemctl status nginx     # 檢視狀態
systemctl enable nginx     # 設定開機啟動
systemctl disable nginx    # 取消開機啟動
journalctl -u nginx        # 檢視服務日誌
```

## 系統監控工具

| 工具 | 用途 | 範例 |
|------|------|------|
| `free -h` | 記憶體使用 | 檢視 RAM/swap |
| `df -h` | 磁碟空間 | 檢視分割區使用率 |
| `du -sh *` | 目錄大小 | 計算各目錄佔用空間 |
| `iostat` | I/O 效能 | 磁碟讀寫吞吐量 |
| `netstat -tlnp` | 網路連線 | 監聽中的埠號 |
| `ss -tuln` | 現代版 netstat | 顯示 socket 狀態 |
| `uptime` | 系統負載 | 平均負載 (1/5/15 分鐘) |
| `dmesg` | 核心日誌 | 硬體與驅動訊息 |

---

## 延伸閱讀

- [Linux 行程管理教學](https://www.google.com/search?q=Linux+process+management+ps+top+kill)
- [Systemd 服務管理](https://www.google.com/search?q=systemd+systemctl+service+management+tutorial)
- [Linux 系統監控工具](https://www.google.com/search?q=Linux+system+monitoring+tools+htop+iostat)
