# 主題三：移動 Web 開發

## 行動瀏覽器概況

### 2010 年主要行動瀏覽器

```
行動瀏覽器市佔率（2010年初）：
─────────────────────────────
Safari (iOS)：    ~60%
Android Browser： ~20%
Opera Mini：      ~15%
其他：            ~5%
```

### WebKit 的崛起

WebKit 在 2010 年已成為行動瀏覽器引擎的霸主：

- **iOS Safari**：WebKit (Nitro Engine)
- **Android Browser**：WebKit
- **Chrome Mobile**：WebKit (後來改用 Blink)
- **BlackBerry**：WebKit
- **Nokia S60**：WebKit

```javascript
// 偵測 WebKit 瀏覽器
const isWebKit = 'WebkitAppearance' in document.documentElement.style;
const isMobileSafari = /iPhone|iPad|iPod/.test(navigator.userAgent);
```

## 移動優先開發策略

### 為何需要移動優先

```
響應式設計策略比較：
──────────────────────
Desktop First：      Mobile First：
───────────────      ──────────────
從大螢幕開始        從小螢幕開始
漸進增強到大       漸進增強到大
 CSS 媒體查詢       預設就是行動版
更容易適配桌面     更容易適配桌面
```

### Viewport 設定

```html
<meta name="viewport" content="
  width=device-width,
  initial-scale=1.0,
  maximum-scale=1.0,
  user-scalable=no
">
```

### 行動優先的 CSS

```css
/* 預設（手機）樣式 */
body {
  font-size: 16px;
  padding: 10px;
}

/* 平板 */
@media (min-width: 768px) {
  body {
    font-size: 18px;
    padding: 20px;
  }
}

/* 桌面 */
@media (min-width: 1024px) {
  body {
    font-size: 20px;
    max-width: 1200px;
    margin: 0 auto;
  }
}
```

## 觸控事件處理

### Touch Events API

```javascript
// 基本觸控事件監聽
element.addEventListener('touchstart', (e) => {
  e.preventDefault(); // 防止滾動
  const touch = e.touches[0];
  console.log('Touch start:', touch.clientX, touch.clientY);
});

element.addEventListener('touchmove', (e) => {
  const touch = e.touches[0];
  console.log('Touch move:', touch.clientX, touch.clientY);
});

element.addEventListener('touchend', (e) => {
  console.log('Touch end');
});
```

### 支援滑鼠和觸控

```javascript
// 統一的點擊處理
element.addEventListener('click', handleClick);

// 進階：同時支援觸控和滑鼠
let isTouching = false;

element.addEventListener('touchstart', (e) => {
  isTouching = true;
  handleTouchStart(e);
});

element.addEventListener('touchend', () => {
  isTouching = false;
});

element.addEventListener('mousemove', (e) => {
  if (!isTouching) {
    handleMouseMove(e);
  }
});
```

## CSS 觸控優化

### 禁用文字選擇

```css
.no-select {
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
}
```

### 禁用觸控高亮

```css
.no-tap-highlight {
  -webkit-tap-highlight-color: transparent;
}
```

### 彈性滾動

```css
.native-scroll {
  -webkit-overflow-scrolling: touch;
  overflow-y: scroll;
}
```

### 清除按鈕樣式

```css
button, input, textarea {
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  border-radius: 0;
}
```

## 行動裝置偵測

### JavaScript 偵測

```javascript
const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);

const isAndroid = /Android/i.test(navigator.userAgent);
const isIOS = /iPhone|iPad|iPod/i.test(navigator.userAgent);
```

### 伺服器端偵測

```python
# Python 範例（使用 Flask）
from flask import request

@app.route('/')
def index():
    user_agent = request.headers.get('User-Agent')

    if 'Mobile' in user_agent or 'Android' in user_agent:
        template = 'mobile/index.html'
    else:
        template = 'desktop/index.html'

    return render_template(template)
```

### CSS 媒體查詢

```css
/* 基本媒體查詢 */
@media (max-width: 768px) {
  /* 平板以下 */
}

@media (max-width: 480px) {
  /* 手機 */
}

/* 螢幕解析度 */
@media (-webkit-min-device-pixel-ratio: 2) {
  /* Retina 顯示器 */
}
```

## 效能優化

### 減少記憶體使用

```javascript
// 避免記憶體洩漏
element.addEventListener('touchend', cleanup);

function cleanup() {
  // 移除事件監聽
  element.removeEventListener('touchmove', handleMove);

  // 清除計時器
  clearTimeout(timer);

  // 釋放大型物件
  largeArray = null;
}
```

### 硬體加速

```css
/* 啟用硬體加速 */
.accelerated {
  -webkit-transform: translateZ(0);
  -webkit-backface-visibility: hidden;
}

/* 動畫優化 */
.animated {
  -webkit-transform: translate3d(0, 0, 0);
  -webkit-transition: transform 0.3s;
}
```

### 圖片優化

```html
<!-- 依裝置提供不同圖片 -->
<img src="photo.jpg"
     srcset="photo-small.jpg 480w,
             photo-medium.jpg 768w,
             photo-large.jpg 1200w"
     sizes="(max-width: 480px) 100vw,
            (max-width: 768px) 80vw,
            60vw">
```

## 離線支援

### HTML5 Application Cache

```html
<html manifest="cache.appcache">
...
</html>
```

```cache
# cache.appcache
CACHE MANIFEST
# version 1.0.0

CACHE:
/index.html
/styles.css
/script.js
/logo.png

NETWORK:
/api/*
```

### Web Storage

```javascript
// localStorage
localStorage.setItem('username', 'john');
const username = localStorage.getItem('username');

// sessionStorage（分頁關閉後清除）
sessionStorage.setItem('tempData', 'value');
```

### 線上/離線事件

```javascript
window.addEventListener('online', () => {
  console.log('網路已連線');
  syncData();
});

window.addEventListener('offline', () => {
  console.log('網路已斷線');
  showOfflineMessage();
});
```

## 表單處理

### 行動裝置鍵盤

```html
<!-- 不同的 input 類型觸發不同鍵盤 -->
<input type="text" pattern="[0-9]*">  <!-- 數字鍵盤 -->
<input type="email">                   <!-- email 鍵盤 -->
<input type="url">                      <!-- URL 鍵盤 -->
<input type="tel">                      <!-- 電話鍵盤 -->
```

### 表單驗證

```javascript
// HTML5 原生驗證
input.required = true;
input.pattern = '[A-Za-z]{3}';

// 自訂驗證訊息
input.addEventListener('invalid', (e) => {
  if (input.validity.valueMissing) {
    input.setCustomValidity('此欄位必填');
  }
});

input.addEventListener('input', () => {
  input.setCustomValidity('');
});
```

## 開發工具

### iOS 模擬器

- 包含在 Xcode 中
- 測試 iOS Safari
- 模擬觸控事件
- 檢視 Console

### Android SDK

- Android Emulator
- DDMS 效能監控
- Chrome DevTools 遠端偵錯

### 遠端偵錯

```javascript
// 在手機上开启 USB 偵錯
// 連接電腦後，在 Chrome DevTools 中選擇設備
```

---

## 結論

移動 Web 開發在 2010 年正在經歷快速發展。WebKit 的統一、viewport 標準的確立、以及 HTML5 API 的成熟，讓開發者能夠建立接近原生應用體驗的 Web 應用。

關鍵要點：
1. 使用 WebKit 為基礎的瀏覽器特性
2. 實施移動優先的響應式設計
3. 正確處理觸控事件
4. 優化效能以適應行動裝置
5. 提供離線支援

---

*本期文章到此結束。*