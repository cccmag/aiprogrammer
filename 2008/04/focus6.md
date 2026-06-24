# HBase 即時資料庫

## HBase 簡介

HBase 是一個分散式的、面向列的 NoSQL 資料庫，建立在 HDFS 之上。它源自 Google 的 BigTable 論文，提供即時讀寫存取 PB 等級資料的能力。

### 與傳統關聯式資料庫的比較

| 特性 | HBase | 傳統 RDBMS |
|------|-------|-----------|
| 資料模型 | 寬欄表（Wide Table） | 關聯式 |
| 儲存 | HDFS | 區塊儲存 |
| 讀寫延遲 | 毫秒級 | 毫秒級 |
| 橫向擴展 | 自動 | 需手動分片 |
| 彈性結構 | 是 | 否 |
| 事務 | 有限 | 完全支援 |

### 適用場景

- 即時隨機存取巨量資料
- 稀疏資料儲存
- 時序資料處理
- 即時讀取的 web 應用

## 資料模型

### 表（Table）

HBase 中的表由多列族組成：

```
Table: user_actions
==================
Row Key         | Column Families
                | profile     | activity    | preferences
----------------|-------------|-------------|--------------
user123         | name: John  | clicks: 150 | theme: dark
                | email: j@.. | views: 320  | lang: zh-TW
----------------|-------------|-------------|--------------
user456         | name: Mary  | clicks: 89  | theme: light
```

### 列族（Column Family）

```bash
# 建立表的語法
create 'user_actions', 'profile', 'activity', 'preferences'
```

### 列（Column）

```
profile:name
profile:email
activity:clicks
```

### 細胞（Cell）

實際儲存的鍵值對，包含時間戳記：

```
(user123, profile, name, t1234567890) = "John"
```

### 時間戳記

每個單元格都有多個版本，依時間戳記區分：

```java
// 獲取所有版本
Get get = new Get(Bytes.toBytes("user123"));
get.addColumn(Bytes.toBytes("profile"), Bytes.toBytes("name"));
get.setMaxVersions(5);  // 最多 5 個版本
Result result = table.get(get);
```

## 安裝與設定

### 安裝 HBase

```bash
wget http://archive.apache.org/dist/hbase/hbase-0.18.0/hbase-0.18.0.tar.gz
tar -xzf hbase-0.18.0.tar.gz
export HBASE_HOME=/path/to/hbase
export PATH=$PATH:$HBASE_HOME/bin
```

### 設定 hbase-site.xml

```xml
<configuration>
    <property>
        <name>hbase.rootdir</name>
        <value>hdfs://namenode:9000/hbase</value>
    </property>
    <property>
        <name>hbase.cluster.distributed</name>
        <value>true</value>
    </property>
    <property>
        <name>hbase.zookeeper.property.dataDir</name>
        <value>/var/lib/zookeeper</value>
    </property>
</configuration>
```

### 啟動 HBase

```bash
# 啟動 HBase
start-hbase.sh

# 進入 shell
hbase shell
```

## HBase Shell 操作

### 建立表

```bash
# 基本表
create 'users', 'profile'

# 多列族
create 'user_actions', 'profile', 'activity', 'preferences'

# 設定屬性
create 'users', {NAME => 'profile', VERSIONS => 3}
```

### 寫入資料

```bash
# 單一 Put
put 'users', 'user123', 'profile:name', 'John'
put 'users', 'user123', 'profile:email', 'john@example.com'

# 批次 Put
put 'users', 'user456', 'profile:name', 'Mary'
```

### 讀取資料

```bash
# 取得一行
get 'users', 'user123'

# 取得特定列
get 'users', 'user123', 'profile:name'

# 取得多個版本
get 'users', 'user123', {COLUMN => 'profile:name', VERSIONS => 5}
```

### 掃描資料

```bash
# 掃描全表
scan 'users'

# 限制結果
scan 'users', {LIMIT => 10}

# 列过滤器
scan 'users', {COLUMNS => ['profile:name', 'profile:email']}
```

### 刪除資料

```bash
# 刪除單一儲存格
delete 'users', 'user123', 'profile:email'

# 刪除整行
deleteall 'users', 'user123'

# 刪除表
disable 'users'
drop 'users'
```

