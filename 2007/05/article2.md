# Google Gears：離線 Web 應用的先驅

## 前言

2007 年，Google 發布了 Gears，這是一個允許 Web 應用離線運作的瀏覽器擴展。

## Gears API

```javascript
// 使用 Google Gears 離線儲存
var db = google.gears.factory.create('beta.database');
db.open('myapp');

// 建立本地資料庫
db.execute('CREATE TABLE IF NOT EXISTS notes (...)');

// 快取資料
db.execute('INSERT INTO notes VALUES (?, ?)', [title, content]);
```

## 結語

Gears 的概念最終被 HTML 5 Application Cache 和 LocalStorage 取代。

---

## 延伸閱讀

- [Google+Gears+2007](https://www.google.com/search?q=Google+Gears+2007)

---