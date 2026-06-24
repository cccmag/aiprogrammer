# Apache Spark 核心概念：記憶體優先的分散式運算

## Spark 簡介

Apache Spark 是一個統一的大規模資料處理引擎，提供了 Java、Scala、Python 和 R 的 API：

```
Spark 定位：
────────────────────────────────

Spark 是 Hadoop MapReduce 的繼承者和增強者：

Hadoop MapReduce：                  Spark：
- 中間結果寫磁片                   - 中間結果存記憶體
- 高延遲                           - 低延遲
- 只支援 Map/Reduce               - 支援 SQL、串流、機器學習
- 磁片 I/O 瓶頸                    - 記憶體運算
```

## RDD 核心概念

### RDD 是什麼？

RDD（Resilient Distributed Dataset）是 Spark 的核心抽象，代表一個不可變的、分區的記錄集合：

```python
# Spark RDD 基本操作
from pyspark import SparkContext

sc = SparkContext("local", "MyApp")

# 從記憶體建立 RDD
data = [1, 2, 3, 4, 5]
rdd = sc.parallelize(data, 4)  # 4 個分區

# 轉換操作（懶惰評估）
squared = rdd.map(lambda x: x ** 2)
filtered = rdd.filter(lambda x: x > 2)

# 動作操作（觸發執行）
result = filtered.collect()  # [3, 4, 5]
```

### RDD 的特性

```
RDD 五大特性：
────────────────────────────────

1. 分區列表
   └── RDD 被劃分為多個分區，每個分區可以在不同節點上計算
   
2. 計算函數
   └── 每個分區上執行的計算函數
   
3. 依賴其他 RDD
   └── RDD 之間的血統關係（lineage）
   
4. 分區器（可選）
   └── 如何分割鍵值對 RDD
   
5. 位置偏好（可選）
   └── 分區最佳化的位置提示
```

### RDD 轉換和動作

```python
# 常用轉換操作
rdd = sc.parallelize([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

# map: 對每個元素執行函數
squared = rdd.map(lambda x: x ** 2)

# filter: 過濾元素
evens = rdd.filter(lambda x: x % 2 == 0)

# flatMap: 類似 map，但展開結果
words = rdd.flatMap(lambda x: str(x).split())

# groupByKey: 將鍵值對按鍵分組
pairs = rdd.map(lambda x: (x % 3, x))  # (key, value)
grouped = pairs.groupByKey()  # (key, [values])

# reduceByKey: 合併相同鍵的值
counts = pairs.reduceByKey(lambda a, b: a + b)

# 動作操作
result = rdd.collect()           # 收集到驅動程式
count = rdd.count()              # 元素數量
first = rdd.first()              # 第一個元素
sample = rdd.take(5)             # 取樣
total = rdd.reduce(lambda a, b: a + b)  # 聚合
```

## DataFrame 和 Dataset

### 為什麼需要 DataFrame？

DataFrame 提供了更高層次的抽象，類似於傳統資料庫的表：

```python
# DataFrame API
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("DataFrame Demo") \
    .getOrCreate()

# 從 JSON 建立 DataFrame
df = spark.read.json("people.json")

# 類似 pandas 的 API
df.show()                        # 顯示資料
df.printSchema()                 # 顯示結構
df.select("name", "age")         # 選擇欄位
df.filter(df.age > 30)           # 過濾
df.groupBy("gender").avg("age") # 聚合
df.orderBy("age")                # 排序

# SQL 查詢
df.createOrReplaceTempView("people")
result = spark.sql("SELECT * FROM people WHERE age > 30")
```

### DataFrame 優勢

```
DataFrame vs RDD：
────────────────────────────────

DataFrame 優勢：
1. 類似 SQL 的高層次 API
2. 自動最佳化（Catalyst 優化器）
3. 結構化資料支援
4. 更好的類型安全（Dataset）
5. 記憶體列式儲存（Tungsten）

效能提升：10-100x（在許多場景下）
```

## 懶惰評估與 DAG

### 懶惰評估（Lazy Evaluation）

Spark 的轉換操作是懶惰的，只記錄轉換，不立即執行：

```python
# 懶惰評估示例
rdd = sc.parallelize([1, 2, 3, 4, 5])

# 這裡只是記錄操作，不實際執行
result = rdd.map(lambda x: x * 2).filter(lambda x: x > 4).map(lambda x: x + 1)

# 只有遇到動作操作時才真正執行
print(result.collect())  # [7, 9, 11]
```

### DAG 和血統追蹤

```python
# RDD 血統追蹤（Lineage）
rdd1 = sc.parallelize([1, 2, 3, 4, 5])
rdd2 = rdd1.map(lambda x: x * 2)   # rdd2 依賴 rdd1
rdd3 = rdd2.filter(lambda x: x > 3) # rdd3 依賴 rdd2
rdd4 = rdd3.map(lambda x: x + 1)     # rdd4 依賴 rdd3

# 查看血統
print(rdd4.toDebugString())
# (4) Map at <console>:1 []
#  |  Map at <console>:1 []
#  |  Filter at <console>:1 []
#  |  Map at <console>:1 []
#  |  ParallelCollectionRDD[0] at parallelize at SparkContext.scala
```

### Catalyst 優化器

DataFrame 使用 Catalyst 進行查詢優化：

```
Catalyst 優化流程：
────────────────────────────────

SQL/DataFrame 查詢
        │
        ▼
 分析（Analysis）──► 解析 SQL、分析 Column
        │
        ▼
 邏輯計劃（Logical Plan）
        │
        ▼
 優化（Optimization）──► 謂詞下推、投影裁剪、常數折疊
        │
        ▼
 優化後的邏輯計劃
        │
        ▼
 物理計劃（Physical Plan）──► 選擇執行策略
        │
        ▼
 選擇的最佳執行計劃
        │
        ▼
 RDD 操作
```

## 共享變數

### Broadcast 變數

用於在所有節點上快取一個值：

```python
# Broadcast 變數
lookup_table = {"a": 1, "b": 2, "c": 3}
broadcast_var = sc.broadcast(lookup_table)

# 在 Map 中使用廣播變數
rdd = sc.parallelize(["a", "b", "c", "a"])
result = rdd.map(lambda x: broadcast_var.value.get(x, 0)).collect()
# [1, 2, 3, 1]
```

### Accumulator

用於計數器等彙總操作：

```python
# Accumulator
accum = sc.accumulator(0)

def count_odds(x):
    global accum
    if x % 2 == 1:
        accum += 1
    return x

rdd = sc.parallelize([1, 2, 3, 4, 5])
rdd.foreach(count_odds)

print(accum.value)  # 3
```

## 延伸閱讀

- [Apache Spark 官方網站](https://www.google.com/search?q=Apache+Spark+official)
- [Spark Programming Guide](https://www.google.com/search?q=Spark+Programming+Guide+Python)
- [RDD API Documentation](https://www.google.com/search?q=Spark+RDD+API+documentation)
- [DataFrame 和 Dataset](https://www.google.com/search?q=Spark+DataFrame+Dataset+guide)
- [Spark SQL 優化](https://www.google.com/search?q=Spark+SQL+optimization+Catalyst)

---

*本篇文章為「AI 程式人雜誌 2020 年 11 月號」歷史回顧系列之一。*