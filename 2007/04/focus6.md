# 未來展望：Web 2.0 與 Mobile 的融合

## Web 2.0 的行動化

Web 2.0 的核心概念——使用者生成內容、社交網路、豐富的互動體驗——正在向行動裝置遷移。2007 年，我們看到了這個趨勢的開端。

### Web 2.0 行動化的關鍵技術

```
Web 2.0 行動技術棧：
───────────────────────
表示層：HTML 5 + CSS 3 + WebKit 專有擴展
通訊層：AJax + WebSocket + JSON
持久層：LocalStorage + SQL Lite + Offline Cache
媒體層：Canvas 2D + SVG + Video + Audio
裝置層：Geolocation + DeviceOrientation + Touch Events
```

## 離線 Web 應用

2007 年，最令人期待的功能之一是離線存取。Google Gears 是這方面的先驅：

### Google Gears API

```javascript
// 檢查 Gears 是否可用
if (window.google && google.gears) {
    var desktop = google.gears.factory.create('beta.desktop');
    var database = google.gears.factory.create('beta.database');

    database.open('myapp');
    database.execute('CREATE TABLE IF NOT EXISTS data ...');
}

// 建立本地資料庫
var db = google.gears.factory.create('beta.database');
db.open('notes-app');

db.execute('CREATE TABLE IF NOT EXISTS notes (' +
    'id INTEGER PRIMARY KEY, ' +
    'title TEXT, ' +
    'content TEXT, ' +
    'modified INTEGER)');

// 插入資料
db.execute('INSERT INTO notes VALUES (?, ?, ?, ?)',
    [null, '標題', '內容', Date.now()]);

// 查詢資料
var rs = db.execute('SELECT * FROM notes ORDER BY modified DESC');
while (rs.isValidRow()) {
    console.log(rs.field(0), rs.field(1));
    rs.next();
}
```

### Application Cache（HTML 5）

HTML 5 的 Application Cache 是另一個離線解決方案：

```html
<!DOCTYPE html>
<html manifest="app.manifest">
<head>
  <title>離線應用</title>
</head>
<body>
  <script src="app.js"></script>
</body>
</html>
```

```manifest
# app.manifest
CACHE MANIFEST
# version 1.0

CACHE:
/index.html
/app.js
/styles.css
/logo.png

NETWORK:
/api/*

FALLBACK:
/api/ offline.html
```

### Local Storage

```javascript
// Local Storage API
// 儲存資料
localStorage.setItem('username', 'john');
localStorage.setItem('preferences', JSON.stringify({
    theme: 'dark',
    fontSize: 16
}));

// 讀取資料
var username = localStorage.getItem('username');
var prefs = JSON.parse(localStorage.getItem('preferences'));

// 刪除資料
localStorage.removeItem('username');

// 清除所有
localStorage.clear();
```

## 地理定位 API

W3C Geolocation API 在 2007 年開始被 Safari 和其他瀏覽器支援：

### 基本使用

```javascript
// 取得目前位置
navigator.geolocation.getCurrentPosition(
    function(position) {
        var lat = position.coords.latitude;
        var lng = position.coords.longitude;
        var accuracy = position.coords.accuracy;

        console.log('緯度: ' + lat);
        console.log('經度: ' + lng);
        console.log('精確度: ' + accuracy + ' 公尺');
    },
    function(error) {
        switch (error.code) {
            case error.PERMISSION_DENIED:
                console.log('使用者拒絕提供位置');
                break;
            case error.POSITION_UNAVAILABLE:
                console.log('位置資訊不可用');
                break;
            case error.TIMEOUT:
                console.log('位置取得逾時');
                break;
        }
    },
    {
        enableHighAccuracy: true,
        timeout: 5000,
        maximumAge: 60000
    }
);
```

### 持續追蹤位置

```javascript
// 持續追蹤位置
var watchId = navigator.geolocation.watchPosition(
    function(position) {
        updateMap(position.coords.latitude, position.coords.longitude);
    },
    function(error) {
        console.error('位置錯誤: ' + error.message);
    },
    {
        enableHighAccuracy: true,
        timeout: 10000,
        maximumAge: 30000
    }
);

// 停止追蹤
navigator.geolocation.clearWatch(watchId);
```

## WebSocket 與即時通訊

WebSocket 提供了一個雙向通訊管道，對於即時應用（如聊天、遊戲）至關重要：

### WebSocket 基礎

