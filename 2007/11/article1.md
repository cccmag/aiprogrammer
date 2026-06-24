# Facebook API 開發指南

## 前言

2007 年 5 月，Facebook 發布了開放平台，讓開發者能夠建立 Facebook 應用程式。本指南介紹如何使用 Facebook API 進行開發。

## Facebook 開發者平台

### 註冊開發者帳號

```python
# Facebook 開發前置準備
# 1. 前往 developers.facebook.com
# 2. 註冊為開發者
# 3. 建立應用程式
# 4. 取得 App ID 和 App Secret
```

### Facebook API 版本（2007 年）

2007 年的 Facebook API 还是 REST API：

```python
# Facebook REST API 调用
import hashlib
import time

class FacebookAPI:
    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key

    def call_method(self, method, **params):
        params['method'] = method
        params['api_key'] = self.api_key
        params['v'] = '1.0'
        params['call_id'] = str(time.time())

        # 生成 sig 參數
        sorted_params = sorted(params.items())
        sig_string = ''.join(f'{k}={v}' for k, v in sorted_params)
        sig_string += self.secret_key
        params['sig'] = hashlib.md5(sig_string.encode()).hexdigest()

        return self._make_request(params)

    def _make_request(self, params):
        # 發送請求到 Facebook API
        pass
```

## FBML 與 FBJS

### FBML（Facebook Markup Language）

Facebook 提供了特殊的標記語言來建立動態內容：

```html
<!-- FBML 範例 -->
<fb:profile-pic uid="12345" size="small" />

<fb:name uid="12345" firstnameonly="true" />

<fb:if-user-is-friend>
    <p>你們是朋友！</p>
</fb:if-user-is-friend>

<fb:serverFbml>
    <script type="text/fbml">
        <fb:fbml>
            <fb:user-item uid="12345" />
        </fb:fbml>
    </script>
</fb:serverFbml>
```

### FBJS（Facebook JavaScript）

FBJS 提供了安全的 JavaScript 環境：

```javascript
// FBJS 範例
function showDialog() {
    Dialog.create('Hello', 'Welcome to Facebook!', 'OK');
}

function getUserInfo() {
    var user = document.get Facebook().getLoggedInUser();
    return user;
}
```

## FQL（Facebook Query Language）

FQL 允許使用類似 SQL 的語法查詢 Facebook 資料：

```python
# FQL 查詢範例
fql_queries = {
    'user_info': '''
        SELECT uid, name, hometown, birthday
        FROM user
        WHERE uid = {uid}
    ''',
    'friends': '''
        SELECT uid, name
        FROM user
        WHERE uid IN (
            SELECT uid2
            FROM friend
            WHERE uid1 = {uid}
        )
    '''
}
```

## 常見 API 端點

### 使用者資訊

| 端點 | 說明 |
|------|------|
| `users.getInfo` | 取得使用者資料 |
| `users.hasAppPermission` | 檢查權限 |
| `friends.get` | 取得好友列表 |
| `friends.areFriends` | 檢查友誼關係 |

### 動態時報

| 端點 | 說明 |
|------|------|
| `feed.publishUserAction` | 發布動態 |
| `feed.getFriendsNews` | 取得好友動態 |
| `feed.publishStoryToUser` | 發布故事給用戶 |

### 應用程式

| 端點 | 說明 |
|------|------|
| `apps.isCanvassed` | 檢查是否能夠顯示 |
| `apps.getPublicInfo` | 取得應用資訊 |

## 結語

Facebook API 開創了社交應用開發的新時代。透過開放平台，開發者能夠建立豐富的社交應用，觸及數百萬用戶。

---

## 延伸閱讀

- [Facebook+API+2007+development](https://www.google.com/search?q=Facebook+API+2007+development)
- [Facebook+FBML+FQL+API](https://www.google.com/search?q=Facebook+FBML+FQL+API)

---