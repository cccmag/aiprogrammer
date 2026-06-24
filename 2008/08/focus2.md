# CDN 內容傳遞網路

## CDN 運作原理

### 基本概念

```python
# CDN 運作
cdn_flow = {
    '使用者請求': 'http://cdn.example.com/static.js',
    'DNS 解析': '指向最近的 CDN 節點',
    '快取命中': '直接從 CDN 返回',
    '快取未命中': 'CDN 回源站取得資源'
}
```

### 優勢

| 優勢 | 說明 |
|------|------|
| 降低延遲 | 內容分發到靠近使用者的節點 |
| 減輕源站負載 | CDN 承擔靜態資源流量 |
| 提高可用性 | 多節點冗餘 |
| 節省頻寬 | CDN 節點分擔流量 |

## CDN 配置

### 常見 CDN 提供者

```python
cdn_providers = {
    'Akamai': '全球最大 CDN',
    'Cloudflare': '簡易設定',
    'Amazon CloudFront': 'AWS 生態整合',
    'MaxCDN': '專注效能',
    'Fastly': '即時清除'
}
```

### 設定範例

```python
# 假設使用 CloudFront
cloudfront_config = {
    'origin': 'origin.example.com',
    'default_ttl': 86400,
    'price_class': 'PriceClass_All',
    'forward_cookies': 'none',
    'compress': True
}
```

## 快取策略

### Cache-Control

```http
# 快取控制
Cache-Control: public, max-age=31536000
```

### 檔案指紋

```python
# 檔案指紋（用於長期快取）
# 原始檔案：/static/app.js
# 指紋檔案：/static/app.a1b2c3d4.js

def fingerprint(filepath):
    """為檔案添加內容指紋"""
    import hashlib
    with open(filepath, 'rb') as f:
        hash = hashlib.md5(f.read()).hexdigest()[:8]
    name, ext = filepath.rsplit('.', 1)
    return f"{name}.{hash}.{ext}"
```

## 結論

CDN 是提升全球使用者存取速度的關鍵設施。正確配置 CDN 可以大幅提升效能。

---

**延伸閱讀**

- [效能度量與監控](focus1.md)
- [CDN+best+practices](https://www.google.com/search?q=CDN+best+practices)