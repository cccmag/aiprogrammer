# 錯誤追蹤與回報

## 前言

錯誤追蹤系統幫助開發者快速發現、診斷、修復問題。2016 年的錯誤追蹤工具更加智慧與整合。

## 錯誤追蹤流程

```
錯誤發生 → 捕获異常 → 發送到伺服器 → 群組與分析 → 警報通知 → 解決問題
```

## Sentry SDK 整合

```python
# sentry_integration.py
import sentry_sdk
from sentry_sdk import capture_exception, capture_message

sentry_sdk.init(
    "https://xxx@sentry.io/1234567",
    traces_sample_rate=0.1
)

try:
    result = risky_operation()
except Exception as e:
    capture_exception(e)
    raise

# 手動上報訊息
capture_message("User signed up", level="info")
```

## 錯誤處理裝飾器

```python
# error_handler.py
import functools
import logging
import sentry_sdk

logger = logging.getLogger(__name__)

def handle_errors(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            logger.warning(f"Validation error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            sentry_sdk.capture_exception(e)
            raise
    return wrapper

@handle_errors
def process_data(data):
    # 可能發生錯誤的程式碼
    pass
```

## 自訂錯誤類別

```python
# custom_errors.py

class AppError(Exception):
    def __init__(self, message, code=None, details=None):
        self.message = message
        self.code = code
        self.details = details or {}
        super().__init__(self.message)

class ValidationError(AppError):
    def __init__(self, message, field=None):
        super().__init__(
            message=message,
            code="VALIDATION_ERROR",
            details={"field": field}
        )

class AuthenticationError(AppError):
    def __init__(self, message="Authentication failed"):
        super().__init__(
            message=message,
            code="AUTH_ERROR"
        )

# 使用
raise ValidationError("Invalid email", field="email")
```

## Flask 錯誤處理

```python
# flask_errors.py
from flask import Flask, jsonify
import sentry_sdk

app = Flask(__name__)

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def internal_error(e):
    sentry_sdk.capture_exception(e)
    return jsonify({"error": "Internal server error"}), 500

@app.route("/api/risky")
def risky_endpoint():
    # 可能拋出異常
    pass
```

## 錯誤群組

```python
# error_grouping.py
import hashlib

class ErrorGrouper:
    def __init__(self):
        self.groups = {}
    
    def get_group_key(self, exception):
        # 基於錯誤類型、訊息、堆疊trace 產生指紋
        fingerprint = [
            type(exception).__name__,
            str(exception.args),
        ]
        
        # 加入堆疊trace（簡化）
        import traceback
        tb = traceback.format_exc()
        fingerprint.append(tb.split('\n')[-2])  # 錯誤發生的行
        
        key = hashlib.md5(
            '|'.join(fingerprint).encode()
        ).hexdigest()
        
        return key
    
    def group_error(self, exception):
        key = self.get_group_key(exception)
        
        if key not in self.groups:
            self.groups[key] = {
                'count': 0,
                'first_seen': now(),
                'examples': []
            }
        
        self.groups[key]['count'] += 1
        self.groups[key]['examples'].append(str(exception))
        
        return self.groups[key]
```

## 健康檢查端點

```python
# health_check.py
from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/health')
def health():
    checks = {
        'status': 'healthy',
        'checks': {
            'database': check_database(),
            'redis': check_redis(),
            'external_api': check_external_api()
        }
    }
    
    if all(checks['checks'].values()):
        return jsonify(checks), 200
    else:
        checks['status'] = 'unhealthy'
        return jsonify(checks), 503

def check_database():
    try:
        db.execute("SELECT 1")
        return True
    except:
        return False
```

## 錯誤儀表板

```python
# error_dashboard.py
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List

@dataclass
class ErrorEvent:
    timestamp: datetime
    error_type: str
    message: str
    count: int
    resolved: bool

class ErrorDashboard:
    def __init__(self):
        self.errors: List[ErrorEvent] = []
    
    def get_error_summary(self, hours=24):
        cutoff = datetime.now() - timedelta(hours=hours)
        recent = [e for e in self.errors if e.timestamp > cutoff]
        
        return {
            'total': sum(e.count for e in recent),
            'unique_types': len(set(e.error_type for e in recent)),
            'resolved': sum(1 for e in recent if e.resolved),
            'unresolved': sum(1 for e in recent if not e.resolved),
            'by_type': self._group_by_type(recent)
        }
    
    def _group_by_type(self, errors):
        groups = {}
        for error in errors:
            if error.error_type not in groups:
                groups[error.error_type] = {'count': 0, 'errors': []}
            groups[error.error_type]['count'] += error.count
            groups[error.error_type]['errors'].append(error)
        return groups
```

## 延伸閱讀

- [Sentry 錯誤追蹤](https://www.google.com/search?q=sentry+error+tracking+tutorial+2016)
- [錯誤處理最佳實踐](https://www.google.com/search?q=error+handling+best+practices+2016)
- [分散式錯誤追蹤](https://www.google.com/search?q=distributed+error+tracking+2016)

---

*本篇文章為「AI 程式人雜誌 2016 年 11 月號」DevOps 系列之一。*