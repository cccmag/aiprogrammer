# 大資料與 Hadoop 生態系

## 前言

大資料處理是現代資料工程的重要領域，Hadoop 是這個領域的核心框架。

---

## Hadoop 核心元件

### HDFS (Hadoop Distributed File System)

分散式檔案系統，設計用於儲存大規模資料。

```
┌─────────────────────────────────────────────┐
│                NameNode                    │
│         (元資料管理)                        │
└──────────────┬──────────────────────────────┘
               │
┌──────────────┴──────────────────────────────┐
│              DataNodes                      │
│  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐    │
│  │ DN  │  │ DN  │  │ DN  │  │ DN  │    │
│  └──────┘  └──────┘  └──────┘  └──────┘    │
└─────────────────────────────────────────────┘
```

### MapReduce

分散式計算框架。

```
Input → Map → Shuffle → Reduce → Output
```

### YARN

資源管理員。

```bash
# Hadoop 命令列
hdfs dfs -ls /user
hdfs dfs -mkdir /user/hadoop
hdfs dfs -put localfile /user/hadoop/
```

---

## Hadoop 生態系

| 工具 | 功能 |
|------|------|
| Hive | SQL 查詢介面 |
| Pig | 資料流程語言 |
| HBase | NoSQL 資料庫 |
| Sqoop | 資料庫同步 |
| Flume | 日誌收集 |
| Kafka | 訊息佇列 |
| Spark | 記憶體計算 |
| Impala | 即時查詢 |

---

## Spark

### 與 MapReduce 的比較

| 特性 | MapReduce | Spark |
|------|-----------|-------|
| 處理速度 | 慢 | 快（記憶體） |
| 處理模型 | 批次 | 批次/串流 |
| API | Java | Scala/Python/Java |
| 圖形處理 | 外掛 | GraphX |

### Spark RDD

```python
from pyspark import SparkContext

sc = SparkContext("local", "App")
data = [1, 2, 3, 4, 5]
distData = sc.parallelize(data)
result = distData.reduce(lambda a, b: a + b)
print(result)
```

### Spark DataFrame

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("App").getOrCreate()
df = spark.read.json("people.json")
df.filter(df.age > 21).show()
df.createOrReplaceTempView("people")
spark.sql("SELECT * FROM people WHERE age > 21").show()
```

[搜尋 Apache Spark tutorial](https://www.google.com/search?q=Apache+Spark+tutorial+Python)

---

## 資料處理流程

### 批次處理

```bash
# 使用 Hive
hive -e "SELECT * FROM logs WHERE date = '2025-01-01'"
```

### 即時處理

```python
# 使用 Spark Streaming
from pyspark.streaming import StreamingContext

ssc = StreamingContext(sc, 1)
lines = ssc.socketTextStream("localhost", 9999)
counts = lines.flatMap(lambda line: line.split(" ")) \
              .map(lambda word: (word, 1)) \
              .reduceByKey(lambda a, b: a + b)
counts.pprint()
ssc.start()
ssc.awaitTermination()
```

---

## Hadoop 安裝與使用

### 單機安裝

```bash
# 下載
wget http://apache.stu.edu.tw/hadoop/common/hadoop-2.7.0/hadoop-2.7.0.tar.gz
tar -xzf hadoop-2.7.0.tar.gz

# 設定環境
export HADOOP_HOME=/path/to/hadoop-2.7.0
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
```

### 偽分散式模式

```xml
<!-- core-site.xml -->
<configuration>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://localhost:9000</value>
    </property>
</configuration>
```

---

## 雲端大資料服務

| 服務 | 說明 |
|------|------|
| AWS EMR | 托管 Hadoop/Spark |
| Google Dataproc | 托管 Hadoop/Spark |
| Azure HDInsight | 托管 Hadoop 生態系 |
| Amazon Redshift | 資料倉儲 |
| Google BigQuery | 無限擴展的 SQL |

---

## 小結

Hadoop 生態系提供了完整的大資料處理解決方案，了解這些工具能幫助你處理大規模資料。

---

*作者：AI 程式人團隊*

*延伸閱讀：*
- [Apache Hadoop 官方網站](https://hadoop.apache.org/)
- [Apache Spark 官方網站](https://spark.apache.org/)
- [Hadoop 生態系介紹](https://www.google.com/search?q=Hadoop+ecosystem+components)