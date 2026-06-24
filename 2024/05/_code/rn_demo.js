#!/usr/bin/env node

/**
 * rn_demo.js — React Native 模擬器
 * 使用 Node.js 模擬 RN 元件渲染、導航狀態、API 呼叫
 */

// ─── 模擬 React Native 核心元件 ─────────────────────────

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

// 工廠函式
const View = (props, ...children) => new Component("View", props, children);
const Text = (props, ...children) => new Component("Text", props, children);
const ScrollView = (props, ...children) =>
  new Component("ScrollView", props, children);
const Image = (props) => new Component("Image", props);
const Button = (props) => new Component("Button", props);

// ─── 導航管理器 ─────────────────────────────────────────

class NavigationManager {
  constructor(routes) {
    this.routes = routes;
    this.history = [routes[0]?.name || "Home"];
    this.params = {};
  }

  get currentRoute() {
    return this.history[this.history.length - 1];
  }

  navigate(name, params = {}) {
    if (this.routes.find((r) => r.name === name)) {
      this.history.push(name);
      if (Object.keys(params).length > 0) this.params[name] = params;
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

// ─── API 客戶端 ─────────────────────────────────────────

class ApiClient {
  constructor(baseURL) {
    this.baseURL = baseURL;
    this.cache = new Map();
  }

  async request(endpoint, method = "GET", body = null) {
    const latency = Math.random() * 600 + 200;
    await new Promise((r) => setTimeout(r, latency));

    const cacheKey = `${method}:${endpoint}`;
    if (method === "GET" && this.cache.has(cacheKey)) {
      const cached = this.cache.get(cacheKey);
      if (Date.now() - cached.timestamp < 300000) {
        return { data: cached.data, cached: true };
      }
    }

    const mockData = {
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
      "/user/login": { token: "mock-jwt-token", user: { name: "Alice" } },
    };

    const data = mockData[endpoint] || { message: "Not Found" };

    if (method === "GET") {
      this.cache.set(cacheKey, { data, timestamp: Date.now() });
    }
    return { data, cached: false };
  }

  get(endpoint) {
    return this.request(endpoint, "GET");
  }
  post(endpoint, body) {
    return this.request(endpoint, "POST", body);
  }
}

// ─── AsyncStorage 模擬 ─────────────────────────────────

class AsyncStorageMock {
  constructor() {
    this._store = {};
  }

  async setItem(key, value) {
    this._store[key] = String(value);
    return true;
  }

  async getItem(key) {
    return this._store[key] || null;
  }

  async removeItem(key) {
    delete this._store[key];
    return true;
  }

  async clear() {
    this._store = {};
    return true;
  }

  async getAllKeys() {
    return Object.keys(this._store);
  }
}

// ─── 主 Demo 函式 ──────────────────────────────────────

async function demo() {
  console.log("=== React Native 模擬器 ===\n");

  // 1. 元件渲染
  console.log("1. 元件渲染測試：");
  const app = View(
    { style: { flex: 1, padding: 16 } },
    View(
      { style: { marginBottom: 16 } },
      Text({}, "歡迎使用 React Native 模擬器"),
      Text({}, "這是一個示範應用程式")
    ),
    View(
      { style: { flexDirection: "row" } },
      Button({ title: "登入", type: "primary" }),
      Button({ title: "註冊", type: "outline" })
    ),
    Image({ src: "https://example.com/logo.png" })
  );
  console.log(app.render());

  // 2. 導航測試
  console.log("2. 導航測試：");
  const nav = new NavigationManager([
    { name: "Home" },
    { name: "Profile" },
    { name: "Settings" },
  ]);
  console.log(`  初始頁面: ${nav.currentRoute}`);
  console.log(`  執行: navigate("Profile", { userId: "123" })`);
  const navResult = nav.navigate("Profile", { userId: "123" });
  console.log(`  → ${JSON.stringify(navResult)}`);
  console.log(`  目前頁面: ${nav.currentRoute}`);
  console.log(`  執行: goBack()`);
  const backResult = nav.goBack();
  console.log(`  → ${JSON.stringify(backResult)}`);
  console.log(`  目前頁面: ${nav.currentRoute}\n`);

  // 3. API 請求
  console.log("3. API 請求測試：");
  const api = new ApiClient("https://api.example.com");
  const products1 = await api.get("/products");
  console.log(
    `  GET /products → ${products1.data.products.length} 項商品（${
      products1.cached ? "使用快取" : "未使用快取"
    }）`
  );
  const products2 = await api.get("/products");
  console.log(
    `  GET /products → ${products2.data.products.length} 項商品（${
      products2.cached ? "使用快取" : "未使用快取"
    }）`
  );
  const login = await api.post("/user/login", {
    email: "alice@example.com",
    password: "xxx",
  });
  console.log(`  POST /user/login → ${login.data.token ? "登入成功" : "失敗"}\n`);

  // 4. AsyncStorage
  console.log("4. AsyncStorage 模擬：");
  const storage = new AsyncStorageMock();
  await storage.setItem("user", JSON.stringify({ name: "Alice", theme: "dark" }));
  console.log("  儲存使用者資料：✓");
  const userData = await storage.getItem("user");
  console.log(`  讀取使用者資料：✓ → ${userData}`);
  await storage.removeItem("user");
  console.log("  刪除使用者資料：✓\n");

  // 5. ScrollView 模擬
  console.log("5. ScrollView 長列表測試：");
  const items = Array.from({ length: 5 }, (_, i) => `列表項目 ${i + 1}`);
  const list = ScrollView(
    { style: { flex: 1 } },
    ...items.map((item) => Text({ style: { padding: 8 } }, item))
  );
  console.log(list.render());

  console.log("=== 模擬完成 ===");
}

// ─── 執行 ──────────────────────────────────────────────

if (require.main === module) {
  demo().catch(console.error);
}

module.exports = { demo, Component, NavigationManager, ApiClient, AsyncStorageMock };
