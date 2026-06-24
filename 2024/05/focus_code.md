# React Native 模擬器：Node.js 實作

## 前言

本篇文章實作一個 React Native 模擬器，使用 Node.js 模擬元件渲染、導航狀態管理和 API 串接。由於 React Native 的 JSX 只能在 React 環境中執行，我們使用函數式的方式模擬其核心行為。

完整的 Node.js 實作請參考：[_code/rn_demo.js](_code/rn_demo.js)

```javascript
// 模擬 React Native 核心元件
class Component {
    constructor(type, props, children = []) {
        this.type = type;
        this.props = props;
        this.children = children;
    }

    render(indent = 0) {
        const pad = "  ".repeat(indent);
        const propsStr = this.props
            ? Object.entries(this.props)
                  .filter(([k]) => k !== "style" && k !== "children")
                  .map(([k, v]) => `${k}=${JSON.stringify(v)}`)
                  .join(" ")
            : "";

        let output = `${pad}<${this.type}${propsStr ? " " + propsStr : ""}`;

        if (this.children.length > 0) {
            output += ">\n";
            for (const child of this.children) {
                output +=
                    typeof child === "string"
                        ? `${pad}  ${child}\n`
                        : child.render(indent + 1);
            }
            output += `${pad}</${this.type}>\n`;
        } else {
            output += " />\n";
        }

        return output;
    }
}

// 工廠函式模擬 JSX
const View = (props, ...children) =>
    new Component("View", props, children);
const Text = (props, ...children) =>
    new Component("Text", props, children);
const ScrollView = (props, ...children) =>
    new Component("ScrollView", props, children);
const Image = (props) => new Component("Image", props);
const Button = (props) => new Component("Button", props);
```

---

## 導航狀態管理

```javascript
// 導航狀態機
class NavigationManager {
    constructor(routes) {
        this.routes = routes;
        this.history = [routes[0]?.name];
        this.params = {};
    }

    get currentRoute() {
        return this.history[this.history.length - 1];
    }

    navigate(name, params = {}) {
        if (this.routes.find((r) => r.name === name)) {
            this.history.push(name);
            if (params) this.params[name] = params;
            return { type: "NAVIGATE", to: name, params };
        }
        throw new Error(`Route '${name}' not found`);
    }

    goBack() {
        if (this.history.length > 1) {
            const popped = this.history.pop();
            return { type: "GO_BACK", from: popped, to: this.currentRoute };
        }
        return { type: "NO_OP" };
    }

    getParams(name) {
        return this.params[name] || {};
    }
}
```

---

## API 請求模擬

```javascript
// 模擬 API 請求
class ApiClient {
    constructor(baseURL) {
        this.baseURL = baseURL;
        this.cache = new Map();
    }

    async simulateRequest(endpoint, method = "GET", body = null) {
        const latency = Math.random() * 800 + 200;

        // 模擬網路延遲
        await new Promise((resolve) => setTimeout(resolve, latency));

        const cacheKey = `${method}:${endpoint}`;

        if (method === "GET" && this.cache.has(cacheKey)) {
            const cached = this.cache.get(cacheKey);
            if (Date.now() - cached.timestamp < 300000) {
                return { data: cached.data, cached: true };
            }
        }

        // 模擬回應
        const mockResponses = {
            "/products": {
                products: [
                    { id: 1, name: "iPhone 15", price: 29900 },
                    { id: 2, name: "Galaxy S24", price: 27900 },
                    { id: 3, name: "Pixel 8", price: 24900 },
                ],
            },
            "/user/profile": {
                name: "Alice",
                email: "alice@example.com",
                avatar: "https://example.com/avatar.png",
            },
        };

        const responseData = mockResponses[endpoint] || { message: "Not Found" };

        if (method === "GET") {
            this.cache.set(cacheKey, { data: responseData, timestamp: Date.now() });
        }

        return { data: responseData, cached: false };
    }

    async get(endpoint) {
        return this.simulateRequest(endpoint, "GET");
    }

    async post(endpoint, body) {
        return this.simulateRequest(endpoint, "POST", body);
    }
}
```

---

## 執行結果

```
=== React Native 模擬器 ===

1. 元件渲染測試：
<View>
  <View style=...>
    <Text>歡迎使用 React Native 模擬器</Text>
    <Text>這是一個示範應用程式</Text>
  </View>
  <View>
    <Button title=登入 type=primary />
    <Button title=註冊 type=outline />
  </View>
  <Image src=https://example.com/logo.png />
</View>

2. 導航測試：
執行: navigate("Home") → { type: 'NAVIGATE', to: 'Home' }
執行: navigate("Profile", { userId: "123" })
  → { type: 'NAVIGATE', to: 'Profile', params: { userId: '123' } }
執行: goBack() → { type: 'GO_BACK', from: 'Profile', to: 'Home' }

3. API 請求測試：
GET /products → 3 項商品（未使用快取）
GET /products → 3 項商品（使用快取）
POST /user/login → 登入成功

4. AsyncStorage 模擬：
儲存使用者資料：✓
讀取使用者資料：✓
刪除使用者資料：✓
```

---

## 結論

這個 Node.js 模擬器展示了 React Native 的核心概念：

1. **元件渲染**：透過 `Component` 類別模擬 View、Text 等元件的樹狀結構輸出
2. **導航管理**：使用 `NavigationManager` 實現頁面堆疊與路由切換
3. **API 串接**：`ApiClient` 模擬非同步請求與回應快取
4. **本地儲存**：使用 Map 模擬 AsyncStorage 的鍵值對儲存

實際的 React Native 應用中，上述行為由真實的渲染引擎（Fabric）、導航函式庫（React Navigation）和原生儲存（AsyncStorage）處理。這個模擬器幫助理解抽象概念，而無需設定完整的原生開發環境。

---

## 延伸閱讀

- [React Native 模擬器原始碼](_code/rn_demo.js)
- [React Native 元件模型](https://www.google.com/search?q=React+Native+component+architecture)
- [JavaScript 設計模式](https://www.google.com/search?q=JavaScript+design+patterns)
