# 設計 Twitter 系統架構

## 從百萬到十億用戶的架構演進之路

## 需求分析

### 功能需求

1. 發布推文（Post Tweet）
2. 查看時間線（Timeline）— 首頁時間線 + 用戶時間線
3. 關注/取消關注用戶（Follow/Unfollow）
4. 搜尋推文（Search）
5. 通知（Notification）

### 非功能需求

- **月活用戶**：3 億
- **每日推文量**：3 億條
- **時間線 QPS**：約 30 萬次/秒
- **讀寫比例**：約 300:1
- **延遲要求**：時間線載入 < 500ms

### 規模估算

```
每日推文：3 億條
每條推文：約 1 KB（含文字、媒體連結、中繼資料）
每日新增儲存：3億 × 1KB ≈ 286 GB
每月：8.4 TB
五年：~500 TB

每日時間線請求：30 萬 QPS × 86400 ≈ 26 億次
每年時間線請求：約 9500 億次
```

---

## 高層次架構

```
              ┌──────────┐
              │  Clients │
              └────┬─────┘
                   │
              ┌────▼─────┐
              │   CDN    │（靜態資源）
              └────┬─────┘
                   │
              ┌────▼─────┐
              │   LB     │（負載平衡器）
              └────┬─────┘
                   │
          ┌────────┼────────┐
          │        │        │
    ┌─────▼──┐ ┌──▼────┐ ┌─▼──────┐
    │ Write  │ │ Read  │ │ Search │
    │ Service│ │ Service│ │Service │
    └────┬───┘ └───┬───┘ └───┬────┘
         │         │         │
    ┌────▼──┐ ┌────▼───┐ ┌──▼─────┐
    │ Fanout│ │ Cache  │ │ Elastic│
    │Service│ │(Redis) │ │ Search │
    └────┬──┘ └────────┘ └────────┘
         │
    ┌────▼──┐
    │ Tweet │
    │ Store │
    └───────┘
```

---

## 核心功能設計

### 發布推文

#### 寫入流程

```
1. 用戶發送推文 → API Gateway → Write Service
2. Write Service 將推文寫入 Tweet Store
3. 觸發 Fanout Service：
   a. 取得用戶的所有粉絲
   b. 將推文 ID 寫入每個粉絲的時間線快取
4. 回傳成功給用戶
```

#### Fanout 策略

**推模式（Fanout on Write）**：
```
發布推文後，立即將推文寫入所有粉絲的時間線快取。

優點：讀取時間線時只需讀取快取（O(1)）
缺點：百萬粉絲的用戶發布推文時，需要寫入百萬次
```

**拉模式（Fanout on Read）**：
```
不預先寫入，讀取時間線時再合併。

優點：寫入開銷小
缺點：讀取時間線需要合併多個來源（O(N)）
```

**混合策略（Twitter 實際做法）**：

```python
class FanoutService:
    def fanout(self, tweet, author_id):
        followers = self.get_followers(author_id)
        # 對普通用戶：推模式
        for follower in followers["normal"]:
            timeline_key = f"timeline:{follower}"
            redis.lpush(timeline_key, tweet.id)
            redis.ltrim(timeline_key, 0, 800)
        # 對大 V：粉絲拉模式
        for follower in followers["massive"]:
            # 不預先寫入，由粉絲自己拉
            pass

    def get_timeline(self, user_id):
        # 合併推模式和拉模式的推文
        pushed_tweets = redis.lrange(f"timeline:{user_id}", 0, 199)
        pulled_tweets = self.get_massive_followers_tweets(user_id)
        return merge(pushed_tweets, pulled_tweets)
```

### 時間線生成

```python
class TimelineService:
    def __init__(self, redis_client, tweet_store):
        self.redis = redis_client
        self.tweet_store = tweet_store

    def get_home_timeline(self, user_id, page=1, size=20):
        # 1. 從快取取得推文 ID 列表
        timeline_key = f"timeline:{user_id}"
        tweet_ids = self.redis.lrange(
            timeline_key,
            (page - 1) * size,
            page * size - 1
        )

        # 2. 從推文儲存取得完整推文
        tweets = self.tweet_store.get_tweets(tweet_ids)

        # 3. 填充用戶資訊（快取）
        tweets = self._enrich_users(tweets)

        return tweets

    def _enrich_users(self, tweets):
        user_ids = {t.user_id for t in tweets}
        users = self.user_cache.get_batch(user_ids)
        for t in tweets:
            t.user = users[t.user_id]
        return tweets
```

