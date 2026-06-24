# 主題三：MongoDB 3.0 新特性

## MongoDB 3.0 概述

MongoDB 3.0 於 2015 年 3 月正式發布，是該資料庫有史以來最大幅度的版本更新。這次更新主要集中在儲存引擎的革新，引入了可插拔儲存引擎架構，讓使用者可以根據應用場景選擇最適合的儲存引擎。

## WiredTiger 儲存引擎

WiredTiger 是 MongoDB 3.0 最重要的新功能。這是一個高效能的儲存引擎，提供了多項關鍵改進：

### 文件級並發控制

傳統的 MMAPv1 儲存引擎使用資料庫級別的鎖定，並發寫入時效能受限。WiredTiger 採用文件級的鎖定機制，允許多個寫入操作同時進行，顯著提升並發效能。

```python
# MongoDB 3.0 的並發寫入示意
import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["test"]

# 多執行緒同時寫入，不同文件不會互相阻塞
def write_worker(worker_id):
    collection = db["concurrent_test"]
    for i in range(1000):
        collection.insert_one({
            "worker_id": worker_id,
            "sequence": i,
            "timestamp": datetime.now()
        })

# 這在 WiredTiger 下會有更好的效能
```

### 壓縮支援

WiredTiger 支援兩種壓縮演算法：
- **Snappy**：快速壓縮，壓縮率約 2-4x
- **zlib**：高壓縮率，壓縮率約 4-7x

儲存空間通常可以節省 50-80%，大幅降低儲存成本。

### 區塊級別的 LSM（日誌結構合併）

WiredTiger 使用改良的 LSM 結構來管理資料，寫入操作首先寫入記憶體中的記憶體表（Memory Table），然後定期刷新到磁碟。這種設計特別適合寫入密集的工作負載。

## 效能提升

根據 MongoDB 官方的效能測試報告，WiredTiger 引擎相比 MMAPv1 有以下提升：

- **寫入效能**：提升 7-10 倍
- **儲存空間**：節省 50-80%
- **並發能力**：提升 3-5 倍

這些提升使得 MongoDB 3.0 能夠更好地支援大數據和高效能應用場景。

## 可插拔儲存引擎架構

MongoDB 3.0 引入了可插拔儲存引擎 API，讓第三方開發者可以開發自己的儲存引擎。目前官方支援的儲存引擎包括：

### MMAPv1

這是 MongoDB 傳統的儲存引擎，繼續作為預設選項以保持向後相容性。MMAPv1 使用記憶體映射檔案（Memory-Mapped Files）來管理資料，簡單可靠但不支援文件級鎖定。

### WiredTiger

新加入的高效能儲存引擎，適合大多數生產環境。

### In-Memory

記憶體儲存引擎，所有資料存放在記憶體中，提供極致的讀寫效能，適合對延遲極度敏感的場景。

## 副本集改進

MongoDB 3.0 也對副本集功能進行了多項改進：

### 更快的初始同步

副本集的初始同步（Initial Sync）速度大幅提升，感謝 WiredTiger 的底層優化。

### Read Preference 增強

新增了更多的讀取偏好選項，讓應用可以更靈活地控制讀取請求的路由。

### Reconfig 改進

副本集配置變更現在更加安全，減少了在變更過程中丟失投票的可能性。

## 操作建議

### 何時使用 WiredTiger

WiredTiger 引擎適合大多數使用場景，特別是：
- 寫入密集型應用
- 需要高並發的場景
- 儲存空間緊張的環境

### 何時繼續使用 MMAPv1

MMAPv1 引擎在某些場景下仍然是更好的選擇：
- 簡單的單機部署
- 以讀取為主的應用
- 對延遲一致性要求極高的場景

### 升級注意事項

從舊版本升級到 MongoDB 3.0 時：
1. 建議先在測試環境驗證
2. 預留足夠的儲存空間（壓縮可能需要重新組織資料）
3. 監控效能變化，適當調整索引

MongoDB 3.0 的這些改進，使其在企業級應用中更加可靠，也為未來的發展奠定了堅實的基礎。