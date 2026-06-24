# iPhone SDK 與 Web 開發：Apple 的開發者策略

## 2007 年六月：歷史性的 WWDC

2007 年六月，蘋果在全球開發者大會（WWDC）上發布了 iPhone，並宣布將在 2008 年二月推出 iPhone SDK。此消息在開發者社群引發了巨大轟動。

### iPhone 發布時的開發者選項

在 SDK 發布之前，iPhone 僅支援「Web 應用」——完全基於 Safari 瀏覽器的 HTML/CSS/JavaScript 應用。蘋果稱之為「Web 2.0 應用」。

```
iPhone Web 應用的優勢：
──────────────────────────
✓ 跨平台：任何能上網的裝置都可以使用
✓ 無需安裝：直接透過 URL 存取
✓ 自動更新：永遠是最新版本
✓ Apple 不抽成

iPhone Web 應用的限制：
──────────────────────────
✗ 無法存取通訊錄、相機、GPS
✗ 無法在離線模式下運行
✗ 無法使用推播通知
✗ 使用者可能找不到你的「應用」
```

## iPhone SDK 的衝擊

2008 年二月，iPhone SDK 正式發布。SDK 提供了完整的原生 API，包括：

### 原生 API 能力

| API 類別 | 能力說明 |
|---------|---------|
| 位置服務 | GPS、細胞基地台、WiFi 定位 |
| 加速計 | 裝置方向偵測、搖晃手勢 |
| 相機 | 拍照、錄影 |
| 通訊錄 | 讀取聯絡人資料 |
| 檔案系統 | 文件目錄存取 |
| SQLite | 本地資料庫 |
| 推播 | Apple Push Notification |

### 開發工具鏈

```
iPhone SDK 工具鏈：
─────────────────────
Xcode     - 整合開發環境
Interface Builder - UI 設計工具
Instruments - 效能分析工具
iPhone Simulator - 模擬器
```

## Web 應用 vs 原生應用

SDK 發布後，開發者面臨一個根本問題：該選擇哪種方式？

### 成本效益分析

```
開發方式比較：
─────────────────────────────────────────────────────
特性         Web 應用        原生 SDK
─────────────────────────────────────────────────────
學習曲線     低（HTML/JS）   高（Cocoa Touch）
開發時間     短              長
跨平台       完全支援        僅 iPhone（當時）
API 存取     有限            完全
效能         依賴 JavaScript 直接近系統
分發管道     URL             App Store
營收分成     無              30% 營收
更新速度     即時            需 App Store 審核
離線能力     有限（Cache API）完整支援
```

### 混合應用模式

一些開發者選擇「混合」（Hybrid）模式——使用 UIWebView 嵌入原生殼：

```objc
// Objective-C：使用 UIWebView 載入 Web 內容
@interface HybridAppViewController : UIViewController {
    UIWebView *webView;
}

- (void)viewDidLoad {
    [super viewDidLoad];

    webView = [[UIWebView alloc] initWithFrame:self.view.bounds];
    webView.delegate = self;
    [self.view addSubview:webView];

    NSURL *url = [NSURL URLWithString:@"http://example.com/app.html"];
    [webView loadRequest:[NSURLRequest requestWithURL:url]];
}

@end
```

在網頁端，使用 JavaScript 介面橋接到原生功能：

```javascript
// JavaScript：呼叫原生功能
function getLocation() {
    if (typeof window.webkit !== 'undefined' &&
        window.webkit.messageHandlers &&
        window.webkit.messageHandlers.locationHandler) {
        window.webkit.messageHandlers.locationHandler.postMessage(
            { action: 'getCurrentLocation' }
        );
    }
}

// 監聽原生回傳
window.locationCallback = function(lat, lng) {
    console.log('Location: ' + lat + ', ' + lng);
    updateMap(lat, lng);
};
```

## Apple 的「Web 應用」宣言

有趣的是，蘋果在 iPhone 發布時特別強調 Web 應用的價值：

喬布斯在 2007 年的演說中說：

> 「你可以用 Safari 開發出非常棒的 Web 2.0 應用。這些應用可以完整存取 iPhone 的功能...我們認為這些 Web 應用將是第三類應用生態系統，與原生應用並列。」

這個願景最終被「App Store」取代，但 Web 應用的理念——「一次撰寫，到處運行」——仍然是行動開發的重要課題。

