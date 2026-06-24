# RESTful API 設計原則：資源導向

## REST 的起源

### Roy Fielding 的論文

2000 年，Roy Fielding 在博士論文中提出了 REST（Representational State Transfer）架構風格。

```markdown
REST 核心原則：

1. 客戶-伺服器架構
2. 無狀態（Stateless）
3. 可快取（Cacheable）
4. 層次化系統
5. 統一接口
```

## 資源導向

### 資源 vs 動作

```markdown
# 非 REST（動作導向）
POST /api/getUser?id=123
POST /api/deleteUser

# REST（資源導向）
GET    /api/users/123    # 取得用戶
DELETE /api/users/123     # 刪除用戶
POST   /api/users         # 新增用戶
PUT    /api/users/123     # 更新用戶
```

## HTTP 方法

```python
# RESTful 路由設計

# GET - 讀取
GET    /users        # 取得所有用戶
GET    /users/123    # 取得 ID 為 123 的用戶

# POST - 新增
POST   /users        # 新增用戶
# Body: {"name": "張三", "email": "zhang@example.com"}

# PUT - 完整更新
PUT    /users/123    # 完整更新用戶
# Body: {"name": "張三", "email": "zhang@example.com"}

# PATCH - 部分更新
PATCH  /users/123    # 部分更新
# Body: {"name": "張三"}

# DELETE - 刪除
DELETE /users/123    # 刪除用戶
```

## 狀態碼

```markdown
# HTTP 狀態碼

200 OK              # 成功
201 Created        # 資源創建成功
204 No Content     # 成功但無返回內容
400 Bad Request    # 客戶端錯誤
401 Unauthorized    # 未認證
403 Forbidden       # 無權限
404 Not Found       # 資源不存在
500 Internal Error  # 伺服器錯誤
```

## 結語

RESTful API 設計已成為 Web 服務的標準，其簡單性和一致性是其成功的關鍵。

---

*本篇文章為「AI 程式人雜誌 2009 年 11 月號」焦點系列之一。*