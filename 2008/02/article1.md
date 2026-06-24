# 瀏覽器歷史回顧

## 前言

從 1990 年第一個網頁瀏覽器誕生，到 2008 年的現代瀏覽器，網頁瀏覽器經歷了二十年的發展。本文回顧這段精彩的歷史。

## 第一個瀏覽器：WorldWideWeb

### Tim Berners-Lee 的發明

1990 年，Tim Berners-Lee 在 CERN 開發了第一個網頁瀏覽器「WorldWideWeb」（後改名為 Nexus）：

```python
first_browser_features = {
    "年代": "1990",
    "發明者": "Tim Berners-Lee",
    "平台": "NeXT 電腦",
    "功能": "瀏覽和編輯網頁",
    "限制": "只能在 NeXT 系統執行"
}
```

### 早期瀏覽器

1992-1993 年出現了多個瀏覽器：
- Erwise（1992）：第一個支援超連結的瀏覽器
- ViolaWWW（1992）：新增圖形、樣式表支援
- Mosaic（1993）：讓網頁有了圖片支援，普及率大增

## Netscape Navigator 時代

### 網景的崛起

1994 年，Marc Andreessen 與 Jim Clark 創立了網景通訊公司，推出了 Netscape Navigator：

```
Netscape 的創新：

1. 友善的 GUI 介面
2. 支援框架（Frames）
3. JavaScript 腳本語言
4. Cookie 支援
5. SSL 安全連線
6. Plug-in 擴充系統
```

### 市場主導

網景在巔峰時期佔據超過 90% 的瀏覽器市場：
- 1994：Navigator 1.0
- 1995：Navigator 2.0
- 1996：Navigator 3.0（支援 Java）
- 1997：Navigator 4.0

## 第一次瀏覽器大戰

### Internet Explorer 的崛起

1995 年，微軟收購了 Spyglass 的 Mosaic 程式碼，推出了 Internet Explorer：

```python
ie_strategy = {
    "Windows 捆綁": "每套 Windows 都包含 IE",
    "快速迭代": "不斷推出新版本",
    "功能追赶": "支援 CSS、JavaScript 等",
    "行銷優惠": "与作業系統整合行銷"
}
```

### 戰爭結果

```
市場份額變化：

1996:  Netscape ~80%  vs  IE ~20%
1998:  Netscape ~50%  vs  IE ~50%
1999:  Netscape ~30%  vs  IE ~70%
2001:  Netscape <5%   vs  IE ~95%
```

微軟勝利了，但代價是網景最終被 AOL 收購並走向衰落。

## Mozilla 專案

### 開放原始碼的火種

1998 年，網景決定開放 Navigator 的原始碼，催生了 Mozilla 專案：

```python
mozilla_origins = {
    "目標": "建立開放原始碼的瀏覽器",
    "核心元件": "Layout Engine (Gecko)",
    "JavaScript": "SpiderMonkey 直譯器",
    "命名由來": "「Mozilla」是網景的吉祥物名稱"
}
```

### Firefox 的誕生

2004 年，Mozilla 推出了 Firefox 1.0，開啟了瀏覽器的復興：

```python
firefox_1_features = {
    "分頁瀏覽": "一個視窗多個分頁",
    "彈出視窗封鎖": "對抗廣告視窗",
    "隱私瀏覽": "不留下瀏覽紀錄",
    "擴充套件": "強大的擴充系統",
    "更快": "比 IE 和 Navigator 更快"
}
```

### Firefox 2 和 3

2006-2008 年間，Firefox 2 和 3 陸續發布：
- Firefox 2：改進書籤系統、加強 RSS 支援
- Firefox 3：全新下載管理器、位址列改進

## WebKit 與 Safari

### KHTML 起點

2001 年，Apple 以 KHTML 為基礎，開發了 WebKit 渲染引擎：

```python
webkit_origin = {
    "基礎": "KDE 的 KHTML",
    "分支": "2001 年建立 WebKit",
    "首個產品": "Safari 瀏覽器",
    "重要特性": "JavaScriptCore 引擎"
}
```

### WebKit 的創新

WebKit 的架構設計非常優雅：

```
WebKit 架構：

┌──────────────────────────────────┐
│          WebKit API             │
├──────────────────────────────────┤
│                                  │
│  ┌────────────┐  ┌────────────┐ │
│  │   Port A   │  │   Port B   │ │
│  │  (Mac)     │  │  (其他)    │ │
│  └─────┬──────┘  └─────┬──────┘ │
│        │               │        │
│  ┌─────┴───────────────┴──────┐ │
│  │        WebCore (DOM/渲染)   │ │
│  ├──────────────────────────────┤
│  │   JavaScriptCore (JS 引擎)   │ │
│  └──────────────────────────────┘ │
└──────────────────────────────────┘
```

## Opera 的貢獻

### 小眾但創新

Opera 雖然市場份額不高，但推出了許多創新功能：

```python
opera_innovations = {
    "1994": "第一個支援框架的瀏覽器",
    "2001": "第一個支援 tab 的瀏覽器",
    "2003": "滑鼠手勢",
    "2005": "內建 BitTorrent 下載",
    "2007": "支援 Unite (個人伺服器)"
}
```

## 2008 年的瀏覽器市場

### 市場份額（2008年初）

```
IE 6/7：     ~70%
Firefox 2/3：~20%
Safari：     ~5%
Opera：      ~2%
其他：       ~3%
```

### 即將到來的變化

2008 年 9 月，Chrome 將發布 Beta 版，徹底改變瀏覽器市場格局。

## 瀏覽器技術演進

### HTML 和 CSS 支援

```python
html_css_timeline = {
    "1991": "HTML 1.0 - 基本標記",
    "1995": "HTML 2.0 - 表單、表格",
    "1997": "HTML 3.2/4.0 - 框架、樣式表",
    "1999": "HTML 4.01 - DOM、層疊樣式表",
    "2000": "XHTML 1.0 - XML 語法",
    "2008": "HTML 5 草案 - 多媒體、離線支援"
}
```

### JavaScript 的成熟

```
JavaScript 發展：

1995: 發明，稱為 LiveScript
1997: ECMAScript 1 (ES3)
1999: ECMAScript 3
2005: AJAX 普及，JavaScript 文藝復興
2008: V8 引擎發布，效能大幅提升
```

## 未來展望

### 2008 年後的趨勢

```
未來瀏覽器發展：

2008: Chrome 發布，第三次瀏覽器大戰開始
2009: Firefox 3.5, IE 8
2010: Firefox 4, Chrome 10
2011: Firefox 5-16, Chrome 14-23
2012: Firefox 17+, Chrome 20+
```

### 行動瀏覽

行動瀏覽器也開始興起：
- Safari iOS（2007）
- Android Browser（2008）
- Chrome Mobile（2012）

---

**延伸閱讀**

- [Browser history timeline](https://www.google.com/search?q=browser+history+timeline)
- [Netscape+Navigator+history](https://www.google.com/search?q=Netscape+Navigator+history)
- [Web+browser+evolution](https://www.google.com/search?q=web+browser+evolution)