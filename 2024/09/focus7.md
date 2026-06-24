# GraphQL 入門

## 什麼是 GraphQL

GraphQL 是由 Facebook 在 2015 年開源的 API 查詢語言。與 REST 不同，GraphQL 讓客戶端可以精確指定它需要哪些資料——不多也不少。

## 核心概念

### Schema（型別系統）

GraphQL 的核心是型別系統。每個 API 都由一個 Schema 定義：

```graphql
# Schema 定義
type User {
  id: ID!
  name: String!
  email: String!
  posts: [Post!]!
  createdAt: String
}

type Post {
  id: ID!
  title: String!
  content: String!
  author: User!
  comments: [Comment!]!
}

type Comment {
  id: ID!
  text: String!
  author: User!
}

# 查詢入口
type Query {
  users: [User!]!
  user(id: ID!): User
  posts(limit: Int): [Post!]!
}

# 變更入口
type Mutation {
  createUser(name: String!, email: String!): User!
  createPost(title: String!, content: String!): Post!
}
```

### Query（查詢）

客戶端精確指定需要的欄位：

```graphql
# 客戶端請求
query {
  user(id: "42") {
    name
    email
    posts {
      title
      comments {
        text
      }
    }
  }
}

# 伺服器回應（只回傳要求的欄位）
{
  "data": {
    "user": {
      "name": "Alice Chen",
      "email": "alice@example.com",
      "posts": [
        {
          "title": "GraphQL 入門",
          "comments": [
            { "text": "Great article!" }
          ]
        }
      ]
    }
  }
}
```

### Mutation（變更）

用於建立、更新、刪除資料：

```graphql
mutation {
  createUser(name: "Bob", email: "bob@test.com") {
    id
    name
    email
  }
}
```

### Resolver（解析器）

後端實作 Schema 中每個欄位的資料來源：

```javascript
const resolvers = {
  Query: {
    users: async () => {
      return await db.users.findAll();
    },
    user: async (_, { id }) => {
      return await db.users.findByPk(id);
    }
  },
  User: {
    posts: async (user) => {
      return await db.posts.findAll({ where: { authorId: user.id } });
    }
  },
  Mutation: {
    createUser: async (_, { name, email }) => {
      return await db.users.create({ name, email });
    }
  }
};
```

## GraphQL vs REST

| 面向 | REST | GraphQL |
|------|------|---------|
| 資料取得 | 多個端點，固定結構 | 單一端點，客戶端自訂 |
| 過度擷取 | 常見（回傳多餘欄位） | 不會（只回傳要求的） |
| 不足擷取 | 需要多次請求（N+1） | 單次請求即可 |
| 快取 | HTTP 快取簡單 | 需額外設定 |
| 版本管理 | URI/Header | Schema 演進，無需版本 |
| 檔案上傳 | 原生支援 | 需額外處理 |
| 學習曲線 | 低 | 中 |
| 工具生態 | Swagger/Postman | GraphiQL/Apollo |

### N+1 問題

REST 中常見的問題：取得使用者列表後，對每個使用者再發請求取得文章。GraphQL 透過 DataLoader 解決：

```javascript
const DataLoader = require('dataloader');

const postLoader = new DataLoader(async (userIds) => {
  const posts = await db.posts.findAll({ where: { authorId: userIds } });
  return userIds.map(id => posts.filter(p => p.authorId === id));
});

const resolvers = {
  User: {
    posts: async (user, _, { loaders }) => {
      return loaders.postLoader.load(user.id);
    }
  }
};
```

## GraphQL 的痛點

1. **查詢複雜度分析**：惡意客戶端可以發出超深層巢狀查詢（如 `user → posts → comments → author → ...`）。需要設定查詢深度限制或成本分析。

2. **快取困難**：因為所有請求都到同一個端點（/graphql），HTTP 快取機制無法直接適用。需要在應用層實作。

3. **效能監控**：不同查詢的執行成本差異極大，需要精細的 tracing 和監控。

4. **檔案上傳**：GraphQL 原生不支援檔案上傳。需要透過 Base64 編碼或使用 multipart 請求規範。

## 選擇 GraphQL 的時機

**適合：** 資料關係複雜、前端需要高度彈性、多種用戶端需要不同資料視角

**不適合：** 簡單的 CRUD API、快取是首要考量、團隊缺乏 GraphQL 經驗

---

**下一步**：[文章集錦](articles.md)

## 延伸閱讀

- [GraphQL 官方文件](https://www.google.com/search?q=GraphQL+official+documentation)
- [Apollo GraphQL 教學](https://www.google.com/search?q=Apollo+GraphQL+tutorial)
- [GraphQL vs REST 比較](https://www.google.com/search?q=GraphQL+vs+REST+comparison)
