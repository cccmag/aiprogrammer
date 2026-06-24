# NoSQL 的興起與分類：從 SQL 到 NoSQL

## NoSQL 的背景

### 為什麼需要 NoSQL？

2000 年代後期，網際網路公司面臨著前所未有的資料挑戰：

```markdown
Web 2.0 公司的資料挑戰：

1. 資料量爆炸
   - Facebook: 10 億用戶
   - Twitter: 每天數億條推文
   - Google: 每天數十億次搜尋

2. 寫入負載
   - 使用者產生內容
   - 日誌和事件
   - 即時分析

3. 快速迭代
   - 需求頻繁變化
   - 需要快速發布
   - Schema 難以預測

傳統 RDBMS 無法有效應對這些挑戰。
```

### NoSQL 的定義

```
NoSQL 的含義：

N ot O nly
S QL

不是「不使用 SQL」，而是「不只有 SQL」

NoSQL 資料庫放棄了：
- 嚴格的一致性
- 複雜的 JOIN
- 固定 Schema

NoSQL 資料庫提供：
- 水平擴展能力
- 彈性資料模型
- 高可用性
```

## NoSQL 的分類

### 四大類型

```
NoSQL 資料庫分類：

┌─────────────────────────────────────────────────────┐
│                    NoSQL 家族                        │
├────────────┬────────────┬────────────┬────────────┤
│ Key-Value  │ 文件       │ 列儲存     │ 圖         │
├────────────┼────────────┼────────────┼────────────┤
│ Redis      │ MongoDB    │ Cassandra  │ Neo4j      │
│ Memcached  │ CouchDB    │ HBase      │ OrientDB   │
│ DynamoDB   │ RavenDB    │ Hypertable │           │
│ Riak       │            │            │           │
└────────────┴────────────┴────────────┴────────────┘
```

### Key-Value 儲存

```python
# Key-Value 儲存的特點

# 優點：
# - 簡單 API：get, set, delete
# - 極速讀寫
# - 容易水平擴展

# 缺點：
# - 無法依值查詢
# - 無法範圍查詢
# - 不適合複雜資料

# 適合場景：
# - 會話管理
# - 快取
# - 簡單配置

# Redis 範例
import redis
r = redis.Redis()
r.set('user:1', '{"name": "張三", "age": 30}')
user = r.get('user:1')
```

### 文件資料庫

```python
# 文件資料庫的特點

# 優點：
# - 靈活 Schema
# - 自然 JSON 格式
# - 可嵌套

# 缺點：
# - 無法完全替代 JOIN
# - 查詢能力有限
# - 事務支援有限

# 適合場景：
# - 內容管理
# - 用戶設定檔
# - 即時分析

# MongoDB 範例
db.users.insert({
    "name": "張三",
    "age": 30,
    "address": {
        "city": "台北",
        "zip": "100"
    }
})
```

### 列儲存資料庫

```python
# 列儲存資料庫的特點

# 優點：
# - 極佳壓縮率
# - 快速大規模讀取
# - 高效能聚合

# 缺點：
# - 寫入效能較低
# - 查詢複雜
# - 學習曲線

# 適合場景：
# - 大量資料分析
# - 時間序列資料
# - ログ儲存

# Cassandra 範例
CREATE TABLE users (
    user_id text PRIMARY KEY,
    name text,
    email text
);
```

### 圖資料庫

```python
# 圖資料庫的特點

# 優點：
# - 複雜關聯查詢高效
# - 圖遍歷快速
# - 自然表達關係

# 缺點：
# - 規模化挑戰
# - 查詢複雜度
# - 學習曲線

# 適合場景：
# - 社交網路
# - 推薦系統
# - 知識圖譜

# Neo4j 範例
CREATE (alice:Person {name: "張三"})
CREATE (bob:Person {name: "李四"})
CREATE (alice)-[:KNOWS]->(bob)
```

## NoSQL vs SQL

### 比較表

```markdown
| 特性         | SQL          | NoSQL           |
|-------------|--------------|------------------|
| Schema      | 固定         | 動態             |
| 擴展方式     | 垂直         | 水平             |
| 查詢語言     | SQL          | 各不相同          |
| 事務        | ACID         | BASE             |
| 一致性      | 強一致性      | 最終一致性        |
| 完整性      | 支援         | 應用層實現        |
| 複雜查詢    | 支援         | 有限             |
```

### ACID vs BASE

```markdown
ACID（傳統 RDBMS）：

- Atomicity（原子性）
- Consistency（一致性）
- Isolation（隔離性）
- Durability（耐久性）

BASE（NoSQL）：

- Basically Available（基本可用）
- Soft state（軟狀態）
- Eventually consistent（最終一致性）
```

## NoSQL 的選擇

### 選擇指引

```markdown
選擇 NoSQL 的考量：

1. 資料模型
   - 簡單 key-value → Redis, Memcached
   - 文件 → MongoDB, CouchDB
   - 大量寫入 → Cassandra, HBase
   - 複雜關係 → Neo4j, OrientDB

2. 一致性需求
   - 強一致性 → MongoDB（有事務）
   - 最終一致性 → Cassandra, Riak

3. 擴展需求
   - 需要水平擴展 → 幾乎所有 NoSQL
   - 垂直擴展優先 → Redis

4. 查詢需求
   - 簡單 → Key-Value
   - 中等複雜 → 文件
   - 複雜 → 圖
```

## 結語

NoSQL 運動代表了對傳統關聯式資料庫的補充。2009 年，各種 NoSQL 資料庫開始嶄露頭角，為開發者提供了更多的選擇。

下一篇文章將深入探討文件資料庫的核心概念。

---

## 延伸閱讀

- [NoSQL 資料庫比較](https://www.google.com/search?q=NoSQL+database+comparison+2009)
- [NoSQL 運動興起](https://www.google.com/search?q=NoSQL+movement+origin)
- [CAP 理論](https://www.google.com/search?q=CAP+theorem+Nosql)
- [四大 NoSQL 分類](https://www.google.com/search?q=NoSQL+types+key-value+document+column+graph)

---

*本篇文章為「AI 程式人雜誌 2009 年 9 月號」焦點系列之一。*