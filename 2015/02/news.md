# 本月新知

## 2015 年 2 月 Node.js 與伺服端技術動態

### Node.js 生態系

**Express 4.0 穩定版**

 Express 4.0 帶來了重大架構調整：

- **移除內建的 Connect 中介層**：需單獨安裝
- **路由器增強**：支援多個路由器
- **app.use() 行為改變**：更嚴格的路由匹配
- **更好的錯誤處理**：統一的錯誤處理中介層

```javascript
// Express 4.0 變更
// 舊版
var express = require('express');
var app = express();

// 新版同樣語法，但中介層需單獨安裝
var morgan = require('morgan');     // 取代 express.logger
var bodyParser = require('body-parser');
var compression = require('compression');
```

**npm 3.0 開發中**

npm 3.0 預計帶來：

- **更智慧的依賴解析**：減少重複安裝
- **平行安裝**：加快安裝速度
- **更好的離線支援**：離線時使用本地快取

### 框架動態

**Koa 1.0 發布**

由 Express 團隊原班人馬打造的 Koa 發布 1.0：

```javascript
// Koa 使用 async/await
var koa = require('koa');
var app = koa();

app.use(async function(ctx, next) {
  var start = new Date();
  yield next;
  var ms = new Date() - start;
  console.log('%s %s - %s', this.method, this.url, ms);
});

app.listen(3000);
```

**Sails.js 0.11**

Sails 發布 0.11 版本，強化了：
- WebSocket 整合
- 自動生成 REST API
- 資料庫 ORM 支援

### 資料庫

**MongoDB 3.0 發布**

MongoDB 3.0 帶來重大效能提升：

```
MongoDB 3.0 新特性：
────────────────────
- WiredTiger 儲存引擎（可選）
- 壓縮率高達 80%
- 寫入效能提升 7-10x
- MMAPv1 引擎持續支援
```

### 雲端服務

**AWS Lambda 支援 Node.js**

AWS Lambda 正式支援 Node.js，讓無伺服器架構更加普及：

```javascript
// AWS Lambda 函式
exports.handler = function(event, context) {
  console.log('Received event:', event);
  context.succeed('Hello from Lambda!');
};
```

### 業界動態

- **PayPal 擴大 Node.js 使用**：從部分服務擴展到核心系統
- **Netflix 全採用 Node.js**：用於 UI 層
- **Walmart 加入 Node.js 基金會**：企業採用持續增加
- **Node Interactive 大會召開**：歐洲首屆官方 Node.js 大會

### 標準與規範

- **HTTP/2 進展順利**：預計 2015 年中正式通過
- **ECMAScript 2015 定案準備**：所有瀏覽器廠商達成共識
- **Node.js 整合 TC39**：參與 JavaScript 標準制定

---

*本期新知到此結束。下期我們將探討資料庫與 SQL 基礎。*