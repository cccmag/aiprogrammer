# 進入點腳本實作

## ENTRYPOINT 與 CMD 的差異

Dockerfile 中有兩個看似相似但功能不同的指令：

**CMD**：提供容器的預設執行命令，可被 `docker run` 的參數覆寫。

**ENTRYPOINT**：設定容器的進入點，CMD 的內容會作為參數傳給 ENTRYPOINT。

```dockerfile
# CMD 示例
FROM alpine
CMD ["echo", "hello"]
# docker run myimage  --> 輸出 "hello"
# docker run myimage echo world --> 輸出 "world"（覆寫了 CMD）

# ENTRYPOINT 示例
FROM alpine
ENTRYPOINT ["echo"]
CMD ["hello"]
# docker run myimage --> 輸出 "hello"
# docker run myimage world --> 輸出 "world"（作為參數傳給 echo）
```

## 常見的進入點腳本用途

1. **準備環境**：設定環境變數、驗證必要檔案、建立目錄
2. **處理資料**：資料庫遷移、初始設定
3. **啟動服務**：啟動 Supervisor 管理多個程序

## 基礎進入點腳本

```bash
#!/bin/sh
set -e

echo "容器啟動中..."

# 設定時區
ln -snf /usr/share/zoneinfo/$TZ /etc/localtime
echo $TZ > /etc/timezone

# 建立必要的目錄
mkdir -p /var/log/myapp
mkdir -p /run

# 執行傳入的命令
exec "$@"
```

```dockerfile
FROM alpine
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
CMD ["python", "app.py"]
```

## 資料庫遷移腳本

```bash
#!/bin/sh
set -e

echo "檢查資料庫連線..."
python -c "import MySQLdb; MySQLdb.connect(...)" 2>/dev/null
DB_READY=$?

if [ $DB_READY -ne 0 ]; then
    echo "等待資料庫就緒..."
    sleep 5
    exec "$0" "$@"
fi

echo "執行資料庫遷移..."
python manage.py migrate --no-input

echo "啟動應用程式..."
exec "$@"
```

## 多程序管理

一個容器通常只應該有一個 PID 1 程序，但有些應用需要多個程序（如 Nginx + PHP-FPM）。可以使用 Supervisor 管理多個程序。

### 安裝 Supervisor

```dockerfile
FROM ubuntu:20.04
RUN apt-get update && apt-get install -y supervisor

# 建立 supervisor 設定檔
RUN mkdir -p /var/log/supervisor
COPY supervisor.conf /etc/supervisor/conf.d/app.conf

CMD ["/usr/bin/supervisord", "-n"]
```

### supervisor.conf

```ini
[supervisord]
nodaemon=true
user=root

[program:app]
command=python app.py
directory=/app
stdout_logfile=/var/log/supervisor/app.log
stderr_logfile=/var/log/supervisor/app_err.log
autostart=true
autorestart=true

[program:worker]
command=celery -A myapp worker
directory=/app
stdout_logfile=/var/log/supervisor/worker.log
stderr_logfile=/var/log/supervisor/worker_err.log
autostart=true
autorestart=true
```

## 使用環境變數的進入點

```bash
#!/bin/sh
set -e

# 設定預設值
: ${DATABASE_URL:=postgres://localhost:5432/myapp}
: ${REDIS_URL:=redis://localhost:6379}
: ${LOG_LEVEL:=INFO}

export DATABASE_URL REDIS_URL LOG_LEVEL

echo "環境設定完成"
echo "DATABASE_URL: ${DATABASE_URL}"
echo "LOG_LEVEL: ${LOG_LEVEL}"

exec "$@"
```

## 信號處理

進入點腳本應正確處理 Linux 信號，確保應用程式能優雅地關閉。

```bash
#!/bin/sh

# 捕獲 SIGTERM 信號
term_handler() {
    echo "收到 SIGTERM，準備關閉..."
    # 停止服務
    kill -TERM $PID
    exit 0
}

trap term_handler SIGTERM

# 啟動應用程式
python app.py &
PID=$!

# 等待應用程式結束
wait $PID
```

## 進入點腳本檢查清單

1. 總是以 `set -e` 開頭，讓指令失敗時立即退出
2. 總是以 `exec "$@"` 結尾，避免 shell 吃掉 PID 1 的地位
3. 處理 SIGTERM 信號，確保可優雅關閉
4. 新增 `--help` 或 `--version` 支援
5. 在 `/bin/sh` 而非 `/bin/bash` 執行，提高相容性

## 參考資源

- https://www.google.com/search?q=Docker+ENTRYPOINT+CMD+差異+Script+進入點+教學+2016
- https://www.google.com/search?q=Docker+進入點+腳本+範例+資料庫遷移+Supervisor+多程序
- https://www.google.com/search?q=Docker+ENTRYPOINT+SIGTERM+優雅+關閉+signal+handle