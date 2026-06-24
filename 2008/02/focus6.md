# 開發者工具

## Chrome 開發者工具簡介

### 開發者工具的意義

現代瀏覽器提供強大的開發者工具，讓網頁開發者能夠：

```python
devtools_purposes = [
    "除錯 JavaScript 程式碼",
    "檢查和修改 DOM 元素",
    "監控網路請求",
    "分析效能問題",
    "審查 CSS 樣式",
    "除錯 AJAX 請求"
]
```

### 開啟開發者工具

```python
open_devtools = {
    "快捷鍵": "F12 或 Ctrl+Shift+I (Windows) / Cmd+Option+I (Mac)",
    "右鍵選單": "在頁面上選擇「檢查元素」",
    "選單": "Chrome 選單 → 更多工具 → 開發者工具"
}
```

## Elements 面板

### DOM 檢視器

```python
dom_inspector_features = {
    "功能": "查看和修改頁面的 DOM 樹",
    "互動": "滑鼠懸停高亮元素",
    "編輯": "雙擊或按 Enter 編輯屬性和文字",
    "搜尋": "使用 Ctrl+F 搜尋 DOM"
}
```

### 範例：檢查元素

```
HTML 結構檢視：

<body>
  <div id="container">
    <h1 class="title">Hello World</h1>
    <p class="description">Welcome to my site</p>
  </div>
</body>

點擊元素 → 右側顯示：
- Styles：套用的 CSS
- Computed：最終計算後的樣式
- Event Listeners：事件監聽器
- Properties：DOM 元素屬性
```

### CSS 編輯

```python
css_editing = {
    "即時預覽": "修改後立即看到效果",
    "顏色選擇器": "內建的顏色選擇器",
    "方塊模型": "視覺化 padding、margin、border",
    "開關樣式": "可暫時停用特定樣式"
}
```

## Console 面板

### JavaScript 控制台

```python
console_features = {
    "執行 JavaScript": "在頁面上下文執行任意程式碼",
    "日誌輸出": "console.log(), console.error() 等",
    "物件檢視": "展開查看物件內容",
    "命令列 API": "$(), $$(), monitor() 等輔助函式"
}
```

### Console API

```javascript
// 常用 Console 方法
console.log("一般訊息");
console.warn("警告訊息");
console.error("錯誤訊息");
console.info("資訊訊息");

// 格式化輸出
console.log("User: %s, Age: %d", "Alice", 25);

// 物件檢視
var obj = {name: "Bob", age: 30, skills: ["JS", "Python"]};
console.log(obj);

// 群組輸出
console.group("User Details");
console.log("Name:", obj.name);
console.log("Age:", obj.age);
console.groupEnd();

// 計時
console.time("operation");
doSomething();
console.timeEnd("operation");

// 斷言
console.assert(condition, "This should not happen");
```

### 命令列快捷方式

```javascript
// $() - 等同於 document.querySelector()
$("div");  // 第一個 div

// $$() - 等同於 document.querySelectorAll()
$$("div"); // 所有 div

// $x() - XPath 查詢
$x("//div[@class='container']");

// copy() - 複製到剪貼簿
copy(object);

// 鍵盤快速鍵
// $0 - 目前選取的元素
// $1 - 上一個選取的元素
```

## Sources 面板

### JavaScript 除錯器

```python
debugger_features = {
    "中斷點": "在任何行設定中斷點",
    "逐步執行": "Step over, step into, step out",
    "監控變數": "加入 Watch 表達式",
    "呼叫堆疊": "查看函式呼叫順序",
    "範圍面板": "查看區域和全域變數"
}
```

### 設定中斷點

```javascript
// 方法 1：直接在程式碼中
function calculateTotal(price, tax) {
    debugger;  // 執行到此處會暫停
    return price + tax;
}

// 方法 2：透過 DevTools
// 在 Sources 面板點擊行號

// 方法 3：條件中斷點
// 右鍵點擊行號 → 設定條件
// 例如：total > 1000 才停下
```

### 逐步執行

```python
step_controls = {
    "Step Over (F10)": "執行下一行，不進入函式",
    "Step Into (F11)": "執行進入呼叫的函式",
    "Step Out (Shift+F11)": "執行到目前函式返回",
    "Resume (F8)": "繼續執行到下一個中斷點"
}
```

