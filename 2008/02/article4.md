# WebKit 渲染引擎

## 前言

WebKit 是用於 Safari 和早期 Chrome 的 HTML 渲染引擎。它的設計以高效能和跨平台聞名，為現代網頁瀏覽器奠定了基礎。

## WebKit 的歷史

### 起源：KHTML

2001 年，Apple 以 KDE 的 KHTML 為基礎，建立了 WebKit 專案：

```python
webkit_origin = {
    "時間": "2001 年",
    "基礎": "KDE KHTML",
    "公司": "Apple",
    "目的": "為 Safari 瀏覽器提供核心",
    "授權": " LGPL（KHTML 部分）"
}
```

### 與 KHTML 的關係

```
KHTML                           WebKit
  │                                │
  ├── KHTML (核心)                 ├── WebCore (核心)
  ├── KHTMLW (Qt 整合)             ├── JavaScriptCore
  └── Konqueror (使用 KHTML)       └── Safari (蘋果的實現)
```

### 重要里程碑

```python
webkit_timeline = {
    "2001": "WebKit 專案啟動",
    "2003": "Safari 1.0 發布",
    "2005": "WebKit 開放原始碼",
    "2007": "iPhone Safari 使用 WebKit",
    "2008": "Chrome 使用 WebKit（後 fork 出 Blink）"
}
```

## 架構概覽

### 兩層主要架構

```
┌─────────────────────────────────────────┐
│              WebKit Port                │
│     (平台特定：Mac, Windows, Qt)        │
├─────────────────────────────────────────┤
│                                         │
│  ┌──────────────────────────────────┐  │
│  │         WebCore                   │  │
│  │  (HTML 解析, CSS 解析, DOM, 渲染) │  │
│  └──────────────────────────────────┘  │
│  ┌──────────────────────────────────┐  │
│  │      JavaScriptCore (JSC)        │  │
│  │      (JavaScript 引擎)            │  │
│  └──────────────────────────────────┘  │
│                                         │
└─────────────────────────────────────────┘
```

## WebCore 元件

### 主要模組

```python
webcore_components = {
    "HTML解析器": "將 HTML 文字轉換為 DOM 樹",
    "CSS解析器": "解析樣式表，計算樣式",
    "DOM": "文件物件模型的實現",
    "Render Tree": "渲染樹，決定如何繪製",
    "Layout": "計算元素位置和大小",
    "Painting": "將內容繪製到螢幕"
}
```

### DOM 實現

```python
# WebKit 的 DOM 結構

dom_architecture = {
    "Document": "整份文件的根節點",
    "Element": "HTML 元素",
    "Text": "文字節點",
    "Attr": "屬性節點",
    "Comment": "註釋節點"
}

# 每個節點都是一個 C++ 物件
# 繼承自 Node 類別
```

## JavaScriptCore

### WebKit 的 JavaScript 引擎

WebKit 有自己的 JavaScript 引擎 JavaScriptCore（JSC）：

```python
jsc_components = {
    "Lexer": "將程式碼分割為 Token",
    "Parser": "將 Token 解析為語法樹",
    "Bytecode Generator": "生成位元組碼",
    "Interpreter": "直譯執行位元組碼",
    "LLINT": "Low Level Interpreter",
    "DFG JIT": "Dynamic Feature Graph JIT（後來新增）",
    "FTL JIT": "Faster Than Light JIT（更後來新增）"
}
```

### 與 V8 的比較

```python
v8_vs_jsc = {
    "V8": {
        "開發者": "Google",
        "用於": "Chrome, Node.js",
        "特點": "full-codegen + TurboFan"
    },
    "JSC": {
        "開發者": "Apple",
        "用於": "Safari, WebKit",
        "特點": "多階段 JIT 架構"
    }
}
```

## 渲染流程

### 從 HTML 到像素

```
HTML → Tokenize → DOM Tree → Attach → Render Tree → Layout → Paint

1. HTML 解析：將 HTML 文字轉換為 Token
2. DOM 建構：將 Token 組合成 DOM 樹
3. 附加樣式：為 DOM 節點計算樣式
4. 渲染樹：建立包含視覺資訊的樹
5. 版面計算：計算每個元素的位置
6. 繪製：將內容繪製到像素
```

