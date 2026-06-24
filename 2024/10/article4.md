# 文章 4：PostgreSQL 連線與查詢

## 使用 Node.js 連接 PostgreSQL

PostgreSQL 是功能豐富的開源關聯式資料庫。本文示範如何使用 Node.js 進行連線配置與 SQL 查詢操作。

### 安裝驅動程式

```bash
npm install pg
```

### 連線管理

```javascript
import pg from 'pg'

// 連線池設定 (建議用於生產環境)
const pool = new pg.Pool({
  host: 'localhost',
  port: 5432,
  database: 'mydb',
  user: 'app_user',
  password: process.env.DB_PASSWORD,
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 5000
})

// 連線事件監聽
pool.on('error', (err) => {
  console.error('資料庫連線異常:', err.message)
})

// 單一連線 (適合快速腳本)
const client = new pg.Client({
  connectionString: 'postgresql://app_user:password@localhost:5432/mydb'
})
await client.connect()
```

### 資料表建立與查詢

```javascript
// 建立資料表
await pool.query(`
  CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    age INTEGER CHECK (age >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  )
`)

// 新增資料
const insertResult = await pool.query(
  'INSERT INTO users (name, email, age) VALUES ($1, $2, $3) RETURNING *',
  ['Alice Chen', 'alice@example.com', 28]
)
console.log('新增使用者:', insertResult.rows[0])

// 批次新增
const users = [
  ['Bob', 'bob@example.com', 25],
  ['Charlie', 'charlie@example.com', 32]
]
for (const [name, email, age] of users) {
  await pool.query(
    'INSERT INTO users (name, email, age) VALUES ($1, $2, $3) ON CONFLICT (email) DO NOTHING',
    [name, email, age]
  )
}
```

### 查詢操作

```javascript
// 基本查詢
const { rows } = await pool.query(
  'SELECT id, name, email, age FROM users WHERE age >= $1 ORDER BY age DESC LIMIT $2',
  [18, 10]
)

// 單一資料查詢
const { rows: [user] } = await pool.query(
  'SELECT * FROM users WHERE email = $1',
  ['alice@example.com']
)

// 聚合查詢
const stats = await pool.query(`
  SELECT
    COUNT(*) as total,
    AVG(age)::numeric(10,2) as avg_age,
    MAX(age) as max_age,
    MIN(age) as min_age
  FROM users
`)
```

### 更新與刪除

```javascript
// 更新資料
await pool.query(
  'UPDATE users SET age = $1, updated_at = CURRENT_TIMESTAMP WHERE email = $2',
  [29, 'alice@example.com']
)

// 刪除資料
await pool.query('DELETE FROM users WHERE age < $1', [18])
```

### 事務處理

```javascript
async function transferMoney(fromId, toId, amount) {
  const client = await pool.connect()
  try {
    await client.query('BEGIN')

    const { rows: [from] } = await client.query(
      'SELECT balance FROM accounts WHERE id = $1 FOR UPDATE',
      [fromId]
    )
    if (from.balance < amount) throw new Error('餘額不足')

    await client.query(
      'UPDATE accounts SET balance = balance - $1 WHERE id = $2',
      [amount, fromId]
    )
    await client.query(
      'UPDATE accounts SET balance = balance + $1 WHERE id = $2',
      [amount, toId]
    )

    await client.query('COMMIT')
    return { success: true }
  } catch (e) {
    await client.query('ROLLBACK')
    return { success: false, error: e.message }
  } finally {
    client.release()
  }
}
```

### 連線安全建議

```javascript
// 使用環境變數管理連線資訊
// .env 檔案範例:
// DATABASE_URL=postgresql://user:password@localhost:5432/mydb?sslmode=require

const pool = new pg.Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: process.env.NODE_ENV === 'production'
    ? { rejectUnauthorized: true }
    : false
})
```

延伸閱讀：https://www.google.com/search?q=PostgreSQL+Nodejs+connection+tutorial
https://www.google.com/search?q=PostgreSQL+query+optimization+guide
