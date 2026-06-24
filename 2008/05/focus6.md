# Redis 記憶體鍵值儲存

## Redis 概述

Redis 是一個記憶體鍵值儲存，以高效能和豐富的資料結構聞名。2008 年 Redis 1.0 發布，迅速成為最受歡迎的鍵值資料庫之一。

### 特點

- **記憶體儲存**：極速讀寫
- **豐富資料結構**：字串、雜湊、列表、集合、有序集合
- **持久化**：可選 RDB 或 AOF
- **發布/訂閱**：支援訊息佇列
- **Lua 腳本**：原子操作

## 安裝與設定

### 安裝 Redis

```bash
wget http://redis.googlecode.com/files/redis-1.2.6.tar.gz
tar -xzf redis-1.2.6.tar.gz
cd redis-1.2.6
make
```

### 啟動服務

```bash
# 啟動伺服器
./redis-server

# 連接客戶端
./redis-cli
```

## 基本資料結構

### 字串（String）

```bash
# 設定和讀取
SET name "John"
GET name

# 數值操作
SET counter 1
INCR counter
INCRBY counter 5

# 過期時間
SET key "value" EX 10
```

### 雜湊（Hash）

```bash
# 設定欄位
HSET user:123 name "John"
HSET user:123 email "john@example.com"

# 讀取
HGET user:123 name

# 讀取所有欄位
HGETALL user:123

# 欄位操作
HINCRBY user:123 age 1
```

### 列表（List）

```bash
# 左側插入
LPUSH mylist "a"
LPUSH mylist "b"

# 右側插入
RPUSH mylist "c"

# 讀取範圍
LRANGE mylist 0 -1

# 彈出
LPOP mylist
```

### 集合（Set）

```bash
# 新增成員
SADD tags "python"
SADD tags "mongodb"

# 讀取成員
SMEMBERS tags

# 判斷成員
SISMEMBER tags "python"

# 集合操作
SINTER set1 set2  # 交集
SUNION set1 set2  # 聯集
```

### 有序集合（Sorted Set）

```bash
# 新增成員
ZADD leaderboard 100 "John"
ZADD leaderboard 90 "Mary"

# 按分數範圍查詢
ZRANGEBYSCORE leaderboard 90 100

# 排名
ZRANK leaderboard "John"
```

## Python API

### 使用 redis-py

```python
import redis

# 連接
r = redis.Redis(host='localhost', port=6379)

# 字串操作
r.set('name', 'John')
name = r.get('name')

# 計數器
r.set('counter', 0)
r.incr('counter')
print(r.get('counter'))

# 雜湊操作
r.hset('user:123', 'name', 'John')
r.hset('user:123', 'email', 'john@example.com')
user = r.hgetall('user:123')
print(user)

# 列表操作
r.lpush('mylist', 'a')
r.lpush('mylist', 'b')
items = r.lrange('mylist', 0, -1)
print(items)

# 集合操作
r.sadd('tags', 'python', 'mongodb')
tags = r.smembers('tags')
print(tags)

# 有序集合
r.zadd('leaderboard', {'John': 100, 'Mary': 90})
top = r.zrevrange('leaderboard', 0, 2, withscores=True)
print(top)
```

## 持久化

### RDB 快照

```bash
# 設定儲存頻率
save 900 1   # 900 秒內有 1 次改變
save 300 10  # 300 秒內有 10 次改變
save 60 10000 # 60 秒內有 10000 次改變
```

### AOF 日誌

```bash
# 啟用 AOF
appendonly yes
appendfsync everysec
```

### 混合持久化（Redis 4.0+）

```bash
aof-use-rdb-preamble yes
```

## 發布/訂閱

### 基本使用

```python
# 發布者
r.publish('news', 'Breaking news!')

# 訂閱者
pubsub = r.pubsub()
pubsub.subscribe('news')

for message in pubsub.listen():
    print(message['data'])
```

## 結論

Redis 的豐富資料結構和高效能使其成為快取、計數器、排行榜等場景的首選。其記憶體儲存特性需要注意記憶體管理。

---

**延伸閱讀**

- [NoSQL 程式實作](focus_code.md)
- [Redis+documentation](https://www.google.com/search?q=Redis+documentation)