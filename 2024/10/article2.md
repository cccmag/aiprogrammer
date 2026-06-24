# 文章 2：MongoDB CRUD 操作

## 使用 Node.js 操作 MongoDB

MongoDB 的 CRUD 操作是使用資料庫的基礎。本文將示範如何使用官方 MongoDB Node.js 驅動程式進行新增、查詢、更新與刪除操作。

### 環境設定

```bash
npm install mongodb
```

### 連線設定

```javascript
import { MongoClient } from 'mongodb'

const uri = 'mongodb://localhost:27017'
const client = new MongoClient(uri)

async function connect() {
  await client.connect()
  console.log('已連線到 MongoDB')
  return client.db('myapp')
}

const db = await connect()
const users = db.collection('users')
```

### Create (新增)

```javascript
// 新增單一文件
const result = await users.insertOne({
  name: 'Alice Chen',
  email: 'alice@example.com',
  age: 28,
  tags: ['developer', 'javascript'],
  createdAt: new Date()
})
console.log('新增 ID:', result.insertedId)

// 新增多筆文件
const manyResult = await users.insertMany([
  { name: 'Bob', email: 'bob@example.com', age: 25 },
  { name: 'Charlie', email: 'charlie@example.com', age: 32 }
])
console.log('新增數量:', manyResult.insertedCount)
```

### Read (查詢)

```javascript
// 查詢所有文件
const allUsers = await users.find().toArray()

// 條件查詢
const developers = await users.find({
  tags: 'developer',
  age: { $gte: 25 }
}).sort({ age: 1 }).limit(10).toArray()

// 單一文件查詢
const user = await users.findOne({ email: 'alice@example.com' })

// 投影 (只回傳特定欄位)
const names = await users.find(
  { age: { $gte: 18 } },
  { projection: { name: 1, email: 1, _id: 0 } }
).toArray()

// 計數
const count = await users.countDocuments({ tags: 'developer' })
```

### Update (更新)

```javascript
// 更新單一文件
const updateResult = await users.updateOne(
  { email: 'alice@example.com' },
  { $set: { age: 29 }, $push: { tags: 'mongodb' } }
)
console.log('修改數量:', updateResult.modifiedCount)

// 更新多筆文件
const multiResult = await users.updateMany(
  { age: { $lt: 30 } },
  { $inc: { age: 1 } }
)

// 取代文件 (替換整個文件內容)
await users.replaceOne(
  { email: 'bob@example.com' },
  { name: 'Bob Updated', email: 'bob@example.com', age: 26 }
)
```

### Delete (刪除)

```javascript
// 刪除單一文件
const deleteResult = await users.deleteOne({ email: 'charlie@example.com' })
console.log('刪除數量:', deleteResult.deletedCount)

// 刪除多筆文件
await users.deleteMany({ age: { $lt: 20 } })

// 刪除整個集合
await users.drop()
```

### 聚合查詢

MongoDB 的聚合管線提供強大的資料分析能力：

```javascript
const pipeline = [
  { $match: { age: { $gte: 25 } } },
  { $group: { _id: '$tags', count: { $sum: 1 }, avgAge: { $avg: '$age' } } },
  { $sort: { count: -1 } },
  { $limit: 5 }
]

const result = await users.aggregate(pipeline).toArray()
```

### 錯誤處理

```javascript
async function safeInsert(data) {
  try {
    return await users.insertOne(data)
  } catch (err) {
    if (err.code === 11000) {
      console.error('重複鍵錯誤:', err.message)
    } else {
      console.error('資料庫錯誤:', err)
    }
    throw err
  }
}
```

延伸閱讀：https://www.google.com/search?q=MongoDB+CRUD+operations+tutorial+Nodejs
https://www.google.com/search?q=MongoDB+aggregation+pipeline+examples
