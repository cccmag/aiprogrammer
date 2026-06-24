# 主題六：YUI 與 Yahoo

## 企業級 JavaScript 方案

Yahoo! User Interface Library (YUI) 是 Yahoo! 在 2007 年發布的一套企業級 JavaScript 框架。YUI 以其完善的文件、豐富的元件庫和嚴格的代碼品質，成為大型 Web 應用開發的熱門選擇。

## YUI 的設計理念

YUI 的核心設計理念是「模組化」和「可組合」：

```javascript
// YUI 3 的 Seed 載入
YUI().use("node", "event", function(Y) {
    Y.one("#demo").set("text", "Hello YUI!");
    Y.one("#demo").on("click", function(e) {
        alert("Clicked!");
    });
});
```

## YUI 2 與 YUI 3

2007 年的 YUI 正處於 2.x 向 3.x 過渡的時期：

### YUI 2 (2007 年主流版本)

```javascript
// DOM 操作
YAHOO.util.Dom.get("myId");
YAHOO.util.Dom.addClass("myId", "highlight");
YAHOO.util.Dom.setStyle("myId", "opacity", 0.5);

// 事件處理
YAHOO.util.Event.on("button", "click", function(e) {
    YAHOO.util.Event.preventDefault(e);
});
```

### YUI 3 (新興版本)

```javascript
YUI().use("node", "event", "anim", function(Y) {
    // 鏈式操作
    Y.one("#container")
        .addClass("active")
        .setHTML("<p>New content</p>");

    // 動畫
    new Y.Anim({
        node: "#myElement",
        to: { opacity: 0 },
        duration: 0.5
    }).run();
});
```

## YUI 元件類別

### 萬用資料結構 (DataTable)

```javascript
YAHOO.widget.DataTable Formatter:
var myDataTable = new YAHOO.widget.DataTable(
    "container",
    [
        { key: "id", label: "ID", sortable: true },
        { key: "name", label: "Name", sortable: true },
        { key: "email", label: "Email" }
    ],
    new YAHOO.util.DataSource(yahooDataSource, {
        responseType: YAHOO.util.DataSource.TYPE_JSON,
        responseSchema: {
            resultsList: "records",
            fields: ["id", "name", "email"]
        }
    }),
    {
        caption: "使用者列表",
        paginator: new YAHOO.widget.Paginator({
            rowsPerPage: 10
        })
    }
);
```

### 日曆元件

```javascript
var calendar = new YAHOO.widget.Calendar("calendarContainer", {
    pages: 2,
    mindate: "1/1/2007",
    maxdate: "12/31/2007"
});

calendar.selectEvent.subscribe("click", function(e, args) {
    var date = args[0];
    alert("Selected: " + date);
});

calendar.render();
```

### 自動完成

```javascript
var oAutoComp = new YAHOO.widget.AutoComplete("inputContainer", "suggestionContainer", dataSource, {
    autoHighlight: true,
    typeAhead: true,
    minQueryLength: 2,
    queryDelay: 300,
    resultTypeList: false
});

oAutoComp.formatResult = function(oResultData, sQuery, sResultMatch) {
    return "<b>" + sResultMatch + "</b>";
};
```

### 面板和對話框

```javascript
var panel = new YAHOO.widget.Panel("panelContainer", {
    width: "400px",
    height: "300px",
    modal: true,
    visible: true,
    constraintoviewport: true
});

panel.setHeader("標題");
panel.setBody("<p>內容區域</p>");
panel.setFooter("底部");
panel.render(document.body);

panel.show();
```

### TabView

```javascript
var tabView = new YAHOO.widget.TabView("tabContainer");

tabView.addTab(new YAHOO.widget.Tab({
    label: "第一頁",
    content: "<p>第一頁內容</p>",
    active: true
}));

tabView.addTab(new YAHOO.widget.Tab({
    label: "第二頁",
    content: "<p>第二頁內容</p>"
}));
```

## YUI 的工具庫

### YAHOO.util.Dom

