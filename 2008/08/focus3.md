# 瀏覽器快取策略

## HTTP 緩存

### 快取頭

```http
# Expires（過期時間）
Expires: Thu, 01 Jan 2020 00:00:00 GMT

# Cache-Control（優先）
Cache-Control: max-age=3600, public
```

### ETag

```http
# 伺服器回應
ETag: "abc123"

# 用戶端請求
If-None-Match: "abc123"
```

## 快取策略

### 靜態資源

```python
# 靜態資源長期快取
static_cache_policy = {
    'Cache-Control': 'public, max-age=31536000',
    'Expires': '1 year from now'
}
```

### 動態內容

```python
# 動態內容短期或無快取
dynamic_cache_policy = {
    'Cache-Control': 'no-cache, no-store',
    'Pragma': 'no-cache'
}
```

## 離線應用

### Application Cache

```html
<!-- manifest 檔案 -->
<!DOCTYPE html>
<html manifest="app.cache">
<head>
    <link rel="stylesheet" href="/style.css">
    <script src="/app.js"></script>
</head>
<body>
    <p>Offline capable app</p>
</body>
</html>
```

### Cache Manifest

```text
CACHE MANIFEST
# version 1.0.0

CACHE:
/style.css
/app.js
/offline.html

NETWORK:
/api/*

FALLBACK:
/api/ /offline.json
```

## 結論

正確的快取策略可以大幅減少 HTTP 請求，提升效能。

---

**延伸閱讀**

- [CDN 內容傳遞網路](focus2.md)
- [HTTP+caching](https://www.google.com/search?q=HTTP+caching+best+practices)