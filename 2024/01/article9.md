# 瀏覽器儲存：localStorage 與 cookie

## 瀏覽器儲存技術概覽

瀏覽器提供了多種用戶端資料儲存方式，各有不同的用途和限制：

| 儲存方式 | 容量 | 生命週期 | 伺服器可讀 |
|---------|------|---------|-----------|
| Cookie | 4KB | 可設定過期時間 | 是（自動發送） |
| localStorage | 5-10MB | 永久（除非清除） | 否 |
| sessionStorage | 5-10MB | 分頁關閉時清除 | 否 |
| IndexedDB | 不限 | 永久 | 否 |
| Cache API | 不限 | 手動管理 | 否 |

## localStorage

### 基本操作

```javascript
// 儲存資料
localStorage.setItem('username', 'Alice');
localStorage.setItem('theme', 'dark');
localStorage.setItem('settings', JSON.stringify({
  fontSize: 16,
  notifications: true,
  language: 'zh-TW'
}));

// 讀取資料
const username = localStorage.getItem('username');
const settings = JSON.parse(localStorage.getItem('settings'));

// 刪除單一項目
localStorage.removeItem('theme');

// 清除所有資料
// localStorage.clear();

// 取得儲存空間資訊
console.log('項目數量:', localStorage.length);
console.log('第 0 個鍵:', localStorage.key(0));
```

### 實際應用範例

```javascript
// 主題切換
function saveTheme(theme) {
  localStorage.setItem('theme', theme);
  document.documentElement.setAttribute('data-theme', theme);
}

function loadTheme() {
  const saved = localStorage.getItem('theme');
  if (saved) {
    document.documentElement.setAttribute('data-theme', saved);
  }
  return saved || 'light';
}

// 表單自動儲存
function autoSaveForm(formId) {
  const form = document.getElementById(formId);

  form.addEventListener('input', () => {
    const data = {};
    const elements = form.elements;

    for (const element of elements) {
      if (element.name) {
        data[element.name] = element.value;
      }
    }

    localStorage.setItem(`form-${formId}`, JSON.stringify(data));
  });

  // 恢復儲存的資料
  const savedData = localStorage.getItem(`form-${formId}`);
  if (savedData) {
    const data = JSON.parse(savedData);
    for (const [name, value] of Object.entries(data)) {
      const element = form.elements[name];
      if (element) element.value = value;
    }
  }
}

// 購物車功能
class ShoppingCart {
  constructor() {
    this.items = JSON.parse(
      localStorage.getItem('cart') || '[]'
    );
  }

  addItem(product) {
    const existing = this.items.find(item => item.id === product.id);
    if (existing) {
      existing.quantity += product.quantity || 1;
    } else {
      this.items.push({ ...product, quantity: product.quantity || 1 });
    }
    this.save();
  }

  removeItem(productId) {
    this.items = this.items.filter(item => item.id !== productId);
    this.save();
  }

  getTotal() {
    return this.items.reduce(
      (sum, item) => sum + item.price * item.quantity, 0
    );
  }

  save() {
    localStorage.setItem('cart', JSON.stringify(this.items));
  }

  clear() {
    this.items = [];
    this.save();
  }
}
```

## sessionStorage

sessionStorage 與 localStorage 的 API 完全相同，但資料在分頁關閉後自動清除：

```javascript
// 暫存登入狀態（分頁存活期間）
sessionStorage.setItem('sessionId', 'abc123');

// 儲存當前頁面狀態
sessionStorage.setItem('scrollPosition', window.scrollY);

// 表單草稿（僅當前分頁）
function saveDraft(formData) {
  sessionStorage.setItem('draft', JSON.stringify(formData));
}

function loadDraft() {
  const saved = sessionStorage.getItem('draft');
  return saved ? JSON.parse(saved) : null;
}
```

## Cookie

### 基本操作

