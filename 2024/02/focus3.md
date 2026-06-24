# Express 框架入門

## 為什麼需要 Express？

雖然 Node.js 的 `http` 內建模組可以建立 HTTP 伺服器，但直接使用它開發大型應用會遇到許多問題：

- 路由處理繁瑣，需要手動解析 URL
- 請求主體解析需要自行處理
- 缺少中介軟體機制
- 靜態檔案服務需要手動實作

Express 解決了這些問題，它提供了簡潔的 API 和豐富的中介軟體生態。

## 安裝與設定

```bash
# 建立專案
mkdir my-express-app
cd my-express-app
npm init -y

# 安裝 Express
npm install express
```

### 基本伺服器

```javascript
const express = require('express');
const app = express();
const port = 3000;

app.get('/', (req, res) => {
  res.send('Hello Express!');
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
```

相較於純 Node.js，Express 的程式碼更加簡潔直觀。

### 請求與回應物件

Express 擴充了 Node.js 的 `req` 和 `res` 物件，提供許多便利方法：

```javascript
app.get('/user/:id', (req, res) => {
  // 路由參數
  console.log(req.params.id);

  // 查詢字串
  console.log(req.query.page);

  // 回應 JSON
  res.json({ id: req.params.id });

  // 回應狀態碼
  res.status(201).json({ created: true });

  // 重新導向
  res.redirect('/login');
});
```

## 常用中介軟體

Express 的核心設計之一是中介軟體（Middleware）。以下是一些常用的內建和第三方中介軟體：

```javascript
const express = require('express');
const app = express();

// 解析 JSON 請求主體
app.use(express.json());

// 解析 URL 編碼的請求主體
app.use(express.urlencoded({ extended: true }));

// 提供靜態檔案服務
app.use(express.static('public'));

// 記錄請求日誌（自製中介軟體）
app.use((req, res, next) => {
  console.log(`${req.method} ${req.url}`);
  next();
});
```

## 路由基礎

Express 支援鏈式路由定義和路由分組：

```javascript
const express = require('express');
const app = express();

// 基本路由
app.get('/', (req, res) => res.send('Home'));
app.post('/users', (req, res) => res.send('Create user'));
app.put('/users/:id', (req, res) => res.send('Update user'));
app.delete('/users/:id', (req, res) => res.send('Delete user'));

// 萬用路由（匹配所有方法）
app.all('/api/*', (req, res) => {
  res.json({ path: req.path });
});
```

## 路由模組化

將路由拆分成獨立檔案有助於維護：

```javascript
// routes/users.js
const express = require('express');
const router = express.Router();

router.get('/', (req, res) => {
  res.json([{ id: 1, name: 'Alice' }]);
});

router.get('/:id', (req, res) => {
  res.json({ id: req.params.id, name: 'Bob' });
});

module.exports = router;
```

```javascript
// app.js
const express = require('express');
const userRoutes = require('./routes/users');
const app = express();

app.use('/api/users', userRoutes);

app.listen(3000);
```

## 請求生命週期

Express 請求的處理流程如下：

```
請求進入
    ↓
中介軟體 1 → next()
    ↓
中介軟體 2 → next()
    ↓
路由處理器
    ↓
回應送出
    ↓
錯誤中介軟體（如果發生錯誤）
```

## 靜態檔案服務

Express 透過 `express.static` 提供靜態檔案服務：

```javascript
// 將 public 目錄對應到根路徑
app.use(express.static('public'));

// 虛擬路徑前綴
app.use('/static', express.static('public'));
```

目錄結構範例：

```
my-express-app/
├── public/
│   ├── index.html
│   ├── style.css
│   └── app.js
├── routes/
│   └── users.js
├── app.js
└── package.json
```

## 總結

Express 是 Node.js 生態中最成熟的 Web 框架，其簡潔的中介軟體架構和豐富的生態系統使其成為後端開發的首選。從最基本的伺服器到大型應用，Express 提供了從簡到繁的完整方案。

## 延伸閱讀

- [Express 官方文件](https://www.google.com/search?q=Express.js+documentation)
- [Express 入門教學](https://www.google.com/search?q=Express.js+tutorial+beginner)
- [Express 中介軟體清單](https://www.google.com/search?q=Express+middleware+list)
