# 快取策略實踐

## Redis 快取

```python
import redis

r = redis.Redis()
r.setex('key', 3600, 'value')
```

## 結論

快取是效能優化的有效手段。

---

**延伸閱讀**

- [瀏覽器快取策略](focus3.md)