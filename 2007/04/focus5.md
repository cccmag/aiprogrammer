# 行動瀏覽器的相容性挑戰：破碎的生態系

## 2007 年的瀏覽器碎片化

2007 年的行動瀏覽器生態系是碎片化的。同一個 HTML 頁面在不同裝置上可能呈現截然不同的結果。

### 市場上的主要瀏覽器

| 瀏覽器 | 平台 | 引擎 | JavaScript |
|--------|------|------|------------|
| Safari Mobile | iPhone | WebKit | Nitro |
| Android Browser | Android | WebKit | V8-like |
| Internet Explorer Mobile | Windows Mobile | IE | JScript |
| Opera Mini | Java ME | Presto | Interpreted |
| BlackBerry Browser | BlackBerry | NetFront | Interpreted |
| Palm WebOS | webOS | WebKit | Nitro |

## 使用者代理偵測

處理相容性問題最常見的方法是偵測瀏覽器型別：

### 使用者代理字串範例

```
Safari Mobile:
Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en)
AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A543a Safari/419.3

Android:
Mozilla/5.0 (Linux; U; Android 1.0; en-us; dream) AppleWebKit/525.10+
 (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2

Windows Mobile IE:
Mozilla/4.0 (compatible; MSIE 6.0; Windows CE; IEMobile 6.12)
```

### 傳統的 UA 偵測

```javascript
// 偵測 iPhone
var isIPhone = /iPhone/i.test(navigator.userAgent);

// 偵測 Android
var isAndroid = /Android/i.test(navigator.userAgent);

// 偵測 Windows Mobile
var isWM = /Windows CE|IEMobile/i.test(navigator.userAgent);

// 根據 UA 載入不同樣式
if (isIPhone) {
    loadStylesheet('iphone.css');
} else if (isAndroid) {
    loadStylesheet('android.css');
} else {
    loadStylesheet('generic.css');
}

// 根據 UA 執行不同邏輯
if (isIPhone) {
    enableTouchGestures();
} else if (isWM) {
    enableD-padNavigation();
} else {
    enableClickNavigation();
}
```

### UA 偵測的問題

```javascript
// UA 欺騙：很多瀏覽器允許使用者修改 UA
// 例如：iPhone 的「全天候」模式可以偽裝成桌面瀏覽�器

// 版本號不一致
// Safari/420+ vs Safari/523.12.2

// Android 裝置差異極大
// 同一 UA 字串可能來自 2.2 吋或 5.5 吋螢幕
```

## 特性偵測：更好的策略

2007 年，Modernizr 等庫推廣了「特性偵測」的概念：

### 基本特性偵測

```javascript
// 檢查 Canvas 支援
var hasCanvas = !!document.createElement('canvas').getContext;

// 檢查觸控支援
var hasTouch = 'ontouchstart' in window;

// 檢查地理位置 API
var hasGeolocation = 'geolocation' in navigator;

// 檢查本地儲存
var hasLocalStorage = 'localStorage' in window;

// 檢查 WebSocket
var hasWebSocket = 'WebSocket' in window;

// 檢查 CSS 3
var hasBorderRadius = 'borderRadius' in document.body.style;
var hasBoxShadow = 'boxShadow' in document.body.style;
```

### 完整特性偵測框架

```javascript
var FeatureDetect = {
    supported: {},

    detect: function() {
        // 渲染引擎
        var ua = navigator.userAgent;
        if (ua.indexOf('WebKit') !== -1) {
            this.supported.engine = 'WebKit';
        } else if (ua.indexOf('Trident') !== -1) {
            this.supported.engine = 'Trident';
        } else if (ua.indexOf('Gecko') !== -1) {
            this.supported.engine = 'Gecko';
        } else if (ua.indexOf('Presto') !== -1) {
            this.supported.engine = 'Presto';
        }

        // HTML 5 API
        this.supported.canvas = !!document.createElement('canvas').getContext;
        this.supported.video = !!document.createElement('video').canPlayType;
        this.supported.geolocation = 'geolocation' in navigator;
        this.supported.websockets = 'WebSocket' in window;
        this.supported.webworkers = 'Worker' in window;
        this.supported.applicationCache = 'applicationCache' in window;

        // CSS 3
        var dummy = document.createElement('div').style;
        this.supported.borderRadius = 'borderRadius' in dummy;
        this.supported.boxShadow = 'boxShadow' in dummy;
        this.supported.transform = 'transform' in dummy;
        this.supported.transition = 'transition' in dummy;

        // 觸控
        this.supported.touch = 'ontouchstart' in window;
        this.supported.multiTouch = this.supported.touch &&
            navigator.maxTouchPoints > 1;

        return this.supported;
    },

    // 漸進增強 helper
    when: function(feature, callback) {
        if (this.supported[feature]) {
            callback();
        }
    }
};

FeatureDetect.detect();
```

## 漸進增強原則

漸進增強（Progressive Enhancement）是一種設計策略：

```
漸進增強模型：
────────────────

內容層（HTML）     所有瀏覽器都能存取
        ↓
表現層（CSS）      功能增強，裝置适配
        ↓
行為層（JavaScript）互動增強，AJAX
```

### 實作範例

