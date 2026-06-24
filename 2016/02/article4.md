# 磁碟區與資料持久化

## 為什麼需要磁碟區

容器預設是無狀態的，刪除容器後所有資料都會消失。但多數應用（特別是資料庫）需要持久化資料。Docker Volume 提供了資料持久化的機制。

## 磁碟區類型對比

| 類型 | 說明 | 適用場景 |
|------|------|----------|
| Named Volume | Docker 管理的命名磁碟區 | 一般資料持久化 |
| Bind Mount | 主機檔案系統映射 | 開發環境、本機設定 |
| tmpfs | 記憶體檔案系統 | 敏感資料、暫存檔案 |
| Npipe | 命名管道 | 容器間通訊 |

## Named Volume 操作

```bash
# 建立磁碟區
docker volume create my_data

# 匿名磁碟區（自動建立，隨容器刪除）
docker run -v /data myapp

# 列出磁碟區
docker volume ls

# 檢視磁碟區資訊
docker volume inspect my_data

# 刪除未使用磁碟區
docker volume prune

# 刪除指定磁碟區
docker volume rm my_data
```

## Bind Mount 操作

```bash
# 掛載主機目錄
docker run -v /host/path:/container/path myapp

# 唯讀掛載
docker run -v /host/path:/container/path:ro myapp

# 使用 mount 語法（更明確）
docker run --mount type=bind,source=/host/path,target=/container/path myapp
```

## tmpfs 操作

```bash
# 建立 tmpfs 磁碟區
docker run --tmpfs /run:rw,noexec,nosuid,size=64m myapp

# 使用 mount 語法
docker run --mount type=tmpfs,target=/run myapp
```

## 資料庫的磁碟區設定

### PostgreSQL

```bash
docker run -d \
    --name postgres \
    -e POSTGRES_PASSWORD=secret \
    -e POSTGRES_DB=myapp \
    -v postgres_data:/var/lib/postgresql/data \
    postgres:13
```

### MySQL

```bash
docker run -d \
    --name mysql \
    -e MYSQL_ROOT_PASSWORD=secret \
    -e MYSQL_DATABASE=myapp \
    -v mysql_data:/var/lib/mysql \
    mysql:8
```

### MongoDB

```bash
docker run -d \
    --name mongodb \
    -e MONGO_INITDB_ROOT_USERNAME=admin \
    -e MONGO_INITDB_ROOT_PASSWORD=secret \
    -v mongo_data:/data/db \
    mongo:5
```

## 磁碟區遷移

當需要更換主機或升級資料庫時，磁碟區遷移非常有用。

```bash
# 在舊主機上建立備份
docker run --rm \
    -v old_data:/from \
    -v $(pwd):/backup \
    alpine \
    tar czf /backup/backup.tar.gz -C /from .

# 傳送到新主機
scp backup.tar.gz new-host:/path/

# 在新主機上還原
docker volume create new_data
docker run --rm \
    -v new_data:/to \
    -v $(pwd):/backup \
    alpine \
    tar xzf /backup.tar.gz -C /to
```

## 在 Compose 中的磁碟區

```yaml
version: "3.8"
services:
  app:
    image: myapp
    volumes:
      # Named Volume
      - app_data:/var/lib/app
      # Bind Mount
      - ./config:/etc/myapp:ro

  db:
    image: postgres:13
    volumes:
      - db_data:/var/lib/postgresql/data

# 頂層 volumes 區塊宣告命名的磁碟區
volumes:
  app_data:
  db_data:
```

## 磁碟區許可權

在 Linux 上，磁碟區內的檔案由 root 所有。若應用程式以非 root 使用者執行，可能需要調整許可權。

```dockerfile
# 方法一：在 Dockerfile 中建立使用者並設定許可權
RUN mkdir -p /data && chown -R appuser:appgroup /data

# 方法二：在執行時變更許可權
docker run -v my_data:/data myapp chown -R appuser:appgroup /data
```

## 參考資源

- https://www.google.com/search?q=Docker+磁碟區+Volume+資料持久化+named+bind+tmpfs+2016
- https://www.google.com/search?q=Docker+磁碟區+backup+還原+migration+postgresql+mysql
- https://www.google.com/search?q=Docker+Compose+volumes+設定+教學+Named+Volume