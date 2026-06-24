# Hive 資料倉儲系統

## Hive 簡介

Hive 是建立在 Hadoop 之上的資料倉儲系統，最初由 Facebook 開發並貢獻給 Apache。它提供類似 SQL 的查詢語言（HiveQL），讓熟悉傳統資料庫的開發者能夠輕鬆處理巨量資料。

### 與傳統資料庫的比較

| 特性 | Hive | 傳統 RDBMS |
|------|------|------------|
| 查詢語言 | HiveQL (SQL-like) | SQL |
| 儲存 | HDFS | 區塊儲存 |
| 處理引擎 | MapReduce | 原生引擎 |
| 延遲 | 高（秒級到分鐘） | 低（毫秒級） |
| 資料規模 | PB 等級 | GB 等級 |
| 事務支援 | 有限 | 完全支援 |

## 安裝與設定

### 安裝 Hive

```bash
wget http://archive.apache.org/dist/hive/hive-0.18.0/hive-0.18.0.tar.gz
tar -xzf hive-0.18.0.tar.gz
export HIVE_HOME=/path/to/hive
export PATH=$PATH:$HIVE_HOME/bin
```

### 設定 Metastore

Hive 需要一個關聯式資料庫儲存元數據：

```bash
# 使用 Derby（單機）
export HIVE_HOME=/path/to/hive
cp $HIVE_HOME/conf/hive-default.xml $HIVE_HOME/conf/hive-site.xml

# 編輯 hive-site.xml
<property>
    <name>javax.jdo.option.ConnectionURL</name>
    <value>jdbc:derby:;databaseName=/path/to/metastore_db;create=true</value>
</property>
```

### 啟動 Hive

```bash
# 進入 CLI
hive

# 或使用 HWI（HTTP 接口）
hive --service hwi
```

## 基本操作

### 建立資料庫

```sql
CREATE DATABASE IF NOT EXISTS web_logs;
USE web_logs;
```

### 建立表格

```sql
-- 內部表（由 Hive 管理）
CREATE TABLE page_views (
    view_time INT,
    user_id BIGINT,
    page_url STRING,
    referrer STRING,
    ip STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
STORED AS TEXTFILE;

-- 外部表（資料由外部管理）
CREATE EXTERNAL TABLE page_views_ext (
    view_time INT,
    user_id BIGINT,
    page_url STRING,
    referrer STRING,
    ip STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
LOCATION '/user/hduser/external/page_views';
```

### 載入資料

```sql
-- 從 HDFS 載入
LOAD DATA INPATH '/user/hduser/data/page_views.txt'
INTO TABLE page_views;

-- 從本機檔案載入
LOAD DATA LOCAL INPATH '/local/data/page_views.txt'
INTO TABLE page_views;
```

### 查詢資料

```sql
-- 基本查詢
SELECT * FROM page_views WHERE user_id > 100;

-- 聚合查詢
SELECT user_id, COUNT(*) as views
FROM page_views
GROUP BY user_id
HAVING COUNT(*) > 10;

-- JOIN 查詢
SELECT u.name, p.page_url
FROM users u
JOIN page_views p ON u.id = p.user_id;
```

## HiveQL 語法

### SELECT 語句

```sql
-- 基本 SELECT
SELECT col1, col2 FROM table1;

-- 運算式
SELECT col1, col2, col3 * 10 as col3_times_10 FROM table1;

-- CASE WHEN
SELECT
    CASE
        WHEN col1 > 100 THEN 'high'
        WHEN col1 > 50 THEN 'medium'
        ELSE 'low'
    END as category
FROM table1;

-- DISTINCT
SELECT DISTINCT col1 FROM table1;
```

### 聚合函數

```sql
-- 基本聚合
SELECT COUNT(*), SUM(col1), AVG(col1), MIN(col1), MAX(col1)
FROM table1;

-- 多重聚合
SELECT user_id, COUNT(*) as cnt, SUM(amount) as total
FROM orders
GROUP BY user_id;

-- HAVING
SELECT user_id, COUNT(*) as cnt
FROM orders
GROUP BY user_id
HAVING COUNT(*) > 5;
```

### JOIN

