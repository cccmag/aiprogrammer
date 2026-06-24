# Node.js 安全性最佳實踐

## 前言

安全性是伺服端開發的重要課題，本篇介紹 Node.js 應用的安全實踐。

## Express 安全中介層

```javascript
// 安裝
npm install helmet

const helmet = require('helmet');
app.use(helmet());
```

### helmet 功能

```javascript
// 防止點擊劫持
app.use(helmet.frameguard('deny'));

// XSS 防護
app.use(helmet.xssFilter());

// 移除 X-Powered-By
app.use(helmet.hidePoweredBy());
```

## 輸入驗證

```javascript
// 安裝
npm install express-validator

const { body, validationResult } = require('express-validator');

app.post('/register',
  body('email').isEmail(),
  body('password').isLength({ min: 6 }),
  (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }
  }
);
```

## CORS

```javascript
const cors = require('cors');

app.use(cors({
  origin: 'https://example.com',
  credentials: true
}));
```

---

## 延伸閱讀

- [Node.js Security Best Practices](https://www.google.com/search?q=Node.js+security+best+practices)

---

*本篇文章為「AI 程式人雜誌 2015 年 2 月號」文章之一。*