## Safari Mobile 的 Web 應用能力

2007 年的 Safari Mobile 已經具備了相當完整的 Web 能力：

### 支援的 Web 標準

```
Safari Mobile (2007) 標準支援：
──────────────────────────────────
HTML      ████████████████████  HTML 4.01 完整支援
CSS       ████████████████░░░░  CSS 2.1 + 部分 CSS 3
JavaScript███████████████░░░░  ECMAScript 3 + AJAX
DOM       ████████████████████  DOM Level 2 完整
XMLHttpRequest ████████████████  完整支援
Canvas    ████████████░░░░░░░  2D Context
SVG       ████████░░░░░░░░░░  基礎支援
```

### Safari Mobile 特有的 meta 標籤

```html
<!-- 設定檢視區 -->
<meta name="viewport"
      content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">

<!-- 將網頁設為「應用程式模式」（全螢幕） -->
<meta name="apple-mobile-web-app-capable" content="yes">

<!-- 自訂狀態列顏色 -->
<meta name="apple-mobile-web-app-status-bar-style" content="black">

<!-- 圖示 -->
<link rel="apple-touch-icon" href="icon.png">

<!-- 啟動畫面 -->
<link rel="apple-touch-startup-image" href="splash.png">
```

### 觸控事件處理

```javascript
// 單點觸控手勢
document.addEventListener('touchstart', handleTouch, false);
document.addEventListener('touchmove', handleTouch, false);
document.addEventListener('touchend', handleTouch, false);
document.addEventListener('touchcancel', handleTouch, false);

// 雙擊偵測
element.addEventListener('click', function(e) {
    var now = Date.now();
    if (now - lastClickTime < 300) {
        // 雙擊處理
        handleDoubleTap();
    }
    lastClickTime = now;
});

// 拖曳實現
var startX, startY, currentX, currentY;

function handleTouch(e) {
    if (e.type === 'touchstart') {
        startX = e.touches[0].clientX;
        startY = e.touches[0].clientY;
    } else if (e.type === 'touchmove') {
        currentX = e.touches[0].clientX;
        currentY = e.touches[0].clientY;
        updatePosition(currentX - startX, currentY - startY);
    }
}
```

## iPhone 對 Web 開發的長遠影響

iPhone 雖然在初期打壓了 Web 應用生態，但長期來說它推動了多項 Web 標準：

### 推動的標準

1. **觸控事件 API**：iPhone 的觸控 API 最終被标准化为 Touch Events 規範
2. **Viewport 控制**：這個 meta 標籤成為行動 Web 開發的標準
3. **WebSocket**：iPhone Safari 最早支援 WebSocket
4. **離線 Web 應用**：Application Cache API 的部分靈感來自 iPhone
5. **地理位置 API**：iPhone 率先實現了 W3C Geolocation API

### WebKit 的主導地位

iPhone Safari 基於 WebKit，這直接推動了 WebKit 成為行動瀏覽器的主導引擎：

```
2007-2010 年 WebKit 採用趨勢：
───────────────────────────────
2007      Safari Mobile
2008      Android Browser
2009      Palm webOS
2010      BlackBerry 6
2011      Windows Phone (IE Mobile 放棄)
```

## 結語

iPhone SDK 的發布開啟了原生應用時代，但 Web 應用的價值從未消失。十年後，「漸進式 Web 應用」（PWA）將重新定義這個辯論——結合 Web 的便利性和原生的能力。

在 2007 年，開發者需要做出選擇：為今天寫 Web 應用？還是為明天寫原生應用？這個選擇從來沒有標準答案，只有最適合專案需求的決定。

---

## 延伸閱讀

- [iPhone+SDK+2008+announcement](https://www.google.com/search?q=iPhone+SDK+2008+announcement)
- [Safari+Mobile+Web+Applications](https://www.google.com/search?q=Safari+Mobile+Web+Applications+2007)
- [Web+vs+Native+iPhone+debate](https://www.google.com/search?q=Web+vs+Native+iPhone+development+debate)
- [Apple+Web+2.0+apps+strategy](https://www.google.com/search?q=Apple+Web+2.0+apps+Steve+Jobs+2007)

---

*本篇文章為「AI 程式人雜誌 2007 年 4 月號」本期焦點系列之一。*