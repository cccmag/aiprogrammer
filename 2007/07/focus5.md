# 主題五：Dojo Toolkit

## 全方位 JavaScript 框架

Dojo Toolkit 是 2007 年企業級 JavaScript 應用的首選方案。不同於 jQuery 的專注簡潔，Dojo 提供了一套完整的企業級解決方案，涵蓋從底層 DOM 操作到高層 UI 元件、資料存取、動畫效果、動畫圖表等各個方面。

## Dojo 的模組化架構

Dojo 採用了類似 Java 的套件和模組組織方式：

```javascript
// 引入核心模組
dojo.require("dojo.ready");

// 引入 UI 元件
dojo.require("dijit.form.Button");
dojo.require("dijit.Dialog");
dojo.require("dijit.Tree");

// 引入資料相關
dojo.require("dojo.data.ItemFileReadStore");

// 引入動畫
dojo.require("dojo.fx");
```

## DOM 操作

```javascript
// 基本 DOM 操作
dojo.query(".container > div")  // CSS 選擇器
    .addClass("highlight")
    .onclick(function(e) {
        console.log("Clicked:", e.target);
    });

// 查詢引擎
var nodes = dojo.query("#container p.special");

// DOM 屬性操作
dojo.setAttr(node, "src", "image.jpg");
dojo.getAttr(node, "alt");
dojo.removeAttr(node, "disabled");
```

## 事件處理

```javascript
// 連接事件
dojo.connect(dojo.byId("myButton"), "onclick", function(e) {
    console.log("Button clicked!");
});

// 訂閱/發布主題
dojo.subscribe("/app/start", function(data) {
    console.log("App started:", data);
});
dojo.publish("/app/start", [{ message: "Hello" }]);

// 事件委託
dojo.query(".container")
    .connect("click", ".item", function(e) {
        dojo.stopEvent(e);
        console.log("Item clicked:", this);
    });
```

## DojoX 擴展元件

DojoX 是 Dojo 的擴展庫，提供更多高級元件：

### 圖表元件

```javascript
// 引入 Charting
dojo.require("dojox.charting.Chart2D");
dojo.require("dojox.charting.action2d.Highlight");
dojo.require("dojox.charting.action2d.Magnify");

var chart = new dojox.charting.Chart2D("chartNode");
chart.addPlot("default", {
    type: "Lines",
    markers: true
});
chart.addSeries("Series 1", [1, 2, 3, 4, 5]);
chart.addSeries("Series 2", [5, 4, 3, 2, 1]);
chart.render();
```

### Grid 資料網格

```javascript
dojo.require("dojox.grid.DataGrid");
dojo.require("dojo.data.ItemFileWriteStore");

var store = new dojo.data.ItemFileWriteStore({
    url: "data.json"
});

var grid = new dojox.grid.DataGrid({
    store: store,
    structure: [
        { name: "ID", field: "id", width: "50px" },
        { name: "Name", field: "name", width: "200px" },
        { name: "Email", field: "email", width: "250px" }
    ]
}, "gridNode");
grid.startup();
```

### GFX 向量圖形

```javascript
dojo.require("dojox.gfx");

var surface = dojox.gfx.createSurface("surfaceNode", 400, 300);
surface.createCircle({ cx: 100, cy: 100, r: 50 })
    .setFill("red")
    .setStroke("black");
surface.createRect({ x: 200, y: 50, width: 100, height: 100 })
    .setFill("blue");
```

## Dijit UI 元件庫

Dijit 是 Dojo 的 UI 元件庫，提供了豐富的可訪問性支援：

### 按鈕和表單

```javascript
dojo.require("dijit.form.Form");
dojo.require("dijit.form.TextBox");
dojo.require("dijit.form.ValidationTextBox");
dojo.require("dijit.form.NumberTextBox");
dojo.require("dijit.form.FilteringSelect");

// 驗證文字框
new dijit.form.ValidationTextBox({
    required: true,
    invalidMessage: "請輸入有效的電子郵件",
    regExp: "[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}"
}, "emailInput");
```

### 對話框和浮動層

```javascript
// 對話框
var dialog = new dijit.Dialog({
    title: "我的對話框",
    content: "<p>這是對話框內容</p><button>關閉</button>"
});

// 工具提示
new dijit.Tooltip({
    connectId: ["helpIcon"],
    label: "這是幫助文字"
});

// 進度條
var progressBar = new dijit.ProgressBar({
    value: "50%"
}, "progressNode");
progressBar.startup();
```

### 日曆和時間選擇

```javascript
new dijit.form.DateTextBox({
    value: new Date(),
    constraints: {
        datePattern: "yyyy/MM/dd",
        max: new Date(),
        min: new Date(2000, 0, 1)
    }
}, "dateInput");
```

## 動畫效果

```javascript
dojo.require("dojo.fx");

// 基本動畫
dojo.animateProperty({
    node: "myElement",
    properties: {
        opacity: 0,
        left: 0,
        fontSize: { end: 24, unit: "px" }
    },
    duration: 500
}).play();

// 滑動效果
dojo.fx.wipeIn({ node: "content" }).play();
dojo.fx.wipeOut({ node: "content" }).play();

// 組合動畫
dojo.fx.chain([
    dojo.animateProperty({ node: "box", properties: { width: 300 } }),
    dojo.animateProperty({ node: "box", properties: { height: 200 } })
]).play();

// 並行動畫
dojo.fx.combine([
    dojo.animateProperty({ node: "box", properties: { left: 100 } }),
    dojo.animateProperty({ node: "box", properties: { top: 50 } })
]).play();
```

## 資料存取

```javascript
dojo.require("dojo.data.ItemFileReadStore");
dojo.require("dojo.data.ItemFileWriteStore");

// 讀取資料
var store = new dojo.data.ItemFileReadStore({
    url: "data.json"
});

store.fetch({
    query: { type: "person" },
    onComplete: function(items) {
        dojo.forEach(items, function(item) {
            console.log(store.getValue(item, "name"));
        });
    }
});

// 寫入資料
var writeStore = new dojo.data.ItemFileWriteStore({
    data: {
        items: [
            { id: 1, name: "John" },
            { id: 2, name: "Jane" }
        ]
    }
});

writeStore.newItem({ id: 3, name: "Bob" });
writeStore.save();
```

## 國際化與本地化

```javascript
dojo.require("dojo.i18n");
dojo.require("dojo.cldr.nls.number");

// 數字格式化
dojo.number.format(1234567.89, { pattern: "#,##0.00" });

// 貨幣格式化
dojo.currency.format(1234.56, { currency: "USD" });

// 日期格式化
dojo.date.locale.format(new Date(), {
    formatLength: "full",
    selector: "date"
});
```

## 企業應用案例

Dojo 在企業環境中的優勢：

1. **完整的解決方案** -- 從 UI 到資料存取一手包辦
2. **模組化載入** -- 按需載入，優化效能
3. **豐富的文件** -- 企業級文件支援
4. **可訪問性** -- 符合 WCAG 標準
5. **跨平台支援** -- 所有主流瀏覽器

## 結語

Dojo Toolkit 以其全面的功能和企業級的品質，成為 2007 年大型 Web 應用開發的首選。雖然學習曲線較陡，但其豐富的元件庫和強大的功能，使其在企業環境中佔有一席之地。

---

*延伸閱讀：*
- [Dojo Toolkit 官方網站](https://developers.google.com/search/?q=dojo+toolkit+official)
- [Dojo 文件](https://developers.google.com/search/?q=dojo+documentation)