# 瀏覽器 API 與現代 JS 開發

## BOM 與 Window 物件

### Window 物件

BOM（Browser Object Model）提供與瀏覽器視窗互動的 API。window 是全域物件：

```javascript
// 視窗資訊
window.innerWidth;   // 視窗寬度
window.innerHeight;  // 視窗高度
window.outerWidth;   // 瀏覽器視窗總寬度
window.outerHeight;  // 瀏覽器視窗總高度
window.screenX;      // 視窗左側位置
window.screenY;      // 視窗頂部位置

// 瀏覽器資訊
window.navigator.userAgent; // 使用者代理字串
window.navigator.language;  // 瀏覽器語言
window.navigator.platform;  // 作業系統平台

// URL 資訊
window.location.href;       // 完整 URL
window.location.protocol;   // 協定（https:）
window.location.host;       // 主機名稱
window.location.pathname;   // 路徑
window.location.search;     // 查詢參數
window.location.hash;       // 雜湊值

// URL 操作
window.location.href = 'https://example.com';
window.location.reload();      // 重新載入頁面
window.location.replace(url);  // 取代當前紀錄
```

### 計時器

```javascript
// setTimeout：延遲執行
const timeoutId = setTimeout(() => {
  console.log('1 秒後執行');
}, 1000);

// 取消 setTimeout
clearTimeout(timeoutId);

// setInterval：定期執行
let count = 0;
const intervalId = setInterval(() => {
  count++;
  console.log(`第 ${count} 次`);
  if (count >= 5) {
    clearInterval(intervalId);
  }
}, 1000);
```

## Fetch API

### 基本用法

Fetch API 是現代瀏覽器提供的 HTTP 請求介面，基於 Promise：

```javascript
// GET 請求
fetch('https://api.example.com/users')
  .then(response => {
    if (!response.ok) {
      throw new Error(`HTTP 錯誤: ${response.status}`);
    }
    return response.json();
  })
  .then(data => console.log('使用者列表:', data))
  .catch(error => console.error('請求失敗:', error));

// 使用 async/await
async function getUsers() {
  try {
    const response = await fetch('https://api.example.com/users');
    if (!response.ok) throw new Error(`狀態: ${response.status}`);
    return await response.json();
  } catch (error) {
    console.error('請求失敗:', error);
    return [];
  }
}
```

### 進階請求

```javascript
// POST 請求
async function createUser(userData) {
  const response = await fetch('https://api.example.com/users', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer your-token'
    },
    body: JSON.stringify(userData)
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message);
  }

  return response.json();
}

// 帶有查詢參數
async function searchUsers(query) {
  const params = new URLSearchParams({
    q: query,
    limit: '10',
    page: '1'
  });
  const response = await fetch(`/api/users?${params}`);
  return response.json();
}

// 上傳檔案
async function uploadFile(file) {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('description', '上傳檔案');

  const response = await fetch('/api/upload', {
    method: 'POST',
    body: formData
  });
  return response.json();
}
```

### 進度監控

```javascript
// 下載進度
async function downloadWithProgress(url) {
  const response = await fetch(url);
  const reader = response.body.getReader();
  const contentLength = +response.headers.get('Content-Length');
  let receivedLength = 0;

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    receivedLength += value.length;
    const progress = (receivedLength / contentLength * 100).toFixed(2);
    console.log(`下載進度: ${progress}%`);
  }
}
```

## Web Storage

### localStorage

```javascript
// 儲存資料
localStorage.setItem('username', 'Alice');
localStorage.setItem('theme', 'dark');
localStorage.setItem('settings', JSON.stringify({
  fontSize: 14,
  notifications: true
}));

// 讀取資料
const username = localStorage.getItem('username');
const settings = JSON.parse(localStorage.getItem('settings'));

// 刪除資料
localStorage.removeItem('theme');

// 清除所有資料
// localStorage.clear();

// 儲存空間變更事件
window.addEventListener('storage', (event) => {
  console.log('儲存空間變更:', {
    key: event.key,
    oldValue: event.oldValue,
    newValue: event.newValue
  });
});
```

### sessionStorage

```javascript
// sessionStorage 在分頁關閉後即清除
sessionStorage.setItem('sessionId', 'abc123');
sessionStorage.setItem('formData', JSON.stringify({
  name: 'Bob',
  email: 'bob@example.com'
}));

const sessionId = sessionStorage.getItem('sessionId');
```

## 模組打包工具

### 現代開發流程

```javascript
// 使用 ES Modules
// math.js
export function add(a, b) { return a + b; }
export const PI = 3.14159;

// app.js
import { add, PI } from './math.js';
console.log(add(PI, 2)); // 5.14159
```

### 常見工具

- **Vite**：新一代前端構建工具，開發伺服器極快
- **Webpack**：功能最完整的打包工具
- **esbuild**：極速的 JavaScript 打包器
- **Rollup**：適合函式庫的打包工具

```javascript
// 使用動態載入
async function loadModule() {
  const module = await import('./heavyModule.js');
  module.doSomething();
}
```

## 綜合範例

```javascript
// 現代 JS 應用範例
async function initApp() {
  // 從 localStorage 載入設定
  const settings = JSON.parse(
    localStorage.getItem('appSettings') || '{}'
  );

  // 從 API 載入資料
  const data = await fetch('/api/data', {
    headers: {
      'Authorization': `Bearer ${settings.token}`
    }
  }).then(r => r.json());

  // 動態載入功能模組
  if (data.needChart) {
    const { renderChart } = await import('./chart.js');
    renderChart(data.chartData);
  }
}
```

---

**延伸閱讀**

- [MDN Window](https://www.google.com/search?q=MDN+Window+API)
- [MDN Fetch API](https://www.google.com/search?q=MDN+Fetch+API)
- [MDN Web Storage](https://www.google.com/search?q=MDN+Web+Storage)
