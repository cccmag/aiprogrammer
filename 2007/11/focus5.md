# 社交應用架構：處理海量資料

## 社交網路的規模

### 2007 年的規模

```
Facebook 規模（2007 年）：
───────────────────────────
用戶數          > 50,000,000
每日活躍用戶    > 10,000,000
好友連接數      每人平均 100+
動態產生        每秒數十萬
```

## 技術架構

### 資料儲存

```python
# 社交圖譜儲存
# 使用圖資料庫的概念
class SocialGraph:
    def __init__(self):
        self.users = {}  # user_id -> User
        self.friendships = {}  # user_id -> set(friend_ids)

    def add_friendship(self, user_id, friend_id):
        if user_id not in self.friendships:
            self.friendships[user_id] = set()
        self.friendships[user_id].add(friend_id)

    def get_friends(self, user_id):
        return self.friendships.get(user_id, set())

    def get_friends_of_friends(self, user_id):
        fof = set()
        for friend in self.get_friends(user_id):
            fof.update(self.get_friends(friend))
        fof.discard(user_id)  # 移除自己
        return fof
```

### 快取策略

```python
# 多層快取
cache = Memcached()

def get_user_profile(user_id):
    # L1: 本地快取
    cached = local_cache.get(user_id)
    if cached:
        return cached

    # L2: Memcached
    cached = cache.get(f'user:{user_id}')
    if cached:
        local_cache.set(user_id, cached, ttl=60)
        return cached

    # L3: 資料庫
    user = db.get_user(user_id)
    cache.set(f'user:{user_id}', user, ttl=300)
    return user
```

### 資料分片

```python
# 使用者資料分片
def get_shard(user_id):
    shard_id = user_id % NUM_SHARDS
    return f'shard_{shard_id}'

# 查詢
def get_user(user_id):
    shard = get_shard(user_id)
    return db[shard].get_user(user_id)
```

## 結語

社交網路需要在即時性、一致性和可用性之間取得平衡。2007 年的架構經驗影響了後來的系統設計。

---

## 延伸閱讀

- [social+network+architecture+2007](https://www.google.com/search?q=social+network+architecture+2007)

---