# 文章 3：Mongoose ODM

## 使用 Mongoose 管理 MongoDB

Mongoose 是 Node.js 中最受歡迎的 MongoDB ODM (Object Document Mapper)，提供結構化的資料模型、驗證與中間件功能。

### 安裝與設定

```bash
npm install mongoose
```

```javascript
import mongoose from 'mongoose'

await mongoose.connect('mongodb://localhost:27017/myapp')
console.log('Mongoose 已連線')
```

### 定義 Schema 與 Model

Mongoose 的核心是 Schema，用於定義文件的結構與驗證規則：

```javascript
const userSchema = new mongoose.Schema({
  name: {
    type: String,
    required: [true, '姓名為必填'],
    trim: true,
    minlength: [2, '姓名至少需要 2 個字元']
  },
  email: {
    type: String,
    required: true,
    unique: true,
    lowercase: true,
    match: [/^\S+@\S+\.\S+$/, '請提供有效的 Email']
  },
  age: {
    type: Number,
    min: [0, '年齡不能小於 0'],
    max: [150, '年齡不能大於 150']
  },
  tags: [{
    type: String,
    enum: ['developer', 'designer', 'manager']
  }],
  profile: {
    bio: { type: String, maxlength: 500 },
    avatar: String
  },
  status: {
    type: String,
    enum: ['active', 'inactive', 'suspended'],
    default: 'active'
  }
}, {
  timestamps: true,  // 自動新增 createdAt 與 updatedAt
  toJSON: { virtuals: true }
})

// 虛擬欄位
userSchema.virtual('isAdult').get(function() {
  return this.age >= 18
})

const User = mongoose.model('User', userSchema)
```

### CRUD 操作

```javascript
// 建立
const user = new User({
  name: 'Alice Chen',
  email: 'alice@example.com',
  age: 28,
  tags: ['developer']
})
await user.save()

// 查詢
const users = await User.find({ age: { $gte: 18 } })
  .sort({ createdAt: -1 })
  .limit(20)
  .select('name email age')
  .populate('posts')

const userById = await User.findById('664f1a2b3c4d5e6f7a8b9c0d')

// 更新
await User.findByIdAndUpdate(user._id,
  { $set: { age: 29 }, $push: { tags: 'manager' } },
  { new: true, runValidators: true }
)

// 刪除
await User.findByIdAndDelete(user._id)
```

### 中間件 (Middleware)

Mongoose 中間件提供了 hook 功能，在特定操作前後執行邏輯：

```javascript
// 儲存前自動加密密碼
userSchema.pre('save', async function(next) {
  if (!this.isModified('password')) return next()
  this.password = await bcrypt.hash(this.password, 10)
  next()
})

// 查詢後處理
userSchema.post('find', function(docs) {
  docs.forEach(doc => {
    doc.loginCount = doc.loginHistory?.length || 0
  })
})
```

### 驗證與自訂

```javascript
// 自訂驗證器
userSchema.path('email').validate(async function(email) {
  const count = await mongoose.model('User').countDocuments({
    email,
    _id: { $ne: this._id }
  })
  return count === 0
}, '此 Email 已被使用')

// 自訂方法
userSchema.methods.generateToken = function() {
  return jwt.sign({ id: this._id, role: this.role }, process.env.JWT_SECRET)
}

// 靜態方法
userSchema.statics.findByEmail = function(email) {
  return this.findOne({ email: email.toLowerCase() })
}
```

### 查詢最佳化

```javascript
// 使用 lean() 提升查詢效能 (回傳純 JS 物件)
const fastUsers = await User.find().lean()

// 索引定義
userSchema.index({ email: 1 }, { unique: true })
userSchema.index({ tags: 1, status: 1 })
userSchema.index({ 'profile.bio': 'text' })
```

延伸閱讀：https://www.google.com/search?q=Mongoose+ODM+tutorial+2024
https://www.google.com/search?q=Mongoose+schema+validation+best+practices