```javascript
// 取得元素
YAHOO.util.Dom.get("id");           // ID
YAHOO.util.Dom.getElementsByClassName("class"); // 類別

// 類別操作
YAHOO.util.Dom.hasClass(el, "active");
YAHOO.util.Dom.addClass(el, "active");
YAHOO.util.Dom.removeClass(el, "active");
YAHOO.util.Dom.toggleClass(el, "active");

// 位置和尺寸
YAHOO.util.Dom.getXY(el);      // [x, y]
YAHOO.util.Dom.getRegion(el);  // { top, right, bottom, left }
YAHOO.util.Dom.getStyle(el, "height"); // "100px"

// 獲取子/父元素
YAHOO.util.Dom.getChildren(el);
YAHOO.util.Dom.getParent(el);
```

### YAHOO.util.Event

```javascript
// 添加事件監聽
YAHOO.util.Event.on("button", "click", handler);

// 一次性事件
YAHOO.util.Event.on("button", "click", handler, obj, true);

// 鍵盤事件
YAHOO.util.Event.on(document, "keydown", function(e) {
    if (e.keyCode === 13) {
        // Enter 鍵
    }
});

// 阻止預設行為和冒泡
YAHOO.util.Event.preventDefault(e);
YAHOO.util.Event.stopPropagation(e);
```

### YAHOO.util.Connect

```javascript
// AJAX 請求
var callback = {
    success: function(o) {
        var data = YAHOO.util.Json.parse(o.responseText);
        // 處理資料
    },
    failure: function(o) {
        alert("請求失敗");
    }
};

YAHOO.util.Connect.asyncRequest("GET", "data.json", callback);

// POST 請求
YAHOO.util.Connect.asyncRequest("POST", "submit.php", callback, "name=John&age=30");
```

### YAHOO.util.Anim

```javascript
// 屬性動畫
var anim = new YAHOO.util.Anim("element", {
    opacity: { to: 0 },
    left: { to: 100, unit: "px" }
}, 1, YAHOO.util.Easing.easeOut);

anim.onComplete.subscribe(function() {
    console.log("Animation complete");
});

anim.animate();
```

## YUI 的 CSS 框架

YUI 提供了一套完整的 CSS 基礎架構：

```html
<!-- YUI CSS Reset -->
<link rel="stylesheet" href="http://yui.yahooapis.com/2.5.0/build/reset/reset-min.css">

<!-- YUI Fonts -->
<link rel="stylesheet" href="http://yui.yahooapis.com/2.5.0/build/fonts/fonts-min.css">

<!-- YUI Grids -->
<link rel="stylesheet" href="http://yui.yahooapis.com/2.5.0/build/grids/grids-min.css">
```

### YUI Grids

```html
<div class="yui-g">
    <div class="yui-u first">
        <!-- 2/3 寬度 -->
    </div>
    <div class="yui-u">
        <!-- 1/3 寬度 -->
    </div>
</div>
```

## Yahoo! 的應用案例

Yahoo! 將 YUI 應用於多個產品：

1. **Yahoo! Mail** -- 使用 DataTable 和 DOM 操作
2. ** Flickr** -- 使用 Animation 和 Event
3. ** Yahoo! Finance** -- 使用 Charting 和 DataTable

## 優缺點分析

### 優點

- **完善的文件** -- Yahoo! 提供了詳盡的文件和範例
- **穩定的效能** -- 經過 Yahoo! 內部產品驗證
- **豐富的元件** -- 涵蓋企業應用的各個方面
- **良好的支援** -- Yahoo! 社群和技術支援

### 缺點

- **學習曲線** -- API 較為複雜
- **檔案較大** -- 完整版約 300KB
- **語法較繁瑣** -- 不如 jQuery 簡潔

## 結語

YUI 是企業級 Web 應用的可靠選擇。雖然學習曲線較陡，但其完善的文件、豐富的元件庫和 Yahoo! 的品質保證，使其在 2007 年的 JavaScript 框架生態中佔有重要地位。

---

*延伸閱讀：*
- [YUI 官方網站](https://developers.google.com/search/?q=yui+library+official)
- [YUI 文件](https://developers.google.com/search/?q=yui+documentation)