# 分散式檔案系統：HDFS 與物件儲存的設計

## 分散式檔案系統的必要性

### 傳統檔案系統的局限性

```
單一檔案系統的問題：
────────────────────────────────

1. 容量限制
   └── 單一機器的磁碟空間有限
   
2. 頻寬限制
   └── 單一機器對外提供頻寬有限
   
3. 可用性
   └── 磁碟故障導致資料丢失
   
4. 地理限制
   └── 無法跨資料中心分布
```

## HDFS 架構

### NameNode 和 DataNode

HDFS 採用主從架構：

```
HDFS 架構：
────────────────────────────────

         NameNode (Single Point)
         ┌─────────────────────┐
         │  Namespace           │
         │  ├── /user/data      │
         │  ├── /user/reports   │
         │  └── /warehouse      │
         │                      │
         │  Block Map           │
         │  ├── blk_1 → [DN1, DN2, DN3] │
         │  └── blk_2 → [DN2, DN3, DN4] │
         └─────────────────────┘
              │
              │  Heartbeat / Block Report
    ┌─────────┼─────────┬─────────┐
    │         │         │         │
    ▼         ▼         ▼         ▼
┌────────┐┌────────┐┌────────┐┌────────┐
│DataNode││DataNode││DataNode││DataNode│
│        ││        ││        ││        │
│ blk_1  ││ blk_1  ││ blk_1  ││ blk_2  │
│ blk_2  ││ blk_2  ││ blk_3  ││ blk_2  │
│ blk_3  ││ blk_4  ││ blk_3  ││ blk_4  │
└────────┘└────────┘└────────┘└────────┘

特點：
- 每個 Block 預設 128MB
- 每個 Block 複製 3 份
- NameNode 全域管理元資料
```

### HDFS 讀寫流程

```python
# HDFS 讀取流程
def hdfs_read(file_path):
    # 1. 用戶端請求 NameNode 獲取檔案區塊位置
    block_locations = namenode.get_block_locations(file_path)
    
    # 2. 直接讀取最近的 DataNode
    for block in block_locations:
        datanode = pick_closest_datanode(block.locations)
        data = datanode.read_block(block.id)
        yield data

# HDFS 寫入流程
def hdfs_write(file_path, data):
    # 1. 請求 NameNode 分配新區塊
    block = namenode.allocate_block()
    
    # 2. 寫入第一個 DataNode
    first_dn = block.locations[0]
    first_dn.write_block(block.id, data[:chunk])
    
    # 3. Pipeline 複製到其他 DataNode
    for dn in block.locations[1:]:
        dn.copy_block(block.id, data[:chunk])
    
    # 4. 確認寫入成功
    return True
```

## HDFS 的特點

### 資料本地性

```
資料本地性：
────────────────────────────────

沒有資料本地性：
  Task ────▶ 網路 ────▶ DataNode
              │
              ▼
         網路傳輸所有資料

有資料本地性（Spark/Hadoop）：
  Task 在資料所在的節點執行
  最大化利用本地磁片讀取
  最小化網路傳輸
```

### 資料複製策略

```python
# HDFS 複製因子為 3 的放置策略

"""
第一份：寫入客戶端所在節點（如果是 DataNode）
第二份：不同機架的某個節點
第三份：與第二份相同機架的不同節點

好處：
- 最大化可靠性和可用性
- 寫入頻寬最小化
- 讀取頻寬最大化（可以從多個副本讀取）
"""
```

## 物件儲存的崛起

### 物件儲存 vs 檔案系統 vs 區塊儲存

```
儲存類型比較：
────────────────────────────────

區塊儲存：
- 提供原始區塊設備
- 低延遲、高 IOPS
- 需要檔案系統管理
- 範例：EBS、iSCSI

物件儲存：
- 以物件為單位儲存
- 每個物件包含資料、元資料、唯一 ID
- 擴展性極強
- 範例：S3、Azure Blob、Google Cloud Storage

檔案系統：
- 階層式目錄結構
- POSIX 相容
- 擴展性有限
- 範例：NFS、HDFS
```

### S3 的設計理念

Amazon S3 採用了完全不同的設計哲學：

```
S3 資料模型：
────────────────────────────────

Bucket（儲存桶）
  └── Object（物件）
        ├── Key（鍵）：物件的唯一識別符
        ├── Value（值）：資料內容
        └── Version ID（版本）：版本控制
              │
              ▼
         Global Namespace
         S3 的 bucket 名稱是全球唯一的
```

### 物件儲存優缺點

```
物件儲存特點：
────────────────────────────────

優點：
✓ 理論上無限擴展（PB 到 EB 等級）
✓ 成本低廉
✓ 高可用（11 個 9 的可用性）
✓ 内建版本控制和生命週期管理
✓ 簡單的 REST API

缺點：
✗ 延遲較高
✗ 不支援隨機寫入（只能完整覆蓋）
✗ 不相容 POSIX
✗ 不適合低延遲應用
```

## MinIO：輕量級物件儲存

MinIO 是一個相容 S3 的輕量級物件儲存，常用於本地開發和邊緣部署：

```bash
# 啟動 MinIO
docker run -p 9000:9000 \
  -e "MINIO_ACCESS_KEY=minioadmin" \
  -e "MINIO_SECRET_KEY=minioadmin" \
  minio/minio server /data

# 使用 Python SDK 存取 MinIO
import boto3

s3 = boto3.client(
    's3',
    endpoint_url='http://localhost:9000',
    aws_access_key_id='minioadmin',
    aws_secret_access_key='minioadmin'
)

# 上傳檔案
s3.upload_file('myfile.txt', 'mybucket', 'myfile.txt')

# 下載檔案
s3.download_file('mybucket', 'myfile.txt', 'downloaded.txt')
```

## 分散式檔案系統的選擇

### 常見分散式檔案系統

```
分散式檔案系統比較：
────────────────────────────────

HDFS：
  - 專為大資料設計
  - 高吞吐量
  - 最佳化寫入一次讀取多次

CephFS：
  - 統一的儲存系統（檔案、區塊、物件）
  - 自我管理、自我修復
  - 適用於雲端原生環境

GlusterFS：
  - 橫向擴展
  - 無中繼資料伺服器
  - 適合媒體和檔案共享

Lustre：
  - 高效能運算首選
  - 支援 PB 級別
  - Linux 核心原生支援
```

## 延伸閱讀

- [HDFS 架構指南](https://www.google.com/search?q=HDFS+architecture+guide)
- [S3 設計原則](https://www.google.com/search?q=Amazon+S3+design+principles)
- [Ceph 分散式儲存](https://www.google.com/search?q=Ceph+distributed+storage)
- [物件儲存 vs 檔案系統](https://www.google.com/search?q=object+storage+vs+file+system)
- [MinIO 文件](https://www.google.com/search?q=MinIO+object+storage)

---

*本篇文章為「AI 程式人雜誌 2020 年 11 月號」歷史回顧系列之一。*