# 主題七：NoSQL 在大數據的角色

## NoSQL 與大數據的關係

大數據時代催生了對新型資料庫的需求，而 NoSQL 正是這個時代的產物之一。NoSQL 資料庫的設計初衷就是為了處理 Volume（大量）、Velocity（高速）、Variety（多樣性）這三個大數據的核心特徵。

NoSQL 資料庫與 Hadoop 生態系的整合，使得處理大規模資料變得更加靈活和高效。

## 文件資料庫與 Hadoop

### MongoDB 與 Hadoop

MongoDB 提供了 MongoDB Connector for Hadoop，可以讓 Hadoop 直接讀取 MongoDB 的資料：

```python
# 使用 PySpark 從 MongoDB 讀取資料進行分析
from pyspark import SparkContext, SparkConf
from pymongo import MongoClient

conf = SparkConf().setAppName("MongoDB-Hadoop-Example")
sc = SparkContext(conf=conf)

# 連接到 MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['test']

# 假設有一個龐大的交易記錄集合
collection = db['transactions']

# 將資料轉換為 Spark RDD
data = list(collection.find({'amount': {'$gt': 100}}))
rdd = sc.parallelize(data)

# 使用 Spark 進行分析
total_amount = rdd.map(lambda x: x['amount']).reduce(lambda a, b: a + b)
print(f"總交易金額: {total_amount}")
```

### CouchDB 與 Hadoop

CouchDB 可以作為 Hadoop 的資料來源或沈沒（Sink），用於處理非結構化或半結構化資料。

## 即時分析與 NoSQL

### 記憶體資料庫的即時能力

Redis 和其他記憶體資料庫為即時分析提供了極低的延遲：

```python
# Redis 即時計數範例
import redis

client = redis.Redis(host='localhost', port=6379)

# 網站流量即時計數
def track_page_view(page_id, user_id):
    pipe = client.pipeline()
    # 總訪問量
    pipe.incr(f'pageviews:{page_id}')
    # 獨立訪客數
    pipe.sadd(f'unique:{page_id}', user_id)
    # 當前線上人數
    pipe.incr('online_users')
    # 5 分鐘後過期
    pipe.expire('online_users', 300)
    pipe.execute()

# 即時取得頁面統計
def get_page_stats(page_id):
    total = int(client.get(f'pageviews:{page_id}') or 0)
    unique = client.scard(f'unique:{page_id}')
    return {'total_views': total, 'unique_visitors': unique}
```

### 時序資料庫

時序資料庫（Time Series Database）是專門為時間序列資料設計的 NoSQL 變種：

- **InfluxDB**：專為 DevOps 和 IoT 設計
- **OpenTSDB**：基於 HBase 的時序資料庫
- **KairosDB**：基於 Cassandra 的時序資料庫

```python
# InfluxDB 時序資料寫入範例
from influxdb import InfluxDBClient

client = InfluxDBClient('localhost', 8086, 'root', 'root', 'mydb')

# 寫入時間序列資料
json_body = [
    {
        "measurement": "cpu_load_short",
        "time": "2009-11-10T23:00:00Z",
        "tags": {
            "host": "server01",
            "region": "us-west"
        },
        "fields": {
            "value": 0.64
        }
    }
]

client.write_points(json_body)
```

## NoSQL 與批次處理的結合

現代資料架構通常結合即時和批次處理：

### Lambda 架構

Lambda 架構是一種結合即時和批次處理的方法論：

```
         查詢
           |
    +------+------+
    |             |
  批次層         速度層
    |             |
    +------+------+
           |
       服務層
```

- **批次層**：處理完整的歷史資料，結果存入靜態存儲
- **速度層**：處理即時資料，提供低延遲的近似結果
- **服務層**：合併批次層和速度層的結果，回答查詢

### Kappa 架構

Kappa 架構是 Lambda 的簡化版本，只使用串流處理：

```python
# 簡化的 Kappa 架構範例
from kafka import KafkaConsumer, KafkaProducer

producer = KafkaProducer(bootstrap_servers='localhost:9092')
consumer = KafkaConsumer('events', bootstrap_servers='localhost:9092')

for message in consumer:
    event = parse_message(message)
    # 即時處理
    process_realtime(event)
    # 同時寫入持久化存儲供批次處理
    persist_to_storage(event)
```

## NoSQL 在大數據生態中的地位

### 資料來源

NoSQL 資料庫常作為大數據處理的資料來源：
- 使用 MongoDB 儲存營運資料
- 使用 Redis 儲存會話和快取資料
- 使用 HBase 儲存歷史歸檔資料

### 結果存儲

分析結果可以存回 NoSQL 資料庫：
- 即時儀表板的查詢結果
- 機器學習模型的預測結果
- 使用者推薦清單

### 常見模式

1. **ELK 堆疊**：Elasticsearch + Logstash + Kibana，用於日誌分析
2. **Hadoop + HBase**：批次處理結果的快速查詢
3. **Redis + 關聯式資料庫**：熱門資料快取，歷史資料存關聯式

## 未來趨勢

NoSQL 與大數據的結合正在演進：

- **多模型資料庫**：結合文件、圖形、鍵值等多種模型
- **HTAP**：混合事務和分析處理（Hybrid Transactional/Analytical Processing）
- **邊緣運算整合**：NoSQL 資料庫在邊緣設備上的應用

NoSQL 資料庫已成為現代大數據架構不可或缺的組成部分，為處理多樣化資料和支援各種應用場景提供了靈活的基礎設施。