# WebKit 成為行動瀏覽器霸主

## WebKit 的崛起

2010 年，WebKit 已成為行動瀏覽器引擎的明確領導者。這個由 Apple 發起的開源專案，正在重塑網頁瀏覽器的格局。

```
WebKit 市佔率（2010年初）：
──────────────────────────
iOS Safari：    ~60% 行動瀏覽�
Android Browser： ~25% 行動瀏覽器
其他：           ~15%（包括 Symbian、WebOS）
桌面 Safari：    少量市佔
```

## WebKit 歷史

### 專案起源

```
WebKit 發展時間線：
──────────────────
1998:  KHTML 專案啟動（KDE）
2001:  Apple 分支 KHTML，建立 WebKit
2003:  Safari 發布，WebKit 首次亮相
2005:  WebKit 開源
2008:  Android 採用 WebKit
2010:  WebKit 成為行動瀏覽器標準
```

### 與其他引擎的比較

```
瀏覽器引擎比較：
──────────────────
 Trident：   IE（桌面為主，逐步淘汰）
 Gecko：     Firefox（桌面为主）
 WebKit：    Safari、Chrome（桌面+行動）
 Blink：     Chrome 28+（WebKit 分支，2013）
```

## WebKit 架構

### 核心元件

```
WebKit 架構：
──────────────────
JavaScriptCore：  JavaScript 引擎
WebCore：         渲染引擎、DOM
UIProcess：       UI 程序
```

### 渲染流程

```
HTML → 解析 → DOM Tree → Render Tree → 佈局 → 繪製
                                          ↓
                                     Compositing → 顯示
```

## WebKit 特有的前綴屬性

### 常見前綴

```
WebKit 前綴屬性（2010年）：
──────────────────────────
-webkit-transform：    變形
-webkit-transition：   過渡動畫
-webkit-animation：     關鍵幀動畫
-webkit-gradient：     漸層
-webkit-border-radius： 圓角
-webkit-box-shadow：   陰影
-webkit-appearance：    外觀
-webkit-tap-highlight-color： 觸控高亮
```

### 使用範例

```css
/* WebKit 特有的圓角和漸層 */
.gradient-box {
  background: -webkit-gradient(
    linear,
    left top,
    left bottom,
    from(#ff0000),
    to(#0000ff)
  );
  -webkit-border-radius: 10px;
  -webkit-box-shadow: 0 2px 4px rgba(0,0,0,0.3);
}

/* 變形動畫 */
.animated {
  -webkit-transition: transform 0.3s;
}

.animated:hover {
  -webkit-transform: scale(1.1);
}

/* 動畫 */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.animated {
  -webkit-animation: fadeIn 1s;
}
```

## 行動 WebKit 特性

### 觸控支援

```javascript
// WebKit 觸控事件
element.addEventListener('touchstart', handler, false);
element.addEventListener('touchmove', handler, false);
element.addEventListener('touchend', handler, false);
```

### 硬體加速

```css
/* WebKit 硬體加速 */
.accelerated {
  -webkit-transform: translateZ(0);
  -webkit-backface-visibility: hidden;
  -webkit-perspective: 1000;
}
```

### WebKit 特有的 JavaScript API

```javascript
// WebKit 特有的 API

// 資料夾操作
window.webkitRequestFileSystem(
  PERSISTENT,  // 或 TEMPORARY
  1024 * 1024, // 位元組
  onSuccess,
  onError
);

// 離線通知
window.webkitNotifications.requestPermission();

// 位置資訊（已標準化）
navigator.geolocation.getCurrentPosition();

// 裝置方向
window.addEventListener('deviceorientation', (e) => {
  console.log('Alpha:', e.alpha);
  console.log('Beta:', e.beta);
  console.log('Gamma:', e.gamma);
});

// 電池 API
navigator.battery.addEventListener('chargingchange', () => {
  console.log('充電中:', navigator.battery.charging);
});
```

## WebKit vs 標準

### 領先標準的特性

```
WebKit 領先實現的功能（2010年）：
───────────────────────────────
CSS Transforms：   領先支援
CSS Animations：   領先支援
Touch Events：     領先支援
WebSocket：        早期支援
Web Storage：      完整支援
Application Cache： 完整支援
```

### 標準化歷程

```
功能 → WebKit 實現 → 其他瀏覽器跟進 → 標準化
──────────────────────────────────────────────
animation：  2009 Safari → 2011 Firefox → 2012 標準
transition： 2009 Safari → 2011 Firefox → 2012 標準
touch：      2009 iOS → 2010 Android → 2013 標準
```

## 開發者體驗

### 一致性優勢

```
WebKit 統一的優點：
──────────────────
iOS Safari：       穩定、效能好
Android Browser：  廣泛支援
桌面 Safari：      與行動一致
BlackBerry：       也用 WebKit
```

### 調試工具

```javascript
// WebKit 遠端偵錯（後來發展）
// 2010 年較少工具，主要依靠：
console.log();           // 主控台輸出
alert();                 // 彈出訊息
document.title = '...';  // 修改標題列
```

### 效能優化

```javascript
// WebKit 特有的效能 API
window.performance;  // 效能監控

// 記憶體使用（WebKit 特有）
console.webkitReportExceptionCount();
```

## 行動瀏覽器市佔

### 2010 年市佔率

```
行動瀏覽器市佔率（2010年）：
───────────────────────────
Safari (iOS)：    60%
Android Browser： 20%
Opera Mini：      10%
黑莓瀏覽器：       5%
其他：            5%
```

### 趨勢變化

```
市佔率變化趨勢：
──────────────────
2009:  Safari 50%, Android 10%, Opera 20%
2010:  Safari 55%, Android 20%, Opera 15%
2011:  Safari 50%, Android 30%, Opera 10%
2012:  Safari 40%, Android 40%, Chrome 10%
```

## WebKit 的影響

```
WebKit 的歷史貢獻：
──────────────────
1. 推動 HTML5/CSS3 標準化
2. 提升瀏覽器效能
3. 統一是動瀏覽器體驗
4. 加速 Web 創新
5. 為 Chromium/Blink 奠定基礎
```

---

## 結論

WebKit 在 2010 年確定了其在行動瀏覽器領域的霸主地位。統一的引擎帶來了更一致的 Web 體驗，也加速了 Web 標準的發展。

雖然後來 Chrome 分支出 Blink，但 WebKit 的影響將持續存在於 Safari 和許多行動瀏覽器中。

---

*本期文章到此結束。*