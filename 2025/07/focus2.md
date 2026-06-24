# 檔案系統與目錄操作

## Linux 檔案系統階層標準 (FHS)

Linux 採用統一的目錄結構，所有檔案從根目錄 `/` 開始。FHS (Filesystem Hierarchy Standard) 定義了各目錄的用途：

```
/         根目錄，所有檔案的起點
/bin      基本使用者命令 (binary)
/sbin     系統管理命令
/etc      系統設定檔
/home     使用者家目錄
/var      可變資料 (日誌、快取)
/tmp      暫存檔案
/usr      使用者共用資源
/opt      第三方軟體
/mnt      手動掛載點
/media    可移除媒體
/proc     虛擬檔案系統 (核心/行程資訊)
/sys      核心裝置資訊
```

## inode 與資料儲存

Linux 檔案系統中，每個檔案由兩部分組成：

- **inode** (索引節點): 儲存檔案的中繼資料 (權限、擁有者、大小、時間戳、資料區塊指標)
- **data block** (資料區塊): 儲存檔案的實際內容

```python
# Python 模擬 stat 命令查看 inode 資訊
import os, stat

def show_inode(path):
    st = os.stat(path)
    print(f"inode: {st.st_ino}")
    print(f"size: {st.st_size} bytes")
    print(f"blocks: {st.st_blocks}")
    print(f"permissions: {stat.filemode(st.st_mode)}")
    print(f"links: {st.st_nlink}")
    print(f"owner: {st.st_uid}:{st.st_gid}")
```

## 軟連結 vs 硬連結

### 硬連結 (Hard Link)

硬連結指向同一個 inode，本質上是同一個檔案的多個名稱。刪除任何一個名稱都不會影響其他名稱。

```
$ ln file1 file2   # 建立硬連結
$ ls -li           # 兩者有相同的 inode 編號
128394 -rw-r--r-- 2 user user 100 Jul 1 10:00 file1
128394 -rw-r--r-- 2 user user 100 Jul 1 10:00 file2
```

### 軟連結 (Symbolic Link)

軟連結類似於捷徑，包含指向目標檔案的路徑。如果目標被刪除，軟連結會失效。

```
$ ln -s /original/file link_name
$ ls -l link_name
lrwxr-xr-x 1 user 15 Jul 1 10:00 link_name -> /original/file
```

## 掛載點與檔案系統類型

Linux 支援多種檔案系統類型，透過掛載 (mount) 整合到同一個目錄樹：

| 類型 | 說明 | 常用場景 |
|------|------|----------|
| ext4 | Linux 標準檔案系統 | 一般用途 |
| XFS | 高效能日誌檔案系統 | 大檔案伺服器 |
| Btrfs | 寫入時複製 + 快照 | NAS 儲存 |
| ZFS | 先進的儲存池 | 企業儲存 |
| tmpfs | 記憶體檔案系統 | 暫存資料 |
| overlay | 聯合檔案系統 | 容器 |

```python
# Python 查看掛載點
import subprocess

result = subprocess.run(["mount"], capture_output=True, text=True)
for line in result.stdout.strip().split("\n")[:5]:
    print(line)
```

---

## 延伸閱讀

- [Filesystem Hierarchy Standard](https://www.google.com/search?q=Filesystem+Hierarchy+Standard+FHS+Linux)
- [Linux inode 詳解](https://www.google.com/search?q=Linux+inode+filesystem+structure+explained)
- [Linux 硬連結與軟連結差異](https://www.google.com/search?q=hard+link+vs+symbolic+link+Linux+difference)
- [Linux 掛載 mount 命令](https://www.google.com/search?q=Linux+mount+command+filesystem+types)
