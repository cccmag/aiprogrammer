# 資料庫連接：MongoDB / SQLite

## 選擇資料庫

Node.js 生態支援多種資料庫。MongoDB 和 SQLite 分別代表了文件型資料庫和嵌入式關聯式資料庫兩種典型方案。

### MongoDB 適合場景

- 文件結構經常變化
- 需要快速原型開發
- 資料不需要複雜的關聯查詢
- 需要水平擴展

### SQLite 適合場景

- 輕量級應用或工具
- 嵌入式裝置或桌面應用
- 測試環境或原型
- 單一伺服器的小型應用

## MongoDB + Mongoose

Mongoose 是 Node.js 最流行的 MongoDB ODM（Object Document Mapper）。

### 安裝與連接

```bash
npm install mongoose
```

```javascript
const mongoose = require('mongoose');

mongoose.connect('mongodb://localhost:27017/myapp')
  .then(() => console.log('Connected to MongoDB'))
  .catch(err => console.error('Connection error:', err));
```

### 定義 Schema

```javascript
const userSchema = new mongoose.Schema({
  name: { type: String, required: true },
  email: { type: String, required: true, unique: true },
  age: { type: Number, min: 0 },
  createdAt: { type: Date, default: Date.now },
  address: {
    street: String,
    city: String,
  },
  tags: [String],
});

const User = mongoose.model('User', userSchema);
```

### CRUD 操作

```javascript
// Create
const user = await User.create({
  name: 'Alice',
  email: 'alice@example.com',
  age: 30,
});

// Read
const users = await User.find({ age: { $gte: 18 } });
const user = await User.findById('someId');
const user = await User.findOne({ email: 'alice@example.com' });

// Update
await User.findByIdAndUpdate(id, { age: 31 });
await User.updateMany({ age: { $lt: 18 } }, { status: 'minor' });

// Delete
await User.findByIdAndDelete(id);
await User.deleteMany({ age: { $lt: 13 } });
```

### 虛擬屬性與中介軟體

```javascript
userSchema.virtual('isAdult').get(function() {
  return this.age >= 18;
});

userSchema.pre('save', function(next) {
  this.updatedAt = new Date();
  next();
});
```

## SQLite + better-sqlite3

better-sqlite3 是 Node.js 中最快的 SQLite 同步操作庫。

### 安裝與連接

```bash
npm install better-sqlite3
```

```javascript
const Database = require('better-sqlite3');
const db = new Database('mydb.sqlite');

// 啟用 WAL 模式以獲得更好的併發效能
db.pragma('journal_mode = WAL');
```

### 建立表格

```javascript
db.exec(`
  CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    age INTEGER,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
  )
`);
```

### CRUD 操作

```javascript
// Create
const stmt = db.prepare(
  'INSERT INTO users (name, email, age) VALUES (?, ?, ?)'
);
const result = stmt.run('Alice', 'alice@example.com', 30);
console.log(result.lastInsertRowid);

// Read
const users = db.prepare('SELECT * FROM users WHERE age >= ?').all(18);
const user = db.prepare('SELECT * FROM users WHERE id = ?').get(id);

// Update
db.prepare('UPDATE users SET age = ? WHERE id = ?').run(31, id);

// Delete
db.prepare('DELETE FROM users WHERE id = ?').run(id);
```

### 交易處理

```javascript
const insertUser = db.transaction((users) => {
  for (const user of users) {
    db.prepare('INSERT INTO users (name, email) VALUES (?, ?)').run(user.name, user.email);
  }
});

try {
  insertUser([
    { name: 'Bob', email: 'bob@test.com' },
    { name: 'Carol', email: 'carol@test.com' },
  ]);
  console.log('Transaction committed');
} catch (err) {
  console.error('Transaction rolled back:', err);
}
```

## 在 Express 中使用

```javascript
const express = require('express');
const app = express();

// MongoDB 版本
app.get('/api/users', async (req, res) => {
  try {
    const users = await User.find().limit(20);
    res.json({ data: users });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// SQLite 版本
app.get('/api/users', (req, res) => {
  try {
    const users = db.prepare('SELECT * FROM users LIMIT 20').all();
    res.json({ data: users });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});
```

## 遷移管理

專案成長後，建議使用遷移工具管理資料庫結構變更：

```bash
# MongoDB
npm install migrate-mongoose

# SQLite
npm install db-migrate-sqlite3
```

## 總結

選擇資料庫時需要權衡專案需求。MongoDB 提供靈活的 Schema 和良好的擴展性，適合快速迭代的產品開發。SQLite 則以零設定、輕量級著稱，適合工具類應用和邊緣裝置。

## 延伸閱讀

- [Mongoose 官方文件](https://www.google.com/search?q=Mongoose+ODM+documentation)
- [better-sqlite3 GitHub](https://www.google.com/search?q=better-sqlite3+npm)
- [Node.js 資料庫整合指南](https://www.google.com/search?q=Node.js+database+integration+guide)
