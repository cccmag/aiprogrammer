# Express 4.0 深入解析

## 前言

Express 4.0 帶來了重大架構調整，讓框架更加輕量和彈性。

## 主要變更

### 移除內建中介層

```javascript
// Express 3.x
app.use(express.bodyParser());
app.use(express.logger());
app.use(express.compress());

// Express 4.x（需單獨安裝）
var bodyParser = require('body-parser');
var morgan = require('morgan');
var compression = require('compression');

app.use(bodyParser.json());
app.use(morgan('dev'));
app.use(compression());
```

### 路由系統增強

```javascript
// 多個路由器
var apiRouter = express.Router();
var adminRouter = express.Router();

apiRouter.get('/users', (req, res) => { /* ... */ });
adminRouter.get('/dashboard', (req, res) => { /* ... */ });

app.use('/api', apiRouter);
app.use('/admin', adminRouter);
```

### 錯誤處理

```javascript
// 同步錯誤自動傳播
app.get('/', (req, res) => {
  throw new Error('Oops!');
});

// 異步錯誤需要 next(err)
app.get('/async', (req, res, next) => {
  asyncOperation((err, data) => {
    if (err) return next(err);
    res.json(data);
  });
});
```

---

## 延伸閱讀

- [Express 4.x 文檔](https://www.google.com/search?q=Express+4+migration+guide)

---

*本篇文章為「AI 程式人雜誌 2015 年 2 月號」文章之一。*