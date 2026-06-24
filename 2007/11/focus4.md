# 社交網路的安全性：隱私與信任

## 社交網路的安全挑戰

### 主要威脅

```
社交網路安全威脅：
──────────────────
1. 身份竊取
2. 社交工程
3. 惡意應用
4. 隱私洩露
5. 網路釣魚
6. 資料外洩
```

## 隱私設定

### Facebook 隱私設定（2007 年）

```python
# 隱私設定級別
privacy_levels = {
    'everyone': '完全公開',
    'friends_of_friends': '好友的好友',
    'friends_only': '僅好友',
    'private': '僅自己'
}

# 設定動態隱私
def set_post_privacy(post, level):
    if level == 'everyone':
        post.public = True
    elif level == 'friends_only':
        post.visible_to = 'friends'
```

### 應用程式許可權

```python
# 許可權控制
# 用戶需要決定應用程式可以存取什麼

# 敏感許可權
dangerous_permissions = [
    'offline_access',      # 離線存取
    'publish_stream',      # 代發動態
    'read_mailbox',        # 讀取訊息
    'friends_photos',      # 存取好友相片
]
```

## 惡意軟體防護

### 應用程式驗證

```python
# Facebook 對應用程式的審核
# 2007 年的審核沒有後來嚴格
# 但有一些基本規則

class AppSecurity:
    def validate_app(self, app):
        # 檢查是否有害
        if self.has_malicious_code(app):
            return False

        # 檢查許可權請求
        if self.requests_dangerous_perms(app):
            return False

        return True
```

### 點擊劫持防護

```html
<!-- Frame busting -->
<script>
if (top != self) {
    top.location = self.location;
}
</script>
```

## 結語

社交網路的安全需要在功能性和隱私之間取得平衡。2007 年的經驗教訓為後來的安全改進奠定了基礎。

---

## 延伸閱讀

- [social+network+privacy+security+2007](https://www.google.com/search?q=social+network+privacy+security+2007)

---