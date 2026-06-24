# Twitter 與 Facebook API：社交 API

## Twitter API

### API 版本

```python
# Twitter API 1.0

# 基本端點
GET https://api.twitter.com/1/statuses/public_timeline.json

# 認證
# 使用 OAuth 1.0a

# 回應格式
[
  {
    "id": 1234567890,
    "text": "Hello, Twitter!",
    "user": {
      "name": "User Name",
      "screen_name": "username"
    },
    "created_at": "Wed Nov 11 12:00:00 +0000 2009"
  }
]
```

### 應用開發

```python
# Twitter 第三方應用

# 2009 年的熱門應用
# - TweetDeck（桌面客戶端）
# - HootSuite（社群管理）
# - UberTwitter（移動應用）
```

## Facebook Open Graph

### Graph API

```python
# Facebook Graph API

# 基本查詢
GET https://graph.facebook.com/me
GET https://graph.facebook.com/me/friends

# 發布動態
POST https://graph.facebook.com/me/feed
# Body: message="Hello, Facebook!"
```

### 社交插件

```html
<!-- Facebook 社交插件 -->
<div class="fb-like" data-href="https://example.com"
     data-layout="standard" data-action="like"
     data-show-faces="true"></div>

<div class="fb-comments" data-href="https://example.com"
     data-num-posts="5"></div>
```

## 結語

社交 API 創造了新的應用生態系統，改變了人們互動的方式。

---

*本篇文章為「AI 程式人雜誌 2009 年 11 月號」焦點系列之一。*