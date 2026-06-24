# Dojo Toolkit 1.0：企業級 JavaScript 框架

## 前言

2007 年，Dojo Toolkit 發布了 1.0 正式版。這是一個全面的企業級 JavaScript/Ajax 框架，提供了從 DOM 操作到圖形繪製、離線儲存的完整工具集。

## Dojo 的模組化架構

```javascript
// 按需載入模組
dojo.require("dojo.io.iframe");
dojo.require("dojox.grid.Grid");
dojo.require("dojox.charting.Chart2D");

// 圖形繪製
var chart = new dojox.charting.Chart2D("chartNode");
chart.addSeries("Sales", [1, 2, 3, 4, 5]);
chart.render();
```

## Dojo 的獨特功能

### 離線儲存

```javascript
// Dojo Offline - 離線支援
dojox.off.enabled = true;

dojox.off.onOnline = function() {
    console.log("網路已連線");
};

dojox.off.onOffline = function() {
    console.log("網路已斷線");
};
```

### 圖形元件

```javascript
// 建立圖表
var chart = new dojox.charting.Chart2D("chart");
chart.addPlot("default", { type: "Lines" });
chart.addSeries("Data", [100, 200, 150, 300]);
chart.render();
```

## 結語

Dojo Toolkit 是第一個真正「企業級」的 JavaScript 框架。其模組化設計和豐富的元件庫，影響了後續的 Ext JS 等框架。

---

## 延伸閱讀

- [Dojo+Toolkit+1.0](https://www.google.com/search?q=Dojo+Toolkit+1.0)
- [Dojo+enterprise+JavaScript+framework](https://www.google.com/search?q=Dojo+enterprise+JavaScript+framework)

---