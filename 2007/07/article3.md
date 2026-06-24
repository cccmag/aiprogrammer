# Adobe AIR 1.0：跨平台桌面應用新時代

## 概述

2007 年 6 月，Adobe 發布了 AIR (Adobe Integrated Runtime) 1.0 Beta 版，並於 2008 年 2 月正式發布 1.0 版本。AIR 是一個跨平台的運行時環境，允許開發者使用 HTML、CSS、JavaScript、Flash 和 ActionScript 構建桌面應用程式，一次開發即可部署到 Windows、Mac 和 Linux。

## AIR 的設計理念

AIR 的核心價值在於「Write Once, Run Everywhere」：

```html
<!-- AIR 應用程式的 HTML 結構 -->
<html>
<head>
    <title>我的 AIR 應用</title>
    <script src="AIRAliases.js"></script>
    <style>
        body { margin: 0; padding: 20px; font-family: Arial; }
        .window-content { background: #fff; padding: 20px; }
    </style>
</head>
<body>
    <h1>歡迎使用 AIR 應用</h1>
    <p>這是一個跨平台的桌面應用程式！</p>
    <button onclick="saveFile()">儲存檔案</button>

    <script>
        function saveFile() {
            var file = air.File.desktopDirectory;
            file.addEventListener(air.Event.SELECT, onFileSelected);
            file.browseForSave("選擇儲存位置");
        }

        function onFileSelected(event) {
            var stream = new air.FileStream();
            stream.open(event.target, air.FileMode.WRITE);
            stream.writeUTFBytes("Hello, AIR!");
            stream.close();
        }
    </script>
</body>
</html>
```

## AIR 的核心功能

### 檔案系統存取

AIR 提供了強大的檔案系統存取能力：

```javascript
// 讀取檔案
var file = air.File.documentsDirectory.resolvePath("myFile.txt");
var stream = new air.FileStream();

stream.open(file, air.FileMode.READ);
var content = stream.readUTFBytes(stream.bytesAvailable);
stream.close();

console.log("檔案內容:", content);

// 寫入檔案
var stream = new air.FileStream();
stream.open(file, air.FileMode.WRITE);
stream.writeUTFBytes("新內容");
stream.close();

// 監控目錄變化
var dir = air.File.documentsDirectory;
var monitor = dir.addEventListener(air.FileEvent.CHANGE, function(event) {
    console.log("目錄已變更:", event.files);
});
```

### SQL資料庫支援

AIR 內建 SQLite 資料庫：

```javascript
var conn = new air.SQLConnection();
var dbFile = air.File.documentsDirectory.resolvePath("myApp.db");

conn.open(dbFile);

// 建立表格
conn.execute("CREATE TABLE IF NOT EXISTS users (" +
    "id INTEGER PRIMARY KEY AUTOINCREMENT, " +
    "name TEXT, " +
    "email TEXT" +
")");

// 插入資料
var stmt = new air.SQLStatement();
stmt.sqlConnection = conn;
stmt.text = "INSERT INTO users (name, email) VALUES (?, ?)";
stmt.parameters[0] = "John";
stmt.parameters[1] = "john@example.com";
stmt.execute();

// 查詢資料
var selectStmt = new air.SQLStatement();
selectStmt.sqlConnection = conn;
selectStmt.text = "SELECT * FROM users WHERE name = ?";
selectStmt.parameters[0] = "John";
selectStmt.execute();

var result = selectStmt.getResult();
for (var i = 0; i < result.data.length; i++) {
    console.log(result.data[i].name, result.data[i].email);
}
```

### 網路功能

```javascript
// HTTP 請求
var url = "http://api.example.com/data";
var request = new air.URLRequest(url);

air.navigateToURL(request);

// 使用 URLLoader
var loader = new air.URLLoader();
loader.addEventListener(air.Event.COMPLETE, function(event) {
    var data = loader.data;
    console.log("收到資料:", data);
});
loader.load(request);

// WebSocket（需要 Socket 類別）
```

