# ls、cd、cp、mv 實戰

## 目錄導航：cd

`cd` (Change Directory) 是使用頻率最高的命令之一。掌握它可以大幅提升工作效率。

### 進階用法

```bash
cd              # 回到家目錄 (~)
cd -            # 回到上一個目錄
cd ~/project    # 使用家目錄相對路徑
cd ..            # 上一層目錄
cd ../..         # 上兩層目錄
cd /var/log     # 絕對路徑
cd !$           # cd 到上一條命令的最後參數
```

### 效率技巧

```bash
# 使用 CDPATH 設定捷徑
export CDPATH=.:~:~/projects:~/work
cd myproject    # 自動搜尋 CDPATH 中的目錄

# pushd/popd：目錄堆疊
pushd /var/log   # 切換目錄並壓入堆疊
pushd /tmp       # 再次切換
dirs             # 檢視堆疊
popd             # 回到上一個目錄
```

## 列表命令：ls

`ls` 是最基本的檔案列表命令，但它的選項非常豐富：

```bash
ls -l           # 詳細列表 (權限、大小、日期)
ls -a           # 顯示隱藏檔 (.開頭)
ls -la          # 兩者結合
ls -lh          # 人類可讀大小 (KB/MB)
ls -lS          # 依大小排序
ls -lt          # 依時間排序
ls -ltr         # 依時間反向排序
ls -R           # 遞迴列出子目錄
ls -d */        # 只顯示目錄
```

### 顏色輸出詳解

`ls -l` 輸出範例：

```
-rw-r--r--  1 alice  staff  1024  Jul 1 10:00 file.txt
d rwxr-xr-x  2 alice  staff    64  Jul 1 10:00 dir/
```

- 第一個字元: `-` 檔案, `d` 目錄, `l` 連結, `b` 裝置
- 後九個字元: 三組 rwx 權限
- 硬連結數、擁有者、群組、大小、修改時間、名稱

## 複製：cp

```bash
cp file.txt backup.txt          # 基本複製
cp -r src/ dest/                # 遞迴複製目錄
cp -a src/ dest/                # 歸檔模式 (保留權限)
cp -i file.txt dest/            # 互動式 (覆蓋前確認)
cp -u *.txt dest/               # 只複製較新的檔案
cp -v file.txt dest/            # 顯示複製過程
```

## 移動/重新命名：mv

```bash
mv file.txt /tmp/               # 移動檔案
mv oldname.txt newname.txt      # 重新命名
mv -i file.txt dest/            # 互動式
mv -u *.txt dest/               # 只移動較新的
mv dir1/ dir2/                  # 移動或重新命名目錄
```

### 批次操作技巧

```bash
# 批次重新命名 (使用迴圈)
for f in *.JPG; do
    mv "$f" "${f%.JPG}.jpg"
done

# 批次移動特定類型
cp -v *.py src/
mv -v *.bak /tmp/backup/
```

## Python 中的檔案操作

```python
import os, shutil, glob

# 列出目錄 (ls)
files = os.listdir(".")
py_files = glob.glob("*.py")
print(f"Python 檔案: {py_files}")

# 建立目錄 (mkdir -p)
os.makedirs("project/src/utils", exist_ok=True)

# 複製檔案 (cp)
shutil.copy2("source.py", "dest.py")  # cp -p (保留中繼資料)

# 複製目錄 (cp -r)
shutil.copytree("src", "backup", dirs_exist_ok=True)

# 移動/重新命名 (mv)
os.rename("old.py", "new.py")
shutil.move("file.txt", "/tmp/")

# 刪除 (rm)
os.remove("file.txt")           # rm file.txt
shutil.rmtree("temp_dir")       # rm -rf temp_dir

# 路徑操作
path = "/home/user/project/file.py"
print(os.path.basename(path))    # file.py
print(os.path.dirname(path))     # /home/user/project
print(os.path.splitext(path))    # ('/home/user/project/file', '.py')
```

### 安全檢查

```python
def safe_copy(src, dst):
    """安全的檔案複製 (檢查存在性)"""
    if not os.path.exists(src):
        print(f"錯誤: {src} 不存在")
        return
    if os.path.exists(dst):
        response = input(f"{dst} 已存在，覆蓋？(y/N) ")
        if response.lower() != 'y':
            print("已取消")
            return
    shutil.copy2(src, dst)
    print(f"已複製 {src} -> {dst}")
```

---

## 延伸閱讀

- [Linux ls 命令選項](https://www.google.com/search?q=Linux+ls+command+options+tutorial)
- [Linux cp 與 mv 命令](https://www.google.com/search?q=Linux+cp+mv+command+tutorial)
- [Python shutil 模組](https://www.google.com/search?q=Python+shutil+file+operations+tutorial)
