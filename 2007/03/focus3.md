# JavaScript 的重生：AJAX 時代的主角

## 前言

2007 年，JavaScript 從一個被低估的客戶端腳本語言，成長為 Web 開發的核心語言。

## JavaScript 的演變

### 從玩具到語言

```
┌────────────────────────────────────────────────────────┐
│            JavaScript 認知轉變                          │
├────────────────────────────────────────────────────────┤
│                                                        │
│  早期（1995-2005）：                                  │
│  - 被視為「玩具語言」                                  │
│  - 主要用於簡單的表單驗證                              │
│  - 各瀏覽器實作不一致                                  │
│                                                        │
│   AJAX 時代（2005-2007）：                            │
│  - XMLHttpRequest 普及                                │
│  - jQuery 簡化 DOM 操作                               │
│  - 成為全端語言的可能                                  │
│                                                        │
│  現代（2009+）：                                      │
│  - V8 引擎大幅效能提升                                │
│  - Node.js 服務端 JavaScript                          │
│  - SPA 應用框架                                       │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## jQuery 的影響

```javascript
// jQuery 簡化了 JavaScript 開發
//  DOM 操作
$("#myId").addClass("highlight");
$("div.content").append("<p>New content</p>");

//  AJAX
$.get("/api/data", function(response) {
    console.log(response);
});

//  事件處理
$("button").click(function() {
    alert("Clicked!");
});
```

## JavaScript 的未來

2007 年，JavaScript 正在經歷重生，為日後的爆發奠定基礎。

---

*本篇文章為「AI 程式人雜誌 2007 年 3 月號」本期焦點系列文章。*