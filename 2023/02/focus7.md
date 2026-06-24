# 檔案系統與儲存（1950s-2023）

## 檔案系統的功能

檔案系統是作業系統中負責管理持久化資料的元件。它提供：

- **檔案抽象**：將磁碟區塊組織為邏輯上連續的位元組序列
- **目錄層次**：以樹狀結構組織檔案（及硬連結、軟連結）
- **命名空間**：提供人類可讀的檔案名（而非磁碟區塊編號）
- **權限控制**：誰可以讀取、寫入、執行檔案
- **可靠儲存**：防止因系統崩潰導致的資料損毀

## 磁碟上的結構

磁碟的最小儲存單位是「區塊」（block，典型大小 4KB）。檔案系統在磁碟上組織以下結構：

```
┌─────────────────────────┐
│ 開機區塊 (Boot Block)    │
├─────────────────────────┤
│ 超級區塊 (Super Block)   │ ← 檔案系統元資料（類型、大小、狀態）
├─────────────────────────┤
│ 索引節點區 (inode table) │ ← inode 陣列（每個檔案一個）
├─────────────────────────┤
│ 資料區塊 (Data Blocks)   │ ← 實際檔案內容
└─────────────────────────┘
```

## inode 結構

inode（index node）是 Unix 檔案系統的核心資料結構。每個檔案和目錄都有一個 inode，儲存了除檔案名以外的所有元資料：

- 檔案類型（普通檔案、目錄、符號連結等）
- 權限位元（rwx-rwx-rwx）
- 擁有者（UID）和所屬群組（GID）
- 時間戳（建立時間、修改時間、存取時間）
- 檔案大小
- 資料區塊指標（直接/間接/雙重間接/三重間接）

```
inode ──┬── 直接區塊 1
        ├── 直接區塊 2
        ├── ...
        ├── 直接區塊 12
        ├── 間接區塊 → 指向更多區塊指標
        ├── 雙重間接 → → 更多
        └── 三重間接 → → → 更多
```

## 常見檔案系統

| 檔案系統 | 作業系統 | 特點 |
|---------|---------|------|
| FAT32 | Windows/Linux/macOS | 簡單、相容性好、最大 4GB 單檔 |
| NTFS | Windows | 日誌、壓縮、加密、ACL |
| ext4 | Linux | 日誌、extent、延遲分配 |
| XFS | Linux | 高效並行 I/O、大檔案 |	
| Btrfs | Linux | 快照、壓縮、自我修復 |	
| ZFS | FreeBSD/Linux | 池化儲存、校驗和、壓縮 |	
| APFS | macOS | 快照、加密、空間共享 |	
| HFS+ | macOS (舊) | 舊版、不支援快照 |

## 日誌（Journaling）

日誌檔案系統在實際修改磁碟結構之前，先將操作記錄到日誌中。如果系統在操作過程中崩潰，重啟時可以回放日誌來恢復一致性。

```
寫入操作前：
1. 將「要修改哪些區塊」記錄到日誌
2. 等待日誌寫入完成（日誌提交）
3. 修改實際的檔案系統結構
4. 標記日誌條目為已處理
```

不同日誌模式：
- **writeback**：只記錄元資料的修改
- **ordered**：記錄元資料，但確保資料先寫入磁碟
- **data**：元資料和資料都記錄到日誌（最安全，最慢）

## 目錄結構

目錄本質上是一個特殊檔案，內容是「檔案名 → inode 編號」的映射表：

```
目錄檔案 /home/user/：
  .         → inode 12345
  ..        → inode 12000
  report.md → inode 23456
  photos/   → inode 34567
```

## VFS 虛擬檔案系統

VFS（Virtual File System）是 Linux 的關鍵抽象，允許不同的檔案系統共存：

```
應用程式 → VFS 層 (open/read/write 系統呼叫)
           ↓
     不同的檔案系統驅動：
    ext4.ko  XFS.ko  NTFS.ko  NFS.ko
           ↓
      區塊裝置層 (block layer)
           ↓
      儲存設備 (SSD/HDD/NVMe)
```

## 延伸閱讀

- [Linux VFS 架構](https://www.google.com/search?q=Linux+Virtual+File+System+VFS)
- [ext4 檔案系統](https://www.google.com/search?q=ext4+filesystem+features)
- [ZFS 檔案系統](https://www.google.com/search?q=ZFS+filesystem+features+architecture)
- [NTFS vs FAT32 vs exFAT](https://www.google.com/search?q=NTFS+FAT32+exFAT+comparison)
