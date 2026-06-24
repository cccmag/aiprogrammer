# Bun 2.0 發布：JavaScript 工具鏈的效能革命

## 前言

2026 年 4 月，Bun 團隊發布了 2.0 版本——這是自 Bun 1.0 以來最大的一次升級。核心改動是將原本的 JavaScriptCore 引擎替換為自研的 **Bun JIT 編譯器**，並推出了全新的**插件系統**（支援 Rust 和 Zig）以及 **Quartz Mirror** 套件下載加速網路。本文深入解析這些關鍵變革。

## Bun JIT：新世代 JavaScript 引擎

### 為什麼放棄 JavaScriptCore？

Bun 1.x 使用 WebKit 的 JavaScriptCore（JSC）作為 JS 引擎，雖然 JSC 效能優秀，但存在幾個問題：

1. 與 Bun 的底層 Zig 基礎設施整合困難
2. JSC 的 API 限制了 Bun runtime 的創新空間
3. JSC 的記憶體模型與 Bun 的 I/O 模型之間有效能損耗

### Bun JIT 的設計

Bun JIT 是從零開始用 Zig 撰寫的 JavaScript 引擎，採用了三層編譯架構：

| 層級 | 名稱 | 策略 | 延遲 |
|------|------|------|------|
| L0 | Bytecode Interpreter | 直接執行位元組碼 | 即時 |
| L1 | Baseline JIT | 輕量編譯，基本優化 | 啟動後 ~10ms |
| L2 | Optimizing JIT | 深度分析，向量化，內聯快取 | 啟動後 ~100ms |

### 效能基準測試

以下資料來自 Bun 團隊發布的官方基準測試：

| 基準測試 | Node.js 22 | Bun 1.2 | Bun 2.0 | 倍數提升 |
|---------|-----------|---------|---------|---------|
| HTTP 吞吐量 (req/s) | 85,000 | 120,000 | **310,000** | 3.6x |
| 冷啟動時間 (ms) | 45ms | 12ms | **5ms** | 9x |
| Hello World (ops/s) | 1,200,000 | 2,100,000 | **5,800,000** | 4.8x |
| JSON 解析 (MB/s) | 480 | 650 | **1,200** | 2.5x |
| Crypto 操作 (ops/s) | 320,000 | 410,000 | **890,000** | 2.8x |

### 程式碼實例：新的 Bun JIT 行為

```javascript
// Bun 2.0 JIT 的型態推導和能力
function sumRange(n) {
  let total = 0;
  for (let i = 0; i < n; i++) {
    total += i;  // JIT 推導為 Int32 累加
  }
  return total;
}

// 熱路徑編譯為 SIMD 向量化程式碼
const result = sumRange(1_000_000_000);
console.log(result);  // 499999999500000000
```

## Quartz Mirror：新一代套件下載加速

Bun 2.0 內建了 **Quartz Mirror**——一個全球分散式的套件鏡像加速網路。它使用 IPFS 協定進行內容定址和快取：

```toml
# bunfig.toml — Quartz Mirror 設定
[mirror]
enabled = true
mode = "auto"  # auto | p2p | cloud

# 在區域網路中發現對等節點
[mirror.peers]
discovery = ["mdns", "dht"]
cache_size = "10GB"

# 企業 Firewall 後的代理設定
[mirror.proxy]
http = "http://proxy.company.com:8080"
https = "http://proxy.company.com:8080"
```

Quartz Mirror 如何運作：

1. **第一次安裝**：從官方 npm registry 下載，同時廣播到 P2P 網路
2. **第二次安裝（同辦公室）**：從區域網路的對等節點下載，延遲 < 5ms
3. **全域快取**：熱門套件由 Cloudflare 邊緣節點快取

```bash
# 安裝速度比較
$ time bun add react      # 0.8s (P2P 快取命中)
$ time npm install react  # 3.2s
$ time pnpm add react     # 1.5s
```

## 插件系統：Rust 和 Zig 原生插件

Bun 2.0 推出了全新的插件 API，允許用 Rust 或 Zig 編寫原生插件：

### Rust 插件範例

```rust
// bun-plugin-render: 用 Rust 編寫 Bun 插件
use bun_plugin::*;

#[bun_plugin]
fn init(env: &mut Env) -> PluginResult {
    env.register_http_middleware(MyMiddleware);
    env.register_transform(MyTransform);
    Ok(())
}

struct MyTransform;

impl Transform for MyTransform {
    fn name(&self) -> &str {
        "markdown-to-html"
    }
    
    fn extensions(&self) -> Vec<&str> {
        vec![".md", ".markdown"]
    }
    
    fn transform(&self, code: &str) -> Result<String, TransformError> {
        // 使用 pulldown-cmark 進行轉換
        let parser = pulldown_cmark::Parser::new(code);
        let mut html = String::new();
        pulldown_cmark::html::push_html(&mut html, parser);
        Ok(html)
    }
}
```

