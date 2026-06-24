// db_cloud.js - 資料庫與雲端服務模擬範例
// 模擬 MongoDB、Redis、Firebase 操作

class MongoCollection {
  constructor() {
    this.docs = []
  }
  insertOne(doc) {
    doc._id = Date.now() + Math.random()
    this.docs.push(doc)
    return { insertedId: doc._id }
  }
  find(query = {}) {
    return this.docs.filter(d =>
      Object.keys(query).every(k => d[k] === query[k])
    )
  }
  updateOne(query, update) {
    const doc = this.docs.find(d =>
      Object.keys(query).every(k => d[k] === query[k])
    )
    if (doc) {
      Object.assign(doc, update.$set || {})
      return { modifiedCount: 1 }
    }
    return { modifiedCount: 0 }
  }
  deleteOne(query) {
    const before = this.docs.length
    this.docs = this.docs.filter(d =>
      !Object.keys(query).every(k => d[k] === query[k])
    )
    return { deletedCount: before - this.docs.length }
  }
}

class RedisCache {
  constructor() {
    this.store = new Map()
  }
  get(k) { return this.store.get(k) }
  set(k, v, ttl) {
    this.store.set(k, v)
    if (ttl) setTimeout(() => this.store.delete(k), ttl)
  }
  del(k) { this.store.delete(k) }
  flush() { this.store.clear() }
}

class FirebaseStore {
  constructor() {
    this.collections = {}
  }
  collection(name) {
    if (!this.collections[name]) this.collections[name] = new MongoCollection()
    return this.collections[name]
  }
}

function demo() {
  console.log('=== 資料庫與雲端服務模擬範例 ===\n')

  // MongoDB 操作
  const db = new MongoCollection()
  db.insertOne({ user: 'Alice', score: 85, tags: ['js', 'db'] })
  db.insertOne({ user: 'Bob', score: 92, tags: ['node', 'cloud'] })
  console.log('MongoDB 插入:', JSON.stringify(db.find()))

  db.updateOne({ user: 'Alice' }, { $set: { score: 90 } })
  console.log('MongoDB 更新:', JSON.stringify(db.find({ user: 'Alice' })))

  db.deleteOne({ user: 'Bob' })
  console.log('MongoDB 刪除後:', JSON.stringify(db.find()))

  // Redis 快取模擬
  const cache = new RedisCache()
  cache.set('session:alice', { name: 'Alice', role: 'admin' }, 60000)
  console.log('Redis 讀取:', JSON.stringify(cache.get('session:alice')))
  cache.del('session:alice')
  console.log('Redis 刪除後:', cache.get('session:alice'))

  // 快取穿透模擬
  cache.set('popular:post:1', { title: '熱門文章', views: 9999 })
  console.log('Redis 快取穿透:', JSON.stringify(cache.get('popular:post:1')))

  // Firebase 模擬
  const fb = new FirebaseStore()
  fb.collection('notes').insertOne({ title: '學習筆記', body: 'Firebase 即時資料庫', createdAt: new Date() })
  fb.collection('notes').insertOne({ title: '雲端架構', body: 'AWS vs GCP 比較' })
  console.log('Firebase 讀取:', JSON.stringify(fb.collection('notes').find()))

  // 即時監聽模擬
  const unsubscribe = fb.collection('notes').find().length
  console.log('Firebase 文件數量:', unsubscribe)

  console.log('\n=== 範例完成 ===')
}

if (require.main === module) demo()
