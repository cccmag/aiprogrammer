# 關聯式 vs NoSQL 資料庫

## 兩種資料庫哲學

在選擇資料庫時，最常見的抉擇是關聯式資料庫（RDBMS）還是 NoSQL 資料庫。兩者並沒有絕對的好壞，而是取決於應用場景。

## 關聯式資料庫

### 核心特徵

- **結構化資料**：預先定義表格結構（Schema）
- **SQL 查詢**：使用標準化查詢語言
- **ACID 交易**：保證資料一致性
- **正規化設計**：減少資料重複

### 適合場景

```sql
-- 金融交易系統：需要原子性和一致性
BEGIN TRANSACTION;
UPDATE accounts SET balance = balance - 1000 WHERE id = 1;
UPDATE accounts SET balance = balance + 1000 WHERE id = 2;
COMMIT;

-- 報表系統：複雜的聚合查詢
SELECT department, AVG(salary), COUNT(*)
FROM employees
GROUP BY department;
```

### 代表產品

- **PostgreSQL**：功能最完整，支援 JSON、陣列、全文檢索
- **MySQL/MariaDB**：Web 應用廣泛使用
- **SQLite**：嵌入式、輕量級
- **Oracle**：企業級商業資料庫

## NoSQL 資料庫

### 核心特徵

- **靈活的資料模型**：無需預先定義結構
- **水平擴展**：容易分散到多台伺服器
- **最終一致性**：部分系統放寬一致性要求
- **專為特定場景設計**：鍵值、文件、圖形等

### 主要類型

```python
# 文件資料庫（MongoDB）的資料格式
{
    "_id": "user_001",
    "name": "王小明",
    "email": "wang@test.com",
    "orders": [
        {"product": "iPhone 17", "price": 35900},
        {"product": "AirPods", "price": 6990}
    ]
    # 內嵌陣列，無需 JOIN
}

# 鍵值資料庫（Redis）的使用方式
SET user:001:name "王小明"
SET user:001:email "wang@test.com"
SADD user:001:orders "order:1001"
SADD user:001:orders "order:1002"
```

### 適合場景

- **MongoDB**：內容管理、目錄、使用者個人資料
- **Redis**：快取、工作階段管理、即時排行榜
- **Neo4j**：社交網路、推薦引擎、知識圖譜
- **Cassandra**：時間序列資料、IoT 感測器資料

## 比較分析

| 特性 | 關聯式 | NoSQL |
|------|--------|-------|
| 資料模型 | 表格（固定結構） | 靈活（動態結構） |
| 查詢語言 | SQL（標準化） | 各資料庫自訂 |
| ACID 支援 | 完整支援 | 視產品而定 |
| 水平擴展 | 較困難 | 原生支援 |
| 複雜 JOIN | 原生支援 | 不支援或有限 |
| 成熟度 | 50+ 年 | 15+ 年 |

## CAP 定理

CAP 定理指出分散式系統無法同時滿足三者：

- **C（Consistency）**：一致性
- **A（Availability）**：可用性
- **P（Partition Tolerance）**：分區容忍性

```
關聯式資料庫：通常選擇 CA（犧牲 P）
MongoDB：      通常選擇 CP（犧牲 A）
Cassandra：    通常選擇 AP（犧牲 C）
```

## 如何選擇

### 選擇關聯式資料庫，如果：

1. 資料結構明確且穩定
2. 需要複雜的關聯查詢（多表格 JOIN）
3. 需要嚴格的資料一致性（金融、庫存）
4. 需要標準化查詢語言（SQL）

### 選擇 NoSQL 資料庫，如果：

1. 資料結構不固定或頻繁變化
2. 需要大規模水平擴展
3. 需要處理大量寫入（高吞吐量）
4. 儲存的是文件、圖形等非表格結構資料

### 混合使用

現代架構經常同時使用兩者：

```python
# PostgreSQL + Redis 混合架構
import psycopg2
import redis

rd = redis.Redis()

def get_user_profile(user_id):
    # 先檢查快取
    cached = rd.get(f"profile:{user_id}")
    if cached:
        return cached

    # 快取未命中，查詢 PostgreSQL
    conn = psycopg2.connect("dbname=app")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cur.fetchone()

    # 寫入快取
    rd.setex(f"profile:{user_id}", 3600, str(user))
    return user
```

## 2026 年的趨勢

關聯式資料庫與 NoSQL 資料庫正在互相靠攏：

- **PostgreSQL** 支援 JSON 和向量搜尋
- **MongoDB** 推出 SQL 相容層
- **SQLite 4.0** 內建向量搜尋
- **EdgeDB** 結合關聯式與物件導向

選擇資料庫時，與其問「關聯式 vs NoSQL」，不如問「哪個資料庫最適合我的使用模式」。

## 參考資料

- [關聯式 vs NoSQL 比較](https://www.google.com/search?q=relational+database+vs+NoSQL+comparison)
- [CAP 定理說明](https://www.google.com/search?q=CAP+theorem+explained)
- [資料庫選型指南](https://www.google.com/search?q=database+selection+guide+2026)
