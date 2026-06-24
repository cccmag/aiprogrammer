# 本期焦點

## 行動 Web 開發：行動瀏覽器、WAP、iPhone SDK 預備

### 引言

2007 年是行動網路的轉捩點。智慧型手機的普及讓人們開始期待在手機上獲得完整的網頁體驗。從 WAP 的文字時代到 WebKit 的豐富介面，行動 Web 開發正在經歷一場革命。

本期，我們將回顧行動 Web 技術的發展歷程，探討當前的技術挑戰，並預覽 iPhone SDK 帶來的機會與挑戰。

---

## 大綱

* [程式：實作 WAP 瀏覽器模擬器](focus_code.md)
   - WML 解析器實作
   - WBMP 圖片處理
   - WAP 會話管理

1. [行動瀏覽器的崛起](focus1.md)
   - 從 WAP 到智慧型手機瀏覽器
   - WebKit 的革命
   - iPhone Safari 的影響

2. [WML 與 XHTML Mobile](focus2.md)
   - WML 的設計理念
   - XHTML MP 的標準化
   - 標記語言的比較

3. [iPhone SDK 與 Web 開發](focus3.md)
   - Apple 的開發者策略
   - Web 應用 vs 原生應用
   - Safari Mobile 的能力

4. [JavaScript Mobile 框架](focus4.md)
   - 觸控時代的瀏覽器技術
   - iUI、QuickConnection、jQTouch
   - 移動優先的設計

5. [行動瀏覽器的相容性挑戰](focus5.md)
   - 破碎的生態系
   - UA 偵測策略
   - 漸進增強原則

6. [未來展望：Web 2.0 與 Mobile](focus6.md)
   - 融合的趨勢
   - 離線 Web 應用
   - 地理定位 API

---

## 濃縮回顧

### 從 WAP 到 WebKit

1999 年，WAP（Wireless Application Protocol）論壇推出了 WML（Wireless Markup Language），這是一種基於 XML 的標記語言，專為有限的行動裝置設計。WML 的設計理念是「將網頁濃縮成文字」，犧牲豐富性換取相容性。

2007 年，WebKit 引擎的出現改變了這一切。WebKit 最初是 KDE 專案的一部分（KHTML），後來被蘋果採用並開源。WebKit 提供了完整的 HTML、CSS 和 JavaScript 支援，讓行動瀏覽器可以呈現和桌面一樣豐富的內容。

### iPhone 的衝擊

2007 年六月，蘋果即將發布 iPhone。iPhone 的 Safari Mobile 是第一個真正「完整」的行動瀏覽器：
- 完整的 HTML 4.01 支援
- CSS 2.1 和部分 CSS 3
- JavaScript AJAX 支援
- 觸控介面的互動設計

iPhone 的推出將徹底改變行動 Web 開發的遊戲規則。

### Web 應用 vs 原生應用

iPhone SDK 公布後，開發者面臨一個抉擇：Web 應用還是原生應用？

Web 應用的優勢：
- 跨平台相容
- 無需安裝
- 易于分發

原生應用的優勢：
- 硬體 API 完全存取
- 離線能力
- App Store 分發管道

---

## 結論與展望

2007 年是行動 Web 開發的關鍵一年。iPhone 的出現、Android 的崛起、以及標準化組織的努力，都在推動行動 Web 技術向前發展。

未來幾年，我們將看到：
1. **HTML 5 的行動支援**：Canvas、離線儲存、地理位置 API
2. **觸控介面的標準化**：觸控事件的統一處理
3. **效能持續提升**：JavaScript 引擎、硬體加速

行動 Web 開發的黃金時代即將來臨。

---

## 延伸閱讀

- [行動瀏覽器的崛起](focus1.md)
- [WML 與 XHTML Mobile](focus2.md)
- [iPhone SDK 與 Web 開發](focus3.md)
- [JavaScript Mobile 框架](focus4.md)
- [行動瀏覽器的相容性挑戰](focus5.md)
- [未來展望：Web 2.0 與 Mobile](focus6.md)

---

*本期焦點到此結束。下期我們將聚焦 REST API 與 Web 服務開發。*