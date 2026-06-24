# JavaScript 語言起源

## 前言

JavaScript 是當今網頁開發的核心語言，但它的發明充滿了戲劇性。1995 年，Brendan Eich 在 10 天內創造了 JavaScript，這段歷史至今仍為人津津樂道。

## 背景：網景與網頁的興起

### 網景的願景

1994 年，網景通訊公司的 Marc Andreessen 和 Jim Clark 预見了網頁的未來：

```python
netscape_vision = {
    "目標": "讓網頁有互動性",
    "問題": "靜態 HTML 不夠",
    "需求": "一种簡單的腳本語言",
    "時間": "1995 年，10 天內完成"
}
```

### 當時的選擇

網景原本考慮使用 Java，但 Java 對一般網頁設計師來說太過複雜。他們需要的是一種簡單的腳本語言。

## JavaScript 的誕生

### Brendan Eich 的故事

1995 年，Brendan Eich 加入網景，接受了創造一種新語言的任務：

```python
# 設計原則

javascript_original_design = {
    "簡單": "語法類似 Java，但更容易學習",
    "彈性": "動態類型，開發者自由度高",
    "解釋執行": "不需要編譯",
    "物件導向": "但使用原型繼承而非類別",
    "函式為一等公民": "函式是物件，可作為參數"
}
```

### 命名風波

```
命名過程：

1. 最初名稱：Mocha（咖啡因）
2. 技術內部名稱：LiveScript
3. 發布時名稱：JavaScript（與 Java 合作行銷）

實際上 JavaScript 與 Java 的關係：
- 只是名字類似
- 語法類似（C 風格）
- 但核心概念完全不同
```

## JavaScript 的設計

### 語法借鏡

```javascript
// JavaScript 語法來自多種語言

// C 風格的語法
for (var i = 0; i < 10; i++) {
    console.log(i);
}

// Java 的物件語法
var obj = new Object();
obj.name = "test";

// Scheme 的函式作為一等公民
var add = function(a, b) {
    return a + b;
};

// Perl 的動態類型
var x = 1;
x = "string";  // 完全合法
```

### 原型繼承

JavaScript 使用原型繼承，而非傳統的類別繼承：

```javascript
// 原型繼承範例

// 物件直接作為另一個物件的原型
var animal = {
    speak: function() {
        console.log(this.name + " makes a sound");
    }
};

var dog = Object.create(animal);
dog.name = "Dog";
dog.speak();  // "Dog makes a sound"

// 直接在物件上定義方法
dog.bark = function() {
    console.log("Woof!");
};
```

## 早期挑戰

### 瀏覽器相容性

JavaScript 早期遇到的最大問題是瀏覽器差異：

```python
browser_wars_js_issues = {
    "DOM 操作": "每個瀏覽器有不同的 API",
    "事件處理": "NN4、IE4、標準之間的差異",
    "AJAX": "各家實現不一致",
    "除錯工具": "幾乎沒有好的除錯工具"
}
```

### 「不好的語言」形象

JavaScript 長期被認為是業餘語言：

```python
# JavaScript 的刻板印象

misconceptions = {
    "只是玩具語言": "功能有限",
    "到處alert": "大量濫用",
    "安全問題": "過去的安全漏洞",
    "效能差": "早期引擎緩慢"
}
```

## ECMAScript 標準化

### 標準的由來

1997 年，JavaScript 1.1 被提交給 ECMA International 標準化：

```
ECMAScript 命名由來：
- JavaScript 是 Netscape 的註冊商标
- ECMA 是歐洲電腦製造商協會
- 因此標準被命名為 ECMAScript (ECMA-262)
```

### 版本歷史

```python
ecmascript_versions = {
    "ES1 (1997)": "第一版標準",
    "ES2 (1998)": "小幅修改",
    "ES3 (1999)": "加入 try/catch、正規表達式、錯誤處理",
    "ES4 (2008)": "被放棄，過於激進的修改",
    "ES5 (2009)": "Strict mode、JSON、陣列新方法"
}
```

## AJAX 的興起

### 2005 年：JavaScript 文藝復興

2005 年，Jesse James Garrett 發表了「Ajax: A New Approach to Web Applications」：

```javascript
// AJAX 範例

var xhr = new XMLHttpRequest();
xhr.open("GET", "/api/data", true);
xhr.onreadystatechange = function() {
    if (xhr.readyState === 4 && xhr.status === 200) {
        var data = JSON.parse(xhr.responseText);
        console.log(data);
    }
};
xhr.send();
```

### AJAX 的影響

```
AJAX 帶來的改變：

1. 無需重新整理頁面就能更新內容
2. 網頁應用開始像桌面應用
3. Gmail, Google Maps 等服務興起
4. JavaScript 價值被重新認識
```

## 2008 年的 JavaScript

### 生態系統

```python
js_ecosystem_2008 = {
    "框架": "Dojo, Prototype, jQuery, ExtJS",
    "除錯": "Firebug 成為標準工具",
    "效能": "各瀏覽器 JIT 引擎開始出現",
    "伺服器端": "Rhino (Java), Spidermonkey (C)"
}
```

### jQuery 的影響

jQuery 在 2006 年發布，到 2008 年已成為最流行的 JavaScript 函式庫：

```javascript
// 原生 DOM 操作
document.getElementById("element").style.color = "red";

// jQuery 操作
$("#element").css("color", "red");

// 事件處理
element.addEventListener("click", handler);
$("#element").click(handler);
```

## V8 引擎的影響

### 效能革命

2008 年 9 月 Chrome 發布時，V8 引擎帶來了 JavaScript 效能的飛躍：

```python
v8_impact = {
    "編譯方式": "JIT 即時編譯為機器碼",
    "效能提升": "比傳統直譯器快 5-10 倍",
    "記憶體管理": "增量垃圾回收減少停頓",
    "未來": "為 Node.js 和現代 Web App 鋪路"
}
```

## 未來展望

### JavaScript 的演進

```python
# JavaScript 未來發展方向

future_directions = {
    "效能": "持續改進 JIT 編譯",
    "新功能": "ES6 模組、類別語法（2015）",
    "應用範圍": "伺服器（Node.js）、手機應用（React Native）",
    "工具鏈": "Webpack、Babel 等現代工具"
}
```

### 今天的 JavaScript

JavaScript 已經成為：
- 網頁開發的核心
- 伺服器端開發（Node.js）
- 行動應用（React Native、Flutter）
- 桌面應用（Electron）
- 嵌入式系統

---

**延伸閱讀**

- [JavaScript history](https://www.google.com/search?q=JavaScript+history)
- [Brendan+Eich+interview](https://www.google.com/search?q=Brendan+Eich+interview)
- [ECMAScript+history](https://www.google.com/search?q=ECMAScript+history)