### Zig 插件範例

```zig
// bun-plugin-csv.zig — 用 Zig 編寫高效 CSV 解析器
const bun = @import("bun-plugin");
const std = @import("std");

pub const Plugin = bun.Plugin.init(.{
    .name = "csv-loader",
    .extensions = &.{".csv"},
    .on_load = onLoad,
});

fn onLoad(ctx: *bun.LoadContext) bun.LoadResult {
    const text = ctx.readFile() catch |err| {
        return .{ .error = err };
    };
    
    var lines = std.mem.splitScalar(u8, text, '\n');
    var headers = std.ArrayList([]const u8).init(ctx.allocator);
    var rows = std.ArrayList([]const u8).init(ctx.allocator);
    
    // 解析 CSV
    if (lines.next()) |header_line| {
        var it = std.mem.splitScalar(u8, header_line, ',');
        while (it.next()) |h| headers.append(h) catch unreachable;
    }
    
    return .{ .module = .{
        .exports = &.{
            .{ .name = "headers", .value = headers.items },
            .{ .name = "parse", .value = parseFn },
        },
    }};
}
```

在 Bun 中使用插件：

```javascript
// bun.config.ts
import { plugin } from "bun";

plugin({
  name: "csv-loader",
  async setup(build) {
    const { parseCSV } = await import("./bun-plugin-csv.zig");
    
    build.onLoad({ filter: /\.csv$/ }, ({ path }) => {
      const data = parseCSV(await Bun.file(path).text());
      return { exports: { default: data }, loader: "object" };
    });
  },
});

// 直接匯入 CSV！
import data from "./data.csv";
console.log(data.headers);  // ["name", "age", "city"]
```

## Bun 2.0 HTTP 伺服器

### 完整範例

```typescript
// Bun 2.0 HTTP 伺服器
import { Hono } from "hono";
import { cors } from "hono/cors";
import { logger } from "hono/logger";
import { z } from "zod";

const app = new Hono();

app.use("*", cors());
app.use("*", logger());

// 內建 SQLite 支援（無需安裝相依套件）
const db = new Bun.SQLite("todos.db");
db.exec(`
  CREATE TABLE IF NOT EXISTS todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    done INTEGER DEFAULT 0,
    created_at TEXT DEFAULT (datetime('now'))
  )
`);

// 型別安全的請求驗證
const TodoSchema = z.object({
  text: z.string().min(1).max(200),
});

// Bun 2.0 JIT 將這些 handler 編譯為機器碼
app.get("/api/todos", (c) => {
  const todos = db.query("SELECT * FROM todos ORDER BY created_at DESC").all();
  return c.json(todos);
});

app.post("/api/todos", async (c) => {
  const body = await c.req.json();
  const { text } = TodoSchema.parse(body);
  
  const result = db.run("INSERT INTO todos (text) VALUES (?)", [text]);
  const todo = db.query("SELECT * FROM todos WHERE id = ?").get(result.lastInsertRowid);
  
  return c.json(todo, 201);
});

app.put("/api/todos/:id/toggle", (c) => {
  const id = c.req.param("id");
  db.run("UPDATE todos SET done = NOT done WHERE id = ?", [id]);
  return c.json({ success: true });
});

app.delete("/api/todos/:id", (c) => {
  db.run("DELETE FROM todos WHERE id = ?", [c.req.param("id")]);
  return c.json({ success: true });
});

// Bun 2.0 伺服器選項
export default {
  port: 3000,
  hostname: "0.0.0.0",
  // Bun JIT 的即時重新載入
  development: process.env.NODE_ENV !== "production",
  // TLS/SSL 支援
  tls: process.env.NODE_ENV === "production" ? {
    key: Bun.file("/etc/ssl/key.pem"),
    cert: Bun.file("/etc/ssl/cert.pem"),
  } : undefined,
};

console.log(`Server running at http://localhost:3000`);
```

## 結語

Bun 2.0 不僅僅是一個版本號的跳躍——它代表了 JavaScript 工具鏈的典範轉移。自研 JIT 編譯器帶來了 3–5 倍的效能提升，Rust/Zig 插件系統打開了原生擴展的大門，Quartz Mirror 從根本上解決了套件下載的瓶頸。對前端和全端開發者來說，Bun 2.0 是目前最接近「一站式解決方案」的工具。

---

**延伸閱讀**

- [Bun 2.0 發布公告](https://www.google.com/search?q=Bun+2.0+release+announcement)
- [Bun JIT 編譯器設計文件](https://www.google.com/search?q=Bun+JIT+compiler+design)
- [Quartz Mirror 技術架構](https://www.google.com/search?q=Bun+Quartz+Mirror)
- [Bun 插件系統文件](https://www.google.com/search?q=Bun+plugin+system+Rust+Zig)
