# Spark Structured Streaming

## 前言

Structured Streaming 是 Spark 2.0 引入的高層次串流處理 API，基於 Spark SQL 引擎，提供彈性和自動化的狀態管理。

## 基本概念

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import window, count

spark = SparkSession.builder \
    .appName("StructuredStreamingDemo") \
    .getOrCreate()

# 從 socket 讀取（測試用）
lines = spark.readStream \
    .format("socket") \
    .option("host", "localhost") \
    .option("port", 9999) \
    .load()

# 單詞計數
word_counts = lines \
    .withColumn("word", explode(split(lines.value, " "))) \
    .groupBy("word") \
    .count()

# 輸出到控制台
query = word_counts \
    .writeStream \
    .format("console") \
    .start()

query.awaitTermination()
```

## 水印和狀態管理

```python
# 使用水印處理延遲到達的資料

windowed_counts = lines \
    .withColumn("timestamp", current_timestamp()) \
    .withColumn("word", explode(split(lines.value, " "))) \
    .groupBy(
        window(col("timestamp"), "5 minutes"),
        col("word")
    ) \
    .count()

# 設定水印，允許最多 10 分鐘的延遲
query = windowed_counts \
    .writeStream \
    .format("parquet") \
    .option("checkpointLocation", "/tmp/checkpoint") \
    .outputMode("complete") \
    .start("/tmp/output")
```

## 延伸閱讀

- [Spark Structured Streaming 文件](https://www.google.com/search?q=Spark+Structured+Streaming+guide)

---

*本篇文章為「AI 程式人雜誌 2020 年 11 月號」文章集錦之一。*