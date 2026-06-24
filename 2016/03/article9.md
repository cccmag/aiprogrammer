# 日誌與入侵偵測

## 安全日誌的重要性

安全日誌是事後調查與即時偵測的基礎。沒有完善的日誌記錄，安全事件往往要等到造成實際損害才會被發現。

## 應該記錄的事件

### 認證相關
- 登入成功與失敗
- 登出
- 密碼變更
- 權限變更
- Session 異常

### 操作相關
- 重要資料的存取與變更
- 管理功能的呼叫
- 敏感 API 的存取

### 錯誤與異常
- 所有 4xx 與 5xx 錯誤
- 應用程式異常
- 資料庫錯誤

## 日誌內容

每條日誌應該包含：
- 時間戳（使用 UTC）
- 事件類型
- 使用者身份
- 來源 IP
- 請求內容（不含敏感資訊）
- 操作結果

```python
import logging
import json
from datetime import datetime

class SecurityLogger:
    def __init__(self):
        self.logger = logging.getLogger('security')
        self.logger.setLevel(logging.INFO)

    def log_event(self, event_type, user_id, request, details=None):
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'event_type': event_type,
            'user_id': user_id,
            'ip': request.remote_addr,
            'user_agent': request.headers.get('User-Agent'),
            'path': request.path,
            'method': request.method,
            'details': details
        }
        self.logger.info(json.dumps(log_entry))

    def log_login_success(self, user_id, request):
        self.log_event('LOGIN_SUCCESS', user_id, request)

    def log_login_failure(self, username, request, reason):
        self.log_event('LOGIN_FAILURE', None, request, {
            'username': username,
            'reason': reason
        })

security_logger = SecurityLogger()
```

## 日誌保護

安全日誌本身也需要保護：

1. **完整性**：防止篡改
   - 寫入一次後不可修改
   - 使用 append-only 儲存
   - 定期備份到隔離系統

2. **機密性**：
   - 遮罩敏感欄位（如密碼、信用卡號）
   - 存取權限控制

3. **可用性**：
   - 足夠的儲存空間
   - 日誌輪轉策略
   - 異地備份

## 異常偵測

### 基本方法

```python
def detect_anomalous_login(user_id, request):
    # 取得歷史登入資訊
    last_login = get_last_login(user_id)

    # 檢查是否來自新 IP
    if last_login and last_login.ip != request.remote_addr:
        # 記錄但不一定阻擋
        security_logger.log_event('LOGIN_NEW_IP', user_id, request)

    # 檢查是否短時間內多次失敗
    failure_count = get_recent_failures(user_id, minutes=5)
    if failure_count >= 3:
        security_logger.log_event('BRUTE_FORCE_DETECTED', user_id, request)
        return True

    return False
```

### 速率異常

```python
def detect_rate_anomaly(user_id, window_seconds=60, max_requests=100):
    key = f"request_count:{user_id}"
    current = redis_client.get(key)

    if current is None:
        redis_client.setex(key, window_seconds, 1)
        return False

    if int(current) >= max_requests:
        security_logger.log_event('RATE_LIMIT_EXCEEDED', user_id, None, {
            'request_count': int(current),
            'threshold': max_requests
        })
        return True

    redis_client.incr(key)
    return False
```

## SIEM 系統

Security Information and Event Management（SIEM）系統整合來自多個來源的日誌，提供集中式的安全監控。

### 常見 SIEM 工具

**開源**：
- ELK Stack（Elasticsearch + Logstash + Kibana）
- Graylog
- OSSEC

**商業**：
- Splunk
- IBM QRadar
- Microsoft Sentinel

### ELK Stack 部署

```yaml
# docker-compose.yml
version: "3.8"
services:
  elasticsearch:
    image: elasticsearch:7.13.0
    environment:
      - discovery.type=single-node
    volumes:
      - es_data:/usr/share/elasticsearch/data

  logstash:
    image: logstash:7.13.0
    volumes:
      - ./pipeline:/usr/share/logstash/pipeline
    depends_on:
      - elasticsearch

  kibana:
    image: kibana:7.13.0
    ports:
      - "5601:5601"
    depends_on:
      - elasticsearch

volumes:
  es_data:
```

## 告警與響應

建立自動化的告警機制：

```python
def send_alert(alert_type, details):
    # 發送郵件
    send_email(
        to='security@example.com',
        subject=f'Security Alert: {alert_type}',
        body=json.dumps(details, indent=2)
    )

    # 發送 Slack 通知
    send_slack(
        channel='#security-alerts',
        message=f':rotating_light: *{alert_type}*\n{json.dumps(details)}'
    )

    # 緊急阻斷
    if alert_type in ['INTRUSION_DETECTED', 'DATA_EXFILTRATION']:
        block_ip(details['ip'])
        lock_account(details['user_id'])
```

## 合規要求

不同產業有不同的日誌保留要求：

- PCI DSS：至少 1 年，90 天可在線查詢
- HIPAA：至少 6 年
- SOC 2：根據業務需求，通常 1-3 年

## 參考資源

- https://www.google.com/search?q=安全+日誌+記錄+設計+入侵偵測+SIEM+ELK+2016
- https://www.google.com/search?q=安全+事件+日誌+內容+認證+操作+異常+偵測+方法
- https://www.google.com/search?q=PCI+DSS+HIPAA+日誌+保留+期限+合規+要求