## Java API

### 配置連線

```java
Configuration config = HBaseConfiguration.create();
config.set("hbase.zookeeper.quorum", "zoo1,zoo2,zoo3");
config.set("hbase.zookeeper.property.clientPort", "2181");
HTable table = new HTable(config, "users");
```

### Put 操作

```java
Put put = new Put(Bytes.toBytes("user123"));
put.add(Bytes.toBytes("profile"), Bytes.toBytes("name"),
        Bytes.toBytes("John"));
put.add(Bytes.toBytes("profile"), Bytes.toBytes("email"),
        Bytes.toBytes("john@example.com"));
table.put(put);
```

### Get 操作

```java
Get get = new Get(Bytes.toBytes("user123"));
get.addColumn(Bytes.toBytes("profile"), Bytes.toBytes("name"));
Result result = table.get(get);
byte[] name = result.getValue(Bytes.toBytes("profile"),
                               Bytes.toBytes("name"));
String nameStr = Bytes.toString(name);
```

### Scan 操作

```java
Scan scan = new Scan();
scan.addColumn(Bytes.toBytes("profile"), Bytes.toBytes("name"));
ResultScanner scanner = table.getScanner(scan);
try {
    for (Result result : scanner) {
        System.out.println("Row: " +
            Bytes.toString(result.getRow()));
    }
} finally {
    scanner.close();
}
```

### 刪除操作

```java
Delete delete = new Delete(Bytes.toBytes("user123"));
delete.deleteColumn(Bytes.toBytes("profile"), Bytes.toBytes("email"));
table.delete(delete);
```

## 架構設計

### HBase 架構

```
┌─────────────────────────────────────────────────┐
│                   HBase 叢集                      │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌──────────┐    ┌─────────────────────────┐   │
│  │ ZooKeeper│    │       HBase Master      │   │
│  │  協調服務 │    │   (元數據、負載均衡)      │   │
│  └──────────┘    └────────────┬────────────┘   │
│                               │                 │
│  ┌──────────────────────────────────────────┐ │
│  │              RegionServer 叢集             │ │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐  │ │
│  │  │Region1   │ │Region2   │ │Region3   │  │ │
│  │  │Table-A   │ │Table-A   │ │Table-B   │  │ │
│  │  │          │ │          │ │          │  │ │
│  │  └──────────┘ └──────────┘ └──────────┘  │ │
│  └──────────────────────────────────────────┘ │
│                               │                 │
│                    ┌──────────┴──────────┐    │
│                    │         HDFS          │    │
│                    │   (實際資料儲存)       │    │
│                    └───────────────────────┘    │
└─────────────────────────────────────────────────┘
```

### Region

HBase 表自動分割為多個 Region：

- 每個 Region 包含連續的行範圍
- RegionServer 負責處理讀寫請求
- 當 Region 太大時，會自動分割

### WAL（Write-Ahead Log）

寫入分為兩步：
1. 寫入 WAL（確保持久性）
2. 寫入記憶體（提供快速讀取）

記憶體中的資料達到閾值後，刷寫到 HDFS 成為 StoreFile。

## 效能優化

### 列族設計

- 將相似存取模式的列放在同一列族
- 限制列族數量（建議 1-3 個）
- 設計寬表而非深表

### RowKey 設計

```
# 避免熱點
# 不好：001, 002, 003, 004 (順序寫入單一 Region)
# 好：hash(001) + 001 (分散到多個 Region)

# 支援範圍查詢
# 將時間戳記放在 key 末端
userId + reversed_timestamp
```

### 快取

```bash
# 設定快取
create 'users', {NAME => 'profile', BLOCKCACHE => 'true'}
```

## 結論

HBase 為巨量資料提供了即時讀寫能力。其與 HDFS 的整合、自動分割和副本機制，使其成為處理即時資料的理想選擇。

---

**延伸閱讀**

- [HDFS 分散式檔案系統](focus2.md)
- [MapReduce 分散式運算](focus1.md)
- [HBase+BigTable+paper](https://www.google.com/search?q=HBase+BigTable+Google+paper)