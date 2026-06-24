# 本期焦點

## Web API 與網路程式設計

### 引言

在現代軟體開發中，Web API（Application Programming Interface）無所不在。當你打開手機 App 查看天氣時，它在呼叫 API；當你在網站上搜尋商品時，它在呼叫 API；當你使用 ChatGPT 與 AI 對話時，它也在呼叫 API。Web API 是現代網路應用的基礎建築方塊，連接著應用程式與服務之間的資料流。

Web API 的核心是 HTTP 協定——這個誕生於 1989 年的協定，經過三十多年的演進，已成為全球資訊網路的基石。從簡單的 GET 請求，到 RESTful 架構風格，再到非同步串流和 WebSocket，Web API 的技術棧不斷豐富。Python 憑藉其簡潔的語法和豐富的生態系，成為 Web API 開發的熱門選擇。

本期的技術回顧將帶領讀者從基礎到進階，全面掌握 Web API 與網路程式設計的核心知識。

---

## 大綱

* [程式：Web API 完整實作範例](focus_code.md)
   - 使用 requests 呼叫公開 API
   - JSON 資料處理與驗證
   - FastAPI 應用程式實作
   - API 認證機制

1. [網路通訊基礎：HTTP 與 REST](focus1.md)
   - HTTP 協定的發展歷程
   - REST 架構風格的核心原則
   - URL 結構與資源定位
   - HTTP 請求和回應模型

2. [使用 requests 呼叫 API](focus2.md)
   - requests 套件安裝與基本用法
   - GET、POST、PUT、DELETE 請求
   - 請求頭、參數與逾時設定
   - 例外處理與重試機制

3. [JSON 資料處理](focus3.md)
   - JSON 格式的基礎語法
   - Python 的 json 模組
   - 序列化與反序列化
   - 資料驗證與 schema 檢查

4. [FastAPI 建立 REST API](focus4.md)
   - FastAPI 的設計哲學
   - 路徑裝飾器與端點定義
   - 路徑參數與查詢參數
   - 請求主體與回應模型

5. [API 認證與安全性](focus5.md)
   - API Key 認證機制
   - JWT（JSON Web Token）
   - OAuth2 授權框架
   - HTTPS 與安全最佳實踐

6. [非同步請求與 WebSocket](focus6.md)
   - asyncio 與 async/await
   - aiohttp 非同步客戶端
   - WebSocket 即時通訊
   - Server-Sent Events

7. [API 設計最佳實踐](focus7.md)
   - 資源命名與版本控制
   - 分頁、過濾與排序
   - 錯誤回應格式
   - API 文件與 SDK 生成

---

## 濃縮回顧

### HTTP 的誕生與演進

HTTP（HyperText Transfer Protocol）由 Tim Berners-Lee 於 1989 年在 CERN 發明。HTTP/1.0（1996）支援基本請求和回應；HTTP/1.1（1997）引入了持久連線和管線化；HTTP/2（2015）帶來了多路復用和伺服器推送；HTTP/3（2022）基於 QUIC 協定，實現了更低的延遲。

### REST 架構風格

Roy Fielding 在 2000 年的博士論文中提出了 REST（Representational State Transfer）架構風格。REST 的核心原則是資源導向——每個 URL 代表一個資源，HTTP 方法代表對該資源的操作。RESTful API 的設計已成為 Web API 的事實標準。

### Python Web API 生態系

Python 的 Web API 生態系豐富多樣：
- **requests**：最受歡迎的 HTTP 客戶端套件
- **FastAPI**：現代高效能 Web 框架
- **Flask**：輕量級 Web 框架
- **Django REST Framework**：全功能 API 框架

### JSON 資料交換格式

JSON（JavaScript Object Notation）已成為 Web API 最常用的資料交換格式。其簡潔的語法、跨語言的支援，以及與 JavaScript 的原生相容性，使其取代 XML 成為 API 的首選格式。

### API 安全性的演進

從早期的 HTTP Basic Auth，到 API Key，再到 JWT 和 OAuth2，API 認證技術持續演進。現代 API 安全方案不僅關注身份驗證，還包括速率限制、輸入驗證、HTTPS 強制執行等防護措施。

---

## 結論與展望

Web API 是現代軟體開發的核心技能。從最基礎的 HTTP 請求到複雜的非同步通訊，從簡單的 JSON 處理到完整的 API 設計，掌握這些技術將使開發者能夠構建出高效、安全、可維護的網路應用。

展望未來，我們可以看到幾個趨勢：
1. **API 優先開發**：越來越多的團隊採用 API-first 設計流程
2. **即時 API**：WebSocket 和 SSE 將成為 API 標準組成部分
3. **AI 整合 API**：AI 模型的 API 化將持續推動新應用形態
4. **安全自動化**：API 安全將從手動審查走向自動化驗證

無論技術如何變遷，理解 Web API 的核心原理，將是每位開發者的重要資產。

---

## 延伸閱讀

- [網路通訊基礎：HTTP 與 REST](focus1.md)
- [使用 requests 呼叫 API](focus2.md)
- [JSON 資料處理](focus3.md)
- [FastAPI 建立 REST API](focus4.md)
- [API 認證與安全性](focus5.md)
- [非同步請求與 WebSocket](focus6.md)
- [API 設計最佳實踐](focus7.md)

---

*本期焦點到此結束。下期我們將聚焦另一個影響深遠的主題，敬請期待。*
