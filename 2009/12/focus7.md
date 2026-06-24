# 開放平台：OAuth、API 經濟、平台化

## OAuth 1.0a 標準化

### 認證流程

```markdown
# OAuth 1.0a 流程

1. 用戶訪問應用
         ↓
2. 應用請求臨時憑證
         ↓
3. 用戶在服務提供商授權
         ↓
4. 應用交換令牌
         ↓
5. 使用令牌訪問 API
```

## 社交平台 API

### Twitter API

```python
# Twitter API 1.0（2009年）

# 端點
GET https://api.twitter.com/1/statuses/public_timeline.json
GET https://api.twitter.com/1/statuses/friends_timeline.json
POST https://api.twitter.com/1/statuses/update.json

# 認證：OAuth 1.0a
```

### Facebook Open Graph

```python
# Facebook Graph API（2009年）

# 基本查詢
GET https://graph.facebook.com/me
GET https://graph.facebook.com/me/friends

# 發布
POST https://graph.facebook.com/me/feed
```

## API 經濟

### 新興服務

```markdown
# 2009 年 API 服務

支付：
- Stripe（成立於 2009 年）
- Braintree（收購）

通信：
- Twilio（雲端電話/短信）

基礎設施：
- AWS（EC2, S3, etc.）
- Twilio
- Parse（mBaaS）
```

## PaaS 平台

```python
# 2009 年 PaaS

Google App Engine：
- Python
- Java（新增）

Heroku：
- Ruby
- 簡單部署

Engine Yard：
- Ruby
- 企業支援

Windows Azure：
- .NET（預覽）
```

## 結語

2009 年是開放平台和 API 經濟的起點，這種模式在後續幾年持續發展壯大。

---

*本篇文章為「AI 程式人雜誌 2009 年 12 月號」焦點系列之一。*