# 前端革命：HTML 5、CSS 3 與 JavaScript

## HTML 5 的進展

### 規格狀態

```markdown
# 2009 年 HTML 5 狀態

- W3C 宣布進入「最後呼籲」階段
- 預計 2010 年正式定案
- 瀏覽器廠商積極實作

新特性：
- <video> 和 <audio>
- <canvas>
- 本地儲存
- Web Workers
- Geolocation
```

## CSS 3 的採用

### 瀏覽器支援

```css
/* 2009 年 CSS 3 支援 */

/* border-radius */
.round {
  -webkit-border-radius: 10px;
  -moz-border-radius: 10px;
  border-radius: 10px;
}

/* box-shadow */
.shadow {
  -webkit-box-shadow: 0 4px 8px rgba(0,0,0,0.3);
  -moz-box-shadow: 0 4px 8px rgba(0,0,0,0.3);
  box-shadow: 0 4px 8px rgba(0,0,0,0.3);
}

/* text-shadow */
.glow {
  text-shadow: 0 0 10px rgba(255,255,255,0.5);
}

/* rgba 顏色 */
.transparent {
  background: rgba(0, 0, 0, 0.5);
}
```

## jQuery 1.4

### 效能提升

```javascript
// jQuery 1.4 效能改進

// DOM 操作快 2-3 倍
$("#element").append("<div>Content</div>");

// 動畫效能提升
$(".box").animate({
  width: "200px",
  height: "200px"
}, 300);

// 新的 API
$.Deferred();
$.when().done();
```

## JavaScript 引擎

```markdown
# 2009 年 JavaScript 引擎

Chrome V8：
- 極速 JavaScript 執行
- 編譯為機器碼
- 記憶體優化

Firefox SpiderMonkey：
-_TRACE 編譯器
- 效能提升

Safari JavaScriptCore：
- 首次引進 JIT
- SquirrelFish Extreme
```

## 結語

2009 年是前端技術的重大轉折點，HTML 5、CSS 3 和更快的 JavaScript 引擎為未來的 Web 應用奠定了基礎。

---

*本篇文章為「AI 程式人雜誌 2009 年 12 月號」焦點系列之一。*