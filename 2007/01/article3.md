# jQuery 席捲前端：JavaScript 庫的崛起

## 前言

2007 年 1 月，jQuery 1.0 正式發布。這款由 John Resig 開發的 JavaScript 庫，以其簡潔的語法和強大的功能，迅速成為前端開發的必備工具。

## jQuery 的誕生背景

### 混亂的 JavaScript 開發

2007 年的 JavaScript 開發面臨諸多挑戰：

```
┌────────────────────────────────────────────────────────┐
│          2007 年 JavaScript 開發的痛點                  │
├────────────────────────────────────────────────────────┤
│                                                        │
│  1. 瀏覽器相容性                                       │
│     └─ IE vs Firefox vs Safari 行為差異                │
│                                                        │
│  2. DOM 操作繁瑣                                       │
│     └─ document.getElementById("x").style.y = "z"    │
│                                                        │
│  3. 事件處理複雜                                       │
│     └─ attachEvent vs addEventListener                │
│                                                        │
│  4. AJAX 実装困難                                      │
│     └─ XMLHttpRequest 各地不同                        │
│                                                        │
│  5. 動畫效果難以實現                                   │
│     └─ 需配合 CSS 或外掛                               │
│                                                        │
└────────────────────────────────────────────────────────┘
```

### John Resig 的願景

John Resig 在 2006 年創建了 jQuery，並在 2007 年 1 月發布 1.0 正式版：

```javascript
// jQuery 的核心理念：「寫得更少，做得更多」

// 選擇器
$("#myId")           // ID 選擇
$(".myClass")         // 類別選擇
$("div > p")          // 組合選擇

// 鏈式語法
$("div")
  .addClass("highlight")
  .css("color", "red")
  .hide("slow");
```

## jQuery 1.0 的核心功能

### 1. CSS 選擇器引擎

jQuery 實現了類似 CSS 的選擇器語法：

```javascript
// 基本選擇器
$("*")                // 所有元素
$("div")              // 標籤選擇器
$("#header")          // ID 選擇器
$(".featured")        // 類別選擇器
$("div, p, span")     // 多重選擇

// 屬性選擇器
$("a[hreflang='en']")
$("img[alt!='product']")
$("input[name*='user']")

// 層級選擇器
$("ul > li")
$("div p")
$("prev + next")
$("prev ~ siblings")
```

### 2. DOM 操作

```javascript
// 遍歷與操作
$("ul")
  .find("li")           // 查找
  .eq(2)                // 取第三個
  .addClass("active")   // 新增類別
  .text("New Text")     // 改變文字
  .html("<strong>Bold</strong>")  // HTML

// 新增與移除
$("<li>New Item</li>").appendTo("ul")
$(".old").remove()
$(".item").clone().appendTo(".container")
```

### 3. 事件處理

```javascript
// 簡潔的事件處理
$("#button").click(function() {
  alert("Clicked!");
});

$("a").hover(
  function() { $(this).addClass("hover"); },
  function() { $(this).removeClass("hover"); }
);

// 委派事件
$("ul").delegate("li", "click", function() {
  $(this).toggleClass("active");
});
```

### 4. AJAX 支援

```javascript
// jQuery AJAX 語法
$.ajax({
  url: "/api/data",
  type: "POST",
  data: { name: "John", age: 30 },
  success: function(response) {
    $("#result").html(response);
  },
  error: function(xhr) {
    alert("Error: " + xhr.status);
  }
});

// 簡化版本
$.get("/api/data", function(data) {
  console.log(data);
});

$.post("/api/submit", { data: "value" });
```

### 5. 動畫效果

```javascript
// 內建動畫
$(".box").fadeIn()
$(".box").fadeOut()
$(".box").slideUp()
$(".box").slideDown()
$(".box").animate({
  left: "+=100",
  opacity: 0.5
}, 300);
```

## jQuery 的設計哲學

### 核心理念

```
┌────────────────────────────────────────────────────────┐
│            jQuery 設計哲學                              │
├────────────────────────────────────────────────────────┤
│                                                        │
│  1. 簡潔性                                              │
│     └─ 一行程式碼達成目的                               │
│                                                        │
│  2. 一致性                                              │
│     └─ 所有方法返回 jQuery 物件，支援鏈式調用          │
│                                                        │
│  3. 擴展性                                              │
│     └─ 插件系統讓任何人都能擴展功能                     │
│                                                        │
│  4. 瀏覽器相容                                          │
│     └─ 統一是個不一致的瀏覽器行為                      │
│                                                        │
└────────────────────────────────────────────────────────┘
```

