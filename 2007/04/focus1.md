# 行動瀏覽器的崛起：從 WAP 到智慧型手機瀏覽器

## WAP 的誕生

1997 年，WAP（Wireless Application Protocol）論壇成立，旨在為行動裝置建立統一的網路標準。WAP 的核心是 WML（Wireless Markup Language），一種專為有限資源裝置設計的 XML 標記語言。

```
WAP 協定堆疊：
─────────────
┌─────────────────────┐
│  應用層 (WAE)       │  WML、WMLS、WMLScript
├─────────────────────┤
│  會話層 (WSP)       │  HTTP-like 協定
├─────────────────────┤
│  傳輸層 (WTP)       │  UDP/TCP 包裝
├─────────────────────┤
│  安全性 (WTLS)      │  TLS 的輕量版本
├─────────────────────┤
│  承載層 (WDP)       │  IP、GSM SMS、USSD
└─────────────────────┘
```

## WML 的特性

WML 設計於 1999 年，充分考慮了當時行動裝置的限制：

### 螢幕尺寸限制
WML 設計用於小螢幕（通常 5-10 行，每行 10-20 字元）。內容需要精心策劃。

### 卡片導航模型
WML 使用「卡片」（Card）的概念組織內容，每個螢幕是一張卡片：

```xml
<?xml version="1.0"?>
<!DOCTYPE wml PUBLIC "-//WAPFORUM//DTD WML 1.1//EN"
"http://www.wapforum.org/DTD/wml_1.1.xml">

<wml>
  <card id="main" title="新聞首頁">
    <p mode="nowrap">
      歡迎使用新聞服務<br/>
      <a href="#sports">體育</a><br/>
      <a href="#tech">科技</a><br/>
      <a href="#finance">財經</a>
    </p>
  </card>

  <card id="sports" title="體育新聞">
    <p>
      體育新聞內容...
      <do type="prev" label="返回">
        <prev/>
      </do>
    </p>
  </card>
</wml>
```

### 任務與事件
WML 支援任務（Task）的概念，用於導航和表單提交：

```xml
<do type="accept" label="提交">
  <go href="http://example.com/submit" method="post">
    <postfield name="data" value="$(userInput)"/>
  </go>
</do>
```

## 從 WAP 到 HTTP

2000 年代初期，WAP 閘道（Gateway）開始支援直接 HTTP 代理。這是一個重要的轉變——行動瀏覽器可以直接存取標準的 Web 網站，而不需要特殊的 WML 內容。

```
早期 WAP 流程：                    現代 WAP 流程：
─────────────────                  ─────────────────
手機 → WAP 閘道 → WAP 伺服器       手機 → HTTP 代理 → 標準 Web 伺服器
(WML 內容)                         (HTML 內容)
```

## WebKit 的革命

2003 年，蘋果開始開發 Safari 瀏覽器，採用了 KDE 的 KHTML 引擎作為基礎。2005 年，蘋果開源了 WebKit 引擎。

WebKit 的成功關鍵：

### KHTML 的血統
WebKit 起源於 KDE 專案的 KHTML，這是一個符合標準的 HTML/CSS 引擎。KHTML 的設計目標是「準確呈現」而非「向後相容」，這使得 WebKit 可以更嚴格地遵循 W3C 標準。

### Nitro JavaScript 引擎
2007 年，WebKit 推出了全新的 JavaScript 引擎 Nitro（又稱 SquirrelFish），大幅提升了 JavaScript 執行速度。Nitro 採用了位元組碼編譯和 JIT（即時編譯）技術。

```javascript
// JavaScript 引擎效能對比（2007 年）
引擎           執行速度（相對值）
─────────────────────────────
SpiderMonkey      1.0x（基準）
Nitro (WebKit)    2.5-3.0x
V8 (Chrome)       2.8-3.2x
```

### 跨平台一致性
WebKit 在 Mac OS X、iOS、Android 等平台上提供一致的呈現。這對於 Web 開發者來說是巨大的解脫——「一次撰寫，到處運行」終於在行動裝置上實現。

## iPhone Safari 的衝擊

2007 年六月，蘋果發布 iPhone。iPhone 的 Safari Mobile 是第一個真正為觸控設計的「完整」瀏覽器。

### iPhone Safari 的規格

| 特性 | 支援情況 |
|------|---------|
| HTML 4.01 | 完整支援 |
| CSS 2.1 | 完整支援 |
| CSS 3 | 部分支援（動畫、陰影、漸層） |
| JavaScript | 完整 AJAX 支援 |
| DOM | 完整 DOM 2 支援 |
| 插件 | 不支援（Flash 等） |
| 觸控事件 | 原生支援 |

### 檢視區（Viewport）設定

iPhone 引入了一種創新的 meta 標籤來控制頁面呈現：

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
```

這個設定讓 Web 開發者可以：
- 設定邏輯像素寬度
- 控制初始縮放比例
- 禁止使用者縮放

### 觸控事件

iPhone Safari 引入了專屬的觸控事件 API：

```javascript
element.addEventListener('touchstart', function(e) {
    var touch = e.touches[0];
    console.log('Touch at: ' + touch.clientX + ', ' + touch.clientY);
}, false);

element.addEventListener('touchmove', function(e) {
    e.preventDefault(); // 阻止滾動
}, false);

element.addEventListener('touchend', function(e) {
    console.log('Touch ended');
}, false);
```

## Android 的崛起

2007 年十一月，Google 宣布成立開放手機聯盟（Open Handset Alliance），並展示了 Android 平台。Android 的瀏覽器同樣基於 WebKit。

### Android 瀏覽器的特性

- 完整 HTML/CSS/JavaScript 支援
- 與 Chrome 共享 WebKit 程式碼庫
- 支援 Flash Lite（部分裝置）
- 地理位置 API
- 離線應用支援

## 瀏覽器市場版圖（2007 年中）

```
行動瀏覽器市場佔有率（估計）：
───────────────────────────────────
Opera Mini        ~25%  （Java ME 功能手機）
Safari Mobile     ~20%  （iPhone）
IE Mobile         ~20%  （Windows Mobile）
WebKit-based      ~15%  （Android、S60）
Others            ~20%
```

## 結語

從 1999 年的 WML 到 2007 年的 WebKit，行動瀏覽器經歷了漫長的進化歷程。WML 教會我們如何在資源受限的環境下設計介面；WebKit 則開啟了「豐富」行動 Web 體驗的可能。

iPhone 的出現是一個轉捩點——它證明了行動瀏覽器可以提供與桌面相當的 Web 體驗。這個認知將徹底改變未來十年的 Web 開發。

---

## 延伸閱讀

- [WAP 協定規範](https://www.google.com/search?q=WAP+Wireless+Application+Protocol+specification)
- [WebKit 開源專案](https://www.google.com/search?q=WebKit+open+source+project)
- [iPhone+Safari+Mobile+features](https://www.google.com/search?q=iPhone+Safari+Mobile+features+2007)
- [W3C+Mobile+Web+best+practices](https://www.google.com/search?q=W3C+Mobile+Web+best+practices)

---

*本篇文章為「AI 程式人雜誌 2007 年 4 月號」本期焦點系列之一。*