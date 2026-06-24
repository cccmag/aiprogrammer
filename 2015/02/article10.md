# Node.js 認證機制

## 前言

認證是 Web 應用的核心功能，本篇介紹 Node.js 中常見的認證機制。

## Session-based 認證

```javascript
const session = require('express-session');

app.use(session({
  secret: 'my-secret-key',
  resave: false,
  saveUninitialized: false,
  cookie: { secure: true }
}));

app.post('/login', (req, res) => {
  // 驗證用戶
  if (validUser(username, password)) {
    req.session.userId = user.id;
    res.json({ success: true });
  }
});

app.get('/profile', (req, res) => {
  if (req.session.userId) {
    // 取得用戶資料
  }
});
```

## JWT (JSON Web Token)

```javascript
const jwt = require('jsonwebtoken');

const token = jwt.sign(
  { userId: user.id },
  'my-secret-key',
  { expiresIn: '1h' }
);

// 驗證
jwt.verify(token, 'my-secret-key', (err, decoded) => {
  if (err) return res.status(401).json({ error: 'Invalid token' });
  console.log(decoded.userId);
});
```

## OAuth 2.0

```javascript
// Passport.js + OAuth
const passport = require('passport');
const FacebookStrategy = require('passport-facebook').Strategy;

passport.use(new FacebookStrategy({
    clientID: 'FACEBOOK_APP_ID',
    clientSecret: 'FACEBOOK_APP_SECRET',
    callbackURL: '/auth/facebook/callback'
  },
  (accessToken, refreshToken, profile, done) => {
    // 處理用戶資料
    return done(null, profile);
  }
));

app.get('/auth/facebook', passport.authenticate('facebook'));

app.get('/auth/facebook/callback',
  passport.authenticate('facebook', { failureRedirect: '/login' }),
  (req, res) => {
    res.redirect('/');
  }
);
```

---

## 延伸閱讀

- [Node.js Authentication](https://www.google.com/search?q=Node.js+authentication+JWT+passport)

---

*本篇文章為「AI 程式人雜誌 2015 年 2 月號」文章之一。*