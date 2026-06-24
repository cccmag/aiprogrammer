# 監控、日誌與維運：生產環境的 Python 應用

## 監控的重要性

### 為什麼需要監控？

```
監控金字塔：
────────────────────────────────

                    ▲
                   /│\
                  / │ \
                 /  │  \
                /   │   \
               /    │    \
              /     │     \
             /      │      \
            /       │       \
           /        │        \
          /         │         \
         /          │          \
        /           │           \
       /            │            \
      /             │             \
     /              │              \
    /               │               \
   ▼                ▼                ▼
 ─────────────────────────────────────────
   可用性監控 → 效能監控 → 業務監控
```

沒有監控的系統就像沒有儀表板的汽車——你不知道速度、油量、溫度和引擎狀態。

## 監控工具

### Prometheus + Grafana

Prometheus 是最受歡迎的開源監控系統，Grafana 則提供了強大的視覺化能力：

```python
# 使用 prometheus_client 暴露指標
from prometheus_client import Counter, Histogram, generate_latest

# 自訂指標
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint']
)

@app.route('/api/users')
def get_users():
    import time
    start = time.time()
    
    # 業務邏輯
    users = User.query.all()
    
    # 記錄指標
    REQUEST_COUNT.labels(method='GET', endpoint='/api/users', status='200').inc()
    REQUEST_LATENCY.labels(method='GET', endpoint='/api/users').observe(time.time() - start)
    
    return jsonify(users)
```

### Flask 監控範例

```python
from flask import Flask, request
from prometheus_client import Counter, Histogram, start_http_server
import time

app = Flask(__name__)

# 在另一執行緒啟動 Prometheus 伺服器
start_http_server(8000)

REQUEST_COUNT = Counter('flask_requests_total', 'Total requests', ['method', 'path'])
REQUEST_LATENCY = Histogram('flask_request_duration_seconds', 'Request duration', ['method', 'path'])

@app.before_request
def before():
    request.start_time = time.time()

@app.after_request
def after(response):
    duration = time.time() - request.start_time
    REQUEST_COUNT.labels(method=request.method, path=request.path).inc()
    REQUEST_LATENCY.labels(method=request.method, path=request.path).observe(duration)
    return response
```

### 其他監控工具

| 工具 | 特點 | 適合場景 |
|------|------|----------|
| DataDog | 全托管、強大分析 | 企業級監控 |
| New Relic | APM 專家 | 應用效能分析 |
| Sentry | 錯誤追蹤 | 異常監控 |
| CloudWatch | AWS 原生 | AWS 部署 |
| Stackdriver | GCP 原生 | GCP 部署 |

## 日誌管理

### 結構化日誌

```python
import logging
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
        return json.dumps(log_data)

# 使用
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger.addHandler(handler)
logger.setLevel(logging.INFO)

logger.info('User logged in', extra={'user_id': 123, 'action': 'login'})
```

### Python 日誌最佳實踐

```python
import logging
import logging.config

# logging.conf 或 dictConfig
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json': {'format': '%(asctime)s %(name)s %(levelname)s %(message)s'},
        'detailed': {'format': '%(asctime)s %(name)s:%(lineno)d %(levelname)s %(message)s'}
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'json',
            'stream': 'ext://sys.stdout'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'detailed',
            'filename': '/var/log/myapp.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console', 'file']
    }
}

logging.config.dictConfig(LOGGING_CONFIG)
```

### 中央化日誌收集

```
日誌收集架構：
────────────────────────────────

  ┌─────────┐   ┌─────────┐   ┌─────────┐
  │ App 1   │   │ App 2   │   │ App 3   │
  │ (Python)│   │ (Python)│   │ (Python)│
  └────┬────┘   └────┬────┘   └────┬────┘
       │             │             │
       └─────────────┼─────────────┘
                     ▼
              ┌─────────────┐
              │  Filebeat   │
              │  (或 Fluentd)│
              └──────┬──────┘
                     ▼
              ┌─────────────┐
              │ Elasticsearch│
              │  (或 Loki)   │
              └──────┬──────┘
                     ▼
              ┌─────────────┐
              │   Kibana    │
              │  (或 Grafana)│
              └─────────────┘
```

## 效能優化

### 常見效能瓶頸

```
Python 應用效能瓶頸：
────────────────────────────────

1. GIL（全域解釋器鎖）
   - CPU 密集任務無法利用多核心
   - 解決：使用 multiprocessing 或 C 擴展

2. 資料庫查詢
   - N+1 查詢問題
   - 解決：使用 JOIN、批量查詢、Redis 快取

3. 同步阻塞 I/O
   - 等待網路回應時阻斷其他請求
   - 解決：使用 async/await

4. 記憶體洩漏
   - 物件未正確釋放
   - 解決：使用弱引用、定期重啟
```

### 效能監控

```python
import cProfile
import pstats
import io

def profile_function(func):
    def wrapper(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        result = func(*args, **kwargs)
        pr.disable()
        
        s = io.StringIO()
        ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
        ps.print_stats(20)  # 前 20 行
        print(s.getvalue())
        return result
    return wrapper

@profile_function
def my_slow_function():
    # ... 你的程式碼
    pass
```

### 效能優化工具

```bash
# 安裝監控工具
pip install line_profiler memory_profiler

# 行級效能分析
python -m memory_profiler myscript.py

# 檢視記憶體使用
@profile
def my_function():
    # ...
    pass
```

## 自動化維運

### 健康檢查端點

```python
from flask import Flask, jsonify
import psycopg2
import redis

app = Flask(__name__)

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

@app.route('/ready')
def ready():
    checks = {
        'database': check_database(),
        'redis': check_redis()
    }
    
    all_healthy = all(checks.values())
    status = 200 if all_healthy else 503
    
    return jsonify({
        'status': 'ready' if all_healthy else 'not_ready',
        'checks': checks
    }), status

def check_database():
    try:
        conn = psycopg2.connect(os.environ['DATABASE_URL'])
        conn.close()
        return True
    except:
        return False

def check_redis():
    try:
        r = redis.from_url(os.environ['REDIS_URL'])
        r.ping()
        return True
    except:
        return False
```

### Graceful Shutdown

```python
import signal
import sys

shutdown_requested = False

def signal_handler(signum, frame):
    global shutdown_requested
    shutdown_requested = True
    print('Shutdown signal received, finishing current requests...')

signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

@app.route('/shutdown')
def shutdown():
    global shutdown_requested
    shutdown_requested = True
    return 'Shutting down...'

# 在請求處理中檢查
def process_request(request):
    if shutdown_requested:
        raise ServiceUnavailable()
    # 正常處理
    pass
```

## 延伸閱讀

- [Prometheus 文件](https://www.google.com/search?q=Prometheus+monitoring+Python+application)
- [Grafana Python 儀表板](https://www.google.com/search?q=Grafana+Python+dashboard)
- [Python 日誌最佳實踐](https://www.google.com/search?q=Python+logging+best+practices)
- [Flask 監控教學](https://www.google.com/search?q=Flask+monitoring+production+tutorial)
- [Kubernetes 健康檢查](https://www.google.com/search?q=Kubernetes+liveness+readiness+probe+Python)

---

*本篇文章為「AI 程式人雜誌 2020 年 10 月號」歷史回顧系列之一。*