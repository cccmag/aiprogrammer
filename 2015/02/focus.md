# 本期焦點

## Node.js 與伺服端 JavaScript

### 引言

Node.js 讓 JavaScript 可以在伺服器執行，這不僅是技術上的突破，更是開發模式的革命。統一的語言讓前後端開發變得無縫接軌。

2015 年 2 月，Node.js 生態系已經相當成熟，從 Express 到 Koa，從原生 TCP 到 WebSocket，Node.js 提供了完整的伺服端開發解決方案。

---

## 大綱

* [程式：Express 框架實務](focus_code.md)
   - REST API 開發
   - 中介層設計
   - 錯誤處理

1. [Node.js 基礎與核心模組](focus1.md)
   - 事件驅動架構
   - 檔案系統操作
   - HTTP 模組

2. [npm 與模組管理](focus2.md)
   - npm 命令详解
   - SemVer 版本控制
   - 套件發布流程

3. [Express 框架](focus3.md)
   - 路由系統
   - 中介層
   - 模板引擎

4. [RESTful API 設計](focus4.md)
   - 資源導向路由
   - HTTP 方法語義
   - 狀態碼與錯誤處理

5. [資料庫整合](focus5.md)
   - MongoDB + Mongoose
   - Redis 緩存
   - MySQL 連線池

6. [即時通訊](focus6.md)
   - Socket.IO
   - WebSocket 握手
   - 房間與命名空間

7. [部署與維運](focus7.md)
   - PM2 程序管理
   - Docker 容器化
   - Nginx 反向代理

---

## 濃縮回顧

### Node.js 的核心特性

```
事件驅動非阻塞 I/O：
─────────────────────

傳統阻塞 I/O：
  請求1 ──→ [讀取 DB] ──→ 回應1
  請求2 ──→ [讀取 DB] ──→ 回應2
  請求3 ──→ [讀取 DB] ──→ 回應3

Node.js 非阻塞 I/O：
  請求1 ──→ [讀取 DB] ──→ 回應1
  請求2 ──→ [讀取 DB]
  請求3 ──→ [讀取 DB]
           ↑              ↑
           └── 事件迴圈 ←──┘
```

### npm 生態系

```
npm 統計（2015 年 2 月）：
───────────────────────────
套件數量：150,000+
下載量：  每月數十億次
活躍專案：全球最大程式碼生態系
```

### Express 的設計哲學

Express 的哲學是「最小化抽象」——它提供了足夠的工具，但不會限制你的選擇。

---

## 結論與展望

Node.js 在 2015 年已經成為企業級伺服端開發的重要選擇。從小型專案到大型系統，Node.js 的彈性和效能證明了 JavaScript 在伺服端的價值。

未來的方向：
1. **async/await**：讓非同步程式碼更像同步
2. **微服務**：Node.js 的輕量非常適合微服務
3. **物聯網**：Node.js 的事件驅動適合 IoT 應用

---

## 延伸閱讀

- [Node.js 基礎與核心模組](focus1.md)
- [npm 與模組管理](focus2.md)
- [Express 框架](focus3.md)
- [RESTful API 設計](focus4.md)
- [資料庫整合](focus5.md)
- [即時通訊](focus6.md)
- [部署與維運](focus7.md)

---

*本期焦點到此結束。*