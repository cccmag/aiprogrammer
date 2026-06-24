# 雲端應用架構：分散式設計模式

## 雲端架構原則

### 無狀態設計

```python
# 無狀態應用
# 每個請求都是獨立的
# 狀態儲存在外部（Redis, S3, 資料庫）

from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/api/users/<user_id>')
def get_user(user_id):
    # 從資料庫讀取，不依賴本地狀態
    user = db.get_user(user_id)
    return jsonify(user)
```

### 水平擴展

```python
# 水平擴展 vs 垂直擴展
# 水平：增加更多伺服器
# 垂直：增加伺服器規格

# 雲端優先選擇水平擴展
# 因為雲端按使用量計費
```

## 常見架構模式

### 1. 負載平衡器模式

```python
# 多實例部署
# 負載平衡器分配流量

# Nginx 作為負載平衡器
upstream app_servers {
    server 10.0.0.1:8000;
    server 10.0.0.2:8000;
    server 10.0.0.3:8000;
}

server {
    location / {
        proxy_pass http://app_servers;
    }
}
```

### 2. 讀寫分離

```python
# 主從複製
# 寫入 master，讀取 replicas

# 寫操作
def write_data(data):
    db_master.execute('INSERT INTO ...', data)

# 讀操作
def read_data(query):
    db_replica.execute('SELECT ...', query)
```

### 3. 快取模式

```python
# 多層快取
# - 瀏覽器快取
# - CDN
# - 應用快取（Redis）
# - 資料庫查詢快取

# Redis 快取範例
cache = Redis(host='localhost', port=6379)

def get_user(user_id):
    # 嘗試從快取讀取
    cached = cache.get(f'user:{user_id}')
    if cached:
        return json.loads(cached)

    # 快取未命中，從資料庫讀取
    user = db.get_user(user_id)
    cache.setex(f'user:{user_id}', 3600, json.dumps(user))
    return user
```

## 結語

雲端應用需要不同的設計思維——假設任何元件都可能失敗，需要有無縫擴展和災難恢復的能力。

---

## 延伸閱讀

- [cloud+architecture+patterns+2007](https://www.google.com/search?q=cloud+architecture+patterns+2007)

---