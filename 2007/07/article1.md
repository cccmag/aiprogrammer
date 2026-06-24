# Ext JS 2.0 發布：企業級 Web 應用新選擇

## 概述

2007 年，Ext JS 發布了 2.0 版本，這是一個專注於企業級 Web 應用的 JavaScript 框架。Ext JS 2.0 以其豐富的 UI 元件、絢麗的視覺效果和強大的資料處理能力，迅速成為開發複雜 Web 應用的首選工具。

## Ext JS 的起源

Ext JS 起源於 Yahoo! UI Library 的擴展，開發者 Jack Slocum 在 YUI 的基礎上開發了一套更完整的元件系統。這套系統後來獨立成為 Ext JS，以其出色的視覺效果和企業級功能贏得了開發者的青睞。

## Ext JS 2.0 的核心特性

### 豐富的 UI 元件

Ext JS 2.0 提供了業界最完整的 UI 元件庫：

```javascript
// 視窗
new Ext.Window({
    title: "使用者管理",
    width: 400,
    height: 300,
    layout: "fit",
    items: [{
        xtype: "grid",
        store: userStore,
        columns: [
            { header: "ID", dataIndex: "id" },
            { header: "姓名", dataIndex: "name" },
            { header: "電子郵件", dataIndex: "email" }
        ]
    }],
    buttons: [
        { text: "新增", handler: addUser },
        { text: "關閉", handler: function() { this.close(); } }
    ]
}).show();

// 表單面板
new Ext.form.FormPanel({
    title: "使用者資訊",
    width: 350,
    bodyStyle: "padding:10px",
    items: [{
        xtype: "textfield",
        fieldLabel: "姓名",
        name: "name",
        allowBlank: false
    }, {
        xtype: "textfield",
        fieldLabel: "電子郵件",
        name: "email",
        vtype: "email"
    }, {
        xtype: "datefield",
        fieldLabel: "出生日期",
        name: "birthday"
    }],
    buttons: [{
        text: "提交",
        handler: function() {
            form.getForm().submit({
                success: function(form, action) {
                    Ext.Msg.alert("成功", "資料已儲存");
                },
                failure: function(form, action) {
                    Ext.Msg.alert("失敗", action.result.message);
                }
            });
        }
    }]
});
```

### 强大的 Grid 元件

Ext JS 的 Grid 是業界最强大的資料表格元件：

```javascript
var grid = new Ext.grid.GridPanel({
    store: dataStore,
    columns: [
        new Ext.grid.RowNumberer(),
        { header: "產品名稱", dataIndex: "name", width: 200 },
        { header: "價格", dataIndex: "price", width: 100,
          renderer: function(value) {
              return "$" + value.toFixed(2);
          }
        },
        { header: "庫存", dataIndex: "stock", width: 80 },
        { header: "操作", width: 100,
          renderer: function(value, metaData, record) {
              return '<a href="#">編輯</a> | <a href="#">刪除</a>';
          }
        }
    ],
    selModel: new Ext.grid.RowSelectionModel({ singleSelect: true }),
    bbar: new Ext.PagingToolbar({
        pageSize: 25,
        store: dataStore,
        displayInfo: true,
        displayMsg: "顯示第 {0} 到 {1} 筆，共 {2} 筆",
        emptyMsg: "無資料"
    }),
    tbar: [
        { text: "新增", handler: addProduct },
        { text: "刪除", handler: deleteProduct },
        "-",
        { text: "匯出", handler: exportData }
    ]
});
```

### Tree 元件

```javascript
var tree = new Ext.tree.TreePanel({
    el: "tree-container",
    useArrows: true,
    autoScroll: true,
    animate: true,
    enableDD: true,
    containerScroll: true,
    loader: new Ext.tree.TreeLoader({
        dataUrl: "tree-data.json"
    })
});

var root = new Ext.tree.AsyncTreeNode({
    text: "根節點",
    draggable: false,
    expanded: true
});

tree.setRootNode(root);
tree.render();
```

### Tab 元件

```javascript
var tabs = new Ext.TabPanel({
    renderTo: "tabs-container",
    activeTab: 0,
    items: [{
        title: "首頁",
        html: "<p>歡迎來到首頁</p>"
    }, {
        title: "產品",
        html: "<p>產品列表</p>"
    }, {
        title: "關於",
        html: "<p>關於我們</p>"
    }]
});

// 動態添加標籤頁
tabs.add({
    title: "新建標籤",
    html: "新內容",
    closable: true
}).show();
```

## 與後端整合

Ext JS 2.0 提供了完善的 AJAX 和資料處理能力：

```javascript
// 載入遠端資料
var store = new Ext.data.Store({
    proxy: new Ext.data.HttpProxy({
        url: "/api/products"
    }),
    reader: new Ext.data.JsonReader({
        totalProperty: "total",
        root: "data",
        id: "id"
    }, [
        { name: "id" },
        { name: "name" },
        { name: "price" },
        { name: "stock" }
    ])
});

store.load();

// 表單提交
var form = new Ext.form.FormPanel({
    standardSubmit: true,
    url: "/api/save",
    items: [{ xtype: "textfield", name: "data" }]
});

form.getForm().submit({
    params: { extraParam: "value" },
    success: function(form, action) {
        Ext.Msg.alert("成功", action.result.message);
    }
});
```

## 主題化系統

Ext JS 2.0 支援完整的主題化：

```javascript
// 切換主題
Ext.util.CSS.swapStyleSheet("theme", "resources/css/xtheme-gray.css");

// 自定義樣式
.x-panel-body {
    background-color: #f0f0f0;
    border: 1px solid #d0d0d0;
}
```

## 企業應用案例

Ext JS 2.0 被廣泛應用於企業級 Web 應用：

1. **ERP 系統** -- 複雜的表單和資料表格
2. **CRM 系統** -- 客戶關係管理
3. **專案管理工具** -- 看板和甘特圖
4. **分析儀表板** -- 圖表和報表

## 結語

Ext JS 2.0 以其豐富的元件、絢麗的效果和强大的功能，為企業級 Web 應用開發提供了一個完整的解決方案。雖然後來 Ext JS 经历了從 Ext JS 到 Sencha Ext JS 的演變，但其在企業級 Web 應用領域的影響力一直延續到今天。

---

*延伸閱讀：*
- [Ext JS 官方網站](https://developers.google.com/search/?q=extjs+official+website)
- [Ext JS 文件](https://developers.google.com/search/?q=extjs+documentation)