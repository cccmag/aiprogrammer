# 檔案權限與使用者管理

## Linux 使用者和群組模型

Linux 是多使用者作業系統，每個程序都由特定使用者執行。使用者分為三類：

- **root (UID 0)**: 超級使用者，擁有系統完整存取權
- **系統使用者 (1-999)**: 用於執行系統服務
- **一般使用者 (1000+)**: 普通使用者帳號

群組 (Group) 是使用者的集合，用於簡化權限管理。

```bash
# 使用者與群組管理命令
useradd alice           # 建立使用者
usermod -aG sudo alice  # 加入 sudo 群組
groupadd developers     # 建立群組
passwd alice            # 設定密碼
```

## UGO 權限模型

每個檔案和目錄都有三組權限，分別對應三種角色：

| 角色 | 簡寫 | 說明 |
|------|------|------|
| User | u | 檔案擁有者 |
| Group | g | 所屬群組 |
| Others | o | 其他所有人 |

每組權限有三個位元：

| 權限 | 數字 | 檔案意義 | 目錄意義 |
|------|------|----------|----------|
| r | 4 | 讀取內容 | 列出檔案列表 |
| w | 2 | 修改內容 | 建立/刪除檔案 |
| x | 1 | 執行 | 進入目錄 |

```python
import os, stat

def parse_permissions(mode):
    """解析權限數字模式"""
    perms = {
        stat.S_IRUSR: "r", stat.S_IWUSR: "w", stat.S_IXUSR: "x",
        stat.S_IRGRP: "r", stat.S_IWGRP: "w", stat.S_IXGRP: "x",
        stat.S_IROTH: "r", stat.S_IWOTH: "w", stat.S_IXOTH: "x",
    }
    result = ""
    for bit, char in perms.items():
        result += char if mode & bit else "-"
    return result

mode = 0o755
perm_str = parse_permissions(mode)
print(f"0o{mode:o} -> {perm_str}")
# 輸出: 0o755 -> rwxr-xr-x
```

## chmod、chown、umask

### chmod：修改權限

```bash
chmod 755 script.sh     # 數字模式
chmod u+x script.sh     # 符號模式 (使用者加執行)
chmod g-w script.sh     # 群組移除寫入
chmod a+r file.txt      # 所有人加讀取
```

### chown：修改擁有者

```bash
chown alice file.txt            # 修改擁有者
chown alice:developers file.txt # 同時修改擁有者和群組
chown -R alice:users /home/     # 遞迴修改
```

### umask：預設權限遮罩

umask 決定新建立檔案的預設權限：

```python
import os

current = os.umask(0)
os.umask(current)
print(f"當前 umask: {current:04o}")
# 檔案預設: 666 - umask
# 目錄預設: 777 - umask
```

## ACL 與 SELinux

### 存取控制清單 (ACL)

當 UGO 模型不夠用時，ACL 允許對特定使用者或群組設定權限：

```bash
setfacl -m u:bob:rwx project/
getfacl project/
```

### SELinux 安全強化 Linux

SELinux 是 Linux 核心的安全模組，提供強制存取控制 (MAC)。比起傳統的 UGO 權限 (自主存取控制)，SELinux 更加精細——它可以限制某個特定程序只能讀取某個特定檔案，即使 root 使用者也無法繞過。

---

## 延伸閱讀

- [Linux 權限管理 chmod 教學](https://www.google.com/search?q=Linux+chmod+permissions+tutorial+ugo)
- [Linux 使用者管理 useradd](https://www.google.com/search?q=Linux+user+management+useradd+usermod)
- [ACL 存取控制清單](https://www.google.com/search?q=Linux+ACL+access+control+list+setfacl)
- [SELinux 入門](https://www.google.com/search?q=SELinux+security+enhanced+Linux+tutorial)
