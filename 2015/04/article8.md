# NoSQL 在即時分析的角色

## 即時分析的需求

在現代商業環境中，即時分析能力變得越來越重要。從網站流量監控到金融交易風控，各種場景都需要即時的資料處理能力。NoSQL 資料庫在這個領域扮演著關鍵角色。

## 即時分析的架構

### 典型架構

```
+-------------+     +-------------+     +-------------+
|  資料來源   | --> |  訊息佇列   | --> |  即時處理   |
+-------------+     +-------------+     +-------------+

                                            v
+-------------+     +-------------+     +-------------+
|  儀表板呈現 | <-- |  NoSQL 儲存  | <-- |  處理結果  |
+-------------+     +-------------+     +-------------+
```

### 常用技術組合

1. **訊息佇列**：Kafka、RabbitMQ
2. **即時處理**：Spark Streaming、Flink、Storm
3. **結果儲存**：Redis、Elasticsearch、MongoDB

## Redis 在即時分析中的應用

### 計數器與聚合

```python
import redis
import time

client = redis.Redis(decode_responses=True)

def track_event(event_type, event_data):
    """追蹤事件並即時更新計數"""
    pipe = client.pipeline()

    # 當前分鐘的計數
    minute_key = f"events:{event_type}:{time.strftime('%Y%m%d%H%M')}"
    pipe.incr(minute_key)
    pipe.expire(minute_key, 86400)  # 24小時過期

    # 小時計數
    hour_key = f"events:{event_type}:hour:{time.strftime('%Y%m%d%H')}"
    pipe.incr(hour_key)
    pipe.expire(hour_key, 86400 * 7)

    # 日計數
    day_key = f"events:{event_type}:day:{time.strftime('%Y%m%d')}"
    pipe.incr(day_key)
    pipe.expire(day_key, 86400 * 365)

    pipe.execute()

def get_event_stats(event_type, period='hour'):
    """取得事件統計"""
    if period == 'hour':
        key = f"events:{event_type}:hour:{time.strftime('%Y%m%d%H')}"
    elif period == 'day':
        key = f"events:{event_type}:day:{time.strftime('%Y%m%d')}"

    return int(client.get(key) or 0)
```

### 即時排行榜

```python
def update_leaderboard(game_id, player_id, score):
    """更新遊戲排行榜"""
    key = f"leaderboard:{game_id}"

    # 使用有序集合，自動排序
    client.zadd(key, {str(player_id): score})

def get_top_players(game_id, count=10):
    """取得 top N 玩家"""
    key = f"leaderboard:{game_id}"
    return client.zrevrange(key, 0, count - 1, withscores=True)
```

## 時序資料庫

### InfluxDB 的使用

```python
from influxdb import InfluxDBClient

client = InfluxDBClient('localhost', 8086, 'root', 'root', 'mydb')

def write_metric(measurement, tags, fields):
    """寫入時序資料"""
    json_body = [{
        "measurement": measurement,
        "tags": tags,
        "fields": fields,
        "time": datetime.utcnow().isoformat()
    }]
    client.write_points(json_body)

def query_recent(measurement, duration='1h'):
    """查詢最近的資料"""
    query = f"""
    SELECT * FROM {measurement}
    WHERE time > now() - {duration}
    """
    return client.query(query)
```

## 即時儀表板

### 結合 Socket.IO

```python
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import threading
import time

app = Flask(__name__)
socketio = SocketIO(app)

def background_task():
    """背景任務：持續發送更新"""
    while True:
        # 從 Redis 或其他來源取得資料
        stats = get_real_time_stats()

        # 廣播到所有客戶端
        socketio.emit('stats_update', stats)
        time.sleep(1)

@app.route('/')
def index():
    return render_template('dashboard.html')

@socketio.on('connect')
def handle_connect():
    print('客戶端連線')

if __name__ == '__main__':
    # 啟動背景任務
    thread = threading.Thread(target=background_task)
    thread.daemon = True
    thread.start()

    socketio.run(app, host='0.0.0.0', port=5000)
```

## 效能考量

### 寫入優化

- 使用批次寫入減少網路往返
- 評估寫入一致性需求，選擇合適的 Write Concern
- 考慮記憶體資料庫作為寫入缓冲

### 讀取優化

- 使用讀寫分離
- Redis 快取熱門資料
- 儀表板查詢使用聚合結果而非原始資料

### 資料保留策略

```python
def setup_retention_policy():
    """設定資料保留策略"""
    client = InfluxDBClient(...)

    # 建立保留策略
    client.create_retention_policy(
        'one_day',
        '1d',
        1,  # 副本數
        default=True
    )

    client.create_retention_policy(
        'one_week',
        '7d',
        1,
        default=False
    )

    client.create_retention_policy(
        'infinite',
        'INF',
        1,
        default=False
    )
```

## 實際案例

### 電子商務即時儀表板

```python
class EcommerceDashboard:
    def __init__(self):
        self.redis = redis.Redis()

    def track_page_view(self, page_id, user_id):
        """追蹤頁面瀏覽"""
        pipe = self.redis.pipeline()

        now = datetime.now()
        minute_key = f"pv:{now.strftime('%Y%m%d%H%M')}"
        page_key = f"page:{page_id}:{minute_key}"

        pipe.incr(page_key)
        pipe.expire(page_key, 90000)
        pipe.sadd(f"visitors:{minute_key}", user_id)
        pipe.execute()

    def get_dashboard_data(self):
        """取得儀表板資料"""
        now = datetime.now()
        minute_key = now.strftime('%Y%m%d%H%M')

        return {
            'page_views_last_minute': self.redis.get(f"pv:{minute_key}") or 0,
            'unique_visitors_last_minute': self.redis.scard(f"visitors:{minute_key}"),
            'active_users': self.redis.get('active_users') or 0
        }
```

## 總結

NoSQL 資料庫，特別是 Redis 和時序資料庫，在即時分析領域有著不可替代的作用。選擇合適的技術和架構，能夠支撐起各類即時分析和監控需求。