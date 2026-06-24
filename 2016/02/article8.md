# 容器化資料庫應用

## 資料庫容器化的優缺點

**優點**：
- 環境一致性：開發、測試、生產環境完全相同
- 快速部署：幾分鐘內啟動完整的資料庫環境
- 資源隔離：與其他服務分開，不互相影響
- 簡化管理：升級、備份、遷移都更簡單

**缺點**：
- 資料持久化需要正確設定磁碟區
- 效能可能低於原生安裝
- 單一容器不適合離線備份還原

## PostgreSQL

### 基本執行

```bash
docker run -d \
    --name postgres \
    -e POSTGRES_PASSWORD=secret \
    -e POSTGRES_USER=appuser \
    -e POSTGRES_DB=myapp \
    -v postgres_data:/var/lib/postgresql/data \
    -p 5432:5432 \
    postgres:13
```

### 進階設定

```bash
docker run -d \
    --name postgres \
    -e POSTGRES_PASSWORD=secret \
    -v postgres_data:/var/lib/postgresql/data \
    -v /host/custom.conf:/etc/postgresql/postgresql.conf \
    -p 5432:5432 \
    postgres:13 \
    -c config-file=/etc/postgresql/postgresql.conf
```

### 連線與管理

```bash
# 使用 psql 客戶端連線
docker exec -it postgres psql -U appuser -d myapp

# 執行 SQL 檔案
docker exec -i postgres psql -U appuser -d myapp < dump.sql

# 備份資料庫
docker exec postgres pg_dumpall -U appuser > backup.sql
```

## MySQL

### 基本執行

```bash
docker run -d \
    --name mysql \
    -e MYSQL_ROOT_PASSWORD=secret \
    -e MYSQL_DATABASE=myapp \
    -e MYSQL_USER=appuser \
    -e MYSQL_PASSWORD=apppassword \
    -v mysql_data:/var/lib/mysql \
    -p 3306:3306 \
    mysql:8
```

### 初始化腳本

```bash
# 掛載初始化腳本目錄（只在第一次啟動時執行）
docker run -d \
    --name mysql \
    -e MYSQL_ROOT_PASSWORD=secret \
    -v ./init:/docker-entrypoint-initdb.d \
    -v mysql_data:/var/lib/mysql \
    mysql:8
```

### 連線與管理

```bash
# 使用 mysql 客戶端
docker exec -it mysql mysql -u root -p

# 執行 SQL 檔案
docker exec -i mysql mysql -u root -psecret < dump.sql

# 備份
docker exec mysql mysqldump -u root -psecret --all-databases > backup.sql
```

## MongoDB

### 基本執行

```bash
docker run -d \
    --name mongodb \
    -e MONGO_INITDB_ROOT_USERNAME=admin \
    -e MONGO_INITDB_ROOT_PASSWORD=secret \
    -v mongo_data:/data/db \
    -p 27017:27017 \
    mongo:5
```

### 使用 Docker Compose

```yaml
version: "3.8"
services:
  mongodb:
    image: mongo:5
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: secret
    volumes:
      - mongo_data:/data/db
    ports:
      - "27017:27017"

  mongo-express:
    image: mongo-express
    environment:
      ME_CONFIG_MONGODB_SERVER: mongodb
      ME_CONFIG_BASICAUTH_USERNAME: admin
      ME_CONFIG_BASICAUTH_PASSWORD: secret
    ports:
      - "8081:8081"
    depends_on:
      - mongodb

volumes:
  mongo_data:
```

## 資料持久化要點

1. **總是使用 Named Volume**：確保資料在容器重啟後仍然存在。

2. **定期備份**：容器化不應該替代備份策略。

3. **監控磁碟空間**：資料庫日誌和資料可能快速佔用磁碟空間。

4. **分開儲存**：日誌和資料最好分開磁碟區管理。

## 健康檢查

```bash
# PostgreSQL 健康檢查
docker run -d \
    --name postgres \
    -e POSTGRES_PASSWORD=secret \
    --health-cmd="pg_isready -U postgres" \
    --health-interval=10s \
    --health-timeout=5s \
    --health-retries=5 \
    postgres:13
```

## 資料遷移

當需要將資料庫升級或遷移到新主機時：

```bash
# 匯出
docker exec postgres pg_dumpall -U postgres > dump.sql

# 傳送到新主機
scp dump.sql new-host:/path/

# 匯入
docker exec -i postgres psql -U postgres < dump.sql
```

## 參考資源

- https://www.google.com/search?q=PostgreSQL+MySQL+MongoDB+Docker+容器化+部署+設定+2016
- https://www.google.com/search?q=Docker+資料庫+磁碟區+資料持久化+備份+還原
- https://www.google.com/search?q=Docker+Compose+PostgreSQL+MySQL+完整+範例+設定