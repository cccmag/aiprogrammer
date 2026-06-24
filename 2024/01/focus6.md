# 非同步 JavaScript：Callback、Promise、async/await

## 同步與非同步

JavaScript 是單執行緒語言，一次只能執行一個任務。非同步程式設計允許我們在等待某些操作（如網路請求、檔案讀取）完成時，繼續執行其他程式碼：

```javascript
// 同步程式碼
console.log('開始');
const result = heavyComputation(); // 阻塞直到完成
console.log('結果：', result);

// 非同步程式碼
console.log('開始');
setTimeout(() => {
  console.log('延遲執行');
}, 1000);
console.log('結束');
// 輸出順序：開始 → 結束 → 延遲執行
```

## Callback 模式

### 什麼是 Callback

Callback（回呼函數）是傳遞給另一個函數的函數，在非同步操作完成後被調用：

```javascript
// 基本的 callback 範例
function fetchUserData(userId, callback) {
  setTimeout(() => {
    const user = { id: userId, name: 'Alice' };
    callback(null, user);
  }, 1000);
}

function fetchUserPosts(userId, callback) {
  setTimeout(() => {
    const posts = [
      { id: 1, title: 'Post 1' },
      { id: 2, title: 'Post 2' }
    ];
    callback(null, posts);
  }, 1000);
}

// 使用 callback
fetchUserData(1, (error, user) => {
  if (error) {
    console.error('取得使用者失敗:', error);
    return;
  }
  console.log('使用者:', user);
});
```

### Callback Hell（回呼地獄）

```javascript
// 巢狀 callback 導致的可讀性問題
fetchUserData(1, (err, user) => {
  if (err) return console.error(err);
  fetchUserPosts(user.id, (err, posts) => {
    if (err) return console.error(err);
    fetchComments(posts[0].id, (err, comments) => {
      if (err) return console.error(err);
      console.log('留言:', comments);
    });
  });
});
```

## Promise

### 建立 Promise

Promise 是 ES6 引入的非同步解決方案，用來解決 Callback Hell：

```javascript
// 建立 Promise
function fetchUserData(userId) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (userId <= 0) {
        reject(new Error('無效的使用者 ID'));
        return;
      }
      const user = { id: userId, name: 'Alice' };
      resolve(user);
    }, 1000);
  });
}

// Promise 有三種狀態
const promise = fetchUserData(1);
// pending（等待中）→ fulfilled（已完成）或 rejected（已拒絕）
```

### Promise 方法

```javascript
// then：處理成功結果
fetchUserData(1)
  .then(user => {
    console.log('使用者:', user);
    return user.name;
  })
  .then(name => {
    console.log('名稱:', name);
  });

// catch：處理錯誤
fetchUserData(-1)
  .then(user => console.log(user))
  .catch(error => console.error('錯誤:', error.message));

// finally：無論成功或失敗都會執行
fetchUserData(1)
  .then(user => console.log('成功'))
  .catch(error => console.error('失敗'))
  .finally(() => console.log('完成'));
```

### Promise 鏈

```javascript
function fetchUserPosts(userId) {
  return new Promise((resolve) => {
    setTimeout(() => resolve(['Post 1', 'Post 2']), 500);
  });
}

// Promise 鏈取代 Callback Hell
fetchUserData(1)
  .then(user => {
    console.log('使用者:', user);
    return fetchUserPosts(user.id);
  })
  .then(posts => {
    console.log('文章:', posts);
    return fetchComments(posts[0]);
  })
  .then(comments => {
    console.log('留言:', comments);
  })
  .catch(error => {
    console.error('任何步驟出錯:', error);
  });
```

### 並行 Promise

```javascript
const fetchUser = fetchUserData(1);
const fetchPosts = fetchUserPosts(1);

// Promise.all：等待所有 Promise 完成
Promise.all([fetchUser, fetchPosts])
  .then(([user, posts]) => {
    console.log('使用者和文章:', user, posts);
  })
  .catch(error => {
    console.error('其中一個失敗:', error);
  });

// Promise.allSettled：等待所有，不論成敗
Promise.allSettled([fetchUser, fetchPosts])
  .then(results => {
    results.forEach(result => {
      if (result.status === 'fulfilled') {
        console.log('成功:', result.value);
      } else {
        console.log('失敗:', result.reason);
      }
    });
  });

// Promise.race：第一個完成的結果
Promise.race([
  fetchUserData(1),
  new Promise((_, reject) =>
    setTimeout(() => reject(new Error('逾時')), 2000)
  )
]).then(user => {
  console.log('最先完成:', user);
}).catch(err => {
  console.error('逾時或錯誤:', err);
});

// Promise.any：第一個成功的結果
Promise.any([
  fetchUserData(1).then(() => { throw new Error('失敗'); }),
  fetchUserPosts(1)
]).then(result => {
  console.log('第一個成功:', result);
});
```

## async/await

### 基本語法

ES2017 引入的 async/await 讓非同步程式碼看起來像同步程式碼：

```javascript
// async 函數
async function getUserInfo(userId) {
  try {
    const user = await fetchUserData(userId);
    const posts = await fetchUserPosts(user.id);
    return { user, posts };
  } catch (error) {
    console.error('取得使用者資訊失敗:', error);
    throw error;
  }
}

// 使用 async 函數
async function main() {
  const result = await getUserInfo(1);
  console.log('使用者資訊:', result);
}

main();
```

### 進階用法

```javascript
// 箭頭函數 async
const getData = async () => {
  const response = await fetch('https://api.example.com/data');
  const data = await response.json();
  return data;
};

// 並行 await
async function getParallelData() {
  // 同時發起所有請求
  const userPromise = fetchUserData(1);
  const postsPromise = fetchUserPosts(1);

  // 等待所有完成
  const [user, posts] = await Promise.all([
    userPromise, postsPromise
  ]);

  return { user, posts };
}

// Top-level await（ES2022）
const config = await fetch('/config.json').then(r => r.json());
```

### 錯誤處理

```javascript
async function robustFetch(url) {
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`HTTP 錯誤: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    if (error.name === 'TypeError') {
      console.error('網路錯誤:', error.message);
    } else {
      console.error('請求錯誤:', error.message);
    }
    return null; // 回傳預設值
  }
}

// 多個 try/catch 區塊
async function processUser(userId) {
  let user;
  try {
    user = await fetchUserData(userId);
  } catch (error) {
    console.error('無法取得使用者');
    return;
  }

  try {
    const posts = await fetchUserPosts(user.id);
    return { user, posts };
  } catch (error) {
    console.error('無法取得文章，但使用者已取得');
    return { user, posts: [] };
  }
}
```

## 總結

```javascript
// 非同步程式設計的演化
// 1. Callback（1995）
// 2. Promise（ES6 / 2015）
// 3. async/await（ES2017）

// 現代 JavaScript 開發建議
async function bestPractice() {
  // 使用 async/await 讓程式碼更可讀
  // 使用 Promise.all 進行並行操作
  // 使用 try/catch 處理錯誤
  // 避免過度序列化的 await
}
```

---

**延伸閱讀**

- [MDN Promise](https://www.google.com/search?q=MDN+Promise)
- [MDN async/await](https://www.google.com/search?q=MDN+async+await)
- [JavaScript 事件循環](https://www.google.com/search?q=JavaScript+event+loop)
