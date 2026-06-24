# MongoDB 3.0：WiredTiger

## 前言

MongoDB 3.0 加入了可選的 WiredTiger 儲存引擎，帶來革命性的效能提升。

## WiredTiger 特色

```
WiredTiger 效能提升：
──────────────────────
寫入效能：7-10x
儲存空間：減少 80%
壓縮率：  80% 壓縮
```

## 設定

```javascript
// 啟動 WiredTiger
mongod --storageEngine wiredTiger

// 副本集設定
{
  "_id": "rs0",
  "members": [
    { "_id": 0, "host": "localhost:27017", "storageEngine": "wiredTiger" }
  ]
}
```

## 壓縮

```javascript
// collection 層級壓縮
{ storageEngine: { wiredTiger: { configString: "block_compressor=zlib" } } }

// index 層級
db.collection.createIndex({ field: 1 }, { storageEngine: { wiredTiger: { configString: "prefix_compression=false" } } });
```

---

## 延伸閱讀

- [WiredTiger 文檔](https://www.google.com/search?q=MongoDB+WiredTiger+storage+engine)

---

*本篇文章為「AI 程式人雜誌 2015 年 3 月號」文章之一。*