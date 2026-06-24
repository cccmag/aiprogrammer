# 即時特徵計算與儲存

## 即時特徵工程

即時推論依賴最新狀態，而非批次處理的歷史快照。使用者最後一次點擊、目前會話的平均停留時間、實時價格變動——這些特徵必須在毫秒內計算完成並寫入特徵儲存。

## Redis 即時特徵儲存

```python
import redis
import json
import time

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def update_user_features(user_id, event):
    # 使用 Pipeline 確保原子性
    pipe = r.pipeline()

    # 更新計數器
    pipe.hincrby(f'user:{user_id}:stats', 'click_count', 1)

    # 更新滑動視窗（保留最近 1000 筆）
    pipe.lpush(f'user:{user_id}:events', json.dumps(event))
    pipe.ltrim(f'user:{user_id}:events', 0, 999)

    # 設定 TTL（避免資料無限成長）
    pipe.expire(f'user:{user_id}:stats', 86400)
    pipe.expire(f'user:{user_id}:events', 3600)

    pipe.execute()

def get_user_features(user_id):
    stats = r.hgetall(f'user:{user_id}:stats')
    events = r.lrange(f'user:{user_id}:events', 0, -1)

    return {
        'click_count': int(stats.get('click_count', 0)),
        'recent_events': [json.loads(e) for e in events],
        'session_start': float(stats.get('session_start', 0)),
    }
```

## 特徵計算服務

即時特徵計算需要低延遲的無狀態服務：

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Event(BaseModel):
    user_id: str
    event_type: str
    value: float
    timestamp: int

@app.post("/features/compute")
async def compute_features(event: Event):
    # 從 Redis 讀取歷史資料
    stats = get_user_features(event.user_id)

    # 計算即時特徵
    features = {
        'avg_value': compute_moving_avg(event, stats),
        'event_rate': compute_rate(event, stats),
        'recency_score': compute_recency(event, stats),
        'trend': compute_trend(stats['recent_events']),
    }

    # 寫回特徵儲存
    update_user_features(event.user_id, event.model_dump())

    return features

def compute_moving_avg(event, stats):
    values = [e['value'] for e in stats['recent_events']]
    if not values:
        return event.value
    return (sum(values) + event.value) / (len(values) + 1)
```

## 滑動視窗計數

精確的視窗統計對即時推論至關重要：

```python
import bisect
from collections import deque

class SlidingWindowCounter:
    def __init__(self, window_sec=60):
        self.window = window_sec
        self.events = deque()

    def add(self, timestamp):
        self.events.append(timestamp)
        self._prune(timestamp)

    def count(self, now=None):
        now = now or time.time()
        self._prune(now)
        return len(self.events)

    def _prune(self, now):
        cutoff = now - self.window
        while self.events and self.events[0] < cutoff:
            self.events.popleft()
```

## TTL 與資料生命週期

即時特徵儲存不應該無限成長。合理的 TTL 策略：

| 特徵類型 | TTL | 儲存方案 |
|---------|-----|---------|
| 會話特徵 | 30 分鐘 | Redis |
| 使用者畫像 | 7 天 | Redis + SSD |
| 聚合統計 | 24 小時 | Redis |
| 原始事件 | 1 小時 | Kafka |

## 特徵新鮮度與模型準確度

實驗顯示，超過 5 分鐘的特徵會導致推薦模型的 AUC 下降 15-20%。即時特徵管線的延遲直接影響推論品質。

## 延伸閱讀

- [Redis 即時資料結構](https://www.google.com/search?q=Redis+real+time+data+structures+tutorial)
- [特徵儲存最佳實務](https://www.google.com/search?q=feature+store+best+practices+real+time)
- [滑動視窗演算法比較](https://www.google.com/search?q=sliding+window+algorithm+stream+processing)
