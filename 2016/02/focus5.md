# 5. 資料管理與磁碟區

## 資料持久化的重要性

容器預設是無狀態的。當容器被刪除時，容器的檔案系統也會被清除。但多數應用程式需要持久化資料，例如資料庫的資料檔案、使用者上傳的檔案、應用程式產生的日誌等。Docker 提供磁碟區（Volume）機制來解決這個問題。

## 磁碟區類型

### Named Volume

由 Docker 管理，可以在多個容器之間共享。

```bash
# 建立磁碟區
docker volume create my_data

# 啟動容器並使用磁碟區
docker run -d -v my_data:/var/lib/data --name app1 myapp

# 另一個容器可掛載同一個磁碟區
docker run -d -v my_data:/var/lib/data --name app2 myapp
```

### Bind Mount

將主機的檔案或目錄直接掛載到容器中。

```bash
# 掛載主機目錄
docker run -d -v /host/path:/container/path --name app myapp

# 唯讀掛載
docker run -d -v /host/path:/container/path:ro --name app myapp
```

### tmpfs Mount

將資料存在記憶體中，適合存放臨時資料或敏感資訊。容器停止後資料會消失。

```bash
# tmpfs 掛載
docker run -d --tmpfs /run:rw,noexec,nosuid,size=64m --name app myapp
```

## 在 Docker Compose 中使用磁碟區

```yaml
version: "3.8"
services:
  app:
    image: myapp
    volumes:
      - app_data:/var/lib/app
      - ./config:/etc/myapp:ro
  db:
    image: postgres:13
    volumes:
      - db_data:/var/lib/postgresql/data

volumes:
  app_data:
  db_data:
```

## 資料庫的磁碟區設定

資料庫容器需要將資料目錄掛載為磁碟區以確保資料持久化。

```bash
# PostgreSQL
docker run -d \
    --name postgres \
    -e POSTGRES_PASSWORD=secret \
    -v postgres_data:/var/lib/postgresql/data \
    postgres:13

# MySQL
docker run -d \
    --name mysql \
    -e MYSQL_ROOT_PASSWORD=secret \
    -v mysql_data:/var/lib/mysql \
    mysql:8
```

## 備份與還原

### 備份磁碟區

```bash
# 建立臨時容器來備份磁碟區
docker run --rm \
    -v postgres_data:/data \
    -v $(pwd):/backup \
    alpine \
    tar czf /backup/backup.tar.gz -C /data .
```

### 還原磁碟區

```bash
# 建立磁碟區
docker volume create postgres_data

# 還原資料
docker run --rm \
    -v postgres_data:/data \
    -v $(pwd):/backup \
    alpine \
    tar xzf /backup.tar.gz -C /data
```

## 磁碟區管理

```bash
# 列出所有磁碟區
docker volume ls

# 檢視磁碟區詳細資訊
docker volume inspect my_data

# 刪除未使用的磁碟區
docker volume prune

# 刪除指定磁碟區
docker volume rm my_data
```

## 資料共享模式

在開發環境中，常需要主機的程式碼變更即時反映到容器中。Bind mount 是常見的解決方案。

```bash
# 開發模式：掛載主機目錄
docker run -d \
    -v $(pwd):/app \
    -v /app/node_modules \
    --name dev_app \
    myapp
```

使用兩個掛載是為了防止 `node_modules` 被主機目錄覆蓋（因為 host 通常沒有 node_modules 目錄）。

## 參考資源

- https://www.google.com/search?q=Docker+磁碟區+Volume+資料持久化+bind+mount+tmpfs+2016
- https://www.google.com/search?q=Docker+Compose+volumes+設定+資料庫+掛載+教學
- https://www.google.com/search?q=Docker+磁碟區+備份+還原+tar+資料庫+資料+方法