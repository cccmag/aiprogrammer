# Redis 3.0 叢集模式

## 前言

Redis 3.0 最重要的新功能是原生叢集支援，實現了自動分片和故障轉移。

## 叢集架構

```
Redis Cluster 架構：
─────────────────────

        ┌────────────────────┐
        │    客戶端路由       │
        └─────────┬──────────┘
                  │
    ┌─────────────┼─────────────┐
    │             │             │
┌───▼───┐    ┌───▼───┐    ┌───▼───┐
│Master1│    │Master2│    │Master3│
│16384  │    │16384  │    │16384  │
│slots  │    │slots  │    │slots  │
└───┬───┘    └───┬───┘    └───┬───┘
    │             │             │
┌───┴───┐    ┌───┴───┐    ┌───┴───┐
│Replica│    │Replica│    │Replica│
└───────┘    └───────┘    └───────┘
```

## 設定

```bash
# 最小叢集設定（3 個主節點）
redis-server --cluster-enabled yes --cluster-config-file nodes.conf
```

## 客戶端

```javascript
const Redis = require('ioredis');
const cluster = new Redis.Cluster([
  { host: '127.0.0.1', port: 7001 },
  { host: '127.0.0.1', port: 7002 },
  { host: '127.0.0.1', port: 7003 }
]);

// 自動路由
cluster.set('key', 'value');
cluster.get('key');
```

---

## 延伸閱讀

- [Redis Cluster 教學](https://www.google.com/search?q=Redis+Cluster+tutorial)

---

*本篇文章為「AI 程式人雜誌 2015 年 3 月號」文章之一。*