# 檔案權限 chmod/chown

## Linux 權限模型的核心概念

Linux 的權限系統圍繞三個核心要素：**使用者**、**群組** 和 **其他人**。

每個檔案都有：

- 一個擁有者 (Owner)
- 一個所屬群組 (Group)
- 三組權限位元 (Owner/Group/Others)

## 數字模式 (Octal Mode)

每個權限對應一個數字值：

```
r = 4  (讀取)
w = 2  (寫入)
x = 1  (執行)
```

權限由三個數字組合而成，每個數字是 rwx 的總和：

```
7 = rwx (4+2+1)
6 = rw- (4+2)
5 = r-x (4+1)
4 = r-- (4)
3 = -wx (2+1)
2 = -w- (2)
1 = --x (1)
0 = --- (0)
```

### 常見權限組合

```bash
chmod 755 script.sh     # rwxr-xr-x (腳本)
chmod 644 file.txt      # rw-r--r-- (一般檔案)
chmod 600 secret.txt    # rw------- (私密檔案)
chmod 700 private_dir   # rwx------ (私密目錄)
chmod 777 public/       # rwxrwxrwx (公開目錄，不建議)
```

## 符號模式 (Symbolic Mode)

語法：`[誰][運算][權限]`

```bash
chmod u+x file    # 擁有者加執行權限
chmod g-w file    # 群組移除寫入權限
chmod o=r file    # 其他人設為唯讀
chmod a+x file    # 所有人加執行權限
chmod u+rwx,g+rx,o-rwx file  # 組合操作
```

### 目錄權限的特殊性

目錄的權限意義與檔案不同：

- **r**: 可以列出目錄內容 (ls)
- **w**: 可以在目錄中建立/刪除檔案
- **x**: 可以進入目錄 (cd) 或存取其中檔案

## chown：修改擁有者與群組

```bash
chown alice file.txt          # 修改擁有者
chown :developers file.txt    # 只修改群組
chown alice:developers file   # 同時修改
chown -R alice:users /home/   # 遞迴修改
chown --reference=ref.txt target  # 參考其他檔案
```

### Python 中的權限操作

```python
import os, stat, pwd, grp

def show_permissions(path):
    st = os.stat(path)
    mode = st.st_mode

    # 檔案類型
    if stat.S_ISDIR(mode): print("類型: 目錄")
    elif stat.S_ISREG(mode): print("類型: 一般檔案")
    elif stat.S_ISLNK(mode): print("類型: 符號連結")

    # 權限字串
    perms = stat.filemode(mode)
    print(f"權限: {perms}")

    # 擁有者
    uid = st.st_uid
    gid = st.st_gid
    try:
        owner = pwd.getpwuid(uid).pw_name
        group = grp.getgrgid(gid).gr_name
        print(f"擁有者: {owner} (UID {uid})")
        print(f"群組: {group} (GID {gid})")
    except (KeyError, ImportError):
        print(f"擁有者 UID: {uid}, GID: {gid}")

def set_permissions(path, mode):
    """設定檔案權限 (類似 chmod)"""
    os.chmod(path, mode)
    print(f"已設定 {path} 權限為 {oct(mode)}")

# 使用範例
set_permissions("script.sh", 0o755)
# 相當於: chmod 755 script.sh
```

## 進階主題

### setuid / setgid / sticky bit

```bash
chmod u+s file    # setuid (執行時以擁有者權限執行)
chmod g+s dir     # setgid (新檔案繼承目錄群組)
chmod +t /tmp     # sticky bit (只有擁有者可刪除)

# 數字模式
chmod 4755 file   # setuid + rwxr-xr-x
chmod 2755 dir    # setgid + rwxr-xr-x
chmod 1777 /tmp   # sticky + rwxrwxrwx
```

### umask

```bash
umask             # 查看當前值
umask 022         # 新檔案 644, 新目錄 755
umask 077         # 新檔案 600, 新目錄 700
```

---

## 延伸閱讀

- [Linux 檔案權限完全教學](https://www.google.com/search?q=Linux+file+permissions+chmod+chown+tutorial)
- [Linux setuid setgid sticky bit](https://www.google.com/search?q=Linux+setuid+setgid+sticky+bit+explained)
- [Python os.chmod 與檔案權限](https://www.google.com/search?q=Python+os+chmod+file+permissions)
