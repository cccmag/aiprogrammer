# SQL 注入防護

## SQL 注入原理

當應用程式將使用者輸入直接拼接到 SQL 查詢中時，攻擊者可以透過輸入特殊的字元或 SQL 程式碼來操控查詢。

```python
# 不安全的程式碼
query = f"SELECT * FROM users WHERE name = '{username}'"
# 如果攻擊者輸入: username' OR '1'='1
# 查詢變成: SELECT * FROM users WHERE name = '' OR '1'='1'
```

## 參數化查詢

使用參數化查詢（Prepared Statements）可以完全防止 SQL 注入：

```python
# Python + PostgreSQL
from psycopg2 import sql

query = sql.SQL("SELECT * FROM users WHERE name = {}").format(
    sql.Identifier(username)
)
cursor.execute(query)

# 更好：使用 %s 佔位符
cursor.execute("SELECT * FROM users WHERE name = %s", (username,))
```

```python
# Python + MySQL
import pymysql
cursor.execute("SELECT * FROM users WHERE name = %s", (username,))
```

```python
# ORM 使用
# SQLAlchemy
result = session.query(User).filter_by(name=username).first()
```

## 輸入驗證

參數化查詢可以防止 SQL 注入攻擊，但輸入驗證仍然是重要的防御層：

```python
import re

def validate_username(username):
    # 只允許字母數字和底線，長度 3-20
    if not re.match(r'^[a-zA-Z0-9_]{3,20}$', username):
        raise ValueError("Invalid username format")
    return username
```

**重要**：輸入驗證應該使用白名單（允許的模式）而非黑名單（拒絕的模式），因為攻擊者總是能找到繞過黑名單的方法。

## 常見錯誤

### 錯誤 1：使用字串格式化

```python
# 不安全
query = f"SELECT * FROM users WHERE id = {user_id}"
```

### 錯誤 2：ORDER BY 子句中的參數

```python
# 不安全
query = f"SELECT * FROM users ORDER BY {sort_column}"

# 安全：白名單驗證
ALLOWED_SORT_COLUMNS = {'name', 'date', 'id'}
if sort_column not in ALLOWED_SORT_COLUMNS:
    raise ValueError("Invalid sort column")
query = f"SELECT * FROM users ORDER BY {sort_column}"
```

### 錯誤 3：LIKE 子句中的特殊字元

```python
# 不安全：% 和 _ 是 LIKE 的萬用字元
query = f"SELECT * FROM users WHERE name LIKE '%{name}%'"

# 安全：使用參數化查詢並轉義萬用字元
search_term = f"%{name}%"
cursor.execute("SELECT * FROM users WHERE name LIKE %s", (search_term,))
```

## ORM 的安全性

ORM（Object-Relational Mapping）如 SQLAlchemy、Django ORM 通常會自動使用參數化查詢。但仍需注意：

```python
# Django ORM - 安全
User.objects.get(name=username)

# 避免 raw SQL，除非必要且使用參數化
from django.db import connection
with connection.cursor() as cursor:
    cursor.execute("SELECT * FROM users WHERE name = %s", [username])
```

## 錯誤處理

錯誤訊息不應該透露系統架構或資料庫結構：

```python
# 不安全的錯誤訊息
return f"SQL Error: {str(e)}"

# 安全的錯誤處理
logger.error(f"Database error for user {username}")
return "An error occurred. Please try again later."
```

## 最小權限原則

資料庫帳號不應該擁有過多權限：

```sql
-- 只給應用程式需要的權限
GRANT SELECT, INSERT, UPDATE, DELETE ON myapp.* TO 'appuser'@'localhost';

-- 不要給予 DROP、ALTER 等危險權限
```

## 參考資源

- https://www.google.com/search?q=SQL+注入+防護+參數化查詢+Prepared+Statements+2016
- https://www.google.com/search?q=SQL+Injection+防護+Python+psycopg2+SQLAlchemy+範例
- https://www.google.com/search?q=SQL+注入+ORDER+BY+LIKE+特殊+字元+轉義+方法