# REST vs GraphQL

## API 風格的全面比較

## REST

REST（Representational State Transfer）是 Roy Fielding 在 2000 年提出的架構風格。它以資源為中心，使用 HTTP 方法操作資源。

### REST 的核心概念

```
GET    /users          # 獲取用戶列表
GET    /users/:id      # 獲取單個用戶
POST   /users          # 創建用戶
PUT    /users/:id      # 更新用戶
DELETE /users/:id      # 刪除用戶
```

### REST 的優勢

**簡單直觀**：URL 結構清晰，與 HTTP 方法對應

**快取友好**：利用 HTTP 快取機制

```http
GET /users/123
Cache-Control: public, max-age=3600
```

**廣泛的工具支援**：幾乎所有的 HTTP 用戶端和伺服器框架都支援 REST

### REST 的痛點

**過度獲取（Over-fetching）**

```http
GET /users/123
// 回傳完整用戶物件，即使只需要名稱
{
  "id": 123,
  "name": "Alice",
  "email": "alice@example.com",
  "address": {...},
  "orders": [...],  // 甚至不需要
  "settings": {...}
}
```

**多次請求（Under-fetching）**

```http
GET /users/123           → 獲取用戶
GET /users/123/orders    → 獲取訂單
GET /orders/456/items    → 獲取商品
// 需要多次請求才能獲取完整資料
```

---

## GraphQL

GraphQL 由 Facebook 在 2015 年開源，讓客戶端可以精確指定需要的資料。

### GraphQL 的核心概念

```graphql
# Schema 定義
type User {
  id: ID!
  name: String!
  email: String!
  posts: [Post!]!
}

type Post {
  id: ID!
  title: String!
  content: String!
}

type Query {
  user(id: ID!): User
  posts(limit: Int): [Post!]!
}
```

**客戶端查詢**

```graphql
query {
  user(id: "123") {
    name
    posts {
      title
    }
  }
}
```

**回傳結果**

```json
{
  "data": {
    "user": {
      "name": "Alice",
      "posts": [
        {"title": "GraphQL 入門"},
        {"title": "REST vs GraphQL"}
      ]
    }
  }
}
```

### GraphQL 的優勢

**精確獲取**：只回傳需要的資料

**單一端點**：所有操作通過 `/graphql` 完成

**強型別 Schema**：API 文檔和驗證合一

### GraphQL 的痛點

**快取複雜**：POST 請求難以利用 HTTP 快取

```
解決方案：使用 Apollo Client 或 Relay 的用戶端快取
```

**N+1 查詢問題**

```graphql
query {
  users {
    posts {  // 每個用戶觸發一次資料庫查詢
      title
    }
  }
}
```

```
解決方案：使用 DataLoader 批量載入
```

**查詢複雜度控制**

```graphql
# 惡意查詢：巢狀深度無限
query {
  user {
    friends {
      user {
        friends {
          ...
        }
      }
    }
  }
}
```

```
解決方案：限制查詢深度（如最大 10 層）
```

---

## 實際選擇指南

### 選擇 REST 的場景

- **簡單 CRUD 應用**：不需要靈活的查詢能力
- **對快取要求高**：需要充分利用 HTTP 快取
- **公開 API**：第三方開發者習慣 REST
- **檔案上傳**：REST 對 multipart 支援更好

### 選擇 GraphQL 的場景

- **複雜的資料關聯**：多種前端需要不同資料組合
- **行動端應用**：頻寬有限，需要精確控制回傳資料
- **快速迭代的前端**：前端可以獨立定義資料需求
- **微服務聚合**：透過 GraphQL Gateway 聚合多個服務

---

## 實戰：REST API 範例

```python
# FastAPI REST
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/api/users/{user_id}")
def get_user(user_id: int):
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404)
    return user

@app.get("/api/users/{user_id}/orders")
def get_user_orders(user_id: int):
    return db.query(Order).filter(Order.user_id == user_id).all()
```

## 實戰：GraphQL API 範例

```python
# Strawberry GraphQL
import strawberry

@strawberry.type
class User:
    id: int
    name: str
    email: str

@strawberry.type
class Query:
    @strawberry.field
    def user(self, id: int) -> User:
        return db.query(User).get(id)

schema = strawberry.Schema(query=Query)
```

---

## 混合策略：誰說只能選一個？

```python
# 同時提供 REST 和 GraphQL
# REST: 穩定、可快取的公開 API
# GraphQL: 靈活的內部客戶端查詢

# /api/v2/users — REST 端點
# /graphql — GraphQL 端點
# 內部服務使用 GraphQL 靈活查詢
# 第三方開發者使用 REST 穩定 API
```

---

## 效能對比

| 場景 | REST | GraphQL |
|------|------|---------|
| 取得用戶 + 訂單 | 2 次請求 | 1 次請求 |
| 回傳資料大小 | 大（over-fetching） | 精確 |
| 快取命中率 | 高 | 中 |
| 服務端效能 | 簡單查詢快 | 複雜解析慢 |
| 學習曲線 | 低 | 中 |

---

## 總結

REST 和 GraphQL 不是對立的，而是適合不同場景的工具。REST 的簡單性和快取能力使其非常適合公開 API 和簡單 CRUD，而 GraphQL 的靈活性使其在複雜資料關聯和前端主導的應用中表現出色。選擇時應考量團隊經驗、業務場景和客戶端需求。

---

## 延伸閱讀

- [REST API Design Best Practices](https://www.google.com/search?q=REST+API+design+best+practices)
- [GraphQL Official Guide](https://www.google.com/search?q=GraphQL+official+documentation)
- [REST vs GraphQL Comparison](https://www.google.com/search?q=REST+vs+GraphQL+API+comparison)

---

*本篇文章為「AI 程式人雜誌 2026 年 11 月號」文章系列之二。*
