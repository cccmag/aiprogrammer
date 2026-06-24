# 檔案系統操作

檔案系統是 Linux 儲存和管理資料的核心機制。

---

## 檔案系統結構

```
/
├── bin     # 執行檔
├── boot    # 開機檔案
├── dev     # 裝置檔案
├── etc     # 設定檔
├── home    # 使用者目錄
├── lib     # 函式庫
├── media   # 卸載式媒體
├── mnt     # 掛載點
├── opt     # 額外軟體
├── proc    # 程序檔案系統
├── root    # 系統管理員目錄
├── run     # 執行時資料
├── sbin    # 系統執行檔
├── srv     # 服務資料
├── sys     # 系統檔案
├── tmp     # 暫存檔案
├── usr     # 使用者程式
└── var     # 變動資料
```

---

## 目錄操作

```bash
# 顯示目錄內容
ls -la /path/to/dir

# 建立目錄
mkdir newdir
mkdir -p path/to/nested/dir

# 刪除空目錄
rmdir emptydir

# 刪除目錄及內容
rm -rf dir

# 複製目錄
cp -r source_dir dest_dir

# 移動/重新命名目錄
mv oldname newname
mv dir /new/path/
```

---

## 檔案操作

```bash
# 複製
cp file1 file2
cp -r dir1 dir2
cp -p preserve.txt /dest/

# 移動/重新命名
mv old.txt new.txt
mv file.txt /new/path/

# 刪除
rm file.txt
rm -f force.txt
rm -i interactive.txt

# 建立檔案
touch newfile.txt
echo "content" > file.txt

# 檢視檔案
cat file.txt
less file.txt
head -n 10 file.txt
tail -n 10 file.txt
tail -f logfile  # 即時監控
```

---

## 權限管理

### chmod

```bash
# 符號方式
chmod u+x script.sh     # 新增執行權限
chmod g-w file.txt       # 移除寫入權限
chmod o+r file.txt       # 其他使用者讀取權限
chmod a+rw file.txt      # 所有人均可讀寫

# 數字方式
chmod 755 script.sh      # rwxr-xr-x
chmod 644 file.txt       # rw-r--r--
chmod 600 secret.txt     # rw-------
chmod 700 .ssh          # rwx------

# 數字對照表
# 4 = r (讀取)
# 2 = w (寫入)
# 1 = x (執行)
```

### chown

```bash
# 改變擁有者
chown user file.txt

# 改變擁有者和群組
chown user:group file.txt

# 遞迴改變
chown -R user:group dir/

# 只改變群組
chgrp group file.txt
```

### 特殊權限

```bash
# SetUID (4)
chmod 4755 program    # -rwsr-xr-x

# SetGID (2)
chmod 2755 dir        # drwxr-sr-x

# Sticky Bit (1)
chmod 1777 /tmp       # drwxrwxrwt
```

---

## 連結

### 符號連結 (Symbolic Link)

```bash
# 建立符號連結
ln -s /path/to/target link_name

# 檢視連結
ls -l link_name

# 刪除連結
rm link_name

# 軟連結特性
# - 可以連結目錄
# - 可以跨檔案系統
# - 原始檔案刪除後連結失效
```

### 硬連結 (Hard Link)

```bash
# 建立硬連結
ln /path/to/file hardlink

# 特性
# - 不能跨檔案系統
# - 不能連結目錄
# - 多個硬連結視為同一檔案
```

---

## 磁碟使用

### df

```bash
# 顯示磁碟空間
df -h                    # 人類可讀格式
df -T                    # 顯示檔案系統類型
df -i                    # 顯示 inode 使用
```

### du

```bash
# 顯示目錄大小
du -h dir/
du -sh *                 # 每個項目的大小
du -h --max-depth=1     # 限制深度
du -ah                   # 包含檔案
```

### 掛載

```bash
# 掛載
mount /dev/sdb1 /mnt/usb

# 卸載
umount /mnt/usb

# 檢視掛載
mount

# 自動掛載設定 (/etc/fstab)
/dev/sdb1 /mnt/usb ext4 defaults 0 2
```

---

## 檔案搜尋

```bash
# find
find /path -name "*.txt"
find /path -type f -mtime -7
find /path -type d -empty
find /path -perm 755

# locate（需要 updatedb）
locate filename

# which（找執行檔）
which python

# whereis
whereis python
```

---

## 壓縮與封存

```bash
# tar
tar -cvf archive.tar dir/
tar -xvf archive.tar
tar -cvzf archive.tar.gz dir/
tar -xvzf archive.tar.gz

# zip
zip -r archive.zip dir/
unzip archive.zip

# gzip
gzip file.txt
gunzip file.txt.gz
```

---

## 小結

掌握檔案系統操作是 Linux 系統管理的基礎，正確的權限設定和目錄管理能確保系統安全和有效運作。

---

*作者：AI 程式人團隊*