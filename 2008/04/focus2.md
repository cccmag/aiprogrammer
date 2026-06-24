# HDFS 分散式檔案系統

## HDFS 概述

Hadoop Distributed File System (HDFS) 是 Hadoop 生態系統的基礎儲存層。專為儲存超大檔案而設計，執行在普通硬體叢集上，具備高容錯性和高吞吐量。

### 設計目標

- **大型檔案**：支援 GB 到 TB 等級的檔案
- **高吞吐量**：最佳化一次寫入、多次讀取場景
- **容錯機制**：自動復原硬體故障
- **資料本地化**：計算盡量靠近資料

### 與傳統檔案系統的差異

| 特性 | HDFS | 傳統 DFS |
|------|------|----------|
| 檔案大小 | TB 等級 | GB 等級 |
| 一致性模型 | 寫入後不變 | 可修改 |
| 最佳化目標 | 吞吐量 | 低延遲 |
| 硬體需求 | Commodity | 昂貴專用 |

## 架構設計

### NameNode 和 DataNode

HDFS 採用主從架構：

```
┌──────────────────────────────────────────────────┐
│                 HDFS 叢集                          │
├──────────────────────────────────────────────────┤
│                                                  │
│   ┌─────────────┐                                │
│   │  NameNode   │                                │
│   │  (主節點)    │                                │
│   └─────────────┘                                │
│          │                                        │
│          │ 元數據管理                              │
│          ↓                                        │
│   ┌────────────────────────────────────────────┐ │
│   │              DataNode 叢集                  │ │
│   │  ┌────────┐ ┌────────┐ ┌────────┐        │ │
│   │  │DataNode│ │DataNode│ │DataNode│  ...    │ │
│   │  └────────┘ └────────┘ └────────┘        │ │
│   └────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────┘
```

#### NameNode 職責

- 維護檔案系統的命名空間（namespace）
- 管理檔案區塊到 DataNode 的映射
- 處理客戶端的檔案操作請求
- 管理副本配置和負載均衡

#### DataNode 職責

- 儲存實際的資料區塊
- 定期向 NameNode 報告狀態（心跳）
- 執行區塊創建、刪除、複製指令

## 區塊複製

### 區塊大小

HDFS 預設區塊大小為 64MB（2008 年），大於多數檔案系統：

```java
// 設定區塊大小
conf.set("dfs.block.size", "134217728"); // 128MB
```

### 複製策略

HDFS 採用機架感知（Rack Awareness）複製策略：

1. **第一副本**：寫入客戶端所在節點（若客戶端不在叢集中，選擇隨機節點）
2. **第二副本**：不同機架的另一節點
3. **第三副本**：與第二副本相同機架的不同節點

```
機架 A                      機架 B
┌────────┐                ┌────────┐
│ Node1  │ ← 第一副本      │ Node3  │ ← 第二副本
│(本地)  │                │        │
├────────┤                ├────────┤
│ Node2  │ ← 第三副本      │        │
└────────┘                └────────┘
```

### 容錯機制

當 DataNode 故障時，NameNode 自動復制不足的區塊：

```bash
# 檢視區塊複製狀態
hdfs dfsadmin -report
```

## 資料讀取流程

### 用戶端讀取流程

1. 用戶端向 NameNode 請求檔案位置
2. NameNode 傳回區塊位置列表
3. 用戶端直接聯繫 DataNode 讀取資料
4. 讀取完成後關閉連接

```
客戶端 → NameNode (請求檔案位置) → DataNode1 → 資料
                    ↑                           ↓
                    └─────── 區塊位置 ──────────┘
```

### 程式碼範例

```java
Configuration conf = new Configuration();
FileSystem fs = FileSystem.get(conf);
Path path = new Path("hdfs://namenode:9000/data/input.txt");
FSDataInputStream in = fs.open(path);
IOUtils.copyBytes(in, System.out, 4096, true);
```

## 資料寫入流程

### 寫入流程

1. 用戶端向 NameNode 請求建立檔案
2. NameNode 檢查許可權並分配新區塊
3. NameNode 傳回 DataNode 列表
4. 用戶端向第一 DataNode 寫入資料
5. 資料透過管線（pipeline）流向其他 DataNode
6. 寫入完成後，確認寫入成功

```
客戶端 → DataNode1 → DataNode2 → DataNode3
  ↑          ↓           ↓           ↓
  └────────確認───────────┴───────────┘
```

### 程式碼範例

```java
Configuration conf = new Configuration();
FileSystem fs = FileSystem.get(conf);
Path path = new Path("hdfs://namenode:9000/data/output.txt");
FSDataOutputStream out = fs.create(path);
out.writeBytes("Hello, HDFS!");
out.close();
```

## 檔案系統命令

### 基本操作

```bash
# 檢視目錄
hadoop fs -ls /

# 建立目錄
hadoop fs -mkdir /user/data

# 複製檔案
hadoop fs -put localfile /user/data/
hadoop fs -get /user/data/remote local

# 檢視檔案內容
hadoop fs -cat /user/data/file.txt

# 刪除檔案
hadoop fs -rm /user/data/file.txt
```

### 進階操作

```bash
# 改變複製因子
hadoop fs -setrep -w 3 /user/data/file

# 檢視檔案大小
hadoop fs -du -h /user/data/

# 檢視叢集狀態
hadoop dfsadmin -report
```

## 安全模式

HDFS 啟動時進入安全模式，只讀不寫：

```bash
# 手動進入安全模式
hadoop dfsadmin -safemode enter

# 離開安全模式
hadoop dfsadmin -safemode leave

# 檢視狀態
hadoop dfsadmin -safemode get
```

## 資料一致性模型

HDFS 採用「一次寫入、多次讀取」的一致性模型：

- 檔案建立後不能修改
- 檔案一旦關閉，寫入的資料不可更改
- 支援在檔案末尾追加（append）

這種設計簡化了一致性問題，提高了讀取吞吐量。

## 快照功能

HDFS 支援時間點快照：

```bash
# 建立快照
hdfs dfsadmin -allowSnapshot /path

# 拍快照
hadoop fs -createSnapshot /path snapshotName

# 恢復快照
hadoop fs -renameSnapshot /path snapshotName backup
```

## 效能考量

### 小檔案問題

大量小檔案會造成：

- NameNode 記憶體壓力
- 搜尋效率降低
- MapReduce 任務啟動开销增加

**解決方案**：

1. 合併小檔案為 SequenceFile
2. 使用 HAR（ Hadoop Archive）封裝
3. 調整區塊大小

### 網路頻寬

區塊複製會消耗網路頻寬。機架感知可以減少跨機架流量。

## 結論

HDFS 是專為巨量資料設計的分散式檔案系統。其簡單的架構、完善的容錯機制和良好的擴展性，使其成為 Hadoop 生態系統的核心儲存層。理解 HDFS 的工作原理對於最佳化 MapReduce 程式至關重要。

---

**延伸閱讀**

- [MapReduce 分散式運算](focus1.md)
- [Hadoop 程式開發實戰](focus4.md)
- [HDFS+architecture](https://www.google.com/search?q=HDFS+architecture)