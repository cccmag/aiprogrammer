# Fetch API 與 HTTP 請求

## Fetch API 簡介

Fetch API 是現代瀏覽器提供的網路請求介面，基於 Promise 設計，取代了傳統的 XMLHttpRequest。它提供了一個更簡潔、更一致的方式來進行 HTTP 請求。

### 基本 GET 請求

```javascript
// 簡單的 GET 請求
fetch('https://api.example.com/users')
  .then(response => {
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
  })
  .then(data => console.log(data))
  .catch(error => console.error('Fetch error:', error));

// 使用 async/await
async function getUsers() {
  try {
    const response = await fetch('https://api.example.com/users');
    if (!response.ok) throw new Error(`狀態: ${response.status}`);
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('請求失敗:', error);
    throw error;
  }
}
```

### Response 物件

```javascript
async function inspectResponse() {
  const response = await fetch('https://api.example.com/data');

  // 狀態資訊
  console.log('狀態碼:', response.status);     // 200
  console.log('成功?', response.ok);            // true
  console.log('狀態文字:', response.statusText); // 'OK'

  // 標頭資訊
  console.log('Content-Type:', response.headers.get('content-type'));
  console.log('Content-Length:', response.headers.get('content-length'));

  // 取得回應資料的不同方式
  const text = await response.text();    // 文字
  const json = await response.json();    // JSON
  const blob = await response.blob();    // 二進位資料
  const formData = await response.formData(); // 表單資料
  const arrayBuffer = await response.arrayBuffer(); // 原始位元組
}
```

## 進階請求配置

### Request 物件

```javascript
// 使用 Request 物件
async function makeRequest() {
  const request = new Request('https://api.example.com/data', {
    method: 'GET',
    headers: {
      'Accept': 'application/json',
      'Authorization': 'Bearer token123'
    },
    cache: 'no-cache',
    credentials: 'same-origin'
  });

  const response = await fetch(request);
  return response.json();
}
```

### POST 請求與 JSON 資料

```javascript
async function createUser(userData) {
  const response = await fetch('https://api.example.com/users', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      'X-Requested-With': 'XMLHttpRequest'
    },
    body: JSON.stringify(userData)
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || '建立使用者失敗');
  }

  return response.json();
}

// 使用範例
const newUser = await createUser({
  name: 'Alice Wang',
  email: 'alice@example.com',
  role: 'editor'
});
```

### 表單資料提交

```javascript
// 傳統表單編碼
async function submitForm(formData) {
  const response = await fetch('/api/submit', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: new URLSearchParams(formData)
  });
  return response.json();
}

// FormData（適合檔案上傳）
async function uploadFile(fileInput) {
  const formData = new FormData();
  formData.append('file', fileInput.files[0]);
  formData.append('description', '使用者上傳檔案');

  const response = await fetch('/api/upload', {
    method: 'POST',
    // 不要設定 Content-Type，瀏覽器會自動設定含 boundary 的內容類型
    body: formData
  });

  return response.json();
}
```

### 自訂標頭與認證

```javascript
// 建立可重複使用的 fetch 包裝
async function apiClient(endpoint, options = {}) {
  const token = localStorage.getItem('authToken');

  const defaultOptions = {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': token ? `Bearer ${token}` : '',
      ...options.headers
    }
  };

  const response = await fetch(
    `https://api.example.com${endpoint}`,
    { ...defaultOptions, ...options }
  );

  if (response.status === 401) {
    // Token 過期，重新導向登入
    localStorage.removeItem('authToken');
    window.location.href = '/login';
    throw new Error('未授權');
  }

  return response.json();
}

// 使用封裝的客戶端
const data = await apiClient('/users', {
  method: 'POST',
  body: JSON.stringify({ name: 'Alice' })
});
```

## 錯誤處理

### 全面的錯誤處理

```javascript
async function robustFetch(url, options = {}) {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 10000);

  try {
    const response = await fetch(url, {
      ...options,
      signal: controller.signal
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      // 嘗試解析錯誤訊息
      let errorMessage = `HTTP 錯誤 ${response.status}`;
      try {
        const errorData = await response.json();
        errorMessage = errorData.message || errorMessage;
      } catch (e) {
        // 無法解析 JSON，使用預設錯誤訊息
      }

      throw new Error(errorMessage);
    }

    return await response.json();

  } catch (error) {
    clearTimeout(timeoutId);

    if (error.name === 'AbortError') {
      throw new Error('請求逾時');
    }

    if (error.name === 'TypeError') {
      throw new Error('網路錯誤，請檢查連線');
    }

    throw error;
  }
}
```

### 重試機制

```javascript
async function fetchWithRetry(url, options = {}, retries = 3) {
  for (let i = 0; i < retries; i++) {
    try {
      return await fetch(url, options);
    } catch (error) {
      if (i === retries - 1) throw error;
      console.log(`請求失敗，第 ${i + 1} 次重試...`);
      await new Promise(r => setTimeout(r, 1000 * Math.pow(2, i)));
    }
  }
}
```

## CORS 與跨域請求

```javascript
// 跨域請求設定
async function crossOriginRequest() {
  const response = await fetch('https://other-domain.com/api/data', {
    mode: 'cors',             // cors, no-cors, same-origin
    credentials: 'include',   // include, same-origin, omit
    headers: {
      'Content-Type': 'application/json'
    }
  });

  return response.json();
}

// JSONP 替代方案（僅供參考，Fetch 請使用 CORS）
function jsonp(url, callbackName) {
  return new Promise((resolve) => {
    const script = document.createElement('script');
    script.src = `${url}?callback=${callbackName}`;
    window[callbackName] = resolve;
    document.body.appendChild(script);
  });
}
```

## 結語

Fetch API 是現代 Web 開發中不可或缺的工具。透過 async/await 的配合，網路請求的程式碼變得清晰且易於維護。搭配完善的錯誤處理和重試機制，可以建構出穩健的資料獲取層。

---

**延伸閱讀**

- [MDN Fetch API](https://www.google.com/search?q=MDN+Fetch+API)
- [HTTP 請求方法](https://www.google.com/search?q=HTTP+request+methods)
- [CORS 跨域資源共享](https://www.google.com/search?q=CORS+explained)
