# 前端工具鏈 Modernizr

## Modernizr 簡介

Modernizr 是一個 JavaScript 函式庫，用於偵測瀏覽器對 HTML5 和 CSS3 功能的支持情況。

## 基本用法

### 包含 Modernizr

```html
<script src="modernizr-1.6.min.js"></script>
```

### 偵測結果

```javascript
// 結果會添加到 <html> 元素的類別
if (Modernizr.geolocation) {
    // 支援地理位置
} else {
    // 不支援，使用 fallback
}
```

## HTML5 功能偵測

### 影片

```javascript
if (Modernizr.video) {
    // 支援 <video>
    var format = Modernizr.video.mp4 ? 'mp4' : 'webm';
    console.log('Supported format:', format);
} else {
    // fallback: Flash
}
```

### 音訊

```javascript
if (Modernizr.audio) {
    var format = Modernizr.audio.mp3 ? 'mp3' :
                 Modernizr.audio.ogg ? 'ogg' : '';
}
```

### 表單

```javascript
if (Modernizr.inputtypes.date) {
    // 支援 date input
} else {
    // 使用 jQuery UI Datepicker
}
```

## CSS3 功能偵測

### 圓角

```javascript
if (Modernizr.borderradius) {
    $('.box').addClass('rounded');
} else {
    // 使用背景圖片
}
```

### 陰影

```javascript
if (Modernizr.boxshadow) {
    $('.card').css('box-shadow', '0 2px 4px rgba(0,0,0,0.3)');
} else {
    // 使用 border-image 或放棄效果
}
```

### 動畫

```javascript
if (Modernizr.cssanimations) {
    $('.spinner').addClass('rotate');
} else {
    // 使用 JavaScript 動畫
}
```

### Flexbox

```javascript
if (Modernizr.flexbox) {
    // 使用彈性盒子
    $('.container').css('display', 'flex');
} else {
    // 使用 float 或 table
}
```

## 使用 featureDetect 類別

Modernizr 會在 <html> 添加類別：

```html
<!-- 支援的 -->
<html class="video mp4 webm">
<!-- 不支援的 -->
<html class="no-video no-webm">
```

### CSS 中的使用

```css
.box {
    /* 預設樣式（fallback） */
    width: 200px;
    height: 200px;
}

.boxshadow .box {
    /* Modernizr 支援的增強 */
    box-shadow: 0 2px 4px rgba(0,0,0,0.3);
}

.no-boxshadow .box {
    /* 使用邊框模擬陰影 */
    border: 1px solid #ccc;
}
```

## Modernizr.load

### 條件載入

```javascript
Modernizr.load([
    {
        test: Modernizr.geolocation,
        yep: 'geo.js',
        nope: 'geo-fallback.js'
    },
    {
        test: Modernizr.canvas,
        yep: 'canvas.js',
        nope: 'no-canvas.js'
    }
]);
```

### 載入外掛

```javascript
Modernizr.load({
    test: Modernizr.hashchange,
    yep: 'js/jquery.ba-hashchange.min.js'
});
```

## 自訂偵測

```javascript
Modernizr.testStyles('#modernizr { }', function(elem, rule) {
    Modernizr.addTest('myfeature', function() {
        return typeof rule !== 'undefined';
    });
});

if (Modernizr.myfeature) {
    console.log('My feature is supported!');
}
```

## 結論

Modernizr 使得漸進增強（Progressive Enhancement）和優雅降級（Graceful Degradation）變得簡單，幫助開發者充分利用新功能的同時保持向後相容。

---

**延伸閱讀**

- [前端開發的未來](focus7.md)
- [Modernizr+official](https://www.google.com/search?q=Modernizr+official+site)