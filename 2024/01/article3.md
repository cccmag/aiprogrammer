# 字串樣板與解構賦值

## 字串樣板（Template Literals）

### 基本語法

ES6 引入的字串樣板使用反引號（`）替代傳統的引號：

```javascript
// 傳統字串
const name = 'Alice';
const greeting1 = 'Hello, ' + name + '!';

// 字串樣板
const greeting2 = `Hello, ${name}!`;

// 多行字串
const multiLine = `
  親愛的 ${name}：
    歡迎使用字串樣板。
  此致
  敬禮
`;
```

### 表達式嵌入

```javascript
const a = 10, b = 20;

// 嵌入運算
console.log(`${a} + ${b} = ${a + b}`);
// "10 + 20 = 30"

// 嵌入函數調用
const formatPrice = (price) => `NT$${price.toFixed(2)}`;
console.log(`價格: ${formatPrice(99.9)}`);
// "價格: NT$99.90"

// 嵌入三元運算
const isLoggedIn = true;
console.log(`歡迎${isLoggedIn ? '回來' : '光臨'}！`);
// "歡迎回來！"

// 巢狀樣板
const items = ['蘋果', '香蕉', '橘子'];
const list = `
  <ul>
    ${items.map(item => `<li>${item}</li>`).join('\n    ')}
  </ul>
`;
```

### 標籤樣板（Tagged Templates）

```javascript
// 自定義樣板處理函數
function highlight(strings, ...values) {
  return strings.reduce((result, str, i) => {
    const value = values[i] ? `<strong>${values[i]}</strong>` : '';
    return result + str + value;
  }, '');
}

const user = 'Alice';
const action = '登入';
const message = highlight`使用者 ${user} 已${action}。`;
// "使用者 <strong>Alice</strong> 已<strong>登入</strong>。"

// 安全的 SQL 查詢
function sql(strings, ...values) {
  const escaped = values.map(v =>
    String(v).replace(/'/g, "''")
  );
  return strings.reduce((result, str, i) =>
    result + str + (escaped[i] || ''), ''
  );
}

const id = 1;
const query = sql`SELECT * FROM users WHERE id = ${id}`;
```

## 解構賦值

### 陣列解構進階

```javascript
const arr = [1, 2, 3, 4, 5, 6];

// 交換變數
let x = 1, y = 2;
[x, y] = [y, x];

// 函數回傳多值
function getMinMax(values) {
  return [Math.min(...values), Math.max(...values)];
}

const [min, max] = getMinMax([3, 1, 4, 1, 5]);
// min = 1, max = 5

// 預設值與 Rest
const [a = 0, b = 0, ...rest] = [1];
// a = 1, b = 0, rest = []

// 巢狀解構
const matrix = [[1, 2], [3, 4]];
const [[a1, a2], [b1, b2]] = matrix;
```

### 物件解構進階

```javascript
const user = {
  id: 42,
  name: 'Alice',
  email: 'alice@example.com',
  profile: {
    age: 30,
    city: 'Taipei',
    address: { street: 'Main St', number: 100 }
  },
  roles: ['admin', 'editor']
};

// 巢狀解構
const {
  name,
  profile: {
    age,
    city,
    address: { street }
  },
  roles: [primaryRole, ...otherRoles]
} = user;

// name = 'Alice', age = 30, city = 'Taipei'
// street = 'Main St', primaryRole = 'admin'

// 函數參數解構
function displayUser({
  name,
  email = 'N/A',
  profile: { age = 0 } = {}
}) {
  console.log(`${name} (${age}) - ${email}`);
}

displayUser(user);
// "Alice (30) - alice@example.com"

// 迴圈中的解構
const users = [
  { id: 1, name: 'Alice' },
  { id: 2, name: 'Bob' }
];

for (const { id, name } of users) {
  console.log(`#${id}: ${name}`);
}
// "#1: Alice"
// "#2: Bob"
```

## 搭配組合

### 字串樣板 + 解構

```javascript
function createEmail({ to, from, subject, body }) {
  return `
    收件人: ${to}
    寄件人: ${from}
    主旨: ${subject}
    ─────────────────
    ${body}
  `;
}

const email = createEmail({
  to: 'bob@example.com',
  from: 'alice@example.com',
  subject: 'Hello',
  body: '這是一封測試郵件。'
});
```

### 動態屬性名稱 + 解構

```javascript
const key = 'dynamicKey';
const obj = {
  [key]: '動態值',
  staticKey: '靜態值'
};

// 使用計算屬性名解構（需要明確的屬性名）
const { [key]: dynamicValue, staticKey } = obj;
// dynamicValue = '動態值', staticKey = '靜態值'
```

## 實用範例

```javascript
// API 回應處理
async function handleApiResponse() {
  const response = await fetch('/api/user');
  const {
    data: { id, name, email } = {},
    error,
    status
  } = await response.json();

  if (error) {
    console.error(`錯誤 (${status}):`, error);
    return null;
  }

  return `${name} (${email})`;
}

// 設定物件合併
const defaultConfig = {
  theme: 'light',
  fontSize: 14,
  language: 'zh-TW'
};

function createConfig(userConfig = {}) {
  return { ...defaultConfig, ...userConfig };
}

const config = createConfig({ theme: 'dark' });
// { theme: 'dark', fontSize: 14, language: 'zh-TW' }
```

## 結語

字串樣板和解構賦值是 ES6 中實用性最高的兩個語法糖。它們讓程式碼更簡潔、可讀性更高。掌握這些技巧，可以大幅減少樣板程式碼的撰寫。

---

**延伸閱讀**

- [MDN 字串樣板](https://www.google.com/search?q=MDN+template+literals)
- [MDN 解構賦值](https://www.google.com/search?q=MDN+destructuring+assignment)
- [ES6 常用語法](https://www.google.com/search?q=ES6+features+guide)
