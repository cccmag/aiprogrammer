# 文章 5：Prisma ORM

## 現代化的資料庫 ORM 工具

Prisma 是新一代的 Node.js/TypeScript ORM，提供型別安全的資料庫存取、自動產生的查詢用戶端與強大的遷移工具。

### 安裝與初始化

```bash
npm install @prisma/client
npm install prisma --save-dev
npx prisma init
```

### 資料模型定義

Prisma 使用自己的 Schema 語言定義資料模型：

```prisma
// prisma/schema.prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id        Int      @id @default(autoincrement())
  email     String   @unique
  name      String
  age       Int?
  posts     Post[]
  profile   Profile?
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}

model Post {
  id        Int      @id @default(autoincrement())
  title     String
  content   String?
  published Boolean  @default(false)
  author    User     @relation(fields: [authorId], references: [id])
  authorId  Int
  tags      String[]
  createdAt DateTime @default(now())
}

model Profile {
  id     Int    @id @default(autoincrement())
  bio    String
  avatar String?
  userId Int    @unique
  user   User   @relation(fields: [userId], references: [id])
}
```

### 執行遷移

```bash
npx prisma migrate dev --name init
npx prisma generate
```

### CRUD 操作

```javascript
import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

// 建立資料
async function createUser(data) {
  return await prisma.user.create({
    data: {
      name: data.name,
      email: data.email,
      age: data.age,
      profile: {
        create: { bio: data.bio || '' }
      }
    },
    include: { profile: true }
  })
}

// 查詢資料
const users = await prisma.user.findMany({
  where: {
    age: { gte: 18 },
    posts: { some: { published: true } }
  },
  orderBy: { createdAt: 'desc' },
  take: 20,
  skip: 0,
  include: {
    posts: {
      where: { published: true },
      select: { title: true, createdAt: true }
    },
    profile: true
  }
})

// 單一查詢
const user = await prisma.user.findUnique({
  where: { email: 'alice@example.com' },
  include: { posts: true }
})

// 更新資料
await prisma.user.update({
  where: { id: 1 },
  data: {
    age: { increment: 1 },
    posts: {
      create: { title: '新文章', content: 'Prisma 教學' }
    }
  }
})

// 刪除資料
await prisma.user.delete({
  where: { id: 1 }
})
```

### 關聯查詢

Prisma 的自動關聯處理大幅簡化了 JOIN 操作：

```javascript
// 建立關聯資料
const post = await prisma.post.create({
  data: {
    title: 'Prisma 入門',
    content: '學習 Prisma ORM',
    author: { connect: { email: 'alice@example.com' } },
    tags: ['database', 'orm', 'prisma']
  },
  include: {
    author: { select: { name: true, email: true } }
  }
})

// 巢狀關聯查詢
const result = await prisma.user.findMany({
  where: {
    posts: {
      some: {
        tags: { has: 'prisma' },
        published: true
      }
    }
  },
  include: {
    posts: {
      where: { published: true },
      include: { author: true }
    }
  }
})
```

### 交易操作

```javascript
async function transferBalance(fromId, toId, amount) {
  return await prisma.$transaction([
    prisma.account.update({
      where: { id: fromId },
      data: { balance: { decrement: amount } }
    }),
    prisma.account.update({
      where: { id: toId },
      data: { balance: { increment: amount } }
    })
  ])
}
```

### 最佳實踐

1. **連線管理**：使用單一 PrismaClient 實例
2. **分頁查詢**：使用 cursor-based pagination 取代 offset
3. **選擇欄位**：只選取需要的欄位減少傳輸
4. **批次處理**：使用 createMany 與 updateMany 批次操作
5. **日誌記錄**：啟用查詢日誌便於除錯

```javascript
const prisma = new PrismaClient({
  log: ['query', 'info', 'warn', 'error'],
})
```

延伸閱讀：https://www.google.com/search?q=Prisma+ORM+tutorial+2024
https://www.google.com/search?q=Prisma+schema+design+best+practices
