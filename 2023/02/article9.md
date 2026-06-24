# 檔案系統實作

## 從磁碟區塊到檔案

檔案系統的核心任務是將物理磁碟上的區塊組織為邏輯上的檔案和目錄。這個過程涉及多個抽象層次：

```
位元組串流 (應用程式看到的)
  │ 檔案系統軟體
檔案 (inode)
  │ 區塊分配策略
磁碟區塊
  │ 磁碟驅動程式
磁碟磁區
```

## inode 結構

inode（index node）是 Unix 檔案系統的核心資料結構。它儲存了檔案的元資料（metadata）和資料區塊的指標。

### inode 的典型內容

```
struct inode {
    mode_t      i_mode;       // 檔案類型 + 權限位元
    uid_t       i_uid;        // 擁有者 UID
    gid_t       i_gid;        // 所屬群組 GID
    off_t       i_size;       // 檔案大小 (bytes)
    time_t      i_atime;      // 最後存取時間
    time_t      i_mtime;      // 最後修改時間
    time_t      i_ctime;      // 最後狀態變更時間
    unsigned    i_blocks;     // 已分配的磁碟區塊數
    unsigned    i_nlink;      // 硬連結計數
    block_t     i_block[15];  // 資料區塊指標
};
```

### 區塊指標方案

ext4 使用 15 個區塊指標的直接/間接尋址方案：

```
i_block[0-11]：直接區塊          (12 個區塊)
i_block[12] ：單重間接區塊        (256 個區塊指標)
i_block[13] ：雙重間接區塊        (256² 個區塊指標)
i_block[14] ：三重間接區塊        (256³ 個區塊指標)

總計（4KB 區塊, 256 個指標/區塊）：
  12 + 256 + 256² + 256³ ≈ 16GB
```

### Extent（範圍）

現代檔案系統（ext4、XFS）使用 extent 取代簡單的間接尋址。一個 extent 描述一段連續的區塊序列：

```c
struct ext4_extent {
    __le32  ee_block;   // 第一個邏輯區塊號
    __le16  ee_len;     // extent 中的區塊數量
    __le16  ee_start_hi; // 起始實體區塊號高 16 位
    __le32  ee_start_lo; // 起始實體區塊號低 32 位
};
```

一個 extent 條目可以表示長達 128MB 的連續空間（32768 × 4KB），這大大減少了中大型檔案的元資料開銷。

## 目錄實現

目錄是一個特殊類型的檔案，其內容是「檔案名 → inode 編號」的映射表：

```
目錄檔案 /home/user/ 的內容：
inode=123  "."      
inode=120  ".."     
inode=456  "doc.txt"
inode=789  "photos"  ← 子目錄也是一個 inode
```

目錄查找流程：

```
路徑：/home/user/doc.txt
1. 從根 inode (2) 讀取根目錄內容
2. 在根目錄中查找 "home" → inode 120
3. 讀取 inode 120 的資料（目錄 home 的內容）
4. 查找 "user" → inode 456
5. 讀取 inode 456 的資料（目錄 user 的內容）
6. 查找 "doc.txt" → inode 789
7. 讀取 inode 789 的資料（檔案內容）
```

大型目錄使用 B-tree（ext4 的 HTree）或 B+ tree（XFS）來加速查找。

## 區塊分配策略

### 連續分配

檔案佔用連續的磁碟區塊——簡單快速，但隨著檔案的增刪會產生碎片。

### 鏈式分配

每個區塊包含指向下一個區塊的指標——無外部碎片，但隨機存取慢。

### 索引式分配

使用 inode 中的區塊指標陣列——支援隨機存取，但間接尋址層級增加了開銷。

### ext4 的延遲分配

ext4 在記憶體中緩衝寫入，等到真正需要寫入磁碟時才決定區塊位置。這樣可以合併連續的寫入，讓檔案盡可能使用連續區塊。

## 日誌機制

日誌檔案系統在修改元資料之前先將操作記錄到日誌中：

```
1. 開始事務 (journal_begin)
2. 將修改記錄到日誌 (journal_add)
3. 提交日誌 (journal_commit)
4. 修改實際的檔案系統結構
5. 標記日誌為已處理 (checkpoint)
```

如果系統在步驟 3-4 之間崩潰，重啟時重放日誌可以恢復一致性。

## 延伸閱讀

- [ext4 檔案系統資料結構](https://www.google.com/search?q=ext4+filesystem+data+structures+inode)
- [Btrfs 檔案系統](https://www.google.com/search?q=Btrfs+filesystem+architecture+COW)
- [ZFS 儲存池](https://www.google.com/search?q=ZFS+storage+pool+architecture)
- [日誌檔案系統](https://www.google.com/search?q=journaling+file+system+writeback+ordered+data)
