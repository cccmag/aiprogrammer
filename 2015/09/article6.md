# CDN 的原理與應用

## 前言

CDN（Content Delivery Network）透過全球分布的伺服器加速內容傳遞。

---

## CDN 運作原理

### 沒有 CDN

```
使用者 ──────────────────────────────────> 原始伺服器（美國）
                 200ms 延遲
```

### 使用 CDN

```
使用者（台北）───> CDN 邊緣節點（香港）───> 原始伺服器（美國）
        20ms            5ms                  5ms
                  快取命中時直接回應
```

### 快取機制

1. **靜態資源快取**：圖片、CSS、JS 等
2. **邊緣儲存**：靠近使用者的位置
3. **智慧路由**：選擇最佳節點
4. **快取失效**：自動化更新

---

## CDN 核心功能

### 1. 地理分散

```
┌─────────┐
│ 全球POP │
└────┬────┘
     │
┌────┴────┬──────────┬──────────┐
│         │          │          │
Asia    Europe    Americas   Oceania
```

### 2. 負載均衡

```python
# DNS 負載均衡
# 使用者 -> 最接近的 CDN 節點 -> 原始伺服器
```

### 3. SSL/TLS 終止

```http
使用者 ──HTTPS──> CDN 邊緣節點 ──HTTP──> 原始伺服器
```

---

## CDN 供應商

### 主流 CDN

| 供應商 | 特點 |
|--------|------|
| CloudFlare | 免費方案、簡單易用 |
| Akamai | 最大規模、企業級 |
| CloudFront | AWS 生態系整合 |
| Fastly | 即時快取清除、VCL |
| MaxCDN | 簡單、WordPress 友好 |

[搜尋 CDN providers comparison](https://www.google.com/search?q=CDN+providers+comparison)

---

## CDN 設定

### CloudFlare 範例

```bash
# DNS 設定
# 將 example.com 的 A 紀錄指向 CDN
example.com.  A  203.0.113.1  (原始伺服器)

# CNAME 設定
cdn.example.com.  CNAME  example.com.cdn.cloudflare.com.
```

### 快取控制

```http
# 原始伺服器設定 Cache-Control
Cache-Control: public, max-age=86400, s-maxage=3600

# CDN 會遵守這些設定
```

### 快取清除

```bash
# CloudFlare API
curl -X DELETE "https://api.cloudflare.com/client/v4/zones/{zone}/purge_cache" \
     -H "Authorization: Bearer {token}" \
     -H "Content-Type: application/json" \
     -d '{"files":["https://example.com/style.css"]}'
```

---

## CDN 對效能的影響

### 測量

| 指標 | 無 CDN | 有 CDN |
|------|--------|--------|
| TTFB | 200ms | 20ms |
| 下載速度 | 2 Mbps | 50 Mbps |
| 可用性 | 99.5% | 99.9% |

### 核心指標

- **TTFB**：Time To First Byte
- **下載速度**：影響大檔案
- **快取命中率**：影響重複訪問

---

## 快取策略

### URL Hashing

```
# 將檔名加上 hash
style.abc123.css  # 內容改變時 hash 改變
```

### 自動化

```yaml
# 部署腳本
- name: 部署到 CDN
  run: |
    # 部署靜態檔案到 CDN
    aws s3 sync build/ s3://my-cdn/ --delete
    # 自動化清除 CDN 快取
    aws cloudfront create-invalidation --distribution-id XXX --paths "/*"
```

---

## 安全考量

### DDoS 防護

```bash
# CDN 提供商的 DDoS 緩解
# 流量先經過 CDN 清洗
```

### 憑證管理

```bash
# 使用 CDN 提供的免費 SSL
# Let's Encrypt 整合
```

### 存取控制

```nginx
# 只允許 CDN IP 訪問原始伺服器
allow 103.21.244.0/22;
allow 103.22.200.0/22;
deny all;
```

---

## 小結

CDN 是提升效能的重要工具，選擇合適的 CDN 能顯著改善使用者體驗。

---

*作者：AI 程式人團隊*

*延伸閱讀：*
- [CloudFlare 官網](https://www.google.com/search?q=CloudFlare+official)
- [CDN 效能測試](https://www.google.com/search?q=CDN+performance+testing)