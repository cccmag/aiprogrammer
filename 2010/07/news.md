# 本月新知

## 2010 年 7 月程式與 Web 技術動態

### 前端開發

**HTML5 標準正式完成**

W3C 於 2010 年 7 月宣布 HTML5 標準正式進入候選推薦階段（Candidate Recommendation）。HTML5 引入了多項重要新特性：

- `<video>` 和 `<audio>` 標籤：原生多媒體支援
- `<canvas>` 元素：2D 繪圖 API
- 本地儲存（LocalStorage）：用戶端持久化資料
- Web Workers：多執行緒背景處理
- WebSocket：雙向即時通訊

這些特性為 Web 應用開發帶來了革命性的變化，減少了對 Flash 等外掛程式的依賴。

**Bootstrap 框架的崛起**

Twitter 團隊在 2010 年發布了 Bootstrap 的早期版本（那時還內部使用名為「Twitter Blueprint」），這個 CSS 框架迅速獲得了廣泛關注。Bootstrap 的核心特點包括：

- 12 欄響應式栅格系統
- 預設樣式的 HTML 元素
- JavaScript 插件系統
- 跨瀏覽器相容性支援

### JavaScript 生態

**Node.js 快速發展**

Node.js 在 2010 年經歷了快速迭代。Ryan Dahl 的這個伺服器端 JavaScript 環境採用了非阻塞 I/O 模型，適合高並發應用場景。npm 套件管理器的早期版本也開始成型，為 Node.js 生態的繁榮奠定了基礎。

**CoffeeScript 流行**

CoffeeScript 1.0 的發布讓更多人開始關注這款「更優雅的 JavaScript」。CoffeeScript 編譯後生成原生 JavaScript，提供了類 Python 的語法：

```coffeescript
# CoffeeScript
square = (x) -> x * x
list = [1, 2, 3, 4, 5]
squares = (square x for x in list)
```

### 資料庫技術

**Redis 2.0 發布**

Redis 2.0 在 2010 年帶來了多項重要更新，包括 Virtual Memory 和 EXPIRE 命令的改進。Redis 作為一個記憶體 key-value 儲存系統，在快取和即時應用場景中展現了卓越效能。

**MongoDB 持續成長**

MongoDB 繼續在文件導向資料庫市場擴大影響力。其灵活的 JSON 式文件儲存模式和豐富的查詢語言吸引了大量 Web 開發者。

### 雲端運算

**雲端服務的普及**

Amazon Web Services（AWS）在 2010 年持續擴張，EC2、S3 等服務的使用量大幅增長。Google App Engine 也開始支援更多程式語言和功能。

**Heroku 支援 Node.js**

Heroku 宣佈支援 Node.js 部署，讓開發者可以更輕鬆地部署和管理伺服器端 JavaScript 應用。

### 開發工具

**GitHub 成長迅猛**

GitHub 在 2010 年經歷了爆發式成長，越來越多的開源專案從 Google Code、SourceForge 遷移到 GitHub。其 pull request 功能和程式碼審查工具重新定義了協作開發的工作流程。

**Heroku 收購**

Salesforce.com 以現金方式收購了 Heroku，標誌著 PaaS 雲端服務的商業化進程加速。

### AI 與機器學習

**Watson 參加 Jeopardy**

IBM 的 Watson 超級電腦在 2010 年完成了與人類冠軍的 Jeopardy! 知識競賽訓練。Watson 採用了 DeepQA 系統，能夠理解自然語言問題並從大量資料中找出準確答案。這是問答系統領域的重大突破。

**深度學習的早期進展**

多倫多大學的 Geoffrey Hinton 團隊在深度學習領域取得了重要進展。他們的研究為日後深度神經網路在影像辨識和語音處理中的廣泛應用奠定了理論基礎。

---

*原文創於 2010 年 7 月，由 AI 程式人雜誌重新整理*