```javascript
// 設定 Cookie
document.cookie = 'username=Alice';

// 設定過期時間
const expires = new Date(Date.now() + 7 * 24 * 60 * 60 * 1000);
document.cookie = `theme=dark; expires=${expires.toUTCString()}; path=/`;

// 設定安全選項
document.cookie = 'sessionId=abc123; Secure; HttpOnly; SameSite=Strict';

// 讀取所有 Cookie
console.log(document.cookie); // "username=Alice; theme=dark"

// 刪除 Cookie（設定過期時間為過去）
document.cookie = 'username=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/';
```

### Cookie 管理工具

```javascript
// Cookie 工具物件
const CookieManager = {
  set(name, value, days = 7, options = {}) {
    let cookie = `${encodeURIComponent(name)}=${encodeURIComponent(value)}`;

    if (days) {
      const expires = new Date();
      expires.setDate(expires.getDate() + days);
      cookie += `; expires=${expires.toUTCString()}`;
    }

    cookie += `; path=${options.path || '/'}`;

    if (options.secure) cookie += '; Secure';
    if (options.sameSite) cookie += `; SameSite=${options.sameSite}`;

    document.cookie = cookie;
  },

  get(name) {
    const cookies = document.cookie.split('; ');
    for (const cookie of cookies) {
      const [key, value] = cookie.split('=');
      if (decodeURIComponent(key) === name) {
        return decodeURIComponent(value);
      }
    }
    return null;
  },

  remove(name, path = '/') {
    this.set(name, '', -1, { path });
  },

  getAll() {
    const cookies = {};
    document.cookie.split('; ').forEach(cookie => {
      if (!cookie) return;
      const [key, value] = cookie.split('=');
      cookies[decodeURIComponent(key)] = decodeURIComponent(value);
    });
    return cookies;
  }
};

// 使用
CookieManager.set('language', 'zh-TW', 30);
console.log(CookieManager.get('language')); // 'zh-TW'
```

## 儲存策略比較

### 何時使用哪種儲存

```javascript
// localStorage：長期儲存非敏感資料
localStorage.setItem('userPreferences', JSON.stringify({
  theme: 'dark',
  fontSize: 14
}));

// sessionStorage：暫存當前分頁的狀態
sessionStorage.setItem('currentStep', '3');

// Cookie：需要伺服器存取的資料（如 Session ID）
document.cookie = 'sessionToken=abc123; Secure; HttpOnly';

// IndexedDB：大量結構化資料（如離線資料庫）
const request = indexedDB.open('MyApp', 1);
```

### 安全性考量

```javascript
// 不要儲存敏感資訊在 localStorage
localStorage.setItem('password', 'secret123'); // 不安全！

// Cookie 設定安全標誌
document.cookie = 'token=xxx; Secure; HttpOnly; SameSite=Strict';

// 驗證儲存資料
function safeParseJSON(str) {
  try {
    return JSON.parse(str);
  } catch {
    return null;
  }
}
```

## 監聽儲存變更

```javascript
// 僅在同源其他分頁變更 localStorage 時觸發
window.addEventListener('storage', (event) => {
  console.log('儲存空間變更:', {
    key: event.key,
    oldValue: event.oldValue,
    newValue: event.newValue,
    url: event.url
  });

  // 同步多分頁的狀態
  if (event.key === 'theme') {
    applyTheme(event.newValue);
  }
});
```

## 結語

瀏覽器儲存技術是 Web 應用不可或缺的一部分。選擇合適的儲存方式取決於資料的生命週期、容量需求和安全性要求。一般建議使用 localStorage 儲存使用者偏好設定，使用 sessionStorage 暫存分頁狀態，使用 Cookie 管理伺服器相關的認證資訊。

---

**延伸閱讀**

- [MDN Web Storage](https://www.google.com/search?q=MDN+Web+Storage+API)
- [MDN Cookie](https://www.google.com/search?q=MDN+document+cookie)
- [IndexedDB 教學](https://www.google.com/search?q=IndexedDB+tutorial)