```html
<!-- 內容層：即使 JavaScript 禁用也能使用 -->
<form action="/search" method="get">
  <input type="text" name="q" placeholder="搜尋...">
  <button type="submit">搜尋</button>
</form>

<script>
// 行為層：增強為 AJAX
$(function() {
    var form = $('form');
    form.on('submit', function(e) {
        e.preventDefault();

        var q = form.find('input[name="q"]').val();

        $.getJSON('/api/search', { q: q }, function(results) {
            renderResults(results);
        });
    });
});
</script>
```

## CSS 相容性策略

### 引擎前綴

```css
/* 所有引擎都支援 */
box-shadow: 0 2px 4px rgba(0,0,0,0.3);

/* WebKit (Safari, Chrome, iOS) */
-webkit-border-radius: 8px;

/* Gecko (Firefox) */
-moz-border-radius: 8px;

/* Presto (Opera) */
-o-border-radius: 8px;

/* IE 9+ */
-ms-border-radius: 8px;

/* 標準 */
border-radius: 8px;
```

### 條件註解

```html
<!--[if IE]>
<link rel="stylesheet" href="ie-only.css">
<![endif]-->

<!--[if lt IE 7]>
<link rel="stylesheet" href="ie6.css">
<![endif]-->

<!--[if IEMobile 7]>
<link rel="stylesheet" href="iemobile7.css">
<![endif]-->
```

### 特定瀏覽器樣式

```css
/* WebKit 專用 */
@media screen and (-webkit-min-device-pixel-ratio: 2) {
    .retina-icon {
        background-image: url('icon@2x.png');
    }
}

/* iPhone 特定樣式 */
@media screen and (max-device-width: 480px) {
    .mobile-layout {
        font-size: 16px;
    }
}

/* Android 特定樣式 */
@media screen and (-webkit-min-device-pixel-ratio: 1.5) {
    .hd-screens {
        /* 高解析度樣式 */
    }
}
```

## JavaScript 相容性處理

### 陣列相容性

```javascript
// 取代 Array.prototype.map（舊瀏覽器）
if (!Array.prototype.map) {
    Array.prototype.map = function(callback, thisArg) {
        var result = [];
        for (var i = 0; i < this.length; i++) {
            result[i] = callback.call(thisArg, this[i], i, this);
        }
        return result;
    };
}

// 取代 Array.prototype.filter
if (!Array.prototype.filter) {
    Array.prototype.filter = function(callback, thisArg) {
        var result = [];
        for (var i = 0; i < this.length; i++) {
            if (callback.call(thisArg, this[i], i, this)) {
                result.push(this[i]);
            }
        }
        return result;
    };
}
```

### DOM 相容性

```javascript
// 取代 addEventListener（IE 7）
function addEvent(element, eventType, handler) {
    if (element.addEventListener) {
        element.addEventListener(eventType, handler, false);
    } else if (element.attachEvent) {
        element.attachEvent('on' + eventType, handler);
    }
}

// 取得相對位置（跨瀏覽器）
function getPosition(element) {
    var left = 0;
    var top = 0;

    while (element) {
        left += element.offsetLeft;
        top += element.offsetTop;
        element = element.offsetParent;
    }

    return { left: left, top: top };
}
```

## 測試策略

### 設備矩陣

```
2007 年測試設備矩陣：
────────────────────────────────────────────────────────
裝置           螢幕      瀏覽器           網路
────────────────────────────────────────────────────────
iPhone 1代     3.5"     Safari Mobile    3G/EDGE
HTC TyTN II   2.8"     IE Mobile        3G/EDGE
Palm Treo     2.5"     Blazer           EDGE
Nokia N95     2.8"     Safari (S60)     3G/WiFi
BlackBerry    2.5"     NetFront         EDGE
Samsung       2.2"     Opera Mini       EDGE
────────────────────────────────────────────────────────
```

### 雲端測試服務

2007 年的測試主要依賴：
- 實際設備測試
- 各瀏覽器模擬器
- 手動截圖比對

---

## 結語

2007 年的行動瀏覽器碎片化問題，在 2010 年代隨著 Android 普及和 HTML 5 標準成熟而逐漸緩解。但「破碎的生態系」這個問題從未完全消失——不同螢幕尺寸、不同瀏覽器版本、不同作業系統版本，始終是行動 Web 開發者必須面對的挑戰。

實用的策略：
1. **從最小螢幕開始設計**：先保證核心功能可用
2. **使用相對單位**：em、%、viewport units
3. **漸進增強**：從基本功能出發，逐步添加進階功能
4. **自動化測試**：減少手動測試的負擔

---

## 延伸閱讀

- [Mobile+browser+compatibility+issues+2007](https://www.google.com/search?q=Mobile+browser+compatibility+issues+2007)
- [User+Agent+detection+mobile+browsers](https://www.google.com/search?q=User+Agent+detection+mobile+browsers)
- [Progressive+enhancement+mobile+web](https://www.google.com/search?q=Progressive+enhancement+mobile+web)
- [CSS+ Vendor+Prefixes+history](https://www.google.com/search?q=CSS+vendor+prefixes+history)

---

*本篇文章為「AI 程式人雜誌 2007 年 4 月號」本期焦點系列之一。*