### 鏈式語法

```javascript
// 鏈式調用的威力
$("#menu")
  .addClass("active")
  .find("a")
  .eq(0)
  .click(function() {
    $(this)
      .addClass("selected")
      .next()
      .show();
  })
  .end()
  .find("span")
  .text("Menu");
```

## 插件生態系統

### 2007 年的 jQuery 插件

jQuery 的插件系統是其成功的關鍵之一：

```javascript
// 熱門插件示例

// UI 類
// - jQuery UI (官方 UI 庫)
// - Interface (影像特效)
// - Flame（視覺效果）

// 表單類
// - Validation (表單驗證)
// - Autocomplete (自動完成)
// - Globalize (國際化)

// 媒體類
// - jPlayer (影片/音訊播放)
// - FancyBox (燈箱效果)

// 實用類
// - DataTables (表格外掛)
// - FullCalendar (日曆)
```

### 插件開發範例

```javascript
// 建立 jQuery 插件
$.fn.greenify = function() {
  this.css("color", "green");
  return this;  // 返回 jQuery 物件以支援鏈式
};

$.fn.londonify = function(options) {
  var settings = $.extend({
    color: "red",
    fontSize: "20px"
  }, options);

  return this.css({
    color: settings.color,
    fontSize: settings.fontSize
  });
};

// 使用插件
$("a").greenify();
$("p").londonify({ fontSize: "30px" });
```

## jQuery 與其他框架的比較

### 2007 年的 JavaScript 框架生態

```python
# 2007 年主要 JavaScript 框架對比
FRAMEWORKS = {
    "jQuery": {
        "優點": "語法簡潔、學習曲線低、插件豐富",
        "缺點": "非完整框架、需自行組合元件",
        "大小": "~18KB (gzipped)"
    },
    "Prototype": {
        "優點": "類別系統、Ruby 語感",
        "缺點": "DOM 擴展爭議",
        "大小": "~30KB"
    },
    "Dojo": {
        "優點": "完整工具箱、Widget 系統",
        "缺點": "學習曲線較高",
        "大小": "~80KB+"
    },
    "MooTools": {
        "優點": "模組化、Class 繼承",
        "缺點": "語法独特",
        "大小": "~25KB"
    },
    "YUI": {
        "優點": "Yahoo 支援、完整文檔",
        "缺點": "較重量級",
        "大小": "~90KB+"
    }
}
```

## jQuery 對前端開發的影響

### 降低門檻

jQuery 使得非專業 JavaScript 開發者也能使用 Ajax 和 DOM 操作：

```
┌────────────────────────────────────────────────────────┐
│          jQuery 對前端開發的影響                        │
├────────────────────────────────────────────────────────┤
│                                                        │
│  1. 民主化 JavaScript 開發                            │
│     └─ 任何人都能寫互動效果                            │
│                                                        │
│  2. 加速 AJAX 應用普及                                 │
│     └─ 複雜的 AJAX 變得簡單                            │
│                                                        │
│  3. 推動標準化                                         │
│     └─ 選擇器成為事實標準                               │
│                                                        │
│  4. 催生前端工程師角色                                  │
│     └─ 專業的前端開發需求                              │
│                                                        │
│  5. 為未來框架奠基                                     │
│     └─ 影響了 Angular, React 等                        │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## 結論

jQuery 的出現徹底改變了前端開發的面貌。它不僅簡化了 JavaScript 編程，更催生了一個繁榮的插件生態系統。

「 Write Less, Do More」—— 這句口號精確地總結了 jQuery 的價值。

---

## 延伸閱讀

- [jQuery 1.0 發布](https://www.google.com/search?q=jQuery+1.0+released+January+2007)
- [jQuery 官方網站](https://www.google.com/search?q=jQuery+official+site)
- [JavaScript 框架比較](https://www.google.com/search?q=JavaScript+library+comparison+2007)

---

*本篇文章為「AI 程式人雜誌 2007 年 1 月號」文章集錦系列。*