```sql
-- INNER JOIN
SELECT a.col1, b.col2
FROM table1 a
JOIN table2 b ON a.id = b.id;

-- LEFT OUTER JOIN
SELECT a.col1, b.col2
FROM table1 a
LEFT OUTER JOIN table2 b ON a.id = b.id;

-- 多重 JOIN
SELECT a.col1, b.col2, c.col3
FROM table1 a
JOIN table2 b ON a.id = b.id
JOIN table3 c ON b.id = c.id;
```

### 子查詢

```sql
SELECT col1
FROM (SELECT col1, col2 FROM table1) subq
WHERE col2 > 10;
```

## 函數

### 內建函數

```sql
-- 字串函數
SELECT CONCAT('Hello', ' ', 'World');
SELECT SUBSTR('Hello', 1, 3);
SELECT UPPER('hello');
SELECT LOWER('WORLD');

-- 日期函數
SELECT FROM_UNIXTIME(UNIX_TIMESTAMP());
SELECT TO_DATE('2008-04-15 10:30:00');

-- 條件函數
SELECT IF(price > 100, 'expensive', 'cheap') FROM products;
```

### 使用者自訂函數（UDF）

```java
import org.apache.hadoop.hive.ql.exec.UDF;
import org.apache.hadoop.io.Text;

public class MyUDF extends UDF {
    public Text evaluate(Text input) {
        if (input == null) return null;
        return new Text(input.toString().toUpperCase());
    }
}
```

### 註冊和使用 UDF

```sql
-- 臨時函數
CREATE TEMPORARY FUNCTION my_upper AS 'com.example.MyUDF';
SELECT my_upper(name) FROM users;

-- 永久函數（需新增 JAR）
ADD JAR /path/to/udf.jar;
CREATE FUNCTION my_upper AS 'com.example.MyUDF';
```

## 分割區（Partitioning）

分割區可以加速查詢：

```sql
-- 建立分割區表
CREATE TABLE page_views_partitioned (
    user_id BIGINT,
    page_url STRING,
    referrer STRING
)
PARTITIONED BY (dt STRING)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t';

-- 動態插入分割區
SET hive.exec.dynamic.partition=true;
SET hive.exec.dynamic.partition.mode=nonstrict;

INSERT OVERWRITE TABLE page_views_partitioned
PARTITION (dt)
SELECT user_id, page_url, referrer, dt
FROM page_views;
```

### 查詢分割區

```sql
-- 只查詢特定分割區
SELECT * FROM page_views_partitioned WHERE dt = '2008-04-15';

-- 多分割區查詢
SELECT * FROM page_views_partitioned
WHERE dt >= '2008-04-01' AND dt < '2008-05-01';
```

## 儲存格式

### TEXTFILE

```sql
STORED AS TEXTFILE
```

### SEQUENCEFILE

```sql
STORED AS SEQUENCEFILE
```

### RCFile（行-列儲存）

```sql
STORED AS RCFILE
```

### 壓縮

```sql
SET hive.exec.compress.output=true;
SET mapred.output.compression.codec=org.apache.hadoop.io.compress.GzipCodec;

CREATE TABLE compressed AS
SELECT * FROM page_views;
```

## 效能調校

### 避免全表掃描

```sql
-- 使用分割區
WHERE dt = '2008-04-15'

-- 使用 TABLESAMPLE
SELECT * FROM page_views TABLESAMPLE(10 PERCENT);
```

### JOIN 優化

```sql
-- 大表在前
INSERT OVERWRITE TABLE result
SELECT /*+ MAPJOIN(b) */ a.id, a.value, b.name
FROM large_table a
JOIN small_table b ON a.id = b.id;
```

### 控制 MapReduce 任務數

```sql
SET mapred.map.tasks = 10;
SET mapred.reduce.tasks = 5;
```

## 結論

Hive 為巨量資料處理提供了一個親民的 SQL 介面。雖然查詢延遲較高，但其強大的聚合能力和 SQL 相容性使其成為資料倉儲的理想選擇。

---

**延伸閱讀**

- [MapReduce 分散式運算](focus1.md)
- [HBase 即時資料庫](focus6.md)
- [Hive+documentation](https://www.google.com/search?q=Apache+Hive+documentation)