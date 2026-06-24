# Redis 記憶體儲存的應用場景

## 常見應用

### 快取

```python
# 頁面快取
r.set('page:1', html_content, ex=3600)
```

### 計數器

```python
# API 請求計數
r.incr('api_requests')
```

### Session 儲存

```python
# 使用雜湊儲存 Session
r.hset('session:123', 'user_id', 'user123')
r.expire('session:123', 86400)
```

## 結論

Redis 的高效能和豐富資料結構使其成為現代 Web 應用的重要组件。

---

**延伸閱讀**

- [Redis 記憶體鍵值儲存](focus6.md)