# Python 連接 SQLite

## 使用 Python 操作資料庫

Python 內建 `sqlite3` 模組，無需安裝任何第三方套件即可操作 SQLite 資料庫。這讓 Python 成為學習資料庫操作的絕佳選擇。

## 基本連接與查詢

### 建立連接

```python
import sqlite3

# 連接到資料庫（如果檔案不存在會自動建立）
conn = sqlite3.connect('mydb.db')

# 建立游標（Cursor）
cursor = conn.cursor()

# 執行 SQL
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL
    )
''')

# 提交變更
conn.commit()

# 關閉連接
conn.close()
```

### 使用 with 語句

```python
import sqlite3

with sqlite3.connect('mydb.db') as conn:
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (name, email)
        VALUES (?, ?, ?)
    ''', ('王小明', 'wang@test.com'))
    conn.commit()
```
# 使用 ? 作為參數佔位符可以防止 SQL 注入攻擊

## 參數化查詢

永遠使用參數化查詢，而不是字串格式化：

```python
import sqlite3

# 危險！不要這樣做！
name = "王小明"
# cursor.execute(f"SELECT * FROM users WHERE name = '{name}'")
# 這容易受到 SQL 注入攻擊

# 安全！使用參數化查詢
cursor.execute("SELECT * FROM users WHERE name = ?", (name,))
```

### 多種參數傳遞方式

```python
# 位置參數（使用 ?）
cursor.execute("INSERT INTO users VALUES (?, ?, ?)", (1, '王小明', 'wang@test.com'))

# 命名參數
cursor.execute(
    "INSERT INTO users VALUES (:id, :name, :email)",
    {'id': 2, 'name': '李小華', 'email': 'lee@test.com'}
)

# 從列表插入多筆
users = [
    ('張小英', 'chang@test.com', 25),
    ('陳小豪', 'chen@test.com', 30),
    ('林小美', 'lin@test.com', 28),
]
cursor.executemany(
    "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
    users
)
```

## 查詢結果處理

```python
# 執行查詢
cursor.execute("SELECT * FROM users")

# fetchone()：取一筆
user = cursor.fetchone()
print(user)  # (1, '王小明', 'wang@test.com')

# fetchmany(n)：取 n 筆
users = cursor.fetchmany(3)

# fetchall()：取全部
all_users = cursor.fetchall()

# 迭代游標（節省記憶體，適合大資料集）
for row in cursor:
    print(row)
```

### 結果格式化

```python
# 使用 row_factory 讓結果以字典形式返回
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
cursor.execute("SELECT * FROM users WHERE id = ?", (1,))
row = cursor.fetchone()
print(row['name'])     # 王小明（使用欄位名稱）
print(row['email'])    # wang@test.com

# 自訂 row_factory
def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return dict(zip(fields, row))

conn.row_factory = dict_factory
```

## 完整的 CRUD 範例

```python
import sqlite3

class Database:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                stock INTEGER DEFAULT 0
            )
        ''')
        self.conn.commit()

    def create(self, name, price, stock=0):
        self.cursor.execute(
            "INSERT INTO products (name, price, stock) VALUES (?, ?, ?)",
            (name, price, stock)
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def read(self, product_id=None):
        if product_id:
            self.cursor.execute(
                "SELECT * FROM products WHERE id = ?", (product_id,)
            )
            return self.cursor.fetchone()
        self.cursor.execute("SELECT * FROM products")
        return self.cursor.fetchall()

    def update(self, product_id, name=None, price=None, stock=None):
        fields = []
        values = []
        if name:
            fields.append("name = ?")
            values.append(name)
        if price:
            fields.append("price = ?")
            values.append(price)
        if stock is not None:
            fields.append("stock = ?")
            values.append(stock)
        values.append(product_id)
        self.cursor.execute(
            f"UPDATE products SET {', '.join(fields)} WHERE id = ?",
            values
        )
        self.conn.commit()
        return self.cursor.rowcount

    def delete(self, product_id):
        self.cursor.execute(
            "DELETE FROM products WHERE id = ?", (product_id,)
        )
        self.conn.commit()
        return self.cursor.rowcount

    def close(self):
        self.conn.close()

# 使用範例
db = Database('shop.db')
db.create('iPhone 17', 35900, 50)
db.create('MacBook Air', 42900, 30)

for product in db.read():
    print(f"{product['name']}: ${product['price']}")

db.update(1, price=34900)
db.delete(2)
db.close()
```

## 交易管理

```python
conn = sqlite3.connect('bank.db')

try:
    conn.execute("BEGIN TRANSACTION")
    conn.execute("UPDATE accounts SET balance = balance - 100 WHERE id = 1")
    conn.execute("UPDATE accounts SET balance = balance + 100 WHERE id = 2")
    conn.commit()
    print("轉帳成功")
except Exception as e:
    conn.rollback()
    print(f"轉帳失敗，已回滾：{e}")
finally:
    conn.close()
```

## 從 CSV 匯入資料

```python
import csv
import sqlite3

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY,
        name TEXT,
        department TEXT,
        salary REAL
    )
''')

with open('employees.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        cursor.execute(
            "INSERT INTO employees VALUES (?, ?, ?, ?)",
            (row['id'], row['name'], row['department'], row['salary'])
        )

conn.commit()
conn.close()
```

## 使用記憶體資料庫

```python
# 使用 :memory: 作為資料庫名稱，資料僅存在記憶體中
conn = sqlite3.connect(':memory:')

# 適合測試和臨時資料處理
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE test (id INTEGER, value TEXT)
''')
cursor.execute("INSERT INTO test VALUES (1, 'hello')")
cursor.execute("SELECT * FROM test")
print(cursor.fetchall())  # [(1, 'hello')]

conn.close()
```

## 錯誤處理

```python
import sqlite3
from sqlite3 import Error

def create_connection(db_path):
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        print(f"成功連接到 {db_path}, SQLite 版本: {sqlite3.sqlite_version}")
        return conn
    except Error as e:
        print(f"連接失敗：{e}")
    return conn

def execute_sql(conn, sql, params=None):
    try:
        cursor = conn.cursor()
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        conn.commit()
        return cursor
    except Error as e:
        print(f"SQL 執行錯誤：{e}")
        return None
```

## 參考資料

- [Python sqlite3 官方文檔](https://www.google.com/search?q=Python+sqlite3+module+documentation)
- [Python SQLite 教學](https://www.google.com/search?q=Python+SQLite+tutorial+CRUD)
- [SQL 注入防護](https://www.google.com/search?q=SQL+injection+prevention+Python)