```javascript
// 建立連接
var ws = new WebSocket('ws://example.com/chat');

// 連接成功
ws.onopen = function() {
    console.log('連接已建立');
    ws.send('Hello Server');
};

// 接收訊息
ws.onmessage = function(event) {
    var data = JSON.parse(event.data);
    console.log('收到訊息:', data);
    displayMessage(data);
};

// 連接關閉
ws.onclose = function() {
    console.log('連接已關閉');
};

// 錯誤處理
ws.onerror = function(error) {
    console.error('WebSocket 錯誤:', error);
};

// 傳送訊息
ws.send(JSON.stringify({ type: 'message', content: 'Hello' }));
```

### 即時應用架構

```
WebSocket 即時應用架構：
────────────────────────────

┌─────────┐    WebSocket    ┌─────────┐
│ 瀏覽器   │ ◄──────────────►│ 伺服器   │
│         │                 │         │
│ JavaScript│   即時雙向     │ Node.js │
│ Client   │    傳輸        │ WS Server│
└─────────┘                 └────┬────┘
                                 │
                           ┌─────▼─────┐
                           │  Redis   │
                           │  Pub/Sub │
                           └──────────┘
```

## 跨設備同步

2007 年出現了「雲端同步」的概念，允許使用者在多個設備間無縫切換：

### 基本同步架構

```javascript
// 同步服務架構
var SyncEngine = {
    localDb: null,
    remoteDb: null,
    syncInterval: 60000,

    init: function() {
        this.localDb = new LocalStorageDB();
        this.remoteDb = new RemoteDB('https://api.example.com');

        // 啟動同步循環
        this.startSync();
    },

    startSync: function() {
        setInterval(this.sync.bind(this), this.syncInterval);
    },

    sync: function() {
        // 1. 上傳本地變更
        var localChanges = this.localDb.getChanges();
        localChanges.forEach(function(change) {
            this.remoteDb.push(change);
        }, this);

        // 2. 下載遠端變更
        var remoteChanges = this.remoteDb.getChanges();
        remoteChanges.forEach(function(change) {
            this.localDb.apply(change);
        }, this);

        // 3. 解決衝突
        this.resolveConflicts();
    },

    resolveConflicts: function() {
        // 最後寫入勝出（LWW）
        // 或基於時間戳、版本號的更複雜策略
    }
};
```

## 移動 Web 的未來趨勢

### 將會發生的變化

**1. HTML 5 的全面勝利**

HTML 5 的各種 API——Canvas、Video、地理位置、WebSocket——將使 Web 應用擁有接近原生的能力。

**2. 統一開發體驗**

「一次撰寫，到處運行」在行動 Web 領域將逐步實現。WebGL 讓 3D 遊戲可以在瀏覽器中流暢運行。

**3. 離線優先**

越來越多的應用將採用「離線優先」設計——本地處理所有操作，僅在有網路時同步。

**4. 裝置 API 標準化**

Camera API、Contact API、File API 等將逐步標準化，讓 Web 應用可以完全取代原生應用。

### 短期內的現實

```
2007-2010 年行動 Web 發展預測：
────────────────────────────────────────────────────────
2007      iPhone 發布，WebKit 成為主流引擎
2008      iPhone SDK 發布，原生應用時代來臨
2009      Android 上市，WebKit 市場佔有率提升
2010      HTML 5 標準制定中，行動瀏覽器開始支援
────────────────────────────────────────────────────────
```

## 結語

2007 年是行動 Web 發展的轉捩點。iPhone 的出現重新定義了「行動瀏覽器」的可能性；WebKit 的開源為整個產業提供了共享的引擎基礎；HTML 5 的發展讓 Web 應用的能力邊界不斷擴展。

未來十年，我們將看到：
- Web 與原生的界線日益模糊
- 漸進式 Web 應用（PWA）將成為主流
- 離線功能將是標配而非選項
- 跨設備的無縫體驗將是常態

行動 Web 的黃金時代才剛開始。

---

## 延伸閱讀

- [HTML5+mobile+web+applications+future](https://www.google.com/search?q=HTML5+mobile+web+applications+future)
- [WebSocket+real+time+mobile+apps](https://www.google.com/search?q=WebSocket+real+time+mobile+apps)
- [Offline+web+applications+Google+Gears](https://www.google.com/search?q=Offline+web+applications+Google+Gears)
- [Geolocation+API+W3C+specification](https://www.google.com/search?q=Geolocation+API+W3C+specification)

---

*本篇文章為「AI 程式人雜誌 2007 年 4 月號」本期焦點系列之一。*