### 系統整合

```javascript
// 系统托盘
var tray = new air.NativeApplication();
var icon = air.Icon.createFromPath("app:/icon.png");

// 使用原生視窗
air.NativeWindow
```

### 視窗管理

```javascript
// 建立新視窗
var options = new air.NativeWindowInitOptions();
options.type = air.NativeWindowType.NORMAL;
options.width = 800;
options.height = 600;

var newWindow = air.NativeWindow.init(options);
newWindow.title = "新視窗";
newWindow.activate();

// 設定視窗位置
newWindow.x = 100;
newWindow.y = 100;
```

## 使用 Flash/Flex 開發 AIR

```actionscript
// ActionScript AIR 應用
package {
    import flash.display.Sprite;
    import flash.text.TextField;
    import air.desktop.IAdobeDesktop;
    import air.desktop.IAdobeWindow;

    public class AIRApp extends Sprite {
        private var textField:TextField;

        public function AIRApp() {
            textField = new TextField();
            textField.text = "Hello, Adobe AIR!";
            textField.x = 50;
            textField.y = 50;
            textField.width = 300;
            addChild(textField);

            stage.nativeWindow.title = "我的 AIR 應用";
        }
    }
}
```

## 使用 Flex Builder 開發 AIR

```xml
<!-- Flex AIR 應用 -->
<?xml version="1.0" encoding="utf-8"?>
<mx:WindowedApplication xmlns:mx="http://www.adobe.com/2006/mxml"
    title="連絡人管理"
    width="600" height="400">

    <mx:Script>
        <![CDATA[
            import mx.collections.ArrayCollection;

            [Bindable]
            private var contacts:ArrayCollection = new ArrayCollection([
                { name: "John", email: "john@example.com" },
                { name: "Jane", email: "jane@example.com" }
            ]);
        ]]>
    </mx:Script>

    <mx:Panel title="連絡人列表" width="100%" height="100%">
        <mx:DataGrid dataProvider="{contacts}" width="100%" height="100%">
            <mx:columns>
                <mx:DataGridColumn headerText="姓名" dataField="name"/>
                <mx:DataGridColumn headerText="電子郵件" dataField="email"/>
            </mx:columns>
        </mx:DataGrid>
    </mx:Panel>

</mx:WindowedApplication>
```

## 知名 AIR 應用

2007-2008 年間，許多知名應用使用 AIR 開發：

1. **TweetDeck** -- Twitter 用戶端
2. **Pandora AIR** -- 網路電台用戶端
3. **Salesforce CRM** -- CRM 客戶端
4. **eBay Desktop** -- eBay 桌面應用
5. **NASA World Wind** -- 3D 地球檢視器

## AIR 的優勢

| 優勢 | 說明 |
|------|------|
| 跨平台 | 一次開發，多平台部署 |
| 豐富媒體 | 支援 Flash、視訊、音訊 |
| 離線能力 | 本地資料庫和檔案存取 |
| 桌面整合 | 系統托盤、通知、檔案關聯 |
| 開發彈性 | HTML/JS 或 Flash/Flex 皆可 |

## AIR 的局限性

- 執行時需要安裝 AIR Runtime
- HTML/JS 效能不如原生應用
- 檔案較大（完整 Runtime 約 15MB）
- 無法存取所有系統 API

## 結語

Adobe AIR 1.0 為 Web 開發者打開了一扇通往桌面應用的大門。透過 AIR，開發者可以使用熟悉的 Web 技術（HTML、CSS、JavaScript、Flash）開發跨平台桌面應用，無需學習複雜的原生開發語言。雖然 AIR 後來逐漸式微，但其跨平台桌面應用的理念，在 Electron 等新技術中得到了延續。

---

*延伸閱讀：*
- [Adobe AIR 官方網站](https://developers.google.com/search/?q=adobe+air+official)
- [Adobe AIR 開發文件](https://developers.google.com/search/?q=adobe+air+documentation)