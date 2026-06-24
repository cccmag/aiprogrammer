# 瀏覽器擴充功能

## 前言

瀏覽器擴充功能讓使用者可以自訂和增強瀏覽器的功能。2008 年的 Chrome 還沒有擴充功能系統，但 Firefox 的擴充功能生態已經非常成熟。

## 擴充功能 vs 外掛程式

### 基本區別

```python
extensions_vs_plugins = {
    "擴充功能 (Extensions)": {
        "用途": "增強或修改瀏覽器行為",
        "存取": "可訪問瀏覽器 API",
        "安全": "在沙盒中執行",
        "範例": "廣告封鎖、密碼管理"
    },
    "外掛程式 (Plugins)": {
        "用途": "顯示特定內容（如 Flash）",
        "存取": "NPAPI 可訪問系統層級",
        "安全": "較大攻擊面",
        "範例": "Flash Player, PDF Reader"
    }
}
```

## Firefox 擴充功能系統

### XUL 和 XPCOM

Firefox 擴充功能基於 Mozilla 的技術：

```python
firefox_extension_tech = {
    "XUL": "XML User Interface Language，定義 UI",
    "XPCOM": "Cross-Platform Component Object Model",
    "JavaScript": "擴充功能的主要開發語言",
    "DOM": "可訪問和修改頁面 DOM"
}
```

### 擴充功能結構

```python
extension_structure = {
    "install.rdf": "擴充功能元資料",
    "chrome.manifest": "內容註冊",
    "defaults/preferences/": "預設設定",
    "components/": "XPCOM 元件",
    "skin/": "樣式和圖示",
    "locale/": "國際化字串"
}
```

### 安裝與執行

```
擴充功能安裝流程：

1. 使用者下載 .xpi 檔案
2. Firefox 解壓縮並讀取 install.rdf
3. 檢查相容性和權限
4. 安裝到 profile 目錄
5. 啟動時載入元件
```

## NPAPI 外掛程式

### 外掛程式架構

```python
npapi_basics = {
    "全名": "Netscape Plugin API",
    "用途": "在網頁中顯示非標準內容",
    "機制": "瀏覽器啟動外掛程式程序",
    "記憶體隔離": "外掛程式執行在獨立程序"
}
```

### 外掛程式生命週期

```python
# NPAPI 外掛程式的標準函式

plugin_lifecycle = {
    "NP_Initialize": "外掛程式初始化",
    "NP_GetEntryPoints": "取得外掛程式函式指標",
    "NPP_New": "新實體建立",
    "NPP_Destroy": "實體銷毀",
    "NPP_SetWindow": "設定視窗",
    "NPP_NewStream": "新資料流",
    "NPP_WriteReady": "可寫入資料",
    "NPP_Write": "寫入資料"
}
```

### 常見外掛程式

| 外掛程式 | 用途 |
|----------|------|
| Flash Player | SWF 動畫和影片 |
| Java Plugin | Java Applet |
| Adobe Reader | PDF 顯示 |
| QuickTime | 視訊播放 |
| Windows Media Player | WMV 播放 |

## Chrome 擴充功能（後來）

### 2008 年的 Chrome 擴充功能

2008 年 Chrome 發布時，**沒有擴充功能功能**。擴充功能 API 在 2009 年 1 月的 Chrome 2.0 才正式加入。

```python
# Chrome 擴充功能時間線

chrome_extension_timeline = {
    "2008/09": "Chrome 1.0，無擴充功能",
    "2009/01": "Chrome 2.0，擴充功能 API 引入",
    "2010/01": "Chrome 4.0，支援使用者腳本",
    "2011/09": "Chrome 14，Manifest v1",
    "2013/02": "Manifest v2",
    "2022/01": "Manifest v3"
}
```

### Chrome 擴充功能結構

```python
# Chrome 擴充功能檔案結構

chrome_extension_manifest = {
    "manifest.json": "擴充功能中繼資料和設定",
    "background.js": "背景腳本（可訪問瀏覽器 API）",
    "content_scripts.js": "在頁面中執行的腳本",
    "popup.html/js": "彈出視窗",
    "options.html/js": "選項頁面"
}
```

