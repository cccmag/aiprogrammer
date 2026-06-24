# 社群網路 API 實作

## 概述

本程式實作了一個簡化的社群網路 API，模擬了使用者管理、好朋友關係、發布動態和取得動態等核心功能。

## 核心類別

### SocialNetwork

主要的社群網路類別，提供以下方法：

| 方法 | 說明 |
|------|------|
| `create_user(name, email)` | 建立新使用者 |
| `add_friend(user_id, friend_id)` | 新增好友關係 |
| `get_friends(user_id)` | 取得使用者好友列表 |
| `post_status(user_id, message)` | 發布動態 |
| `get_feed(user_id)` | 取得使用者動態 |

## 資料結構

### 使用者資料

```python
self.users = {
    user_id: {
        'id': user_id,
        'name': '名稱',
        'email': 'email@example.com',
        'created_at': timestamp
    }
}
```

### 好友關係

```python
self.friendships = {
    user_id: {friend_id1, friend_id2, ...}
}
```

### 動態資料

```python
self.posts = [{
    'id': 1,
    'user_id': user_id,
    'message': '動態內容',
    'timestamp': 1234567890,
    'likes': 0
}]
```

## 使用範例

```python
sn = SocialNetwork()

# 建立使用者
alice_id = sn.create_user('Alice', 'alice@example.com')
bob_id = sn.create_user('Bob', 'bob@example.com')

# 成為好友
sn.add_friend(alice_id, bob_id)

# 發布動態
sn.post_status(alice_id, 'Hello, World!')

# 取得動態
feed = sn.get_feed(alice_id)
```

## 與真實社群網路的差異

| 功能 | 模擬實作 | 真實 Facebook |
|------|----------|---------------|
| 認證 | 簡單 | OAuth 2.0 |
| 隱私設定 | 無 | 完整的隱私控制 |
| 按讚功能 | 基本 | 複雜的互動系統 |
| 分享功能 | 無 | 多種分享方式 |
| 訊息功能 | 無 | 即時訊息 |
| 社團功能 | 無 | 社團管理 |

## 執行方式

```bash
python3 social_network.py
```

## 延伸閱讀

- [Facebook+API+2007+Social+Graph](https://www.google.com/search?q=Facebook+API+2007+Social+Graph)
- [social+network+API+design](https://www.google.com/search?q=social+network+API+design)

---