### 附加（Attachment）

```python
attachment_process = {
    "目的": "將 DOM 節點與 Render 物件關聯",
    "輸入": "DOM 樹 + 計算後的樣式",
    "輸出": "Render 樹",
    "觸發": "DOM 改變或樣式改變時"
}
```

## CSS 處理

### CSSOM：CSS 物件模型

```python
css_processing = {
    "解析": "CSS 文字 → CSS 規則",
    "套用": "將規則應用到 DOM 元素",
    "層疊": "處理多個來源的衝突",
    "計算": "計算每個屬性的最終值"
}
```

### 選擇器匹配

```python
# 選擇器匹配複雜度

selector_matching = {
    "簡單選擇器": "tag, class, id",
    "複雜選擇器": "後代、子女、兄弟",
    "屬性選擇器": "[attr=value]",
    "偽類": ":hover, :first-child"
}

# WebKit 使用特化過的選擇器匹配器
```

## 效能最佳化

### 增量 Layout

```python
# 避免完整版面重算

incremental_layout = {
    "問題": "DOM 改變可能需要整頁重新計算",
    "解決": "只更新受影響的部分",
    "觸發": "inline 改變、絕對定位元素改變"
}
```

### 硬體加速

```python
hardware_acceleration = {
    "方法": "使用 GPU 加速繪製",
    "觸發": "某些元素使用 transform: translateZ(0)",
    "效果": "提升動畫效能",
    "代價": "額外記憶體使用"
}
```

## 平台抽象

### 跨平台支援

```python
webkit_ports = {
    "Cocoa": "macOS 和 iOS 原生 API",
    "Windows": "Windows API",
    "Qt": "跨平台 Qt 框架",
    "GTK": "Linux GTK+",
    "EFL": "Enlightenment Foundation Libraries"
}
```

### 依賴的差異

```
不同 Port 的實作差異：

┌─────────────────┐
│    WebCore     │  ← 共享核心
├─────────────────┤
│   WebKit API   │  ← 統一的 API 層
├─────────────────┤
│ Platform Layer │  ← 平台特定實作
└─────────────────┘
```

## Safari 與 Chrome

### Safari 使用 WebKit

```python
safari_webkit = {
    "渲染引擎": "WebKit",
    "JavaScript 引擎": "JavaScriptCore",
    "優點": "省電，與 macOS/iOS 深度整合",
    "缺點": "Windows 版更新較慢"
}
```

### Chrome 最初使用 WebKit

```python
# 2008 年的 Chrome 使用 WebKit

chrome_webkit_era = {
    "原因": "避免從頭建立渲染引擎",
    "好處": "專注於 JavaScript 引擎和安全",
    "後來": "2013 年 Chrome fork 出 Blink"
}
```

## 離線與現代功能

### 早期的離線支援

```python
offline_early_2008 = {
    "Application Cache": "在 WebKit 中已支援",
    "Web Storage": "localStorage/sessionStorage",
    "Indexed Database": "尚未支援（2011 年才標準化）"
}
```

### Canvas 和 SVG

```python
graphics_apis = {
    "Canvas 2D": "完整支援，2D 繪圖 API",
    "SVG": "支援，基於向量圖形",
    "WebGL": "部分支援，3D 圖形"
}
```

## 未來：Blink 的 fork

### 為何 Chrome fork？

2013 年，Google 決定從 WebKit fork 出 Blink：

```python
blink_fork_reasons = {
    "方向不同": "Google 和 Apple 的目標有差異",
    "簡化架構": "移除不必要的抽象層",
    "獨立發展": "不受 Apple 的限制",
    "長期規劃": "實現自己的功能路線圖"
}
```

### Blink 的改變

```python
# Blink 與 WebKit 的差異

blink_changes = {
    "架構簡化": "移除了 WebKit Ports 抽象",
    "獨立排程": "有自己的事件迴圈",
    "新功能": "Service Workers, Web Components"
}
```

---

**延伸閱讀**

- [WebKit architecture](https://www.google.com/search?q=WebKit+architecture)
- [WebKit+history](https://www.google.com/search?q=WebKit+history)
- [Rendering+engine+comparison](https://www.google.com/search?q=rendering+engine+comparison)