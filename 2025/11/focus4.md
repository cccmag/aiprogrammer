# 快取策略

## 速度與成本的權衡

快取是系統設計中最有效的效能優化手段。將昂貴的計算結果或頻繁存取的資料儲存在高速儲存中，可以大幅降低延遲並減輕後端系統的負載。

---

## 為什麼需要快取？

一條典型的資料讀取路徑包含多個層次，每個層次的速度差異巨大：

```
CPU L1 快取：      ~1 ns（~0.001 µs）
CPU L2 快取：      ~4 ns
CPU L3 快取：      ~10 ns
主記憶體（RAM）：   ~100 ns
SSD：              ~100 µs
傳統硬碟：         ~10 ms
網路請求：         ~100 ms
資料庫查詢：       ~100 ms - 1 s
```

快取的核心理念：**將常用資料放在離 CPU 更近、速度更快的地方**。

---

## 快取層次

### 客戶端快取

**瀏覽器快取**：靜態資源（CSS、JS、圖片）通過 HTTP Cache-Control 標頭控制快取時間。

```
Cache-Control: max-age=31536000
// 瀏覽器一年內不再請求此資源
```

**CDN 快取**：將靜態內容快取在全球邊緣節點。

```
用戶在東京 → 請求 Tokyo CDN 節點（快取命中）
用戶在倫敦 → 請求 London CDN 節點（快取命中）
原始伺服器只在 CDN 未命中時被訪問
```

### 伺服器端快取

**應用層快取**：在記憶體中快取運算結果或資料庫查詢結果。

```python
# 使用 Redis 快取用戶資料
def get_user(user_id):
    cache_key = f"user:{user_id}"
    user = redis.get(cache_key)
    if user:
        return user
    user = db.query(User).get(user_id)
    redis.setex(cache_key, 3600, user)  # TTL: 1小時
    return user
```

**資料庫快取**：資料庫自身的 Buffer Pool、Query Cache。

---

## 快取淘汰策略

### LRU（Least Recently Used）

淘汰最久未被存取的資料。最常用的策略。

```
存取順序：A → B → C → A → D

容量 3 時的狀態變化：
[A]
[A, B]
[A, B, C]        # A 是最久未使用
[A, B, C] → A   # 存取 A，A 移到最前面
[B, C, A]
[B, C, A] → D   # 容量滿，淘汰 B
[C, A, D]
```

### LFU（Least Frequently Used）

淘汰被存取次數最少的資料。

```
A 被存取 10 次
B 被存取 5 次
C 被存取 3 次

容量滿時淘汰 C
```

**注意**：LFU 有「快取汙染」問題——過去熱門但現在不再需要的資料仍留在快取中。

### TTL（Time To Live）

設定過期時間，時間到自動失效。

```python
redis.setex("key", timeout_seconds, value)
```

### 比較

| 策略 | 優點 | 缺點 | 適用場景 |
|------|------|------|---------|
| LRU | 實作簡單，適合大多數場景 | 突發流量可能淘汰重要資料 | Web 應用快取 |
| LFU | 對長期熱門資料友好 | 可能保留過時的熱門資料 | CDN 快取 |
| TTL | 保證資料新鮮度 | 無法動態適應存取模式 | Session 快取 |
| FIFO | 最簡單 | 忽略存取頻率和時效性 | 很少單獨使用 |

---

## 快取模式

### Cache-Aside（旁路快取）

應用程式自行管理快取。

```
讀取流程：
1. 檢查快取 → 命中返回
2. 未命中 → 查資料庫 → 寫入快取 → 返回

寫入流程：
1. 更新資料庫
2. 使快取失效（刪除該鍵值）
```

### Read-Through（讀取穿透）

快取層負責從資料庫載入資料。

```
應用程式 → 快取層（讀取穿透） → 資料庫
```

### Write-Through（寫入穿透）

寫入操作同時更新快取和資料庫。

```
應用程式 → 快取層（同時寫入快取和資料庫）
```

**優點**：快取和資料庫始終一致
**缺點**：寫入延遲增加

### Write-Behind（非同步寫入）

先更新快取，再非同步寫入資料庫。

```
應用程式 → 更新快取（立即返回）
                    ↓
            非同步寫入資料庫（後台執行）
```

**優點**：寫入延遲低
**缺點**：當機時可能丟失資料

---

## 快取穿透與雪崩

### 快取穿透（Cache Penetration）

請求的資料既不在快取中，也不在資料庫中。

```python
# 使用布隆過濾器防護
bloom = BloomFilter(size=1_000_000, hash_count=7)

def get_user(user_id):
    if not bloom.contains(user_id):
        return None  # 一定不存在
    # 正常查快取/資料庫
```

### 快取雪崩（Cache Avalanche）

大量快取同時過期，導致請求全部打到資料庫。

```python
# 解決方案：隨機過期時間
cache.setex(key, base_ttl + random.randint(0, 300), value)
```

### 快取擊穿（Cache Breakdown）

某個熱點 key 過期時，大量請求同時穿透到資料庫。

```python
# 解決方案：互斥鎖
def get_hot_data(key):
    data = cache.get(key)
    if data:
        return data
    lock = redis.lock(f"lock:{key}")
    if lock.acquire(timeout=1):
        data = db.query(...)
        cache.set(key, data, ttl=60)
        lock.release()
    return data
```

---

## 實際案例：資料庫查詢快取

```python
class ArticleService:
    def get_article(self, article_id):
        cache_key = f"article:{article_id}"
        article = cache.get(cache_key)
        if article:
            return article
        article = db.execute(
            "SELECT * FROM articles WHERE id = ?", 
            article_id
        )
        cache.setex(cache_key, 1800, article)
        return article

    def update_article(self, article_id, data):
        db.execute(
            "UPDATE articles SET ... WHERE id = ?",
            data, article_id
        )
        cache.delete(f"article:{article_id}")
```

這個簡單的模式可以將讀取速度從 50ms（資料庫查詢）降至 1ms（記憶體讀取）。

---

## 延伸閱讀

- [Redis Cache Patterns](https://www.google.com/search?q=redis+caching+patterns+aside+through)
- [Cache Eviction Algorithms](https://www.google.com/search?q=cache+eviction+algorithms+LRU+LFU+TTL)
- [Cache Penetration and Avalanche](https://www.google.com/search?q=cache+penetration+avalanche+breakdown)

---

*本篇文章為「AI 程式人雜誌 2026 年 11 月號」系統設計系列之四。*
