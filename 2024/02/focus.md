# 本期焦點

## Node.js 後端開發入門

### 引言

Node.js 自 2009 年由 Ryan Dahl 創建以來，已經徹底改變了 JavaScript 的生態。它讓開發者能夠使用 JavaScript 編寫伺服器端程式，實現前後端語言的統一。Node.js 的非同步 I/O 模型和事件驅動架構，使其在高併發場景中表現出色，成為現代後端開發的主流選擇之一。

本期雜誌將帶領讀者全面了解 Node.js 後端開發的各個面向，從基礎概念到實戰技巧，從核心模組到生態框架，完整的學習路徑讓初學者也能快速上手。

---

## 大綱

- [程式：Node.js 完整示範](focus_code.md) — Express-like 伺服器、JWT、檔案操作

1. [Node.js 執行期與事件循環](focus1.md)
   - V8 引擎與 Node.js 架構
   - Event Loop 原理
   - 非同步 I/O 模型

2. [內建模組：fs、path、http](focus2.md)
   - 檔案系統操作
   - 路徑處理
   - HTTP 伺服器建立

3. [Express 框架入門](focus3.md)
   - 安裝與設定
   - 基本路由
   - 請求與回應物件

4. [路由與中介軟體](focus4.md)
   - 路由參數與萬用路由
   - 中介軟體串接
   - 錯誤處理中介軟體

5. [REST API 設計](focus5.md)
   - RESTful 原則
   - CRUD 操作設計
   - API 版本管理

6. [資料庫連接：MongoDB / SQLite](focus6.md)
   - MongoDB 與 Mongoose
   - SQLite 整合
   - ORM/ODM 使用

7. [認證與授權：JWT](focus7.md)
   - JWT 結構解析
   - Token 發放與驗證
   - 路由保護機制

---

## 濃縮回顧

Node.js 的核心優勢在於其事件驅動、非阻塞 I/O 模型。不同於傳統的多執行緒伺服器，Node.js 使用單一執行緒配合事件循環（Event Loop）來處理大量併發請求，這使得它在處理 I/O 密集型任務時具有極高的效率和資源利用率。

### 執行期架構

```
┌──────────────────────────────┐
│        JavaScript Code        │
├──────────────────────────────┤
│   Node.js API (fs, http...)   │
├──────────────────────────────┤
│       V8 JavaScript Engine    │
├──────────────────────────────┤
│          libuv (I/O)          │
└──────────────────────────────┘
```

Node.js 之所以能處理大量併發連接，關鍵在於 libuv 這個 C 語言庫實現的非同步 I/O 機制。libuv 封裝了 epoll (Linux)、kqueue (macOS) 和 IOCP (Windows) 等系統底層的非同步 I/O 介面，提供一致的跨平台 API。

### Express 生態

Express 是目前最成熟的 Node.js Web 框架，其簡潔的中介軟體架構讓開發者可以靈活地組合各種功能。從路由、靜態檔案服務到認證授權，Express 以輕量、靈活著稱，也衍生出了大量的中介軟體套件。

### 資料庫整合

Node.js 支援多種資料庫方案：SQLite 適合輕量級原型開發和小型應用，MongoDB 適合文件型資料的場景，PostgreSQL 和 MySQL 則是傳統關聯式資料庫的可靠選擇。

---

## 結論與展望

Node.js 生態持續快速發展。隨著 WinterCG 標準的推動，未來各 JavaScript 執行期之間的互操作性將進一步提升。Express 5.0 與 TypeScript 原生支援的到來，也標誌著 Node.js 生態的成熟。

無論你是前端開發者想跨足後端，或是後端開發者想探索新的技術棧，Node.js 都是一個值得深入學習的選擇。

---

## 延伸閱讀

- [Node.js 官方文件](https://www.google.com/search?q=Node.js+official+documentation)
- [Node.js 執行期與事件循環](focus1.md)
- [Express 框架入門](focus3.md)
- [本期程式實作](focus_code.md)