## Network 面板

### 網路請求監控

```python
network_features = {
    "請求列表": "顯示所有網路請求",
    "時間軸": "每個請求的時間分配",
    "詳情面板": "請求和回應的詳細內容",
    "篩選": "依類型、網域等篩選",
    "保留": "頁面重新整理時保留紀錄"
}
```

### 請求詳情

```python
request_details = {
    "Headers": "HTTP 標頭",
    "Preview/Response": "回應內容（格式化）",
    "Timing": "時間分解（DNS、連線、SSL 等）",
    "Cookies": "傳送和接收的 Cookie"
}
```

### 監控 AJAX 請求

```javascript
// 範例：fetch API
fetch("/api/users")
    .then(response => response.json())
    .then(data => console.log(data));

// 在 Network 面板可以看到：
// - Request URL: /api/users
// - Method: GET
// - Status: 200
// - Time: 45ms
// - Response: [ {...}, {...} ]
```

## Timeline 面板

### 效能分析

```python
timeline_features = {
    "錄製": "記錄一段時間內的所有活動",
    "幀率": "檢視頁面 FPS",
    "JavaScript 执行": "JS 執行時間分析",
    "Rendering": "重繪和重排時間",
    "繪圖": "GPU 繪圖操作"
}
```

### 讀取 Timeline

```
Timeline 面板顯示：

- 垂直軸：資源使用或 FPS
- 水平軸：時間經過

顏色含義：
- 藍色：網路請求
- 黃色：JavaScript 執行
- 紫色：CSS 計算和佈局
- 綠色：繪製
```

## Resources 面板

### 檢視資源

```python
resources_features = {
    "Frames": "iframe 內容",
    "Scripts": "載入的 JavaScript 檔案",
    "Style Sheets": "CSS 檔案",
    "Images": "圖片資源",
    "Fonts": "網頁字體",
    "Local Storage": "Local Storage 資料",
    "Session Storage": "Session Storage 資料",
    "Cookies": "網站 Cookie"
}
```

### localStorage 操作

```javascript
// 設定值
localStorage.setItem("username", "Alice");
localStorage.setItem("preferences", JSON.stringify({theme: "dark"}));

// 讀取值
var username = localStorage.getItem("username");
var prefs = JSON.parse(localStorage.getItem("preferences"));

// 刪除
localStorage.removeItem("username");
localStorage.clear();
```

## Profiles 面板

### JavaScript CPU Profiler

```python
cpu_profiling = {
    "目的": "找出 JavaScript 的效能瓶頸",
    "方法": "錄製一段時間的函式呼叫",
    "結果": "顯示每個函式呼叫的時間和次數"
}
```

### 記憶體分析

```python
memory_profiling = {
    "Heap Snapshot": "某時間點的記憶體狀態",
    "Allocation Timeline": "記憶體配置的時間線",
    "Heap Growth": "記憶體成長趨勢"
}
```

## 實用技巧

### 常見工作流程

```python
workflows = {
    "1. 除錯 JS": "Sources 面板設定中斷點，檢查變數",
    "2. 檢查 CSS": "Elements 面板修改樣式，即時預覽",
    "3. 網路問題": "Network 面板查看慢的請求",
    "4. 效能問題": "Timeline 面板錄製分析瓶頸"
}
```

### 遠程除錯

```python
remote_debugging = {
    "設定": "Chrome 啟動時加 --remote-debugging-port=9222",
    "連接": "在另一個 Chrome 開啟 localhost:9222",
    "用途": "除錯手機瀏覽器、測試環境"
}
```

### 行動裝置模擬

```python
device_mode = {
    "功能": "模擬不同螢幕尺寸和解析度",
    "操作": "點擊左上角電話圖示切換",
    "自訂": "可新增自訂裝置"
}
```

---

**延伸閱讀**

- [Chrome DevTools official](https://www.google.com/search?q=Chrome+DevTools+official)
- [JavaScript+debugging+tutorial](https://www.google.com/search?q=JavaScript+debugging+tutorial)
- [Chrome+developer+tools+tips](https://www.google.com/search?q=Chrome+developer+tools+tips)