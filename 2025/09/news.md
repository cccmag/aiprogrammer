# 本月新知

## 2025 年 9 月測試工具與品質保證技術動態

### 測試框架

**pytest 9.0 發布：新一代測試執行引擎**

pytest 9.0 於本月正式發布，這是 Python 測試框架最大的一次升級。新版本引入了「平行執行引擎 2.0」，在多核心機器上測試執行速度提升了 3-5 倍。pytest 9.0 也整合了原生的覆盖率支援，無需額外安裝 pytest-cov 套件。此外，新的斷言內省（assertion introspection）機制可以更清楚地顯示複雜資料結構的差異。

**JUnit 5.12 強化參數化測試**

Java 生態的 JUnit 5.12 發布，強化了參數化測試（Parameterized Tests）的能力。新的 `@CsvSource` 和 `@MethodSource` 支援巢狀資料結構和動態測試名稱生成。JUnit 5.12 也引入了測試套件（Test Suite）的自動發現機制，不再需要手動列舉測試類別。

**Playwright 1.50：跨瀏覽器測試的革新**

Playwright 1.50 發布，新增了「時間旅行偵錯」功能——測試失敗時可以倒帶觀看瀏覽器狀態的逐幀變化。新版本也支援 iOS Safari 和 Android Chrome 的真實裝置模擬，以及 WebSocket 請假的攔截與模擬。

### 測試工具

**Selenium 4.30：WebDriver BiDi 協議成熟**

Selenium 4.30 全面採用 WebDriver BiDi（雙向通訊）協議，取代了傳統的 WebDriver Wire Protocol。BiDi 協議讓測試腳本可以直接監聽瀏覽器事件（如 Console 日誌、網路請求、DOM 變化），不再需要輪詢或注入 JavaScript。Selenium 4.30 也原生支援了 Edge 和 Safari 的最新版本。

**Cypress 14：元件測試與端到端測試的統一**

Cypress 14 發布，將元件測試（Component Testing）和端到端測試（End-to-End Testing）整合到同一個執行環境中。開發者可以在同一個測試檔案中混合元件測試和 E2E 測試，共用同一個 fixture 和 mock 設定。Cypress 14 也引入了 AI 輔助的測試生成功能——錄製使用者操作後自動轉換為測試腳本。

**Postman 測試自動化升級**

Postman 發布了全新的「測試自動化工作流」功能，允許使用者將 API 測試串聯成多步驟的測試管線。新的 Collection Runner 支援條件分支、循環和動態變數，讓 API 測試可以涵蓋複雜的業務邏輯場景。Postman 也整合了 GitHub Actions 和 GitLab CI 的測試結果報告。

### 程式碼品質

**SonarQube 10.8：AI 驅動的程式碼審查**

SonarQube 10.8 引入了 AI 驅動的程式碼審查引擎。除了傳統的靜態分析規則，新版本可以自動理解程式碼的業務邏輯，發現「邏輯錯誤」——語法正確但行為不符合預期的程式碼。SonarQube 10.8 也支援了更多程式語言的深度分析，包括 Rust、Go 和 Kotlin。

**Coverage.py 7.6：分支覆蓋率全面支援**

Python 的 Coverage.py 7.6 發布，全面支援分支覆蓋率（Branch Coverage）測量。新版本可以顯示每一行程式碼中哪些分支被執行、哪些分支未被覆蓋。Coverage.py 7.6 也整合了 pytest 9.0 的原生覆盖率報告功能，產生的 HTML 報表可以互動式地瀏覽原始碼和覆蓋率資料。

### 產業趨勢

**AI 輔助測試生成成為主流**

2025 年第三季，AI 輔助測試生成工具的使用率大幅上升。GitHub Copilot 在 9 月的更新中加入了「測試模式」——AI 可以根據原始碼自動生成完整的測試套件，包括邊界條件、錯誤路徑和效能測試。市場上出現了多個專注於測試生成的 AI 工具，如 TestPilot、AutoTest 和 TestSpark。

**Shift-Left 測試的深化**

「Shift-Left」測試理念在 2025 年進一步深化。越來越多的團隊將測試整合到開發流程的早期階段——從需求分析階段就開始撰寫測試案例，在程式碼提交前就執行靜態分析和單元測試。GitHub 的數據顯示，採用 Shift-Left 實踐的團隊，生產環境缺陷率降低了 47%。

**Contract Testing 的興起**

合約測試（Contract Testing）在本月受到廣泛關注。Pact 框架的使用者數在 2025 年成長了 120%。合約測試在微服務架構中特別有用——每個服務提供者定義自己的 API 合約，消費者根據合約進行測試，確保服務之間的相容性。多個大型企業（如 Uber、Netflix、Spotify）公開分享了他們的合約測試實踐。

### 重點回顧

- pytest 9.0 引入平行執行引擎 2.0，測試速度提升 3-5 倍
- Playwright 1.50 新增時間旅行偵錯和真實裝置模擬
- AI 輔助測試生成全面普及
- Shift-Left 測試降低 47% 的生產環境缺陷率
- Coverate.py 7.6 支援分支覆蓋率測量
