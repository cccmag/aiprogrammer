# WebKit 開源：瀏覽器引擎的新時代

## 前言

2006 年 4 月，蘋果將 WebKit 開源，這是一個改變瀏覽器產業格局的決定。WebKit 的起源、發展和成功，展示了一個開放原始碼專案如何能夠主導整個產業。

## WebKit 的起源

### KHTML 專案

WebKit 的核心是 KDE 的 KHTML 引擎。1998 年，KDE 團隊開始開發 KHTML，作為 Konqueror 瀏覽器的渲染引擎。KHTML 的設計目標是：

- 符合 W3C 標準
- 模組化架構
- 高效能
- 跨平台支援

### 蘋果的採用與重構

2001 年，蘋果開始開發 Safari 瀏覽器。蘋果選擇以 KHTML 為基礎，但進行了大量的重構和優化：

- 重新設計 JavaScript 引擎（JavaScriptCore）
- 引入「Nitro」引擎（後來的名稱）
- 最佳化 DOM 操作效能
- 新增作業系統整合功能

### 開源的決定

2006 年，蘋果宣布開源 WebKit。這個決定有多重因素：

1. **社群貢獻**：吸引外部開發者參與
2. **標準化**：推動 Web 標準的發展
3. **生態系統**：建立以 WebKit 為核心的開發者生態

## WebKit 架構

```
WebKit 架構圖：
─────────────────
┌────────────────────────────────────────┐
│            WebKit 層                   │
│  提供跨平台 API 與統一介面             │
├────────────────────────────────────────┤
│        WebCore（渲染引擎）             │
│  HTML/CSS 解析、DOM、版面計算          │
├────────────────────────────────────────┤
│     JavaScriptCore（JS 引擎）          │
│  JavaScript 執行環境                   │
├────────────────────────────────────────┤
│     Ports（平台特定實作）              │
│  Mac OS X、Windows、GTK、Qt            │
└────────────────────────────────────────┘
```

## WebKit 的關鍵創新

### 1. KHTML 的血統

WebKit 繼承了 KHTML 的嚴格標準相容性。不同於其他瀏覽器，WebKit 的設計目標是「正確呈現」而非「向後相容」。這使得 WebKit 能夠更嚴格地遵循 W3C 標準。

### 2. Nitro JavaScript 引擎

2007 年，WebKit 推出了全新的 JavaScript 引擎 Nitro，大幅提升了 JavaScript 執行速度：

```
JavaScript 效能對比（SUNSpider 基準測試）：
──────────────────────────────────────────
引擎                    時間（ms）
──────────────────────────────────────────
SpiderMonkey (Firefox)    3000
Nitro (WebKit/Safari)    1200
V8 (Chrome)              1100
──────────────────────────────────────────
```

### 3. 硬體加速渲染

WebKit 是最早支援硬體加速 CSS 動畫的引擎：

```css
.animated {
    -webkit-transform: translate3d(0, 0, 0);
    -webkit-transition: transform 0.3s;
}
```

## WebKit 的影響

### 行動瀏覽器的主導

WebKit 迅速成為行動瀏覽器的主流引擎：

```
2007 年 WebKit 採用率：
─────────────────────
Safari Mobile     100% iPhone
Android Browser   100% Android
BlackBerry 6      2010 年採用
webOS             2009 年採用
─────────────────────
```

### 標準化的推動

WebKit 的開源推動了多項 Web 標準的發展：

- CSS 3 動畫與過渡
- 觸控事件 API
- WebSocket
- 地理位置 API

## 結語

WebKit 的成功展示了開源專案的力量。從 KHTML 出發，經過蘋果的重構和開源，WebKit 最終成為主宰行動瀏覽器市場的引擎。

這個故事告訴我們：**有時最好的創新不是從零開始，而是站在巨人的肩膀上**。

---

## 延伸閱讀

- [WebKit+open+source+2006](https://www.google.com/search?q=WebKit+open+source+2006)
- [KHTML+history+KDE](https://www.google.com/search?q=KHTML+history+KDE+browser)
- [Safari+WebKit+architecture](https://www.google.com/search?q=Safari+WebKit+architecture)

---