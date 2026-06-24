# 本期焦點

## Node.js 誕生：伺服器端 JavaScript 革命

### 引言

2009 年是 JavaScript 徹底改變的一年。Node.js 的誕生開創了伺服器端 JavaScript 的新時代，讓同一種語言可以同時用於前端和後端開發。

本期歷史回顧將帶領讀者回顧 Node.js 誕生的歷史背景、技術原理、以及對後端開發的深遠影響。

---

## 大綱

* [程式：Event Loop 與非同步程式設計](focus_code.md)
   - 事件驅動程式模型
   - 回呼函式與錯誤處理
   - 非阻塞 I/O 操作

1. [Node.js 的誕生背景](focus1.md)
   - Ryan Dahl 與 Node.js 的起源
   - 為什麼選擇 JavaScript
   - V8 引擎的選擇

2. [事件驅動架構](focus2.md)
   - Event Loop 機制
   - 非阻塞 I/O 原理
   - 单執行緒設計

3. [CommonJS 模組系統](focus3.md)
   - require() 機制
   - 模組導出與導入
   - npm 的前身

4. [npm 的起源](focus4.md)
   - 套件管理需求
   - 早期模組生態
   - 共享函式庫

5. [HTTP 伺服器開發](focus5.md)
   - 建立 HTTP 伺服器
   - 路由與中介軟體
   - 請求與回應處理

6. [即時通訊應用](focus6.md)
   - WebSocket 協定
   - Socket.IO 簡介
   - 即時雙向通訊

7. [未來展望](focus7.md)
   - npm 生態爆發
   - 微服務架構
   - 即時全端開發

---

## 濃縮回顧

### Node.js 的核心优势

```
Node.js 與傳統伺服器比較：
─────────────────────────
傳統（Apache/PHP）：
  - 每個連線一個執行緒
  - 阻塞式 I/O
  - 高記憶體使用

Node.js：
  - 事件驅動單執行緒
  - 非阻塞 I/O
  - 低記憶體使用
  - 高併發處理能力
```

### JavaScript: 統一的語言

Node.js 讓 JavaScript 成為真正的全端語言：

```
前端：DOM 操作、事件處理、使用者介面
    ↓ 相同的語法
後端：HTTP 伺服器、檔案 I/O、資料庫連線

優勢：
- 減少上下文切換
- 統一的開發體驗
- 豐富的 JSON 支援
- npm 生態系的威力
```

### 事件驅動的優雅

傳統的同步程式設計：
```javascript
const data = database.query("SELECT * FROM users");
// 等待查詢完成
console.log(data);
// 這裡才執行
```

Node.js 的非同步程式設計：
```javascript
database.query("SELECT * FROM users", (error, data) => {
  console.log(data);
});
// 不等待，繼續執行其他任務
```

---

## 結論與展望

Node.js 的誕生標誌著 JavaScript 生態系的一個重要轉折點。事件驅動、非阻塞 I/O 的設計理念，讓 Node.js 特別適合處理高併發、I/O 密集的應用場景。

未來的方向是清晰的：
1. **全端 JavaScript**：統一的語言，全端的應用
2. **即時應用**：WebSocket、聊天室、即時協作工具
3. **微服務**：輕量級、快速的後端服務
4. **npm 生態**：世界上最大的套件註冊中心

---

## 延伸閱讀

- [Node.js 的誕生背景](focus1.md)
- [事件驅動架構](focus2.md)
- [CommonJS 模組系統](focus3.md)
- [HTTP 伺服器開發](focus5.md)
- [未來展望](focus7.md)

---

*本期焦點到此結束。下期我們將聚焦雲端平台與 PaaS 服務的發展。*