---

## 資料庫設計

### 推文儲存

```sql
-- 主表：按 tweet_id 分片
CREATE TABLE tweets (
    id BIGINT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    content TEXT,
    media_ids JSON,
    created_at TIMESTAMP,
    INDEX idx_user_id_created (user_id, created_at)
) PARTITION BY HASH(id) PARTITIONS 64;
```

### 關注關係

```python
# 使用 Redis Set 儲存關注關係
class FollowGraph:
    def follow(self, follower_id, followee_id):
        redis.sadd(f"follows:{follower_id}", followee_id)
        redis.sadd(f"followers:{followee_id}", follower_id)

    def unfollow(self, follower_id, followee_id):
        redis.srem(f"follows:{follower_id}", followee_id)
        redis.srem(f"followers:{followee_id}", follower_id)

    def get_followers(self, user_id):
        return redis.smembers(f"followers:{user_id}")

    def get_following(self, user_id):
        return redis.smembers(f"follows:{user_id}")
```

---

## 快取策略

```
第一層：CDN（靜態資源、圖片、影片）
第二層：Redis Cluster（時間線快取）
  - timeline:{user_id} → 前 800 條推文 ID
  - tweet:{tweet_id} → 推文內容（JSON）
  - user:{user_id} → 用戶資訊
  - follow_count:{user_id} → 粉絲/關注數

第三層：資料庫快取（MySQL Buffer Pool）
```

### 快取淘汰策略

```python
class TimelineCache:
    TWEETS_PER_PAGE = 20
    MAX_CACHED = 800  # 最多快取 800 條

    def add_tweet(self, user_id, tweet_id):
        key = f"timeline:{user_id}"
        redis.lpush(key, tweet_id)
        redis.ltrim(key, 0, self.MAX_CACHED - 1)

    def get_tweets(self, user_id, page):
        key = f"timeline:{user_id}"
        start = (page - 1) * self.TWEETS_PER_PAGE
        end = start + self.TWEETS_PER_PAGE - 1
        return redis.lrange(key, start, end)
```

---

## 搜尋功能

使用 Elasticsearch 實現全文搜尋。

```python
class SearchService:
    def __init__(self, es_client):
        self.es = es_client

    def index_tweet(self, tweet):
        self.es.index(
            index="tweets",
            id=tweet.id,
            body={
                "content": tweet.content,
                "user_id": tweet.user_id,
                "created_at": tweet.created_at,
                "hashtags": self._extract_hashtags(tweet.content)
            }
        )

    def search(self, query, page=1, size=20):
        result = self.es.search(
            index="tweets",
            body={
                "query": {
                    "match": {"content": query}
                },
                "sort": [{"created_at": "desc"}],
                "from": (page - 1) * size,
                "size": size
            }
        )
        return [hit["_source"] for hit in result["hits"]["hits"]]
```

---

## 瓶頸與解決方案

### 瓶頸一：熱門用戶的 Fanout

```
問題：Elon Musk 發布推文 → 1 億粉絲 → 寫入 1 億次快取
解決：大 V 使用拉模式，普通用戶使用推模式
```

### 瓶頸二：時間線延遲

```
問題：長時間未上線的用戶，時間線需累積大量推文
解決：增量載入，僅載入上次登入後的推文
```

### 瓶頸三：推文儲存

```
問題：500 TB 的推文資料，單機無法存放
解決：按 tweet_id 分片（64 個分片），Hot/Warm/Cold 分層儲存
```

---

## 總結

設計 Twitter 這樣的系統需要在多個維度做出取捨：

- 推模式 vs 拉模式（寫入開銷 vs 讀取延遲）
- 強一致性 vs 最終一致性（時間線允許短暫不一致）
- 快取層次（成本 vs 速度）
- 分片策略（均勻分佈 vs 查詢效率）

Twitter 的架構證明了：沒有一種設計適合所有規模。隨著用戶成長，架構需要持續演進。

---

## 延伸閱讀

- [Twitter System Design](https://www.google.com/search?q=Twitter+system+design+architecture)
- [Timeline Fanout Service](https://www.google.com/search?q=fanout+service+timeline+twitter)
- [Scaling Twitter](https://www.google.com/search?q=scaling+twitter+engineering+blog)

---

*本篇文章為「AI 程式人雜誌 2026 年 11 月號」文章系列之十。*
