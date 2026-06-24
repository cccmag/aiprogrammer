#!/usr/bin/env node

// node_server.js — Node.js 後端開發示範
// 模擬 Express-like 伺服器、檔案操作、JWT 認證

const http = require('http');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

// 簡易 JWT 實作 (模擬)
function createToken(payload, secret) {
  const header = Buffer.from(JSON.stringify({ alg: 'HS256', typ: 'JWT' })).toString('base64url');
  const body = Buffer.from(JSON.stringify(payload)).toString('base64url');
  const signature = crypto.createHmac('sha256', secret).update(`${header}.${body}`).digest('base64url');
  return `${header}.${body}.${signature}`;
}

function verifyToken(token, secret) {
  const parts = token.split('.');
  if (parts.length !== 3) return null;
  const [header, body, signature] = parts;
  const expected = crypto.createHmac('sha256', secret).update(`${header}.${body}`).digest('base64url');
  if (signature !== expected) return null;
  return JSON.parse(Buffer.from(body, 'base64url').toString());
}

// 簡易路由模擬
class App {
  constructor() {
    this.routes = { GET: {}, POST: {}, PUT: {}, DELETE: {} };
    this.middlewares = [];
  }

  use(fn) { this.middlewares.push(fn); return this; }

  get(path, handler) { this.routes.GET[path] = handler; return this; }
  post(path, handler) { this.routes.POST[path] = handler; return this; }
  put(path, handler) { this.routes.PUT[path] = handler; return this; }
  delete(path, handler) { this.routes.DELETE[path] = handler; return this; }

  handle(req, res) {
    const run = (i) => {
      if (i < this.middlewares.length) {
        this.middlewares[i](req, res, () => run(i + 1));
      } else {
        const route = this.routes[req.method]?.[req.url];
        if (route) route(req, res);
        else { res.statusCode = 404; res.end('Not Found'); }
      }
    };
    run(0);
  }
}

function demo() {
  console.log('=== Node.js 後端開發示範 ===\n');

  // 1. 檔案操作演示
  console.log('1. 檔案系統操作');
  const dir = path.join(__dirname, '_tmp');
  if (!fs.existsSync(dir)) fs.mkdirSync(dir);
  const filePath = path.join(dir, 'hello.txt');
  fs.writeFileSync(filePath, 'Hello, Node.js!', 'utf8');
  const content = fs.readFileSync(filePath, 'utf8');
  console.log(`   寫入/讀取: ${content}`);
  fs.unlinkSync(filePath);
  fs.rmdirSync(dir);
  console.log('   暫存檔案已清理\n');

  // 2. HTTP 伺服器模擬
  console.log('2. HTTP 伺服器模擬');
  const app = new App();

  // 中介軟體
  app.use((req, res, next) => {
    console.log(`   [${new Date().toISOString()}] ${req.method} ${req.url}`);
    next();
  });

  app.get('/api/hello', (req, res) => {
    res.statusCode = 200;
    res.end(JSON.stringify({ message: 'Hello World' }));
  });

  app.post('/api/data', (req, res) => {
    let body = '';
    req.on('data', chunk => body += chunk);
    req.on('end', () => {
      res.statusCode = 201;
      res.end(JSON.stringify({ received: JSON.parse(body) }));
    });
  });

  // 模擬請求
  const req1 = { method: 'GET', url: '/api/hello', on: () => {} };
  const res1 = { statusCode: 0, end: (data) => console.log(`   GET 回應: ${data}`) };
  app.handle(req1, res1);

  // 3. JWT 示範
  console.log('\n3. JWT 認證示範');
  const secret = 'my-secret-key';
  const token = createToken({ userId: 123, role: 'admin' }, secret);
  console.log(`   產生的 Token: ${token}`);
  const decoded = verifyToken(token, secret);
  console.log(`   驗證結果:`, decoded);

  // 路由守衛
  app.use((req, res, next) => {
    const auth = req.headers?.authorization;
    if (req.url.startsWith('/api/protected')) {
      if (!auth || !auth.startsWith('Bearer ')) {
        res.statusCode = 401;
        res.end('Unauthorized');
        return;
      }
      const payload = verifyToken(auth.slice(7), secret);
      if (!payload) {
        res.statusCode = 403;
        res.end('Forbidden');
        return;
      }
      req.user = payload;
    }
    next();
  });

  app.get('/api/protected/profile', (req, res) => {
    res.end(JSON.stringify({ user: req.user }));
  });

  console.log('\n=== 示範完成 ===');
}

if (require.main === module) demo();
