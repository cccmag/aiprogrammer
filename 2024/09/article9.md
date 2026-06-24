# GraphQL 查詢語言

## GraphQL 查詢語法

GraphQL 查詢語言讓客戶端可以宣告式地指定需要的資料結構。伺服器回傳的 JSON 結構完全匹配查詢結構。

## Query（查詢）

```graphql
# 基本查詢
query {
  user(id: 42) {
    name
    email
    profile {
      avatar
      bio
    }
  }
}

# 回應
{
  "data": {
    "user": {
      "name": "Alice Chen",
      "email": "alice@example.com",
      "profile": {
        "avatar": "https://example.com/avatar.jpg",
        "bio": "Full-stack developer"
      }
    }
  }
}
```

### 查詢參數與變數

```graphql
# 查詢變數（Query Variables）
query GetUser($userId: ID!, $includePosts: Boolean!) {
  user(id: $userId) {
    name
    email
    posts @include(if: $includePosts) {
      title
      createdAt
    }
  }
}

# 變數 JSON
{
  "userId": "42",
  "includePosts": true
}
```

### 片段（Fragment）

片段讓查詢可以重複使用欄位組合：

```graphql
fragment UserFields on User {
  id
  name
  email
  createdAt
}

query GetUsers {
  users {
    ...UserFields
    posts {
      title
      author {
        ...UserFields
      }
    }
  }
}

query GetUser($id: ID!) {
  user(id: $id) {
    ...UserFields
    profile {
      bio
    }
  }
}
```

## Mutation（變更）

Mutation 用於修改資料，與 Query 的語法相同，但語意不同——Mutation 是修改操作，Query 是讀取操作：

```graphql
mutation CreatePost($input: CreatePostInput!) {
  createPost(input: $input) {
    id
    title
    createdAt
    author {
      name
    }
  }
}

# 變數
{
  "input": {
    "title": "GraphQL 入門",
    "content": "GraphQL 是一種查詢語言...",
    "authorId": "42"
  }
}
```

## Subscription（訂閱）

Subscription 建立了 WebSocket 連線，用於即時推送：

```graphql
subscription OnNewPost {
  newPost {
    id
    title
    author {
      name
    }
    createdAt
  }
}
```

```javascript
// Apollo Server 實作
const { PubSub } = require('graphql-subscriptions');
const pubsub = new PubSub();

const resolvers = {
  Subscription: {
    newPost: {
      subscribe: () => pubsub.asyncIterator(['NEW_POST'])
    }
  },
  Mutation: {
    createPost: async (_, { input }) => {
      const post = await db.posts.create(input);
      pubsub.publish('NEW_POST', { newPost: post });
      return post;
    }
  }
};
```

## 指令（Directive）

```graphql
# 內建指令
# @include(if: Boolean)：條件包含
# @skip(if: Boolean)：條件跳過
# @deprecated(reason: String)：標記已棄用

query GetUsers($withEmail: Boolean!) {
  users {
    name
    email @include(if: $withEmail)
    role @skip(if: $withEmail)
  }
}

# 自訂指令
# @auth：需要認證
# @rateLimit：速率限制
```

## DataLoader：解決 N+1 問題

```javascript
const DataLoader = require('dataloader');

// 批次載入函式
const batchUsers = async (ids) => {
  const users = await db.users.findAll({
    where: { id: ids }
  });
  // DataLoader 要求結果順序與輸入 ID 順序一致
  return ids.map(id => users.find(u => u.id === id) || null);
};

const userLoader = new DataLoader(batchUsers);

const resolvers = {
  Post: {
    author: (post, _, { loaders }) => {
      return loaders.userLoader.load(post.authorId);
    }
  },
  Comment: {
    author: (comment, _, { loaders }) => {
      return loaders.userLoader.load(comment.authorId);
    }
  }
};

// Apollo Server 上下文中的 DataLoader
const server = new ApolloServer({
  context: () => ({
    loaders: {
      userLoader: new DataLoader(batchUsers),
      postLoader: new DataLoader(batchPosts)
    }
  })
});
```

## 查詢複雜度分析

```javascript
const { createComplexityLimitRule } = require('graphql-validation-complexity');

const server = new ApolloServer({
  schema,
  validationRules: [
    // 限制查詢複雜度
    createComplexityLimitRule(1000, {
      onCost: cost => console.log(`Query cost: ${cost}`)
    })
  ]
});

// 成本計算
// user: 1
// user.posts: 每個 post 加 2
// user.posts.comments: 每個 comment 加 3
// 深度嵌套查詢可能導致指數級成本
```

## Apollo Server 生產配置

```javascript
const { ApolloServer } = require('@apollo/server');
const { expressMiddleware } = require('@apollo/server/express4');
const { ApolloServerPluginDrainHttpServer } = require('@apollo/server/plugin/drainHttpServer');

const server = new ApolloServer({
  typeDefs,
  resolvers,
  plugins: [
    ApolloServerPluginDrainHttpServer({ httpServer }),
    // 持久化查詢（Persisted Queries）
    // 自動化 persisted query 快取
  ],
  introspection: process.env.NODE_ENV !== 'production',
  persistedQueries: {
    ttl: 900  // 15 分鐘
  },
  formatError: (formattedError) => {
    // 統一的錯誤格式
    return {
      code: formattedError.extensions?.code || 'INTERNAL_ERROR',
      message: formattedError.message,
      locations: formattedError.locations,
      path: formattedError.path
    };
  }
});
```

## 小結

GraphQL 的查詢語言賦予了客戶端前所未有的資料取得彈性。但要充分發揮它的威力，需要搭配 DataLoader、查詢複雜度分析和適當的快取策略。

---

## 延伸閱讀

- [GraphQL 學習平台](https://www.google.com/search?q=GraphQL+learning+platform)
- [Apollo Server 文件](https://www.google.com/search?q=Apollo+Server+documentation)
- [GraphQL Security 最佳實踐](https://www.google.com/search?q=GraphQL+security+best+practices)
