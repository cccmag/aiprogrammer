# 資料庫整合：MongoDB、Redis、MySQL

## 前言

Node.js 可以連接幾乎所有主流資料庫。本篇介紹 MongoDB（Mongoose）、Redis 和 MySQL 的整合方式。

## MongoDB + Mongoose

### 安裝與連線

```bash
npm install mongoose
```

```javascript
const mongoose = require('mongoose');

mongoose.connect('mongodb://localhost:27017/mydb', {
  useNewUrlParser: true,
  useUnifiedTopology: true
});

const db = mongoose.connection;

db.on('error', (err) => {
  console.error('連線錯誤:', err);
});

db.once('open', () => {
  console.log('MongoDB 連線成功');
});

db.on('disconnected', () => {
  console.log('MongoDB 連線中斷');
});
```

### 定義模型

```javascript
const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const userSchema = new Schema({
  name: {
    type: String,
    required: true,
    trim: true
  },
  email: {
    type: String,
    required: true,
    unique: true,
    lowercase: true
  },
  age: {
    type: Number,
    min: 0,
    max: 150
  },
  createdAt: {
    type: Date,
    default: Date.now
  }
});

const User = mongoose.model('User', userSchema);
```

### CRUD 操作

```javascript
// 建立
const user = new User({ name: '王小明', email: 'wang@example.com', age: 25 });
await user.save();

// 建立（另一種方式）
const newUser = await User.create({ name: '李小華', email: 'lee@example.com' });

// 讀取
const user = await User.findById('123');
const users = await User.find({ age: { $gte: 18 } });
const oneUser = await User.findOne({ name: '王小明' });

// 更新
await User.findByIdAndUpdate('123', { age: 30 }, { new: true });
await User.updateOne({ name: '王小明' }, { age: 26 });

// 刪除
await User.findByIdAndDelete('123');
await User.deleteOne({ name: '王小明' });
```

### 查詢輔助

```javascript
// 分頁
const users = await User.find()
  .skip(10)
  .limit(10)
  .sort({ createdAt: -1 })
  .select('name email');

// 計數
const count = await User.countDocuments({ age: { $gte: 18 } });

// 存在檢查
const exists = await User.exists({ email: 'wang@example.com' });

// 執行原生的 MongoDB 查詢
const raw = await User.collection.find({ name: '王小明' }).toArray();
```

### 驗證

```javascript
const userSchema = new Schema({
  email: {
    type: String,
    required: true,
    validate: {
      validator: (v) => /^.+@.+\..+/.test(v),
      message: 'Email 格式不正確'
    }
  },
  age: {
    type: Number,
    min: [0, '年齡不能為負數'],
    max: [150, '年齡不能超過 150']
  }
});
```

## Redis

### 安裝與連線

```bash
npm install redis
```

```javascript
const redis = require('redis');
const client = redis.createClient({
  host: 'localhost',
  port: 6379
});

client.on('error', (err) => {
  console.error('Redis 錯誤:', err);
});

client.on('connect', () => {
  console.log('Redis 連線成功');
});
```

### 基本操作

```javascript
// 字串
await client.set('name', '王小明');
const name = await client.get('name');
await client.del('name');

// 數字遞增/遞減
await client.set('counter', 0);
await client.incr('counter');   // 1
await client.incrby('counter', 5);  // 6
await client.decr('counter');   // 5

// 過期時間
await client.setex('token', 3600, 'abc123'); // 1 小時後過期
await client.expire('token', 3600);

// 雜湊
await client.hset('user:1', 'name', '王小明');
await client.hset('user:1', 'email', 'wang@example.com');
const user = await client.hgetall('user:1');
await client.hincrby('user:1', 'age', 1);

// 列表
await client.lpush('queue', 'task1');
await client.lpush('queue', 'task2');
const tasks = await client.rpop('queue');

// 集合
await client.sadd('tags', 'node', 'javascript', 'express');
const tags = await client.smembers('tags');
```

### 快取模式

```javascript
async function getUser(id) {
  const cacheKey = `user:${id}`;

  // 先查快取
  const cached = await client.get(cacheKey);
  if (cached) {
    return JSON.parse(cached);
  }

  // 查詢資料庫
  const user = await User.findById(id);

  // 存入快取（1 小時）
  await client.setex(cacheKey, 3600, JSON.stringify(user));

  return user;
}
```

## MySQL

### 安裝與連線

```bash
npm install mysql
```

```javascript
const mysql = require('mysql');

const pool = mysql.createPool({
  host: 'localhost',
  user: 'root',
  password: '',
  database: 'mydb',
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0
});

pool.getConnection((err, connection) => {
  if (err) throw err;
  console.log('MySQL 連線成功');
  connection.release();
});
```

### CRUD 操作

```javascript
// 查詢
const [rows] = await pool.query('SELECT * FROM users WHERE id = ?', [1]);
const [users] = await pool.query('SELECT * FROM users WHERE age > ?', [18]);

// 新增
const [result] = await pool.query(
  'INSERT INTO users (name, email) VALUES (?, ?)',
  ['王小明', 'wang@example.com']
);
console.log('新增 ID:', result.insertId);

// 更新
const [updateResult] = await pool.query(
  'UPDATE users SET age = ? WHERE id = ?',
  [30, 1]
);
console.log('影響行數:', updateResult.affectedRows);

// 刪除
const [deleteResult] = await pool.query(
  'DELETE FROM users WHERE id = ?',
  [1]
);
console.log('刪除行數:', deleteResult.affectedRows);
```

### 事務處理

```javascript
async function transfer(fromId, toId, amount) {
  const connection = await pool.getConnection();

  try {
    await connection.beginTransaction();

    await connection.query(
      'UPDATE accounts SET balance = balance - ? WHERE id = ?',
      [amount, fromId]
    );

    await connection.query(
      'UPDATE accounts SET balance = balance + ? WHERE id = ?',
      [amount, toId]
    );

    await connection.commit();
    console.log('轉帳成功');
  } catch (error) {
    await connection.rollback();
    console.error('轉帳失敗:', error);
    throw error;
  } finally {
    connection.release();
  }
}
```

## 結論

Node.js 提供了豐富的資料庫支援。MongoDB 的文件導向適合快速開發、Redis 的記憶體儲存適合作為快取、MySQL 的關聯式模型適合複雜查詢和事務處理。

---

## 延伸閱讀

- [Mongoose 文件](https://www.google.com/search?q=Mongoose+MongoDB+Node.js+tutorial)
- [Redis 指令](https://www.google.com/search?q=Redis+commands+Node.js)
- [MySQL+Node.js](https://www.google.com/search?q=MySQL+Node.js+connection+pool)

---

*本篇文章為「AI 程式人雜誌 2015 年 2 月號」歷史回顧系列之一。*