### Manifest v1 範例

```json
{
    "name": "My Extension",
    "version": "1.0",
    "permissions": ["tabs", "storage"],
    "browser_action": {
        "default_icon": "icon.png",
        "default_popup": "popup.html"
    },
    "content_scripts": [{
        "matches": ["<all_urls>"],
        "js": ["content.js"]
    }]
}
```

## 擴充功能範例

### Firefox 擴充功能：Hello World

```python
# 最簡單的 Firefox 擴充功能

minimal_extension = {
    "install.rdf": """
        <?xml version="1.0"?>
        <RDF xmlns="http://www.mozilla.org/rdf/vocabulary">
            <em:package>
                <em:id>helloworld@example.com</em:id>
                <em:name>Hello World</em:name>
                <em:version>1.0</em:version>
            </em:package>
        </RDF>
    """,
    "chrome.manifest": "content helloworld ./",
    "helloworld.xul": """
        <?xml version="1.0"?>
        <overlay xmlns="http://www.mozilla.org/keymaster/">
            <toolbar id="main-toolbar">
                <button id="helloworld-btn" label="Hello"/>
            </toolbar>
        </overlay>
    """
}
```

### 注入使用者腳本

```javascript
// Greasemonkey 使用者腳本範例

// ==UserScript==
// @name          Hello World Script
// @namespace     http://example.com/
// @description    顯示 Hello World
// @include        *
// ==/UserScript==

alert("Hello World!");

// 或直接修改頁面
document.body.innerHTML += "<div style='position:fixed;top:10px;right:10px;background:yellow;padding:10px;'>Hello World!</div>";
```

## 安全性考量

### 擴充功能的安全風險

```python
extension_risks = {
    "過度權限": "擴充功能請求過多權限",
    "惡意程式碼": "假冒知名擴充功能",
    "第三方函式庫": "可能包含惡意程式碼",
    "過時依賴": "已知漏洞未修補"
}
```

### 安全最佳實踐

```python
extension_security = {
    "最小權限": "只請求必需的權限",
    "內容驗證": "驗證所有輸入",
    "安全儲存": "敏感資料加密儲存",
    "定期更新": "及時修補漏洞"
}
```

## 擴充功能生態系統

### 2008 年的 Firefox 擴充功能生態

```python
firefox_extension_ecosystem = {
    "數量": "數千個擴充功能",
    "知名擴充": [
        "Adblock Plus - 廣告封鎖",
        "Firebug - 網頁除錯",
        "Greasemonkey - 使用者腳本",
        "Gmail Manager - Gmail 管理",
        "NoScript - JavaScript 控制"
    ],
    "分發": "addons.mozilla.org (AMO)"
}
```

### 受歡迎的擴充功能類型

```python
popular_extensions = {
    "開發者工具": ["Firebug", "Web Developer", "YSlow"],
    "隱私安全": ["Adblock Plus", "NoScript", " Ghostery"],
    "生產力": ["Gmail Manager", "DownThemAll", "Tab Mix Plus"],
    "自訂": ["Stylish", "Classic Theme Restorer"]
}
```

## 未來展望

### 擴充功能的演進

```python
# 擴充功能未來發展方向

future_extensions = {
    "Chrome Manifest v3 (2022)": "更嚴格的隱私控制",
    "WebExtension 標準": "跨瀏覽器相容性",
    "更安全的模型": "沙盒化執行",
    "效能改進": "減少資源占用"
}
```

### WebExtensions API

```python
# Firefox 和 Chrome 都支援的標準 API

webextension_common_apis = {
    "tabs": "操作標籤頁",
    "storage": "儲存設定",
    "runtime": "通訊和元資料",
    "permissions": "權限管理",
    "webNavigation": "導航事件"
}
```

---

**延伸閱讀**

- [Browser+extensions+history](https://www.google.com/search?q=browser+extensions+history)
- [Firefox+extension+development](https://www.google.com/search?q=Firefox+extension+development)
- [Chrome+extension+API](https://www.google.com/search?q=Chrome+extension+API)