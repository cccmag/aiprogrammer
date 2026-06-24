# HTML 5 規格接近完成：Web 標準新時代

## 前言

2009 年 7 月，W3C 宣布 HTML 5 規格進入「最後呼籲」（Last Call）階段，這是 HTML 5 正式定案前的重要里程碑。經過多年的開發，HTML 5 終於從一個遠大的願景，變成了一個即將可用的標準。

## HTML 5 的誕生背景

### HTML 4 的局限性

HTML 4 於 1999 年發布，雖然經歷了多年的使用，但在 2000 年代後期已經顯現出諸多不足：

1. **語義不足**：\<div\> 和 \<span\> 無法表達結構語義
2. **多媒體需要外掛**：音訊和影片需要 Flash 或 Silverlight
3. **無離線支援**：Web 應用無法在離線狀態使用
4. **繪圖能力有限**：無法在瀏覽器中直接繪圖
5. **無本地儲存**：只能依賴 cookies

### WHATWG 的貢獻

HTML 5 的發展始於 2004 年，當時由 Apple、Mozilla 和 Opera 組成的 WHATWG（Web Hypertext Application Technology Working Group）開始制定新的 HTML 規格。

```
HTML 5 發展歷程：
2004年：WHATWG 開始制定 Web Applications 1.0
2007年：W3C 採用 HTML 5 作為正式工作項目
2008年：W3C 發布 First Public Working Draft
2009年：HTML 5 進入 Last Call 階段
預計2010年：W3C Recommendation
```

## HTML 5 的核心新特性

### 1. 語義化標籤

```html
<!-- 過去 -->
<div id="header">...</div>
<div id="nav">...</div>
<div id="main">...</div>
<div id="footer">...</div>

<!-- HTML 5 -->
<header>...</header>
<nav>...</nav>
<main>...</main>
<article>...</article>
<section>...</section>
<aside>...</aside>
<footer>...</footer>
```

### 2. 影片與音訊

```html
<!-- 影片標籤 -->
<video src="movie.mp4" controls width="640" height="480">
  您的瀏覽器不支援 video 標籤
</video>

<!-- 音訊標籤 -->
<audio src="music.mp3" controls>
  您的瀏覽器不支援 audio 標籤
</audio>
```

### 3. Canvas 繪圖

```html
<canvas id="myCanvas" width="800" height="600">
  您的瀏覽器不支援 canvas
</canvas>

<script>
var canvas = document.getElementById('myCanvas');
var ctx = canvas.getContext('2d');
ctx.fillStyle = '#3498db';
ctx.fillRect(10, 10, 100, 100);
</script>
```

### 4. 本地儲存

```javascript
// localStorage
localStorage.setItem('name', 'John');
var name = localStorage.getItem('name');

// sessionStorage
sessionStorage.setItem('token', 'abc123');
```

### 5. 離線 Web 應用

```html
<html manifest="cache.manifest">
```

```text
CACHE MANIFEST
# version 1.0
/index.html
/style.css
/script.js
/images/logo.png
```

### 6. Geolocation API

```javascript
if (navigator.geolocation) {
  navigator.geolocation.getCurrentPosition(
    function(position) {
      console.log(position.coords.latitude,
                  position.coords.longitude);
    },
    function(error) {
      console.log('Error:', error.message);
    }
  );
}
```

### 7. Web Workers

```javascript
// main.js
var worker = new Worker('worker.js');
worker.postMessage({cmd: 'start', data: 1000});
worker.onmessage = function(e) {
  console.log('Result:', e.data);
};

// worker.js
self.onmessage = function(e) {
  if (e.data.cmd === 'start') {
    var result = compute(e.data.data);
    self.postMessage(result);
  }
};
```

## 瀏覽器支援状况（2009年）

| 特性 | Firefox | Safari | Chrome | Opera |
|------|---------|--------|--------|-------|
| \<video\> | 3.5+ | 3.0+ | 3.0+ | 10.5+ |
| \<audio\> | 3.5+ | 3.0+ | 3.0+ | 10.5+ |
| \<canvas\> | 3.0+ | 3.0+ | 1.0+ | 10.0+ |
| localStorage | 3.5+ | 4.0+ | 1.0+ | 10.5+ |
| Geolocation | 3.5+ | 4.0+ | 5.0+ | 10.5+ |
| Web Workers | 3.5+ | 4.0+ | 1.0+ | 10.0+ |
| Offline Apps | 3.5+ | 4.0+ | 1.0+ | 10.5+ |

## HTML 5 的影響

### 對 Web 開發的影響

1. **減少對外掛的依賴**：Flash 的地位受到挑戰
2. **更豐富的互動**：Canvas 遊戲、動畫
3. **更好的行動支援**：觸控、離線、分頁推送
4. **更強大的 Web 應用**：本地儲存、背景處理

### 對標準的影響

```
HTML 5  vs  HTML 4：

HTML 4：
- 一個龐大的單一規格
- 規格制定後很難修改
- 瀏覽器廠商各自為政

HTML 5：
- 模組化設計
- 持續演進
- 更開放的制定過程
```

## 結語

HTML 5 不僅是 HTML 的新版本，更代表了 Web 應用的未來方向。2009 年 HTML 5 進入最後呼籲階段，預示著一個新的 Web 時代即將來臨。

## 延伸閱讀

- [W3C HTML 5 規格](https://www.google.com/search?q=W3C+HTML5+specification+2009)
- [HTML 5 與 HTML 4 的差異](https://www.google.com/search?q=HTML5+vs+HTML4+differences)
- [HTML 5 瀏覽器支援狀況](https://www.google.com/search?q=HTML5+browser+compatibility+2009)
- [HTML 5 示範與範例](https://www.google.com/search?q=HTML5+demos+2009)

---

*本篇文章為「AI 程式人雜誌 2009 年 7 月號」文章系列之一。*