# Facebook API 與開放平台：FBML、FQL、API

## Facebook 開放平台

2007 年 5 月，Facebook 發布了開放平台，讓第三方開發者能夠構建應用程式。

### 平台組成

```
Facebook 開放平台元件：
────────────────────────
1. FBML - Facebook Markup Language
2. FQL - Facebook Query Language
3. API - Facebook Platform API
4. FBJS - Facebook JavaScript
5. 應用程式框架
```

## FBML

FBML 是 HTML 的擴展，允許開發者創建 Facebook 內嵌應用。

```html
<!-- FBML 範例 -->
<fb:serverfbml>
  <script type="text/fbml">
    <fb:fbml version="1.1">
      <fb:user uid="12345">
        <fb:name uid="12345"/> is now friends with
        <fb:user uid="67890">
          <fb:name uid="67890"/>
        </fb:user>
      </fb:user>
    </fb:fbml>
  </script>
</fb:serverfbml>
```

### FBML 標籤

```html
<!-- 個人資料方框 -->
<fb:profile-action url="http://example.com/profile">
  View My Profile
</fb:profile-action>

<!-- 好友顯示 -->
<fb:friend-list uid="12345" size="small" flid="45678">
</fb:friend-list>

<!-- 對話框 -->
<fb:dialog id="invite_friends">
  <fb:dialog-title>Invite Friends</fb:dialog-title>
  <fb:dialog-content>
    <fb:friend-selector name="ids"/>
  </fb:dialog-content>
  <fb:dialog-button type="submit" value="Send Invites"/>
</fb:dialog>
```

## FQL

FQL 是類似 SQL 的查詢語言，用於查詢 Facebook 資料。

```sql
-- FQL 查詢範例
-- 查詢好友列表
SELECT uid, name, pic_square
FROM user
WHERE uid IN (
    SELECT uid2
    FROM friend
    WHERE uid1 = me()
)

-- 查詢塗鴉牆
SELECT post_id, actor_id, message
FROM stream
WHERE source_id = me()

-- 查詢相片
SELECT pid, src_small, src_big
FROM photo
WHERE aid IN (
    SELECT aid
    FROM album
    WHERE owner = me()
)
```

```python
# 使用 Facebook API 執行 FQL
import facebook

api = facebook.API('YOUR_API_KEY', 'YOUR_SECRET_KEY')

query = "SELECT name FROM user WHERE uid = 12345"
result = api.fql.query(query)
```

## Facebook API

### API 端點

```python
# Facebook API 呼叫
# 取得使用者資料
api.users.getInfo(uids=[12345], fields=['name', 'pic'])

# 取得好友列表
api.friends.get()

# 發布塗鴉牆
api.stream.publish(
    message='Hello Facebook!',
    uid=12345
)

# 上傳相片
api.photos.upload(
    file=open('photo.jpg'),
    caption='My Photo'
)
```

### 許可權模型

```python
# Facebook 許可權
# 用戶需要授權應用程式存取他們的資料

# 需要的許可權
extended_permissions = [
    'email',
    'offline_access',
    'publish_stream',
    'read_stream',
    'friends_photos'
]

# 授權 URL
auth_url = (
    "https://graph.facebook.com/oauth/authorize?"
    "client_id=YOUR_APP_ID&"
    "redirect_uri=YOUR_REDIRECT_URI&"
    f"scope={','.join(extended_permissions)}"
)
```

## FBJS

FBJS 是 Facebook 的 JavaScript 環境。

```html
<!-- FBJS 範例 -->
<script type="text/javascript">
FBJS.importLibrary('Canvas');

function drawOnCanvas() {
    var canvas = document.getElementById('myCanvas');
    var ctx = canvas.getContext();

    // 只能在 Canvas 中繪製，不能操作頁面
    ctx.fillStyle = 'blue';
    ctx.fillRect(0, 0, 100, 100);
}
</script>
```

## 結語

Facebook 開放平台開創了「社交應用」的先河。Zynga、Playfish 等公司通過這個平台建立了價值數十億美元的業務。

---

## 延伸閱讀

- [Facebook+API+2007+platform](https://www.google.com/search?q=Facebook+API+2007+platform)

---